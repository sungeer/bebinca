from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException


def create_app():
    app = Starlette()

    register_errors(app)
    register_events(app)
    register_middlewares(app)
    register_routers(app)
    return app


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


def register_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],  # 允许所有来源 ['https://example.com', 'https://anotherdomain.com']
        allow_credentials=True,
        allow_methods=['*'],  # 允许所有HTTP方法
        allow_headers=['*'],  # 允许所有请求头
    )


def register_errors(app):
    from bebinca.models.log_model import LogModel
    from bebinca.utils.tools import abort

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        # message = exc.detail
        return abort(exc.status_code)

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        await LogModel().exception(exc)
        return abort(500)


def register_routers(app):
    from bebinca.urls import chat_url, user_url
    app.router.mount('/chat', chat_url.chat_url)
    app.router.mount('/user', user_url.user_url)


app = create_app()
