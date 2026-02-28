# Multi-stage Dockerfile for noticeboard

# Builder: create virtualenv and install Python dependencies
FROM python:3.12-slim as builder

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# System deps needed for building some packages and Postgres client
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       curl \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv (optional) — keep installer in builder so runtime stays small
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

# Copy metadata and lock files first for better layer cache
COPY pyproject.toml uv.lock ./

# Use uv to sync/install dependencies into a virtualenv at /.venv
# If you prefer plain pip, replace these lines with venv + pip install -e .
RUN uv sync --locked

# Ensure venv has pip and tooling upgraded
RUN . /root/.local/bin/env && uv run python -m ensurepip --upgrade || true
RUN . /root/.local/bin/env && uv run python -m pip install --upgrade pip setuptools wheel || true

# Install production server and static tools into the uv-managed venv
# Use Uvicorn directly (no gunicorn)
RUN . /root/.local/bin/env && uv run python -m pip install uvicorn whitenoise || true

# Copy the application code
COPY manage.py ./
COPY core/ ./core/
COPY noticeboard/ ./noticeboard/

# Final stage: slim runtime image
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install runtime system deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv and code from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/manage.py /app/manage.py
COPY --from=builder /app/core /app/core
COPY --from=builder /app/noticeboard /app/noticeboard

# Use venv's bin directory
ENV PATH="/app/.venv/bin:$PATH"

# Static files dir for collectstatic
RUN mkdir -p /app/staticfiles /app/media
ENV STATIC_ROOT=/app/staticfiles MEDIA_ROOT=/app/media

EXPOSE 8000

# Default command: run migrations, collectstatic, then start uvicorn from venv
CMD ["sh", "-lc", "/app/.venv/bin/python manage.py migrate && /app/.venv/bin/python manage.py collectstatic --noinput && /app/.venv/bin/uvicorn core.asgi:application --host 0.0.0.0 --port 8000 --workers 4"]
