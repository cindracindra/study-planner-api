import string

from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory
from app.factories.factory import *

from app.models.confidence_ratings import ConfidenceRating, ModuleRating


class ConfidenceRatingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ConfidenceRating
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    year = Faker("short_year")
    username = Faker("pystr_format", string_format="###???")


class ModuleRatingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ModuleRating
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    module_code = Faker(
        "pystr_format", string_format="#####", letters=string.ascii_uppercase
    )
    rating = Faker("ratings")
    term_week = Faker("pyint", min_value=1, max_value=11)
