from flask import Flask
from app.models.book import db


def create_app():
    # app = Flask(__name__, static_folder='statics')
    app = Flask(__name__)
    register_blueprint(app)
    app.config.from_object('app.secure')  # DEBUG 在flask的配置中默认参数，默认值是false
    app.config.from_object('app.setting')

    db.init_app(app)
    db.create_all(app=app)
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
