import asyncio
from utils import delay


async def create_tasks_no_sleep():
    task1 = asyncio.create_task(delay(1))
    task2 = asyncio.create_task(delay(2))
    print('К задачам применяет gather')
    await asyncio.gather(task1, task2)


async def create_tasks_sleep():
    task1 = asyncio.create_task(delay(1))
    await asyncio.sleep(0)
    task2 = asyncio.create_task(delay(2))
    await asyncio.sleep(0)
    print('К задачам применяет gather')
    await asyncio.gather(task1, task2)


async def main():
    print('--- Без asyncio.sleep(0) ---')
    await create_tasks_no_sleep()
    print('--- С asyncio.sleep(0) ---')
    await create_tasks_sleep()


asyncio.run(main())