# -*- coding: utf-8 -*-
# @Time    : 2018/4/21 下午4:35
# @Author  : zhouyajun
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from fisher import app, db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()



