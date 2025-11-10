# Создание пула процессов
from multiprocessing import Pool

def say_hello(name: str) -> str:
    return f'Привет, {name}'


if __name__ == "__main__":
    # Создали пулл
    with Pool() as process_pool:
        # Выполнить say_hello в отдельных процессах
        hi_jeff = process_pool.apply(say_hello, args=('Jeff',))
        hi_john = process_pool.apply(say_hello, args=('John',))

        print(hi_jeff)
        print(hi_john)
