# -*- coding: utf-8 -*-
# @Time    : 2018/4/22 下午5:03
# @Author  : zhouyajun
from app.libs.enums import PendingEnum
from app.models.drift import Drift

drift = Drift()


class DriftViewModel:
    def __init__(self, drift, current_user_id):
        self.data = self._parse(drift, current_user_id)

    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        global you_are
        if current_user_id == drift.request_id:
            you_are = 'requester'
        if current_user_id == drift.gifter_id:
            you_are = 'gifter'
        return you_are

    def _parse(self, drift, current_user_id):
        you_are = self.requester_or_gifter(drift, current_user_id)
        status_str = PendingEnum.pending_str(drift.status, you_are)
        r = {
            'you_are': you_are,
            'drift_id': drift.id,
            'book_title': drift.book_title,
            'book_img': drift.book_img,
            'book_author': drift.book_author,
            'data': drift.create_time.strftime('%Y-%d-%m'),
            'message': drift.message,
            'address': drift.address,
            'recipient_name': drift.recipient,
            'mobile': drift.mobile,
            'status': drift.status,
            'status_str': status_str,
            'operator': drift.request_nickname if you_are != 'requester' else drift.gifter_name
        }
        return r


class DriftCollection:
    def __init__(self, drifts, current_user_id):
        self.data = []
        self._parse(drifts, current_user_id)

    def _parse(self, drifts, current_user_id):
        for drift in drifts:
            temp = DriftViewModel(Drift, current_user_id)
            self.data.append(temp.data)
