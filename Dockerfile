FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install openenv-core uvicorn fastapi requests

EXPOSE 8000

CMD ["python", "-m", "server.app"]