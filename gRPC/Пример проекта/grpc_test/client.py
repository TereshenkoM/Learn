import asyncio
from grpclib.client import Channel
from todo_grpc import TodoServiceStub  # Импорт из нового файла
from todo_pb2 import TodoCreateRequest, Empty

async def main():
    # Создаем асинхронный канал
    async with Channel("127.0.0.1", 50051) as channel:
        stub = TodoServiceStub(channel)

        create_response = await stub.CreateTodo(
            TodoCreateRequest(
                title="Изучить gRPC",
                description="Написать пример с FastAPI"
            )
        )
        print(f"Создана задача:\n{create_response}")

        list_response = await stub.GetTodos(Empty())
        print("\nСписок задач:")
        for todo in list_response.todos:
            print(f"- {todo.title} (ID: {todo.id})")

if __name__ == "__main__":
    asyncio.run(main())