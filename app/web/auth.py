from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user

from app.web import web
from app.forms.auth import RegisterForm, LoginForm
from app.models.user import User
from app.models.base import db

__author__ = 'zyj'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        current_app.log
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form={'data': {}})


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(form.email.data).first()
        if user and user.check_password(form.password.data):
            # 如果不传remember，默认是一次性的cookie，传了remember后默认是365天，可以更改flask-login配置文件
            # login_user()的作用是将登录用户写入到cookie信息中
            login_user(user, remember=True)
            # next记录，从哪个页面进入的登录页面，登录完成后，需返回到这个页面
            next = request.args.get('next')
            if not next or not next.startwith('/'):
                next = url_for('web.index')
            return redirect(url_for(next))
        else:
            flash('账户不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
