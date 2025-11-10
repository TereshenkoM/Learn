# Вложенная транзакция
import asyncio
import asyncpg
import logging


async def main():
    connection = await asyncpg.connect(
        host="127.0.0.1",
        port=5432,
        user="ishimura",
        database="asyncio_eshop",
        password="1111"
    )

    async with connection.transaction():
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'my_new_brand')")

        try:
            async with connection.transaction():
                await connection.execute("INSERT INTO product_color VALUES(1, 'black')")
        except Exception as ex:
            logging.warning('Ошибка при вставке товара')
    
    await connection.close()


asyncio.run(main())