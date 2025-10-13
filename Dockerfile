FROM python:3.14-slim

WORKDIR /app

RUN mkdir codebase

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main

COPY . .

CMD ["poetry", "run", "python3", "-m", "src"]