import asyncio


async def task(num):
    print(f'Я задача {num}')
    await asyncio.sleep(1)
    print('йоу')


async def main():
    task_1 = asyncio.create_task(task(1))
    task_2 = asyncio.create_task(task(2))
    print('Сплю')
    await asyncio.sleep(5)


asyncio.run(main())