from flask import Flask, render_template, request

from viper.configs import settings


def create_app():
    app = Flask('viper')

    register_logging(app)
    register_blueprints(app)
    register_errors(app)
    return app


def register_logging(app):
    from viper.utils.log_util import logger

    app.logger.handlers = []
    logger.info('Register logging.')


def register_blueprints(app):
    from viper.urls import user_url, chat_url

    app.register_blueprint(chat_url.chat_url)
    app.register_blueprint(user_url.user_url, url_prefix='/user')


def register_errors(app):
    from viper.utils.log_util import logger
    from viper.utils.tools import abort

    @app.errorhandler(400)
    def bad_request(e):
        return abort(400, 'Invalid request.')

    @app.errorhandler(403)
    def bad_request(e):
        return abort(403, 'Access forbidden.')

    @app.errorhandler(404)
    def page_not_found(e):
        return abort(404, 'The requested URL was not found on the server.')

    @app.errorhandler(405)
    def page_not_found(e):
        return abort(405, 'The method is not allowed for the requested URL.')

    @app.errorhandler(500)
    def internal_server_error(e):
        return abort(500, 'An internal server error occurred.')


app = create_app()
