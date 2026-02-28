from factory import Faker, LazyFunction
from factory.alchemy import SQLAlchemyModelFactory
from datetime import date

from app.models.tasks import Task


class TaskFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Task
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    year = Faker("short_year")
    username = Faker("pystr_format", string_format="###???")
    title = Faker("sentence", nb_words=4)
    creation_date = LazyFunction(date.today)
    task_completed = False
