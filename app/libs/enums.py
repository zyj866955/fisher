# -*- coding: utf-8 -*-
# @Time    : 2018/4/22 下午2:13
# @Author  : zhouyajun

from enum import Enum


class PendingEnum(Enum):
    """交易状态"""
    waiting = 1
    success = 2
    reject = 3
    redraw = 4
