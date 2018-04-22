# -*- coding: utf-8 -*-
# @Time    : 2018/4/15 上午11:57
# @Author  : zhouyajun
from flask import render_template
from . import web


@web.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
