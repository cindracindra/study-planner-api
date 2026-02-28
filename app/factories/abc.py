import factory

from app.doc_upstream_services.abc.schemas import (
    Person,
    RestrictedStudentPersonalDetails,
    RoleInDepartment,
)


class PersonFactory(factory.Factory):
    class Meta:
        model = Person

    login = factory.Faker("user_name")
    lastname = factory.Faker("last_name")
    firstname = factory.Faker("first_name")


class RestrictedStudentPersonalDetailsFactory(factory.Factory):
    class Meta:
        model = RestrictedStudentPersonalDetails

    login = factory.Faker("user_name")
    email = factory.Faker("email")
    lastname = factory.Faker("last_name")
    firstname = factory.Faker("first_name")
    salutation = factory.Faker("prefix")
    year = factory.Faker("short_year")
    role_in_department = RoleInDepartment.student
    cohort = factory.Faker("pystr_format", string_format="c#")
    cid = factory.Faker("numerify", text="########")
    exam_class = factory.Faker("pystr_format", string_format="???#")
    degree_code = factory.Faker("pystr_format", string_format="????")
    degree_year = factory.LazyAttribute(lambda obj: f"{obj.degree_code.lower()}#")
    student_status = "active"
    entry_year = factory.Faker("year")
    fee_status = factory.Faker("random_element", elements=["home", "overseas"])
    personal_tutor = factory.SubFactory(PersonFactory)
