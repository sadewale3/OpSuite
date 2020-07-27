# Build actual container
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim as production-stage
WORKDIR /app
RUN apt-get update
RUN apt-get install -y build-essential postgresql curl libpq-dev && \
    apt-get clean && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false


COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-dev

COPY init/ /app/init/
COPY opsuite/ /app/opsuite
RUN poetry build 
RUN python3 -m pip install dist/*.whl
ENV PYTHONPATH=/app