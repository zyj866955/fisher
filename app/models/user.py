from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app.libs.helper import is_isbn_or_key
from app.models.base import Base
from app import login_manager
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(Base, UserMixin):
    """
        UserMixin:用户获取登录用户的信息，写入cookie的数据，如果需自定义，重写UserMixin下的属性
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(50), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        '''
        判断书是否能够赠送
        :param isbn: 书的isbn编号
        :return: bool值，True可以赠送，False不可以赠送
        '''
        # 是不是isbn搜索，主要判断isbn的规则是否正确
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        # 查询这个isbn对应的图书时候存在
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first_element():
            return False
        # 当前用户是否已经赠送过此书，即不允许用户赠送多本相同的书，查询此书是否赠送过
        # 当前用户心愿清单中是否存在此书，即不允许用户既是索要者又是赠送者，查询此书是否添加过心愿清单
        # 同时满足以上两点，才可以赠送
        gift = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()  # 查询没有赠送过的此书
        wish = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()  # 查询此书不在心愿清单
        if not gift and not wish:
            return True
        else:
            return False


# 告诉flask_login，调用这个方法查询用户
@login_manager.user_loader
def get_user(id):
    # 查询主键，可以不用filter_by，用get
    return User.query.get(int(id)).first()
