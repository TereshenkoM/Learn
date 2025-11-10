# Сравнение сопрограмм с обычными функциями
import asyncio


async def coroutine_add_one(number: int) -> int:
    return number + 1

coroutine_res = asyncio.run(coroutine_add_one(1))

print(f'Результат сопрограммы равен {coroutine_res}, а его тип равен {type(coroutine_res)}')
