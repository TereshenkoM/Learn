import asyncio
import asyncio
from asyncio import StreamReader
import sys


async def create_stdin_reader():
    stream_reader = StreamReader()
    protocol = asyncio.StreamReaderProtocol(stream_reader)
    
    loop = asyncio.get_running_loop()
    
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return stream_reader


async def delay(delay_seconds: int) -> int:
    print(f'Засыпаю на {delay_seconds} c.')
    await asyncio.sleep(delay_seconds)
    print(f'Сон в течение {delay_seconds} с. закончился')

    return delay_seconds



async def main():
    stdin_reader = await create_stdin_reader()
    
    while True:
        delay_time = await stdin_reader.readline()
        asyncio.create_task(delay(int(delay_time)))


asyncio.run(main())