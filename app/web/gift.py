from flask_login import login_required, current_user
from flask import current_app, flash, render_template, redirect, url_for

from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_models.gift import MyGiftsViewModel
from . import web

__author__ = 'zyj'


@web.route('/my/gifts')
@login_required
def my_gifts():
    gifts_of_mine = Gift.get_user_gifts(current_user.id)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wishes = Gift.get_wishes_count(isbn_list)
    gift_view_model = MyGiftsViewModel(gifts_of_mine, wishes)
    return render_template('my_gifts.html', gifts=gift_view_model.gifts)


# 赠送书
@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            # current_user实例化User的模型，和user中定义的get_user方法
            current_user.beans += current_app.config['BEAN']
            gift.uid = current_user.id
            db.session.add(gift)
    else:
        flash('这本书已添加至你的赠送清单或存在于你的心愿清单，请不要重复操作')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gift.id).first_or_404()
    if drift:
        flash('该礼物正在交易中，请先处理掉交易，再进行撤销操作')
    else:
        with db.auto_commit:
            current_user.beans -= current_app.config['BEANS']
            gift.delete()
    return redirect(url_for('web.my_gifts'))
