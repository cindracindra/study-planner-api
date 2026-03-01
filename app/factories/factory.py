import random

import factory
from faker.providers import BaseProvider, internet, job, lorem, person, python


TERMS = (1, 2, 3)
RATINGS = [None, -1, 1, 2, 3, 4, 5]


class ShortYear(BaseProvider):
    def short_year(self) -> str:
        return random.choice(["2122", "2223", "2324", "2425", "2526"])  # nosec


class Terms(BaseProvider):
    def terms(self) -> list[int]:
        subset_length = random.randint(1, 3)  # nosec
        return random.sample(TERMS, subset_length)  # nosec


class Ratings(BaseProvider):
    def ratings(self) -> list[int | None]:
        return random.choice(RATINGS)  # nosec


factory.Faker.add_provider(python)
factory.Faker.add_provider(lorem)
factory.Faker.add_provider(internet)
factory.Faker.add_provider(person)
factory.Faker.add_provider(job)
factory.Faker.add_provider(ShortYear)
factory.Faker.add_provider(Terms)
factory.Faker.add_provider(Ratings)
