from fastapi import FastAPI
from app.routers.task import ruter_task
from app.routers.user import ruter_user

app = FastAPI()


@app.get('/')
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(ruter_user)
app.include_router(ruter_task)
