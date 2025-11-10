from todo_grpc import TodoServiceBase
from todo_pb2 import TodoItemResponse, TodoListResponse
import uuid
import json
import os


JSON_FILE = "todos.json"


class TodoServicer(TodoServiceBase):
    def __init__(self):
        self.todos = []
        self._load_from_json()

    def _save_to_json(self):
        with open(JSON_FILE, "w") as f:
            data = []
            for todo in self.todos:
                data.append({
                    "id": todo.id,
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed
                })
            json.dump(data, f)

    def _load_from_json(self):
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r") as f:
                data = json.load(f)
                self.todos = [
                    TodoItemResponse(
                        id=item["id"],
                        title=item["title"],
                        description=item.get("description", ""),
                        completed=item.get("completed", False)
                    ) for item in data
                ]

    async def CreateTodo(self, stream):
        request = await stream.recv_message()
        todo = TodoItemResponse(
            id=str(uuid.uuid4()),
            title=request.title,
            description=request.description,
            completed=False
        )
        self.todos.append(todo)
        self._save_to_json()  # Исправленный вызов
        await stream.send_message(todo)

    async def GetTodos(self, stream):
        await stream.send_message(TodoListResponse(todos=self.todos))