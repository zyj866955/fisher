from flask import current_app, flash, render_template
from flask_login import login_required, current_user

from app.models.base import db
from app.models.wish import Wish
from app.view_models.wish import MyWishesViewModel
from . import web

__author__ = 'zyj'


@web.route('/my/wish')
def my_wish():
    wishes_of_mine = Wish.get_user_gifts(current_user.id)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gifts_count_list = Wish.get_gifts_count(isbn_list)
    wish_view_model = MyWishesViewModel(wishes_of_mine, gifts_count_list)
    return render_template('my_wish.html', wishes=wish_view_model.gifts)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            # current_user实例化User的模型，和user中定义的get_user方法
            # current_user.beans += current_app.config['BEAN']
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash('这本书已添加至你的赠送清单或存在于你的心愿清单，请不要重复操作')


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
