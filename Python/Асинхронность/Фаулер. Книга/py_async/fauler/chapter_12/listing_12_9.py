import asyncio
from asyncio import Queue, PriorityQueue
from dataclasses import dataclass, field


@dataclass(order=True)
class WorkItem:
    priority: int
    order: int
    data: str = field(compare=False)


async def worker(queue: Queue):
    while not queue.empty():
        work_item = await queue.get()
        print(f'Обрабатывается элемент {work_item}')
        queue.task_done()


async def main():
    priority_queue = PriorityQueue()

    work_items = [
        WorkItem(3, 1, 'Low'),
        WorkItem(3, 2, 'Low 2'),
        WorkItem(3, 3, 'Low 3'),
        WorkItem(2, 4, 'Mid'),
        WorkItem(1, 5, 'High')
    ]

    worker_task = asyncio.create_task(worker(priority_queue))

    for work in work_items:
        priority_queue.put_nowait(work)

    await asyncio.gather(priority_queue.join(), worker_task)

asyncio.run(main())