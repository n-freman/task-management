# Task management system

This repository contains the implementation of a test task related to a task management system.
The system allows users to create, update, delete, and track tasks efficiently.

## Tech Stack

* Backend: FastAPI (Python)
* Schema definitions: Pydantic
* Migration management: Alembic
* Database: PostgreSQL
* Web-server: Uvicorn
* Containerization: Docker

## How to run?

### Run on your machine

```bash
mv .env.example .env
```

Fill out .env file

```bash
poetry shell
poetry install
uvicorn task_management.main:app
```

