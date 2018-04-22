from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, current_user

from app.web import web
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.user import User
from app.models.base import db

__author__ = 'zyj'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
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
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 如果不传remember，默认是一次性的cookie，传了remember后默认是365天，可以更改flask-login配置文件
            # login_user()的作用是将登录用户写入到cookie信息中
            login_user(user, remember=True)
            # next记录，从哪个页面进入的登录页面，登录完成后，需返回到这个页面
            next = request.args.get('next')
            if not next or not next.startwith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账户不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            from app.libs.email import send_email
            send_email(form.email.data, '重置你的密码', 'email/reset_password.html', user=user, token=user.generate_token())
            flash('邮件发送成功，请登录邮箱验证并修改密码')
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.new_password.data)
        if success:
            flash('您的密码已更新，请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('重置密码失败')
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
