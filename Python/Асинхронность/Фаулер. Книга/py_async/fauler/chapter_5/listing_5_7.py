# Создание пула подключений и конкурентное выполнение запросов
import asyncio
import asyncpg


product_query = \
    """
    SELECT
        p.product_id,
        p.product_name,
        p.brand_id,
        s.sku_id,
        pc.product_color_name,
        ps.product_size_name
    FROM product p
    JOIN sku s ON s.product_id = p.product_id
    JOIN product_color pc ON pc.product_color_id = s.product_color_id
    JOIN product_size ps ON ps.product_size_id = s.product_size_id
    WHERE p.product_id = 100;
    """


async def query_product(pool):
    async with pool.acquire() as conn:
        return await conn.fetchrow(product_query)


async def main():
    async with asyncpg.create_pool(
        host='127.0.0.1',
        port=5432,
        user='ishimura',
        password='1111',
        database='asyncio_eshop',
        min_size=6,
        max_size=6
    ) as pool: # создать пул с 6 подключениями

        # Конкурентно выполнить запросы
        await asyncio.gather(query_product(pool), query_product(pool)) 

asyncio.run(main())