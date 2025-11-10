# Два параллельных процесса
import time
from multiprocessing import Process


def count(count_to: int) -> int:
    start = time.time()
    counter = 0

    while counter < count_to:
        counter += 1
    
    end = time.time()
    print(f'Закончен подсчёт до {count_to} за время {end-start}')

    return counter


if __name__ == "__main__":
    start_time = time.time()

    # Создаём процессы для выполнения
    to_one_hundred_million = Process(target=count, args=(100000000,))
    to_two_hundred_million = Process(target=count, args=(200000000,))

    # Запускаем процесс. Управление возвращается немедленно
    to_one_hundred_million.start()
    to_two_hundred_million.start()

    # Ждём завершения процесса. Этот метод блокирует управление, пока процесс не завершится
    to_one_hundred_million.join()
    to_two_hundred_million.join()

    end_time = time.time()

    print(f'Полное времпя работы {end_time-start_time}')