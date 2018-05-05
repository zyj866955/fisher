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

    @classmethod
    def pending_str(cls, status, key):
        # 用字典来模拟switch case
        key_map = {
            cls.Waiting: {
                'requester': '等待对方邮寄',
                'gifter': '等待你邮寄'
            },
            cls.Reject: {
                'requester': '对方已拒绝',
                'gifter': '你已拒绝'
            },
            cls.Redraw: {
                'requester': '你已撤销',
                'gifter': '对方已撤销'
            },
            cls.Success: {
                'requester': '对方已邮寄',
                'gifter': '你已邮寄，交易完成'
            }
        }
        return key_map[status][key]

