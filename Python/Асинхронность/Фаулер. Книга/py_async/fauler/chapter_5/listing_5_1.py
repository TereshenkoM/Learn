# Подключение к базе данных Postgres 
import asyncio
import asyncpg


async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='ishimura',
        database='asyncio_eshop',
        password='1111'
    )
    version = connection.get_server_version()
    print(version)
    await connection.close()


asyncio.run(main())