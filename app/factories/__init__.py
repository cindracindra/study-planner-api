from app.factories.abc import PersonFactory, RestrictedStudentPersonalDetailsFactory
from app.factories.confidence_ratings import ConfidenceRatingFactory, ModuleRatingFactory
from app.factories.tasks import TaskFactory


abc_factories = [
    PersonFactory,
    RestrictedStudentPersonalDetailsFactory,
]


orm_factories = [
    ConfidenceRatingFactory,
    ModuleRatingFactory,
    TaskFactory,
]
