# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 上午9:41
# @Author  : zhouyajun
from flask import current_app
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    launched = Column(Boolean, default=False)  # 表明礼物是否送出去
    isbn = Column(String(15), nullable=False)

    @classmethod
    def get_user_gifts(cls, uid):
        user_gifts = Gift.query.filter_by(uid=uid, launched=False).all()
        return user_gifts

    @classmethod
    def get_wishes_count(cls, isbn_list):
        from app.models.wish import Wish
        wishes = db.session.query(func.count(Wish.isbn), Wish.isbn).filter(
            Wish.launched == False, Wish.isbn.in_(isbn_list), Wish.status == 1).group_by(Wish.isbn).all()
        # wishes = db.session.query(Wish).filter(
        #     Wish.launched == False, Wish.isbn.in_(isbn_list), Wish.status == 1).group_by(Wish.isbn).all()
        return [{'isbn': wish[0], 'count': wish[1]} for wish in wishes]

    @classmethod
    def recent(cls):
        # 去重的意义：同一本书可以与多个人关联，形成多个礼物，但是书只有一本
        recent_gift = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(
            desc(Gift.create_time)).limit(current_app.config['RECENT_GIFT_COUNTER']).distinct().all()
        return recent_gift

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first_element
