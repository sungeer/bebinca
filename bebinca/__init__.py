from flask import Flask
from werkzeug.exceptions import HTTPException

from bebinca.configs import settings


def create_app():
    app = Flask('bebinca')

    register_extensions(app)
    register_errors(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    from bebinca.utils.cors import cors

    cors.init_app(app)


def register_errors(app):
    from bebinca.utils.log_util import logger
    from bebinca.utils.tools import abort

    @app.errorhandler(HTTPException)
    def http_exception_handler(error):
        # error_code = getattr(error, 'code', 500)
        # message = HTTP_STATUS_CODES.get(error_code, str(error))
        # error_code = error.code
        return abort(error.code)

    @app.errorhandler(Exception)
    def global_exception_handler(error):
        logger.exception(error)
        return abort(500)


def register_blueprints(app):
    from bebinca.urls import user_url, chat_url

    app.register_blueprint(chat_url.chat_url)
    app.register_blueprint(user_url.user_url, url_prefix='/user')


app = create_app()
