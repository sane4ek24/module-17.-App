from fastapi import FastAPI
from routers.task import router_task
from routers.user import router_user

app = FastAPI()


@app.get('/')
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(router_user)
app.include_router(router_task)
