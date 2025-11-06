# Multi-stage build for development and production
FROM python:3.13.5-slim AS base
WORKDIR /app

RUN adduser --disabled-password --gecos '' appuser
RUN pip install poetry

# Development stage
FROM base AS dev

# Copy package files and install dependencies as root first
COPY pyproject.toml poetry.lock ./

# Set up virtualenv with proper permissions
ENV VIRTUAL_ENV=/app/.venv
RUN python -m venv $VIRTUAL_ENV && chown -R appuser:appuser $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN poetry install --with dev

# Create data directory for SQLite and ensure proper ownership
RUN mkdir -p /app/data && chown -R appuser:appuser /app

# Switch to appuser for running the application
USER appuser
ARG HEIMDALLR_VERSION
ENV HEIMDALLR_VERSION=$HEIMDALLR_VERSION
ARG COMMIT_ID
ENV COMMIT_ID=$COMMIT_ID

# For development, source code will be mounted as volume
# Install dependencies and run with hot reload
CMD ["sh", "-c", "poetry install && python main.py"]

# Production stage
FROM base AS prod
COPY pyproject.toml poetry.lock ./

# Set up virtualenv with proper permissions
ENV VIRTUAL_ENV=/app/.venv
RUN python -m venv $VIRTUAL_ENV && chown -R appuser:appuser $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN poetry install --without dev

# Create data directory for SQLite and ensure proper ownership
RUN mkdir -p /app/data && chown -R appuser:appuser /app

# Copy application code
COPY heimdallr ./heimdallr
COPY main.py ./

# Switch to appuser for running the application
USER appuser

ARG HEIMDALLR_VERSION
ENV HEIMDALLR_VERSION=$HEIMDALLR_VERSION
ARG COMMIT_ID
ENV COMMIT_ID=$COMMIT_ID

# Expose port
EXPOSE 9000

CMD ["python", "main.py"]