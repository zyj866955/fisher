from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from app.forms.book import DriftForm
from app.libs.email import send_email
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_models.book import BookViewModel
from . import web

__author__ = 'zyj'


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
def pending():
    pass


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    pass


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    pass


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    pass


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
