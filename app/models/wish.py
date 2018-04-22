# -*- coding: utf-8 -*-
# @Time    : 2018/4/14 上午9:41
# @Author  : zhouyajun

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    launched = Column(Boolean, default=False)  # 有没有索取到书
    isbn = Column(String(15), nullable=False)

    @classmethod
    def get_user_wishes(cls, uid):
        user_wishes = Wish.query.filter_by(uid=uid, launched=False).all()
        return user_wishes

    @classmethod
    def get_gifts_count(cls, isbn_list):
        from app.models.gift import Gift
        gifts = db.session.query(func.count(Gift.isbn), Wish.isbn).filter(
            Gift.launched == False, Gift.isbn.in_(isbn_list), Gift.status == 1).group_by(Gift.isbn).all()
        # wishes = db.session.query(Wish).filter(
        #     Wish.launched == False, Wish.isbn.in_(isbn_list), Wish.status == 1).group_by(Wish.isbn).all()
        return [{'isbn': gift[0], 'count': gift[1]} for gift in gifts]

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first_element