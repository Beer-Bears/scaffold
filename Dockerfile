FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

CMD ["poetry", "run", "python3", "-m", "src"]