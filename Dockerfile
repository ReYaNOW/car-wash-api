FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/src


RUN apt-get update && apt-get install -y --no-install-recommends \
    make curl && \
    pip install poetry && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false  \
    && poetry install --no-root --no-interaction --no-ansi

COPY . .

# from web какой-то кал
RUN poetry config virtualenvs.create false  \
    && poetry install --no-root --no-interaction --no-ansi
