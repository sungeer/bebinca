from flask import Flask, render_template, request
from werkzeug.exceptions import HTTPException

from viper.configs import settings


def create_app():
    app = Flask('viper')

    register_blueprints(app)
    register_errors(app)
    return app


def register_blueprints(app):
    from viper.urls import user_url, chat_url

    app.register_blueprint(chat_url.chat_url)
    app.register_blueprint(user_url.user_url, url_prefix='/user')


def register_errors(app):
    from viper.utils.log_util import logger
    from viper.utils.tools import abort

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


app = create_app()
