# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 上午9:41
# @Author  : zhouyajun


from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base


class Gift(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    launched = Column(Boolean, default=False)  # 表明礼物是否送出去
    isbn = Column(String, nullable=False)
