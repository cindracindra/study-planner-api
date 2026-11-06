import factory
import random

from app.doc_upstream_services.abc.schemas import (
    Person,
    AppSchemasCustomPeopleDetailsStudentDetails,
    ModuleLevelReadOptimised,
    RoleInDepartment,
)


class PersonFactory(factory.Factory):
    class Meta:
        model = Person

    login = factory.Faker("user_name")
    lastname = factory.Faker("last_name")
    firstname = factory.Faker("first_name")


class ModuleLevelReadOptimisedFactory(factory.Factory):
    class Meta:
        model = ModuleLevelReadOptimised

    code = factory.Faker("numerify", text="#####")
    title = factory.Faker("sentence", nb_words=4)
    ects = factory.Faker("random_element", elements=[7.5, 15.0, 22.5])
    terms = factory.LazyFunction(lambda: [random.randint(1, 3)])
    applicable_cohorts = factory.LazyFunction(
        lambda: [random.choice(["c1", "c2", "c3", "c4"])]
    )
    exam_contribution = None
    coursework_contribution = None
    exam_questions_total = None
    exam_questions_needed = None
    level = None


class AppSchemasCustomPeopleDetailsStudentDetailsFactory(factory.Factory):
    class Meta:
        model = AppSchemasCustomPeopleDetailsStudentDetails

    login = factory.Faker("user_name")
    email = factory.Faker("email")
    lastname = factory.Faker("last_name")
    firstname = factory.Faker("first_name")
    salutation = factory.Faker("prefix")
    year = factory.Faker("short_year")
    role_in_department = RoleInDepartment.student
    cohort = factory.Faker("pystr_format", string_format="c#")
    cid = factory.Faker("numerify", text="########")
    studentstatus = "active"
    degree_year = factory.Faker(
        "random_element", elements=["mc1", "mc2", "mc3", "bc1", "bc2"]
    )
    modules = factory.LazyFunction(list)
    modules_helped = factory.LazyFunction(list)
    personal_tutor = factory.SubFactory(PersonFactory)
