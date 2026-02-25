# Use official Python runtime as base image
FROM python:3.12

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager using curl
# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"
ENV UV_LINK_MODE=copy

# Copy project files
COPY pyproject.toml ./
COPY uv.lock ./
COPY manage.py ./
COPY core/ ./core/
COPY noticeboard/ ./noticeboard/

# Install Python dependencies using uv
RUN uv sync --locked

# Ensure the uv-managed virtualenv has pip installed and upgraded
# Source uv environment and use uv to run ensurepip and upgrade pip/setuptools
RUN . /root/.local/bin/env && uv run python -m ensurepip --upgrade || true
RUN . /root/.local/bin/env && uv run python -m pip install --upgrade pip setuptools wheel || true


# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/admin', timeout=5)" || exit 1

# Run using `uv` so uv-managed dependencies and environment are active
# Use shell form to source the uv env script then run the uv command
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]