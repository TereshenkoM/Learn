import asyncio
from asyncio import Queue


async def main():
    customer_queue = Queue()
    # Не ошибки
    await customer_queue.get()
    # С ошибкой
    # customer_queue.get_nowait()

asyncio.run(main())



async def main():
    queue = Queue(maxsize=1)

    #С ошибкой
    queue.put_nowait(1)
    queue.put_nowait(1)
    # Без ошибки
    queue.put_nowait(1)
    await queue.put(1)

asyncio.run(main())