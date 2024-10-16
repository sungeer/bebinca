from flask import request

from bebinca.models.user_model import UserModel
from bebinca.utils.tools import jsonify, abort
from bebinca.utils import jwt_util


def get_access_token():
    body = request.json
    phone_number = body['phone_number']
    password = body['password']
    user_info = UserModel().get_user_by_phone(phone_number)
    if not user_info:
        return abort(403)
    db_password = user_info['PasswordHash']
    is_pwd = jwt_util.validate_password(password, db_password)
    if not is_pwd:
        return abort(403)
    access_token = jwt_util.generate_token({'id': user_info['ID']})
    jwt_token = {'access_token': access_token, 'token_type': 'bearer'}
    return jsonify(jwt_token)
