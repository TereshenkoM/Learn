import asyncio
import tty
import os
from collections import deque
from chapter_8.listing_8_5 import create_stdin_reader
from chapter_8.listing_8_7 import *
from chapter_8.listing_8_8 import read_line
from chapter_8.listing_8_9 import MessageStore



async def sleep(delay:int, message_store: MessageStore):
    await message_store.append(f'Начало задержки {delay}')
    await asyncio.sleep(delay)
    await message_store.append(f'Конец задержки {delay}')

async def main():
    tty.setcbreak(sys.stdin)
    os.system('clear')
    
    rows = move_to_bottom_of_screen()
    # Обратный вызов, который перемещает курсор в начало
    # экрана, перерисовывает экран и возвращает курсор обратно
    async def redraw_output(items: deque):
        save_cursor_position()
        move_to_top_of_screen()
        for item in items:
            delete_line()
            print(item)
        restore_cursor_position()
    messages = MessageStore(redraw_output, rows - 1)
    stdin_reader = await create_stdin_reader()
    while True:
        line = await read_line(stdin_reader)
        delay_time = int(line)
        asyncio.create_task(sleep(delay_time, messages))
asyncio.run(main())