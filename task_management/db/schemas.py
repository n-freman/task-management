import uuid

from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    MetaData,
    String,
    Table,
    Text,
    func,
)

from task_management import config

metadata = MetaData()

users_table = Table(
    'users',
    metadata,
    Column('id', UUID, default=uuid.uuid4, primary_key=True),
    Column('email', String(120), unique=True),
    Column('password', Text),
    Column('created_at', DateTime, nullable=False, server_default=func.now()),
    Column('updated_at',
           DateTime,
           nullable=False,
           server_default=func.now(),
           onupdate=func.now()),
)

tasks_table = Table(
    'tasks',
    metadata,
    Column('id', UUID, default=uuid.uuid4, primary_key=True),
    Column('user', ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    Column('title', String(64), nullable=False),
    Column('description', Text),
    Column('is_completed', Boolean, default=False),
    Column('created_at', DateTime, nullable=False, server_default=func.now()),
    Column('updated_at',
           DateTime,
           nullable=False,
           server_default=func.now(),
           onupdate=func.now()),
)
