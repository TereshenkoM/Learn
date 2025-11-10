import asyncio


async def positive_integer(until):
    for integer in range(1, until):
        await asyncio.sleep(integer)
        yield integer


async def main():
    async_generator = positive_integer(3)
    print(type(async_generator)) # positive_iterator

    print(await anext(async_generator))
    print(await anext(async_generator))

asyncio.run(main())


import asyncpg
import asyncio
async def take(generator, to_take: int):
    item_count = 0
    async for item in generator:
        if item_count > to_take - 1:
            return
        item_count = item_count + 1
        yield item

async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='password'
    )
    async with connection.transaction():
        query = 'SELECT product_id, product_name from product'
        product_generator = connection.cursor(query)
        async for product in take(product_generator, 5):
            print(product)
        print('Получены первые пять товаров!')
    await connection.close()
asyncio.run(main())