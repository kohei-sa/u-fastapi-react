from fastapi import FastAPI
from routers import route_todo, route_auth
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(route_todo.router)
app.include_router(route_auth.router)
