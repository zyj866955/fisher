from flask import Flask


def create_app():
    app = Flask(__name__)
    register_blueprint(app)
    app.config.from_object('config')  # DEBUG 在flask的配置中默认参数，默认值是false
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)