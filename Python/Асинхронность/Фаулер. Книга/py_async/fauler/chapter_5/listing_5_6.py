import asyncio
import asyncpg
from random import randint, sample
from typing import List, Tuple
from listing_5_5 import load_common_words


def gen_products(
    common_words: List[str],
    brand_id_start: int,
    brand_id_end: int,
    products_to_create: int
) -> List[Tuple[str, int]]:
    products = []
    for _ in range(products_to_create):
        description = [common_words[index] for index in sample(range(100), 100)]
        brand_id = randint(brand_id_start, brand_id_end)
        products.append((" ".join(description), brand_id))
    
    return products


def gen_skus(
    product_start_id: int, product_end_id: int, skus_to_create: int
) -> List[Tuple[int, int, int]]:
    skus = []
    
    for _ in range(skus_to_create):
        product_id = randint(product_start_id, product_end_id)
        size_id = randint(1, 3)
        color_id = randint(1, 2)
        skus.append((product_id, size_id, color_id))
    
    return skus


async def main():
    common_words = load_common_words()
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='postgres'
    )

    product_tuples = gen_products(
        common_words,
        brand_id_start=1,
        brand_id_end=100,
        products_to_create=1000
    )

    await connection.executemany("INSERT INTO product VALUES(DEFAULT, $1, $2)", product_tuples)
    sku_tuples = gen_skus(
        product_start_id=1,
        product_end_id=100,
        skus_to_create=1000
    )
    await connection.executemany("INSERT INTO sku VALUES(DEFAULT, $1, $2, $3)", sku_tuples)

    await connection.close()

asyncio.run(main())