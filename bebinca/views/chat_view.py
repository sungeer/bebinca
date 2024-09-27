import json

import httpx
from starlette.responses import StreamingResponse

from bebinca.configs import settings
from bebinca.utils.log_util import logger
from bebinca.utils.http_client import httpx_common, httpx_stream
from bebinca.utils.tools import jsonify, abort
from bebinca.utils import jwt_util, tools
from bebinca.models.chat_model import ChatModel
from bebinca.models.message_model import MessageModel
from bebinca.models.content_model import ContentModel

api_key = settings.ai_api_key
workspace_id = settings.ai_workspace_id
robot_id = settings.ai_robot_id

headers = {
    'Content-Type': 'application/json',
    'Access-key': api_key,
    'Workspace-Id': workspace_id
}


async def get_chat_id(request):
    user_id, message = jwt_util.verify_token(request)
    if not user_id:
        return abort(404, 'User is not found.')

    body = await request.json()
    title = body.get('title')
    if not title:
        return abort(404, 'Title is not found.')

    url = f'{settings.ai_url}/v1/oapi/agent/chat/conversation/create'
    data = {
        'robot_id': robot_id,
        'user': 'wangxun',
        'title': title
    }
    try:
        response = await httpx_common.post(url, headers=headers, json=data)
    except httpx.TimeoutException:
        logger.error('Timeout from function of get_chat_id.')
        return abort(504, 'Gateway timeout.')
    try:
        response = response.json()
    except json.JSONDecodeError:
        error_code = ErrorEnum.DESERIALIZATION_FAILED.value
        message = 'json error at chat_id'
        logger.error(f'{message}:{response}')
        return abort(error_code, message)
    data = response.get('data')
    if not data:
        error_code = ErrorEnum.EXTERNAL_API_MISSING_DATA.value
        message = 'missing data at chat_id'
        logger.error(f'{message}:{response}')
        return abort(error_code, message)
    conversation_id = data.get('conversation_id')
    if not conversation_id:
        error_code = ErrorEnum.EXTERNAL_API_MISSING_DATA.value
        message = 'missing conversation_id at chat_id'
        logger.error(f'{message}:{data}')
        return abort(error_code, message)
    await ChatModel().add_chat(conversation_id, title, user_id)
    return jsonify(conversation_id)


async def get_response(conversation_id, content):
    url = f'{settings.ai_url}/v1/oapi/agent/chat'
    data = {
        'robot_id': robot_id,
        'conversation_id': conversation_id,
        'content': content,
        'response_mode': 'streaming'
    }
    error_msg = {'finish': 'error'}
    try:
        async with httpx_stream.stream('POST', url=url, headers=headers, json=data) as response:
            async for line in response.aiter_lines():
                if not line:
                    continue
                yield line
    except httpx.TimeoutException:
        logger.error(f'ai time out: 【{conversation_id}】')
        yield f'data: {tools.dict_to_json(error_msg)}\n\n'
    except Exception as exc:
        logger.error(f'ai error 【{conversation_id}】:{exc}', exc_info=True)
        yield f'data: {tools.dict_to_json(error_msg)}\n\n'


async def stream_data(conversation_id, chat_id, trace_id, content):
    full_content = []
    async for line in get_response(conversation_id, content):
        answer = line.replace('data: ', '')
        try:
            answer = tools.json_to_dict(answer)
        except json.JSONDecodeError:
            continue
        is_error = answer.get('finish')
        if is_error:
            yield f'{is_error}\n'
            break
        if answer.get('type') == 'TEXT' and answer.get('status') == 'SUCCEEDED':
            content = answer.get('content')
            full_content.append(content)
            yield f'{content}\n'

    content_str = ''.join(full_content) if full_content else 'error'
    message_id = await MessageModel().add_message(chat_id, trace_id, 'robot')
    await ContentModel().add_content(message_id, content_str)


async def send_message(request):
    user_id, message = jwt_util.verify_token(request)  # 用户鉴权
    if not user_id:
        error_code = ErrorEnum.USER_NOT_FOUND.value
        message = 'user not found at send_message'
        logger.error(message)
        return abort(error_code, message)

    body = await request.json()

    conversation_id = body.get('conversation_id')
    if not conversation_id:
        error_code = ErrorEnum.PARAMETER_MISSING.value
        message = 'missing conversation_id at send_message'
        logger.error(message)
        return abort(error_code, message)

    content = body.get('content')
    if not content:
        error_code = ErrorEnum.PARAMETER_MISSING.value
        message = 'missing content at send_message'
        logger.error(message)
        return abort(error_code, message)

    trace_id = tools.generate_uuid()
    chat_info = await ChatModel().get_chat_by_conversation(conversation_id)
    chat_id = chat_info['ID']
    message_id = await MessageModel().add_message(chat_id, trace_id, 'user')
    await ContentModel().add_content(message_id, content)

    return StreamingResponse(stream_data(conversation_id, chat_id, trace_id, content), media_type='text/event-stream')


# 所有会话
async def get_chats(request):
    user_id, message = jwt_util.verify_token(request)  # 用户鉴权
    if not user_id:
        error_code = ErrorEnum.USER_NOT_FOUND.value
        message = 'user not found at send_message'
        logger.error(message)
        return abort(error_code, message)

    chats = await ChatModel().get_chats(user_id)
    return jsonify(chats)


# 所有问答
async def get_messages(request):
    user_id, message = jwt_util.verify_token(request)  # 用户鉴权
    if not user_id:
        error_code = ErrorEnum.USER_NOT_FOUND.value
        message = 'user not found at send_message'
        logger.error(message)
        return abort(error_code, message)

    body = await request.json()
    conversation_id = body.get('conversation_id')
    if not conversation_id:
        error_code = ErrorEnum.PARAMETER_MISSING.value
        message = 'missing conversation_id at get_messages'
        logger.error(message)
        return abort(error_code, message)

    chats = await MessageModel().get_messages(conversation_id)
    return jsonify(chats)
