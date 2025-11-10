import asyncio
import functools
from asyncio import Event


def trigger_event(event: Event):
    print('Активируется событие!')
    event.set()


async def do_work_on_event(event: Event):
    print('Ожидаю события')
    # Ждать события
    await event.wait()
    print('Работаю')
    # Когда событие произойдёт, блокировка снимается и мы можем начать работу
    await asyncio.sleep(1)
    print('Работа закончена')
    # Сбросить событие, в результате чего последующие обращения к wait блокируются
    event.clear()

async def main():
    event = Event()
    asyncio.get_running_loop().call_later(
        3.0,
        functools.partial(trigger_event, event)
    )
    await asyncio.gather(do_work_on_event(event), do_work_on_event(event))

asyncio.run(main())
