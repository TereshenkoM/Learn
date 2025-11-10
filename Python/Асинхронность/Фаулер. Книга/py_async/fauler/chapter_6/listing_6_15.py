import asyncio
import asyncpg
from utils import async_timed
from typing import List, Dict
from concurrent.futures.process import ProcessPoolExecutor


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


@async_timed()
async def query_products_concurrently(pool, queries):
    queries = [query_product(pool) for _ in range(queries)]

    return await asyncio.gather(*queries)


def run_in_new_loop(num_queries: int) -> List[Dict]:
    async def run_queries():
        async with asyncpg.create_pool(
            host='127.0.0.1',
            port=5432,
            user='ishimura',
            password='1111',
            database='asyncio_eshop',
            min_size=6,
            max_size=6
        ) as pool: # создать пул с 6 подключениями
            return await query_products_concurrently(pool, num_queries)
    
    results = [dict(result) for result in asyncio.run(run_queries())]
    return results


@async_timed()
async def main():
    loop = asyncio.get_running_loop()
    pool = ProcessPoolExecutor()
    tasks = [loop.run_in_executor(pool, run_in_new_loop, 10000) for _ in range(5)]

    all_results =  await asyncio.gather(*tasks)
    total_queries = sum([len(result) for result in all_results])
    print(f'Извлечено товаров из БД: {total_queries}')


if __name__ == "__main__":
    asyncio.run(main())