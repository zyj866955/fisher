from werkzeug.local import Local
import threading
import time


class A:
    b = 1

my_obj = Local()
my_obj.b = 1


def my_work():
    my_obj.b = 2
    print('in new thread b is:' + str(my_obj.b))

new_t = threading.Thread(target=my_work, name='yajun_thread')
new_t.start()
time.sleep(1)

print('in main thread b is:' + str(my_obj.b))
