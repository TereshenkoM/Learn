import asyncio
from aiohttp import ClientSession
from typing import Iterable


async def get_weather(city: str):
    async with ClientSession() as session:
        url = f'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}

        async with session.get(url=url, params=params) as response:
            weather = await response.json()
            print(f'{city}: {weather['weather'][0]['main']}')
            

async def main(cities: Iterable[str]):
    tasks = []
    for city in cities:
        tasks.append(asyncio.create_task(get_weather(city)))
    
    for task in tasks:
        await task


# Для группового запуска задач можно использовать gather
# async def main(cities_):
#     tasks = []
#     for city in cities_:
#         tasks.append(asyncio.create_task(get_weather(city)))

#     results = await asyncio.gather(*tasks)

#     for result in results:
#         print(result)


if __name__ == '__main__':
    cities = ['Moscow', 'St. Petersburg', 'Rostov-on-Don', 'Kaliningrad', 'Vladivostok',
          'Minsk', 'Beijing', 'Delhi', 'Istanbul', 'Tokyo', 'London', 'New York']
    
    asyncio.run(main(cities))