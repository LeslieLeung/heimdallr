FROM python:3.11.6-slim
WORKDIR /app

RUN adduser --disabled-password --gecos '' appuser

RUN pip install poetry && poetry config virtualenvs.create false

ENV PORT=9000

# dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

USER appuser
COPY heimdallr ./heimdallr
COPY main.py ./

CMD python -m uvicorn main:app --host 0.0.0.0 --port $PORT