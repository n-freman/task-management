import pytest
import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from task_management.domain import User, Task
from task_management.db.repositories.tasks import TasksRepository


@pytest.fixture
async def user(session: AsyncSession):
    """Create a test user."""
    test_user = User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        password="hashed_password",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    session.add(test_user)
    await session.commit()
    return test_user


@pytest.fixture
async def repository(session: AsyncSession):
    """Return the TasksRepository instance."""
    return TasksRepository(session)


@pytest.fixture
async def task(repository: TasksRepository, user: User):
    """Create a test task."""
    return await repository.add(
        title="Test Task",
        description="Test Description",
        user=user,
        is_completed=False,
        priority=5,
    )


@pytest.mark.asyncio
async def test_add_task(repository: TasksRepository, user: User):
    """Test adding a new task."""
    task = await repository.add(
        title="New Task",
        description="Description",
        user=user,
        is_completed=False,
        priority=3,
    )
    
    assert task.id is not None
    assert task.title == "New Task"
    assert task.user == str(user.id)


@pytest.mark.asyncio
async def test_get_task(repository: TasksRepository, task: Task):
    """Test retrieving a task by ID."""
    fetched_task = await repository.get(task.id)

    assert fetched_task is not None
    assert fetched_task.id == task.id


@pytest.mark.asyncio
async def test_get_task_not_found(repository: TasksRepository):
    """Test fetching a task that does not exist."""
    with pytest.raises(NoResultFound):
        await repository.get(str(uuid.uuid4()))


@pytest.mark.asyncio
async def test_get_all_for_user(repository: TasksRepository, user: User, task: Task):
    """Test retrieving all tasks for a user."""
    tasks = await repository.get_all_for_user(user)

    assert len(tasks) > 0
    assert any(t.id == task.id for t in tasks)  # Ensure test task is in results


@pytest.mark.asyncio
async def test_get_all_for_user_no_tasks(repository: TasksRepository, user: User):
    """Test retrieving tasks for a user with no tasks."""
    with pytest.raises(NoResultFound):
        await repository.get_all_for_user(user)


@pytest.mark.asyncio
async def test_update_task(repository: TasksRepository, task: Task):
    """Test updating a task."""
    updated_task = await repository.update(task.id, is_completed=True)

    assert updated_task is not None
    assert updated_task.is_completed is True  # is_completed column


@pytest.mark.asyncio
async def test_update_task_not_found(repository: TasksRepository):
    """Test updating a non-existent task."""
    with pytest.raises(NoResultFound):
        await repository.update(str(uuid.uuid4()), is_completed=True)


@pytest.mark.asyncio
async def test_delete_task(repository: TasksRepository, task: Task):
    """Test deleting a task."""
    await repository.delete(task.id)

    with pytest.raises(NoResultFound):
        await repository.get(task.id)


@pytest.mark.asyncio
async def test_delete_task_not_found(repository: TasksRepository):
    """Test deleting a non-existent task."""
    with pytest.raises(NoResultFound):
        await repository.delete(str(uuid.uuid4()))

