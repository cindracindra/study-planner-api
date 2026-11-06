# Study Planner API

[![CI](https://github.com/cindracindra/study-planner-api/actions/workflows/ci.yml/badge.svg)](https://github.com/cindracindra/study-planner-api/actions/workflows/ci.yml)

![Python 3.13](https://img.shields.io/badge/python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688)

A FastAPI service behind a **Study Planner** feature for **Scientia**, the student portal of
Imperial College London's Department of Computing. Students use it to keep a daily to-do list,
rate how confident they feel in each module week by week, and see a motivational banner on
their dashboard.

I built it as my individual project for the Software Systems Engineering (SSE) course at
Imperial (February to March 2026). It includes the service, its database schema and migrations,
the tests, and the integration into the existing Scientia front end and its backend-for-frontend.

## Features

| Area | What it does | Endpoints |
|---|---|---|
| **Personal tasks** | A daily to-do list. Completed tasks drop off the next day; unfinished ones carry over. | `GET / POST /me/{year}/personal-tasks`<br>`GET / PATCH / DELETE /me/{year}/personal-tasks/{id}` |
| **Confidence ratings** | Students rate each enrolled module from 1 to 5 for every term week, shown as a heat map. On first access each day, the service syncs the module list from the department's ABC (student records) API and adds any missing rating slots. | `GET /me/{year}/personal-confidence-ratings`<br>`PATCH /me/{year}/personal-confidence-ratings/modules/{id}` |
| **Daily banner** | Shows a quote from [ZenQuotes](https://zenquotes.io) each day (with a built-in fallback list), a random "excuse", or a message the student writes. | `GET / PATCH /me/{year}/banner` |

Every route is scoped to the authenticated user (`/me/...`) and an academic year (`2526` = 2025–26).
Interactive OpenAPI docs are served at `/`.

## Architecture

```mermaid
flowchart LR
    FE["Scientia front end<br/>(React + TypeScript)"] --> BFF["scientia-api<br/>(FastAPI BFF)"]
    BFF --> SP["study-planner-api<br/>(this repo)"]
    SP --> DB[(PostgreSQL)]
    SP -. module enrolments .-> ABC["ABC API<br/>(student records)"]
    SP -. daily quote .-> ZQ["zenquotes.io"]
```

- **FastAPI + SQLModel** for the routes and ORM models, with **Pydantic** schemas for request and response validation.
- **Alembic** for schema migrations; CI checks that they upgrade, downgrade and upgrade again cleanly.
- **Dependency injection** for the database session, authentication and the upstream ABC client,
  so tests can swap each one out. In development, both the department's LDAP login and the ABC API are
  replaced by in-memory fakes (`app/dev_service_providers/`).
- **Lazy daily sync**: confidence-rating slots are created when the student first loads them each day
  (tracked in `user_sync_status`), rather than by a scheduled job.

### My contributions outside this repo

The feature spans three codebases. This repo is the part I own outright. The other two belong to the
department's EdTech team and are not public, so they are only described here:

- **Scientia front end** (React, TypeScript, Radix UI): a new Study Planner page with
  upcoming-deadline, daily-focus, task-list, confidence-map and banner panes; six data hooks;
  and typed schemas for the new resources (about 1,200 lines).
- **scientia-api** (the backend-for-frontend): authenticated proxy endpoints and a typed service client
  that forward Study Planner requests to this API (about 280 lines).

## Tech stack

Python 3.13 · FastAPI · SQLModel / SQLAlchemy · Pydantic v2 · Alembic · PostgreSQL ·
Typer (CLI) · pytest + factory_boy · Ruff · ty · Docker · GitHub Actions

## Running locally

### With Docker (simplest)

```bash
docker compose -f dev.docker-compose.yml up --build
docker compose -f dev.docker-compose.yml exec api alembic upgrade head
docker compose -f dev.docker-compose.yml exec api python cli.py populate_db 2526
```

The API is then available at <http://localhost:8000>.

### With Poetry

Requires Python 3.13+ and a local PostgreSQL server with a `study_planner` database.
By default the app connects to `postgresql://user:pass@localhost/study_planner`; set
`DATABASE_URL` to use something else.

```bash
poetry install
poetry run alembic upgrade head
poetry run python cli.py populate_db 2526
poetry run fastapi dev --host 0.0.0.0 --port 8000
```

### Logging in

Development mode uses a fake LDAP service, so any username from
`app/dev_service_providers/ldap_authentication.py` (e.g. `hpotter`) works with any password,
via HTTP Basic auth.

## Tests

The suite creates and drops a throwaway `test_study_planner` database on the server given by
`TEST_DB_SERVER_URL` (for example `postgresql://` for a local socket connection).

```bash
TEST_DB_SERVER_URL=postgresql:// poetry run pytest --cov=app
```

Tests that call the real ZenQuotes API are marked `integration` and skipped by default:

```bash
poetry run pytest -m integration
```

## CLI

| Command | Purpose |
|---|---|
| `python cli.py populate_db <year>` | Seed the database with sample students, ratings and tasks |
| `python cli.py erase_data [--force]` | Delete all rows, keeping the tables |
| `alembic upgrade head` / `alembic downgrade -1` | Apply or roll back migrations |

## Acknowledgements

This service was built to run inside the Department of Computing's EdTech ecosystem and follows
the conventions of the department's existing services. A few support modules are adapted from
EdTech code; see [NOTICE](NOTICE) for the list. Everything else is my own work.

## License

My original code is released under the [MIT License](LICENSE). The adapted files listed in
[NOTICE](NOTICE) are not covered by that licence.
