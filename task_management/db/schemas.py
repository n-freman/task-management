import uuid

from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    func,
    CheckConstraint
)
from sqlalchemy.orm import properties, registry, relationship

from task_management import config, domain

metadata = MetaData()
mapper = registry()

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
    Column('priority', Integer, default=10),
    Column('created_at', DateTime, nullable=False, server_default=func.now()),
    Column('updated_at',
           DateTime,
           nullable=False,
           server_default=func.now(),
           onupdate=func.now()),
    CheckConstraint('priority >= 1 AND priority <= 10', name='check_priority_range'),
)


def start_mappers():
    mapper.map_imperatively(domain.User, users_table)
    mapper.map_imperatively(domain.Task,
                            tasks_table,
                            properties={
                                'user': relationship(domain.User)
                            })

