# Использование await для ожидания результата сопрограммы
import asyncio


async def add_one(number: int) -> int:
    return number + 1


async def main() -> None:
    one_plus_one = await add_one(1) # Приостановить и ждать результата
    two_plus_one = await add_one(2) # Приостановить и ждать результата

    print(one_plus_one)
    print(two_plus_one)

asyncio.run(main())