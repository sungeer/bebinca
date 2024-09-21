from starlette.applications import Starlette
from starlette.responses import JSONResponse


def create_app():
    app = Starlette()

    register_errors(app)
    register_events(app)
    return app


def register_errors(app):
    from bebinca.utils.log_util import logger

    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc):
        try:
            logger.exception(exc)
        except (Exception,):
            pass
        return JSONResponse(
            {'detail': 'Internal server error'},
            status_code=500
        )


def register_events(app):
    from bebinca.utils.db_util import db
    from bebinca.utils import http_client

    @app.on_event('startup')
    async def startup():
        await db.connect()

    @app.on_event('shutdown')
    async def shutdown():
        await db.disconnect()
        await http_client.close_httpx()


def register_routers(app):
    from bebinca.urls import chat_url, user_url
    app.router.mount('/chats', chat_url.chat_url)
    app.router.mount('/users', user_url.user_url)


app = create_app()
