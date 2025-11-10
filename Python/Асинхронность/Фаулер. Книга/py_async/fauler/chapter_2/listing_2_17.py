# Хронометраж двух конкурентных задач с помошью декоратора
import asyncio
from utils import async_timed, delay


@async_timed()
async def delay(delay_seconds: int) -> int:
    print(f'Засыпаю на {delay_seconds} c')
    await asyncio.sleep(delay_seconds)
    print(f'Сон в течение {delay_seconds} c закончился')

    return delay_seconds


@async_timed()
async def main():
    task_one = asyncio.create_task(delay(2))
    task_two = asyncio.create_task(delay(3))

    await task_one
    await task_two

asyncio.run(main())