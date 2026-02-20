FROM python:3.12-slim

RUN useradd -m appuser

RUN pip install --no-cache-dir poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-root && \
    rm -rf $POETRY_CACHE_DIR

COPY . .

USER appuser

EXPOSE 8000