# Сравнение сопрограмм с обычными функциями
async def coroutine_add_one(number: int) -> int:
    return number + 1


def add_one(number: int) -> int:
    return number + 1


function_res = add_one(1)
coroutine_res = coroutine_add_one(1)

print(f'Результат функции равен {function_res}, а его тип равен {type(function_res)}')
print(f'Результат сопрограммы равен {coroutine_res}, а его тип равен {type(coroutine_res)}')
