# -*- coding: utf-8 -*-
# @Time    : 2018/4/14 下午3:03
# @Author  : zhouyajun
from contextlib import contextmanager


class MyResource:
    # def __enter__(self):
    #     print("this is enter method!")
    #     return self
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     print('this is exit method')

    def query(self):
        print('this is query method')


@contextmanager
def my_resource():
    yield
    print("this is enter method")
'''
   @contextmanager,构造一个生成器装饰器，通过yield关键来控制先执行那部分代码
   后执行那部分代码，yield可以返回一个对象的实例或者调用一个对象的方法，或者后面什么都没有(只是起控制作用) 
'''

with my_resource():
    print(000000000)
    print(88888888)

# my = my_resource()
# for i in my:
#     print(i)