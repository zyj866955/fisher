from flask import jsonify, request

# from fisher import app  # 单纯的这样导入，该文件的并不会被执行
from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from . import web


@web.route('/index')
def index():
    # 基于类的视图，即插视图
    headers = {
        'comtent-type': 'text-html',
        'location': 'www.baidu.com'
    }
    # response = make_response('<html></html>', 301)
    # response.headers = headers
    return '<html></html>', 200, headers  # 这里也可以返回一个都好分割的元组，会被自动给包装成一个response对象


@web.route('/book/search')
def search():
    """
    :return:
    """
    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data
        page = form.page.data
        key_or_isbn = is_isbn_or_key(q)
        if key_or_isbn == 'isbn':
            result = YuShuBook.search_by_isbn(q)
        else:
            result = YuShuBook.search_by_keyword(q, page)
        # dict序列化
        return jsonify(result)
        # return json.dumps(result), 200, {'content-type': 'application/json'}
    else:
        return jsonify(form.errors)
