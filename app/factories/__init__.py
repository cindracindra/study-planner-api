from app.factories.abc import (
    PersonFactory,
    ModuleLevelReadOptimisedFactory,
    AppSchemasCustomPeopleDetailsStudentDetailsFactory,
)
from app.factories.confidence_ratings import (
    ConfidenceRatingFactory,
    ModuleRatingFactory,
)
from app.factories.tasks import TaskFactory
from app.factories.banner import BannerFactory


abc_factories = [
    PersonFactory,
    ModuleLevelReadOptimisedFactory,
    AppSchemasCustomPeopleDetailsStudentDetailsFactory,
]


orm_factories = [
    ConfidenceRatingFactory,
    ModuleRatingFactory,
    TaskFactory,
    BannerFactory,
]
