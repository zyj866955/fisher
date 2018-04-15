from flask import Flask
from flask_login import LoginManager
from app.models.base import db

login_manager = LoginManager()


def create_app():
    # app = Flask(__name__, static_folder='statics')
    app = Flask(__name__)
    register_blueprint(app)
    app.config.from_object('app.secure')  # DEBUG 在flask的配置中默认参数，默认值是false
    app.config.from_object('app.setting')

    db.init_app(app)
    login_manager.init_app(app)
    # @login_required装饰器的作用，请求需登录的url时，会重定向到登录页面
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    with app.app_context():
        '''利用应用上下问，将APP入栈'''
        db.create_all()
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
