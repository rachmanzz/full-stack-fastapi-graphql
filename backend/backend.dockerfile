FROM python:3.8

WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app/pyproject.toml ./app/poetry.lock* /app/
COPY  ./app/alembic.ini /app/

RUN pip install 'poetry==1.1.4'.
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY ./app /app/app
ENV PYTHONPATH=/app
EXPOSE 8000 8000
