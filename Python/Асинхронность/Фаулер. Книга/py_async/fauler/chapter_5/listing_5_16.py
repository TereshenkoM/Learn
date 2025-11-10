import asyncio
import asyncpg


async def main():
    connection = await asyncpg.connect(
        host="127.0.0.1",
        port=5432,
        user="ishimura",
        database="asyncio_eshop",
        password="1111"
    )

    async with connection.transaction():
        query = "SELECT product_id, product_name FROM product"
        # Создать курсор
        cursor = await connection.cursor(query)
        # Сдвинуть курсор на 500 записей
        await cursor.forward(500)
        # Получить 100 записей
        products = await cursor.fetch(100)

        for product in products:
            print(product)
        
    
    await connection.close()


asyncio.run(main())