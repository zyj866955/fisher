# -*- coding: utf-8 -*-
# @Time    : 2018/4/21 下午1:56
# @Author  : zhouyajun

from flask_mail import Message
from flask import render_template, current_app
import threading

from app import mail


def send_email(to, subject, template, **kwargs):
    msg = Message('[鱼书]' + '' + subject, sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 获取真实的flask核心对象，不能给线程传入代理对象current_app，代理对象受线程隔离对象影响，无法在不同的线程中引用到核心对象
    app = current_app._get_current_object()
    t = threading.Thread(target=send_async_email, args=[app, msg])  # args可以传入多个参数
    t.start()


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(e)
