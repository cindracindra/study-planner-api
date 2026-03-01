FROM python:3.13

# Install required system dependencies
RUN apt update
RUN apt install -y --no-install-recommends build-essential libldap2-dev libsasl2-dev ldap-utils libpq-dev

WORKDIR /study_planner
COPY app /study_planner/app
COPY migrations /study_planner/migrations
COPY main.py cli.py alembic.ini /study_planner/

ENV POETRY_VIRTUALENVS_CREATE=false
COPY poetry.lock pyproject.toml /study_planner/
RUN pip install poetry
RUN poetry install --no-root --no-interaction --no-ansi
