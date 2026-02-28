import string

from factory import Faker, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

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
    rating = Faker("random_element", elements=[None, -1, 1, 2, 3, 4, 5])
    term_week = Faker("pyint", min_value=1, max_value=11)
    confidence_rating = SubFactory(ConfidenceRatingFactory)
