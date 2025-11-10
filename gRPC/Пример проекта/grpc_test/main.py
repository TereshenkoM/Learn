from fastapi import FastAPI, Body
from grpclib.server import Server
from server import TodoServicer
import asyncio
from todo_pb2 import TodoCreateRequest
from todo_grpc import TodoServiceStub
from grpclib.client import Channel
import json
import os


app = FastAPI()
JSON_FILE = "todos.json"

# Инициализация gRPC-сервера
grpc_server = Server([TodoServicer()])

@app.on_event("startup")
async def startup():
    await grpc_server.start("0.0.0.0", 50051)

@app.on_event("shutdown")
async def shutdown():
    await grpc_server.close()

@app.get("/rest/todos")
async def get_todos():
    if not os.path.exists(JSON_FILE):
        return {"todos": []}
    
    with open(JSON_FILE, "r") as f:
        todos = json.load(f)
    return {"todos": todos}

@app.post("/rest/todos")
async def create_todo(
    title: str = Body(...),
    description: str = Body(default="")
):
    async with Channel("127.0.0.1", 50051) as channel:
        stub = TodoServiceStub(channel)
        response = await stub.CreateTodo(
            TodoCreateRequest(title=title, description=description)
        )
        return {
            "id": response.id,
            "title": response.title
        }