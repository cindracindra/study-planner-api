import string

from factory import Faker, LazyFunction
from factory.alchemy import SQLAlchemyModelFactory
from app.factories.factory import *
from datetime import date

from app.models.banner import Banner

class BannerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Banner
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    year = Faker("short_year")
    username = Faker("pystr_format", string_format="###???")
    date = LazyFunction(date.today)
    banner_type = Faker("random_element", elements=["quote", "excuse", "custom"])
    display_text = Faker("pystr", max_chars=100)
