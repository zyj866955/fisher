from flask import Blueprint
# 蓝图中注册蓝图自己的静态文件，模板文件
web = Blueprint('web', __name__, template_folder='templates')

from . import book
from . import auth
from . import drift
from . import gift
from . import wish
from . import main
from . import errors