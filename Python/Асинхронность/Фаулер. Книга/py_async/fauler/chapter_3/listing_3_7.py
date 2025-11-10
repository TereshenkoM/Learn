# Использование селектора для построения неблокирующих сокетов
import selectors
import socket
from selectors import SelectorKey
from typing import List, Tuple


selector = selectors.DefaultSelector()

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.setblocking(False)
server_socket.bind(server_address)
server_socket.listen()

selector.register(server_socket, selectors.EVENT_READ)

while True:
    # Создать селектор с таймаутом 1
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)

    if len(events) == 0:
        print('Событий нет. Жду')
    
    for event, _ in events:
        # Получить сокет, для которого произошло событие
        event_socket = event.fileobj

        # Если событие произошло с серверным сокетом, значит была попытка подключения
        if event_socket == server_socket:
            connection, address = server_socket.accept()
            connection.setblocking(False)
            print(f'Получен запрос на подключение от {address}')

            # Зарегистрировать клиент, подключившийся к сокету
            selector.register(connection, selectors.EVENT_READ)
        else:
            # Если событие произошло не с серверным сокетом
            # получить данные от клиента и отправить обратно
            data = event_socket.recv(1024)
            print(f'Получены данные: {data}')
            event_socket.send(data)