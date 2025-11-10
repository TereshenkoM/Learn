import asyncio
from asyncio import Condition


async def do_work(condition: Condition):
    while True:
        print('Ожидаю блокировки условия...')
        # Ждём возможности захватить блокировку условия;
        # после захвата освободить блокировку
        async with condition:
            print('Блокировка захвачена, освобождаю. и жду выполнения условий')
            # Ждать события. Когда произойдёт снова захватить блокировку
            await condition.wait()
            print('Условие выполнено, вновь захватываю блокировку и начинаю работать...')
            await asyncio.sleep(1)
        print('Работа закончена. Блокировка освобождена.')


async def fire_event(condition: Condition):
    while True:
        await asyncio.sleep(5)
        print('Перед уведомлением захватываю блокировку условия...')
        async with condition:
            print('Блокировка захвачена, уведомляю всех исполнителей')
            # Уведомить все задачи о событии
            condition.notify_all()


async def main():
    condition = Condition()

    asyncio.create_task(fire_event(condition))
    await asyncio.gather(do_work(condition), do_work(condition))

asyncio.run(main())