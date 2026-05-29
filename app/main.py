from fastapi import FastAPI
from app.routes.tasks import router
from fastapi.staticfiles import StaticFiles
from app.database.todo_database import BASE , engine

app = FastAPI()

BASE.metadata.create_all(bind = engine)

app.include_router(router)

app.mount("/static",StaticFiles(directory="static"),name="app/static")

