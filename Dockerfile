FROM python:3.11-slim

WORKDIR /app

COPY . /app

COPY .env /app/.env

RUN pip install poetry

RUN poetry install --extras "docker" --no-root

EXPOSE 8000

CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn task_management.main:app --host 0.0.0.0 --port 8000"]

