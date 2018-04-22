# -*- coding: utf-8 -*-
# @Time    : 2018/4/15 上午8:22
# @Author  : zhouyajun
from app.view_models.book import BookViewModel


class MyWishesViewModel:
    def __init__(self, gifts_list, wishes_list):
        self.gifts = []
        self._gifts_of_mine = gifts_list
        self._wish_count_list = wishes_list
        self.gifts = self._parse_gift()

    def _parse_gift(self):
        temp = []
        for gift in self._gifts_of_mine:
            count = self._parse_wish(gift)
            r = {
                'id': gift.id,
                'book': BookViewModel(gift.book),
                'wishes_count': count
            }
            temp.append(r)
        return temp

    def _parse_wish(self, gift):
        for wish in self._wish_count_list:
            if gift.isbn == wish['isbn']:
                return wish['count']
