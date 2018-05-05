from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from app.forms.book import DriftForm
from app.libs.email import send_email
from app.libs.enums import PendingEnum
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection
from . import web

__author__ = 'zyj'

'''
模型对象：
    我的礼物
    我的心愿
    我的交易
数据库事物：
    一次数据库的操作，也可能包括多个表的操作
    事物的一致性：在一次事物中，要保证所有的操作都完成，如果代码在执行过程中出现问题，则必须回滚，之前的对数据库的操作全部撤销
'''


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    gift = Gift.query.get_or_404(gid)
    # 对礼物进行检查
    if gift.is_yours_gift(current_user.id):
        flash("自己不能向自己请求书籍")
        return redirect(url_for('web.book_detail', gift.isbn))
    # 对用户进行检查
    can = current_user.can_save_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)
    # 请求页面信息准备
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, gift)
        send_email(gift.user.email, '有人想要一本书', 'email/get_gift.html',
                   wisher=current_user,
                   gift=gift)
        return redirect(url_for('web.pending'))
    gifter = gift.user.summary
    return render_template('drift.html', gifter=gifter, user_beans=current_user.beans)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(or_(Drift.request_id == current_user.id,
                                    Drift.gifter_id == current_user.id)).order_by(desc(Drift.create_time)).all()
    drifts_collections = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=drifts_collections)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    """拒绝礼物"""
    with db.auto_commit:
        drift = Drift.query.filter(Drift.id == did, Drift.gifter_id == current_user.id).first_or_404()
        drift.pending = PendingEnum.reject
        requester = User.query.filter_by(id=drift.request_id).first_or_404()
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    with db.auto_commit:
        drift = Drift.query.filter_by(requester_id=current_user.id, id=did).first_or_404()
        drift.status = PendingEnum.redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    with db.auto_commit:
        drift = Drift.query.filter_by(id=did, gifter_id=current_user.id).first_or_404()
        drift.pending = PendingEnum.success
        current_user.beans += 1

        gift = Gift.query.filter_by(id=drift.gifter_id).first_or_404()
        gift.launched = True

        wish = Wish.query.filter_by(id=drift.request_id).first_or_404()
        wish.launched = True


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        # drift.message = drift_form.message.data
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book = BookViewModel(current_gift.book)

        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= 1

        db.session.add(drift)
