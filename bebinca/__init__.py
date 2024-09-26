from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException


def create_app():
    app = Starlette()

    register_errors(app)
    register_events(app)
    register_routers(app)
    return app


def register_errors(app):
    from bebinca.configs import settings
    from bebinca.utils.log_util import logger
    from bebinca.utils.tools import abort
    app_env = settings.env

    error_messages = {
        400: 'Invalid request.',
        403: 'Access forbidden.',
        404: 'The requested URL was not found on the server.',
        405: 'The method is not allowed for the requested URL.'
    }

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        error_code = exc.status_code
        message = error_messages.get(error_code, exc.detail)
        return abort(error_code, message)

    @app.exception_handler(Exception)
    async def internal_server_error_handler(request, exc):
        if app_env != 'dev':
            try:
                logger.exception(exc)
            except (Exception,):
                pass
        return abort(500, 'An internal server error occurred.')


def register_events(app):
    from bebinca.utils.db_util import db

    @app.on_event('startup')
    async def startup():
        await db.connect()

    @app.on_event('shutdown')
    async def shutdown():
        await db.disconnect()

        from bebinca.utils import http_client
        await http_client.close_httpx()

        from bebinca.utils import redis_util
        await redis_util.close_redis()

        try:
            from bebinca.utils.log_util import stop_logger
            stop_logger()
        except (Exception,):
            pass


def register_routers(app):
    from bebinca.urls import chat_url, user_url
    app.router.mount('/chats', chat_url.chat_url)
    app.router.mount('/users', user_url.user_url)


app = create_app()
