from threading import Lock, Thread


list_lock = Lock()

def sum_list(int_list):
    print('Ожидание блокировки')

    with list_lock:
        print('Блокировка захвачена')
        if len(list_lock) == 0:
            print('Сумирование завершено')
            return
        else:
            head, *tail = int_list
            print('Суммируется остаток списка')
            return head + sum_list(tail)


thread = Thread(target=sum_list, args=([1,2,3,4]))
thread.start()
thread.join()
