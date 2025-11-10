# Конкурентное выполнение нескольких задач
import asyncio
from utils import delay
import time

async def main():
    start = time.time()

    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    sleep_one_more = asyncio.create_task(delay(3))

    await sleep_for_three
    await sleep_again
    await sleep_one_more

    end = time.time()

    print(f'Время выполнения {end-start:.4f}') # ~ 3 секунды

asyncio.run(main())