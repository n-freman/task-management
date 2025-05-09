import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import text

from task_management.db.schemas import tasks_table, users_table
from task_management.domain import Task, User

from .base import BaseRepository


class TasksRepository(BaseRepository):
    async def add(self,
                  title: str,
                  description: str,
                  user: User,
                  is_completed: bool,
                  priority: int):
        new_task = Task(
            id=str(uuid.uuid4()),  # Or any other ID generation strategy
            title=title,
            description=description,
            is_completed=is_completed,
            priority=priority,
            user=str(user.id),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.session.add(new_task)
        await self.session.commit()
        return new_task

    async def delete(self, task_id: str) -> None:
        query = select(tasks_table).filter(tasks_table.c.id == task_id)
        result = await self.session.execute(query)
        task_row = result.scalars().first()
        
        if not task_row:
            raise NoResultFound(f"Task with ID {task_id} does not exist")
        
        await self.session.execute(
            tasks_table.delete().where(tasks_table.c.id == task_id)
        )
        await self.session.commit()

    async def get_all_for_user(self,
                               user: User,
                               is_completed: Optional[bool] = None,
                               sort_by: Optional[str] = None):
        query = select(tasks_table).filter(tasks_table.c.user == str(user.id))

        if is_completed is not None:
            query = query.filter(tasks_table.c.is_completed == is_completed)

        if sort_by is not None:
            query = query.order_by(text(sort_by))

        result = await self.session.execute(query)
        tasks = result.fetchall()

        if not tasks:
            raise NoResultFound(f"No tasks found for user with ID {user.id}")

        return tasks

    async def get(self, task_id: str):
        query = select(tasks_table).filter(tasks_table.c.id == task_id)
        result = await self.session.execute(query)
        tasks = result.fetchone()

        if not tasks:
            raise NoResultFound(f"No tasks found with ID {task_id}")

        return tasks

    async def update(self, task_id: str, **kwargs):
        query = (
            update(tasks_table)
            .where(tasks_table.c.id == task_id)
            .values(**kwargs)
            .returning(tasks_table)  # Return the updated row
        )

        result = await self.session.execute(query)
        task = result.fetchone()  # Fetch the updated task

        if not task:
            raise NoResultFound(f"Task with ID {task_id} not found")

        return task

