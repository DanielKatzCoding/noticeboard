# Noticeboard

A minimal Django-based noticeboard application. This repository includes both development and production Dockerfiles and a `docker-compose.yml` that can run dev or prod services alongside PostgreSQL.

## Contents

- `Dockerfile.dev` — Development image with hot-reload (Django `runserver`).
- `Dockerfile.prod` — Production multi-stage build (venv, Uvicorn, collectstatic).
- `docker-compose.yml` — Services: `db`, `web-dev`, `web-prod`.
- `core/` — Django project settings and ASGI/WGI entry points.
- `noticeboard/` — Django app code (models, views, templates).

## Quick start (Development)

1. Copy environment file:

```bash
cp .env.example .env
```

2. Start services (development):

```bash
docker-compose up --build web-dev db
```

3. Visit: http://localhost:8000

Notes:
- The development service mounts the project directory as a volume, so code changes reload immediately.
- Use `docker-compose logs -f web-dev` to view logs.

## Quick start (Production)

This project provides a production-optimized image. It's intended as an example; adjust for your hosting platform.

1. Ensure you have a populated `.env` (see `.env.example`).
2. Build and start production service:

```bash
docker-compose up --build web-prod db
```

3. Production server is exposed on `8001` (mapped to container's `8000`) by default in `docker-compose.yml`.

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

- Collect static files:

```bash
docker compose run --rm web-prod python manage.py collectstatic --noinput
```

## Environment variables

Copy `.env.example` to `.env` and update values for your environment. Do NOT commit secrets to source control.

Important variables (see `.env.example` for full list):

- `DEBUG` — `True` or `False`. Should be `False` in production.
- `SECRET_KEY` — Django secret key.
- `ALLOWED_HOSTS` — Comma-separated allowed hostnames.
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` — Postgres credentials.
- `DB_HOST`, `DB_PORT` — Database host and port (compose uses service name `db`).

## Database

This project uses PostgreSQL. The `db` service in `docker-compose.yml` uses `postgres:15-alpine` and mounts a named volume `postgres_data` to persist data.

If you see a warning like `database "noticeboard_db" has no actual collation version, but a version was recorded` during startup, it is usually harmless and related to locale differences between the image and the created DB cluster. It does not affect functionality.

## ASGI lifespan warning

If your server logs `ASGI 'lifespan' protocol appears unsupported.`, we've added a small wrapper in `core/asgi.py` to handle the lifespan protocol gracefully.

## Running tests

Run Django tests inside a container or locally if you prefer:

```bash
docker compose run --rm web-dev python manage.py test
```

## Static files

- The production image runs `collectstatic` at container start.
- Static files are stored in `/app/staticfiles` inside the container and served by the Uvicorn process with `whitenoise` in the production image.

## Developing and contributing

- Create a branch per feature/bug: `git checkout -b feat/your-feature`
- Keep commits small and focused.
- Run tests before opening a PR.

## Troubleshooting

- If the prod container fails to start, check logs:

```bash
docker compose logs web-prod
```

- Ensure `.env` values are correct and Postgres credentials match.

- If you mount a local virtualenv or Python binary into the container, remove the mount — it can conflict with container Python.

## Files of interest

- `core/asgi.py` — ASGI entrypoint and lifespan wrapper.
- `core/settings.py` — Project settings.
- `noticeboard/models.py` — Example models and app logic.

## License

This project does not include a license by default. Add an appropriate `LICENSE` file if you plan to open-source it.
