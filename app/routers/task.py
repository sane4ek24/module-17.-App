from fastapi import APIRouter

ruter_task = APIRouter(prefix='/task', tags=['task'])


@ruter_task.get('/')
async def all_tasks():
    pass


@ruter_task.get('/task_id')
async def task_by_id():
    pass


@ruter_task.post('/create')
async def create_task():
    pass


@ruter_task.put('/update')
async def update_task():
    pass


@ruter_task.delete('/delete')
async def delete_task():
    pass
