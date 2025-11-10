
### **Что такое `.proto` файл?**

Это файл для описания:

1. **Структуры данных** (сообщения, которые будут передаваться)
    
2. **Сервисов** (RPC-методы, которые можно вызывать)
    

Он используется утилитой `protoc` для генерации кода на выбранном языке (в нашем случае — Python).


### Основные элементы синтаксиса
1. **Версия синтаксиса**
```protobuf
syntax = "proto3";  // Обязательная первая строка
```

2. **Пакет (опционально)**
```protobuf

package todo;  // Помогает избежать конфликтов имен
```

3. **Сообщения (`message`)**

Определяют структуры данных.
```protobuf
message TodoCreateRequest {
  string title = 1;       // Поле типа string с тегом 1
  string description = 2; // Тег 2 (уникальный номер в рамках message)
}
```

- **Теги полей** (1, 2, ...):
    
    - Уникальные номера для идентификации полей при сериализации
        
    - Нельзя менять после начала использования (ломает обратную совместимость!)
        
- **Типы данных**:
    
    - Примитивы: `string`, `int32`, `bool`, `float`, и т.д.
        
    - Составные типы: другие `message`
        
    - Повторяющиеся поля: `repeated TodoItemResponse todos = 1;`


4. **Сервисы (`service`)**
Определяют RPC-методы. Пример:

```protobuf
service TodoService {
  rpc CreateTodo (TodoCreateRequest) returns (TodoItemResponse);
  rpc GetTodos (Empty) returns (TodoListResponse);
}
```

- **Структура метода**:
```protobuf    
    rpc ИмяМетода (ТипЗапроса) returns (ТипОтвета);
```

Пример готового `.proto` файла
```protobuf
syntax = "proto3";

package todo;

service TodoService {
  rpc CreateTodo (TodoCreateRequest) returns (TodoItemResponse);
  rpc GetTodos (Empty) returns (TodoListResponse);
}

message TodoCreateRequest {
  string title = 1;
  string description = 2;
}

message TodoItemResponse {
  string id = 1;
  string title = 2;
  string description = 3;
  bool completed = 4;
}

message TodoListResponse {
  repeated TodoItemResponse todos = 1;
}

message Empty {}
```

Далее запускается команда для генерации кода.
Пример команды
```python
 python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. todo.proto```


### Как это работает в коде?

На основе описанным в `.proto` генерируется код на соответсвующем языке. **ГЕНЕРИРУЕТСЯ 2 ФАЙЛА!**.

1. <название пакета>_pb2.py
2. <название пакета>_pb2_grpc.py
 
 `todo_pb2.py`
**Что содержит:**
- Классы для всех сообщений (messages), определенных в `.proto` файле.
    
- Например: `TodoCreateRequest`, `TodoItemResponse` и т.д.
    
- Логику сериализации/десериализации данных в бинарный формат.
    

**Для чего нужен:**
- Работа с данными (создание объектов, преобразование в байты, парсинг из байтов).
    
- Может использоваться **без gRPC**, например, для сохранения данных в файл или обмена через очереди (RabbitMQ, Kafka).    
---

`todo_pb2_grpc.py`

**Что содержит:**
- Классы для работы с gRPC:
    - **Серверная часть**: Базовые классы сервисов (например, `TodoServiceServicer`), которые нужно наследовать и реализовывать.
        
    - **Клиентская часть**: Классы-заглушки (stubs) для вызова методов (например, `TodoServiceStub`).
        
- Логику сетевого взаимодействия (отправка запросов, прием ответов).
    
**Для чего нужен:**
- Только для gRPC-коммуникации (клиент-серверное взаимодействие).
- Не требуется, если вы используете protobuf **без gRPC**.
---
 **Почему именно два файла?**
1. **Разделение ответственности**
    - `*_pb2.py` — чисто данные.
    - `*_grpc.py` — сетевое взаимодействие.
        
2. **Гибкость**
    - Можно использовать protobuf-сообщения **отдельно от gRPC** (например, для сериализации в файл).
    - Если вы не используете gRPC, файл `*_grpc.py` можно игнорировать.
        
3. **Совместимость**
    - Некоторые проекты используют protobuf без gRPC, и им не нужны зависимости от grpc-библиотек.


