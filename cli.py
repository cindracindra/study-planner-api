from datetime import date, timedelta, timezone

from sqlmodel import SQLModel, Session
from typer import Typer, confirm, echo, Argument, Option, Exit

from app.database.connection import engine
from app.factories import orm_factories

from app.utils.factories import set_factories_session


cli = Typer(help="Study Planner API CLI")


@cli.command("erase_data")
def erase_data(
    force: bool = Option(
        False,
        "--force",
        "-f",
        help="Erase data without asking for confirmation.",
    )
):
    """
    Erase all data from database tables without dropping the tables.

    WARNING: This command will delete all data from all tables.
    Tables themselves remain intact (use Alembic migrations for schema changes).
    """

    if not force:
        delete_confirmation = confirm(
            "Are you sure you want to erase all data from the tables? This action cannot be undone."
        )

        if not delete_confirmation:
            echo("Operation cancelled.")
            raise Exit()

    with Session(engine) as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.exec(table.delete())
        session.commit()
    echo("All data erased successfully.")


@cli.command(name="populate_db")
def populate_db(
    year: str = Argument(help="Academic year in short form e.g. 2324 for 2023-2024"),
):
    """
    Populate the database with Harry Potter-themed test data for development or for QA environment.
    """
    with Session(engine) as session:
        set_factories_session(orm_factories, session)

        students = ["hpotter", "hgranger", "llovegood", "rweasley", "nlongbott"]
        module_codes = ["60001", "60003", "60004"]

        for student in students:
            cr = orm_factories.ConfidenceRatingFactory(username=student, year=year)
    
            for code in module_codes:
                for week in range(1, 12):
                    orm_factories.ModuleRatingFactory(
                        confidence_rating=cr,
                        module_code=code,
                        term_week=week,
                        rating=None,
                    )

            for i in range(5):
                orm_factories.TaskFactory(
                    username=student,
                    year=year,
                    title=f"Task {i+1} for {student}",
                    creation_date=date.now(timezone.utc) - timedelta(days=i),
                    task_completed=(i % 2 == 0),
                )

        echo("✓ Successfully seeded the database with Harry Potter-themed test data")


if __name__ == "__main__":
    cli()
