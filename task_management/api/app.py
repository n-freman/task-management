from contextlib import asynccontextmanager

from fastapi import FastAPI

from task_management.db.schemas import start_mappers

from .auth.routes import router as auth_router
from .tasks import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_mappers()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(task_router)


@app.get('/')
def lifecheck():
    return {'detail': 'API is up and running'}

