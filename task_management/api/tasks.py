import uuid
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound

from task_management.db.repositories.tasks import TasksRepository
from task_management.db.utils import AsyncSession, get_async_session
from task_management.domain import User

from .auth.utils import JWTBearer
from .schemas import (
    AllowedTaskSortFields,
    TaskCreateRequest,
    TaskDataResponse,
    TaskUpdateRequest,
)

router = APIRouter(prefix='/tasks', tags=['Task Management'])


@router.post('/')
async def create_task(
    request: TaskCreateRequest,
    user: Annotated[User, Depends(JWTBearer())],
    session: AsyncSession = Depends(get_async_session)
) -> TaskDataResponse:
    tasks_repo = TasksRepository(session)
    task = await tasks_repo.add(request.title,
                         request.description,
                         user,
                         request.is_completed,
                         request.priority)
    return TaskDataResponse.from_dataclass(task)


@router.get('/')
async def get_current_users_tasks(
    user: Annotated[User, Depends(JWTBearer())],
    is_completed: Optional[bool] = None,
    sort_by: Optional[AllowedTaskSortFields] = None,
    session: AsyncSession = Depends(get_async_session)
) -> List[TaskDataResponse]:
    tasks_repo = TasksRepository(session)
    tasks = await tasks_repo.get_all_for_user(user, is_completed, sort_by)
    return list(map(TaskDataResponse.from_dataclass, tasks))


@router.get('/{task_id}')
async def get_task(
    task_id: uuid.UUID,
    user: Annotated[User, Depends(JWTBearer())],
    session: AsyncSession = Depends(get_async_session)
) -> TaskDataResponse:
    try:
        tasks_repo = TasksRepository(session)
        task = await tasks_repo.get(str(task_id))
        if task.user != user.id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                'You can only access your own tasks')
        return TaskDataResponse.from_dataclass(task)
    except NoResultFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            str(e))


@router.put('/{task_id}')
async def update_task(
    request: TaskUpdateRequest,
    user: Annotated[User, Depends(JWTBearer())],
    session: AsyncSession = Depends(get_async_session)
) -> TaskDataResponse:
    try:
        tasks_repo = TasksRepository(session)
        update_data = request.model_dump()
        update_data.pop('id')
        task = await tasks_repo.update(request.id, **update_data)
        return TaskDataResponse.from_dataclass(task)
    except NoResultFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            str(e))


@router.delete('/{task_id}')
async def delete_task(
    task_id: uuid.UUID,
    user: Annotated[User, Depends(JWTBearer())],
    session: AsyncSession = Depends(get_async_session)
):
    try:
        tasks_repo = TasksRepository(session)
        task = await tasks_repo.get(str(task_id))
        if task.user != user.id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                'You can only delete your own tasks')
        await tasks_repo.delete(str(task_id))
    except NoResultFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            str(e))

