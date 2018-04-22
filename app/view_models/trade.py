# -*- coding: utf-8 -*-
# @Time    : 2018/4/14 下午4:10
# @Author  : zhouyajun


class Trade:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self._parse(goods)

    def _parse(self, goods):
        self.total = len(goods)
        self.trades = [self._map_to_trades(single) for single in goods]

    @staticmethod
    def _map_to_trades(single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%y-%m-%d')
        else:
            time = '未知'
        return dict(
            nickname=single.user.nickname,
            time=time,
            id=single.id
        )
