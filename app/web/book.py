from flask import jsonify, request, flash, render_template

# from fisher import app  # 单纯的这样导入，该文件的并不会被执行
from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from . import web

import json

#
# @web.route('/index')
# def index():
#     # 基于类的视图，即插视图
#     headers = {
#         'content-type': 'text-html',
#         'location': 'www.baidu.com'
#     }
#     # response = make_response('<html></html>', 301)
#     # response.headers = headers
#     return '<html></html>', 200, headers  # 这里也可以返回一个都好分割的元组，会被自动给包装成一个response对象


@web.route('/book/search')
def search():
    """
    :return:
    """
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data
        page = form.page.data
        yushu_book = YuShuBook()
        key_or_isbn = is_isbn_or_key(q)

        if key_or_isbn == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(q, yushu_book)
        # dict序列化
        # return jsonify(books)
        # return json.dumps(result), 200, {'content-type': 'application/json'}
    else:
        flash('您搜索的关键字不合法！！')
    # return json.dumps(books, default=lambda o: o.__dict__)  序列化
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first_element)
    return render_template('book_detail.html', book=book)