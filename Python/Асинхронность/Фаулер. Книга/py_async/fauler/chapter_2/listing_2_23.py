# Выполнение счётного кода в отладочном режиме
import asyncio
from utils import async_timed


@async_timed()
async def cpu_bound_work() -> int:
    counter = 0

    for _ in range(100000000000):
        counter += 1
    
    return counter


async def main():
    task_1 = asyncio.create_task(cpu_bound_work())

    await task_1

asyncio.run(main(), debug=True)