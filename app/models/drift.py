# -*- coding: utf-8 -*-
# @Time    : 2018/4/22 下午1:48
# @Author  : zhouyajun
from sqlalchemy import Column, Integer, String, SmallInteger

from app.libs.enums import PendingEnum
from app.models.base import Base


class Drift(Base):
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient = Column(String(64), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(100))
    mobile = Column(String(11), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(30))

    # 请求者信息
    request_id = Column(Integer)
    request_nickname = Column(String(30))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_name = Column(String(30))

    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        return PendingEnum(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value
