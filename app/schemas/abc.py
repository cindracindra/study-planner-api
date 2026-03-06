from sqlmodel import SQLModel

class Module(SQLModel):
    code: str
    title: str
    terms: list[int]


class StudentInfo(SQLModel):
    login: str
    modules: list[Module]
