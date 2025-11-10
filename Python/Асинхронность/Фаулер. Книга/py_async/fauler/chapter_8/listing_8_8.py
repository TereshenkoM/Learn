import sys
from asyncio import StreamReader
from collections import deque
from chapter_8.listing_8_7 import move_back_one_char, clear_line


async def read_line(stdin_reader: StreamReader) -> str:
    # Функция удаления предыдщуео символа из стандартного вывода
    def erase_last_chat():
        move_back_one_char()
        sys.stdout.write(' ')
        move_back_one_char()
    
    delete_char = b'\x7f'
    input_buffer = deque()
    
    while (input_char := await stdin_reader.read(1)) != b'\n':
        # Если введём символ delete, то удалить предыдущий символ
        if input_char == delete_char:
            if len(input_buffer) > 0:
                input_buffer.pop()
                erase_last_chat()
                sys.stdout.flush()
            else:
                # Все символы, кроме delete, добавляются 
                # в конец буфера и эхо-копируются
                input_buffer.append(input_char)
                sys.stdout.write(input_char.decode())
                sys.stdout.flush()

    clear_line()
    return b''.join(input_buffer).decode()