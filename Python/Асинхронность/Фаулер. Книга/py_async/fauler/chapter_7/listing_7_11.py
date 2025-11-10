from threading import Lock, Thread
import time


a_lock = Lock()
b_lock = Lock()


def a():
    with a_lock:
        print('Захвачена блокировка а из метода а!')
        time.sleep(1)
        
        
        with b_lock:
            print('Захвачены обе блокировки из метода b')


def b():
    with b_lock:
        print('Захвачена блокировка b из метода b')

        with a_lock:
            print('Захвачены обе блокировки из метода b')


thread_1 = Thread(target=a)
thread_2 = Thread(target=b)

thread_1.start()
thread_2.start()
thread_1.join()
thread_2.join()