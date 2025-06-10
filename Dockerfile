FROM python:3.11-slim

WORKDIR /app

COPY . .


CMD ["python3", "-m", "src"]