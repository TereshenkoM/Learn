import asyncio
from asyncio import Queue, PriorityQueue
from dataclasses import dataclass, field


# order=True - создаёт дандер методы для сравнения
@dataclass(order=True)
class WorkItem:
    priority: int
    # Параметр compare=False говорит: не использовать это поле при сравнении объектов.
    data: str = field(compare=False)


async def worker(queue: Queue):
    while not queue.empty():
        work_item: WorkItem = await queue.get()
        print(f'Обрабатывается элемент {work_item}')
        queue.task_done()


async def main():
    priority_queue = PriorityQueue()

    work_items = [
        WorkItem(3, 'Lowest'),
        WorkItem(2, 'Medium'),
        WorkItem(1, 'High')
    ]
    worker_task = asyncio.create_task(worker(priority_queue))

    for work in work_items:
        priority_queue.put_nowait(work)

    await asyncio.gather(priority_queue.join(), worker_task)

asyncio.run(main())
