import asyncio
import asyncpg
import tty
import os
from asyncpg.pool import Pool
from collections import deque
from chapter_8.listing_8_5 import create_stdin_reader
from chapter_8.listing_8_7 import *
from chapter_8.listing_8_8 import read_line
from chapter_8.listing_8_9 import MessageStore


async def run_query(query: str, pool: Pool, message_store: MessageStore):
    async with pool.acquire() as connection:
        try:
            result = await connection.fetch_row(query)
            await message_store.append(f'Выбрано {len(result)} строк по запросу')
        except Exception as e:
            await message_store.append(f'Получено исключение {e} от: {query}')

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

    async with asyncpg.create_pool(
        host='127.0.0.1',
        port=5432,
        user='postgres'
        password='postgres',
        database='products',
        min_size=6,
        max__size=6
    ) as pool:
        while True:
            query = await read_line(stdin_reader)
            asyncio.create_task(run_query(query, pool, messages))

asyncio.run(main())