from typing import Annotated, Union

from fastapi import FastAPI, Request, Form, Header
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uuid import uuid4

class Todo:
  def __init__(self, text: str):
    self.id = uuid4()
    self.text = text
    self.done = False

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

todos = []

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
  return templates.TemplateResponse(request=request, name="index.html")

@app.get("/todos", response_class=HTMLResponse)
async def list_todos(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
  if hx_request:
    return templates.TemplateResponse(
      request=request, name="todos.html", context={"todos": todos}
    )

  return JSONResponse(content=jsonable_encoder(todos))

@app.post("/todos", response_class=HTMLResponse)
async def create_todo(request: Request, todo: Annotated[str, Form()]):
  todos.append(Todo(todo))
  return templates.TemplateResponse(
    request=request, name="todos.html", context={"todos": todos}
  )

@app.put("/todos/{todo_id}", response_class=HTMLResponse)
async def update_todo(request: Request, todo_id: str, text: Annotated[str, Form()]):
  for index, todo in enumerate(todos):
    if str(todo.id) == todo_id:
      todo.text = text
      break
  return templates.TemplateResponse(
    request=request, name="todos.html", context={"todos": todos}
  )

@app.post("/todos/{todo_id}/toggle", response_class=HTMLResponse)
async def toggle_todo(request: Request, todo_id: str):
  for index, todo in enumerate(todos):
    if str(todo.id) == todo_id:
      todos[index].done = not todos[index].done
      break
  return templates.TemplateResponse(
    request=request, name="todos.html", context={"todos": todos}
  )

@app.post("/todos/{todo_id}/delete", response_class=HTMLResponse)
async def delete_todo(request: Request, todo_id: str):
  for index, todo in enumerate(todos):
    if str(todo.id) == todo_id:
      del todos[index]
      break
  return templates.TemplateResponse(
    request=request, name="todos.html", context={"todos": todos}
  )
