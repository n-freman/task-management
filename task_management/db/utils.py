from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from task_management import config

aengine = create_async_engine(url=config.get_db_uri())
AsyncSessionLocal = sessionmaker(
    bind=aengine,  # type: ignore
    class_=AsyncSession,
    expire_on_commit=False,
    future=True
)


async def get_async_session():
    async with AsyncSessionLocal() as session: # type: ignore
        yield session

