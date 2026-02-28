# Noticeboard

A minimal Django-based noticeboard application. This repository includes both development and production Dockerfiles and a `docker-compose.yml` that can run dev or prod services alongside PostgreSQL.

## Contents

- `Dockerfile.dev` — Development image with hot-reload (Django `runserver`).
- `Dockerfile.prod` — Production multi-stage build (venv, Uvicorn, collectstatic).
- `docker-compose.yml` — Services: `db`, `web-dev`, `web-prod`.
- `core/` — Django project settings and ASGI/WGI entry points.
- `noticeboard/` — Django app code (models, views, templates).

## Quick start (Development)

1. Copy environment files:

```bash
cp .env.example .env.dev
cp .env.example .env.prod
cp .env.example .env.db
```

2. Update the copied files with your preferred values (especially `SECRET_KEY`).

3. Start services (development):

```bash
docker-compose up --build web-dev db
```

4. Visit: http://localhost:8001

Notes:
- The development service mounts the project directory as a volume, so code changes reload immediately.
- Use `docker-compose logs -f web-dev` to view logs.

## Quick start (Production)

This project provides a production-optimized image. It's intended as an example; adjust for your hosting platform.

1. Ensure you have populated `.env.prod` and `.env.db` files (see `.env.example`).

2. Build and start production service:

```bash
docker-compose up --build web-prod db
```

3. Production server is exposed on `8000` (mapped to container's `8000`) by default in `docker-compose.yml`.
   Visit: http://localhost:8000

## Environment Files

This project now uses separate environment files for different services:

- `.env.db` - Database configuration (used by the `db` service)
- `.env.dev` - Development configuration (used by the `web-dev` service)
- `.env.prod` - Production configuration (used by the `web-prod` service)
- `.env.example` - Template file to copy from when creating your environment files

To set up your environment files, copy `.env.example` to each of the required files and customize as needed:

```bash
cp .env.example .env.db
cp .env.example .env.dev
cp .env.example .env.prod
```

Then edit each file to set your preferred values, especially ensuring that:
- Database credentials match across all files
- `SECRET_KEY` is changed to a secure random value
- `DEBUG` is set to `False` in production

## Common Docker commands

- Rebuild images:

```bash
docker-compose build --no-cache
```

- Stop and remove containers:

```bash
docker-compose down
```

- Run migrations manually in a service:

```bash
docker compose run --rm web-prod python manage.py migrate
```

## Environment variables

Each service uses its own environment file:
- `db` service uses `.env.db`
- `web-dev` service uses `.env.dev`
- `web-prod` service uses `.env.prod`

Important variables (see `.env.example` for full list):

- `DEBUG` — `True` or `False`. Should be `False` in production.
- `SECRET_KEY` — Django secret key (must be unique and secret).
- `ALLOWED_HOSTS` — Comma-separated allowed hostnames.
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` — Postgres credentials.
- `DB_HOST`, `DB_PORT` — Database host and port (compose uses service name `db`).

## Database

This project uses PostgreSQL. The `db` service in `docker-compose.yml` uses `postgres:15-alpine` and mounts a named volume `postgres_data` to persist data.

If you see a warning like `database "noticeboard_db" has no actual collation version, but a version was recorded` during startup, it is usually harmless and related to locale differences between the image and the created DB cluster. It does not affect functionality.

## Running tests

Run Django tests inside a container or locally if you prefer:

```bash
docker compose run --rm web-dev python manage.py test
```

Or run tests locally (requires setting up local environment):

```bash
python manage.py test
```

## Static files

- The production image runs `collectstatic` at container start.
- Static files are stored in `/app/staticfiles` inside the container and served by the Uvicorn process with `whitenoise` in the production image.

## Troubleshooting

- If the prod container fails to start, check logs:

```bash
docker compose logs web-prod
```

- Ensure `.env` values are correct and Postgres credentials match across all environment files.

- If you mount a local virtualenv or Python binary into the container, remove the mount — it can conflict with container Python.

## Files of interest

- `core/asgi.py` — ASGI entrypoint and lifespan wrapper.
- `core/settings.py` — Project settings.
- `noticeboard/models.py` — Example models and app logic.
