# Операции ограниченные производительностью ввода-вывода и быстродействием процессора
import requests


response = requests.get('https://example.com') # Веб запрос ограничен производительностью ввода-вывода
headers = [f'{key}: {header}' for key,header in response.headers.items()] # Обработка ответа ограничена быстродейтсвием процессора

formatted_headers = '\n'.join(headers) # Конкатенация строк ограничена быстродействием процессора

with open('chapter_1/headers.txt', 'w') as file:
    file.write(formatted_headers) # Запись на диск ограничена производительностью ввода-вывода