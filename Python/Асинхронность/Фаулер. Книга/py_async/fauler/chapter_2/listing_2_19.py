# Счётный код и длительная задача
import asyncio
from utils import async_timed, delay


@async_timed()
async def cpu_bount_work() -> int:
    counter = 0
    for _ in range(100000000):
        counter += 1
    
    return counter


@async_timed()
async def main():
    task_one = asyncio.create_task(cpu_bount_work())
    task_two = asyncio.create_task(cpu_bount_work())
    task_three = asyncio.create_task(delay(4))

    await task_one
    await task_two
    await task_three

asyncio.run(main())