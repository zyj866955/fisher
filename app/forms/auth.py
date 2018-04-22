# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 下午11:26
# @Author  : zhouyajun

from wtforms import Form, StringField, IntegerField, PasswordField, ValidationError
from wtforms.validators import Length, NumberRange, DataRequired, Email, equal_to

from app.models.user import User


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='邮箱格式不正确')])


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='邮箱格式不正确')])
    password = PasswordField(validators=[DataRequired(message='密码不可以为空, 请输入你的密码'),
                                         Length(6, 32, message='密码长度最少6个字符，最多32个字符')])


class RegisterForm(EmailForm):
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称至少需要两个字符, 最多10个字符')])

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已被使用')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮箱已被注册')


class ResetPasswordForm(Form):
    password = PasswordField(validators=[DataRequired(message='密码不可以为空, 请输入你的密码'),
                                         Length(6, 32, message='密码长度最少6个字符，最多32个字符'),
                                         equal_to('new_password', '新密码和确认密码不能相同')])
    new_password = PasswordField('new_password', validators=[DataRequired(message='密码不可以为空, 请输入你的密码'),
                                                             Length(6, 32, message='密码长度最少6个字符，最多32个字符')])
