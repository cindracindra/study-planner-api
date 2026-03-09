# Study Planner API: SSE Project [cc4525]


## Project Requirements

* [Poetry](https://python-poetry.org/) for dependency management
* [FastAPI](https://fastapi.tiangolo.com/) - modern, fast web framework for building APIs
* [SQLModel](https://sqlmodel.tiangolo.com/) - SQL databases with Python type annotations
* [Pydantic](https://docs.pydantic.dev/) - data validation using Python type annotations
* [Alembic](https://alembic.sqlalchemy.org/) - database migrations
* [Typer](https://typer.tiangolo.com/) - CLI interface
* **Postgres SQL** - databases


## Running the app

You can run the app via Poetry or via Docker. At the moment, the instructions for running the app via Poetry are specific for MacOS users (due to the `brew` references); Windows and other Unix users may find it more convenient to run the app via Docker.

### Via Poetry (recommended for MacOS users)

> This option relies on a running local PostgreSQL instance. Make sure you have a `study-planner` database and a `user` user with password `pass` and full usage, creation and deletion privileges on it.

```shell
brew services start postgresql
poetry install
poetry run alembic upgrade head
poetry run python cli.py populate_db 2526
poetry run fastapi dev --host 0.0.0.0 --port 8000
```

For executing the test suite:

```shell
poetry run pytest
```

### Note on dummy users

The _development_ (default) configuration runs with a fake instance of the
LDAP service (to make things easier
locally). The users recognised by this fake service are defined in
`dev_service_providers/ldap_authentication.py`. You are provided
with several fake users. To log into the application,
you can actually enter anyone of the available usernames and any
character you wish as password (the actual value is ignored by the fake LDAP).

## CLI interface

The application uses Typer for its CLI interface. Custom commands can be found in `cli.py` at the project root.

Available commands:
* `python cli.py populate_db <year>` - Populate database with dummy data
* `python cli.py erase_data` - Erase all data from tables

Database migrations are handled by Alembic:
* `alembic upgrade head` - Apply all migrations
* `alembic downgrade -1` - Rollback one migration
* `alembic revision --autogenerate -m "description"` - Create a new migration