import json
from dataclasses import dataclass

from fastapi import HTTPException
from starlette import status

from app.doc_upstream_services.abc.schemas import (
    AppSchemasCustomPeopleDetailsStudentDetails,
)
from app.protocols import AbcUpstreamService


@dataclass
class DummyResponse:
    content: str | None
    status_code: int = 200
    headers: list | None = None

    def json(self):
        return json.loads(self.content) if self.content is not None else None


class DummyAbcAPIService(AbcUpstreamService):
    def student_info(
        self,
        usernames: list[str] | None,
        year: str,
        cohorts: list[str] | None = None,
        proxied_user: str | None = None,
    ) -> list[AppSchemasCustomPeopleDetailsStudentDetails]:
        # Year 1 modules (all students)
        module_40009 = {
            "code": "40009",
            "title": "Programming Foundations",
            "ects": 10,
            "terms": [1, 2],
            "applicable_cohorts": ["c1", "j1"],
            "exam_contribution": 0,
            "coursework_contribution": 100,
            "exam_questions_total": None,
            "exam_questions_needed": None,
            "level": 1,
        }

        module_40016 = {
            "code": "40016",
            "title": "Calculus",
            "ects": 5,
            "terms": [1],
            "applicable_cohorts": ["c1", "j1"],
            "exam_contribution": 80,
            "coursework_contribution": 20,
            "exam_questions_total": 2,
            "exam_questions_needed": 2,
            "level": 1,
        }

        module_40018 = {
            "code": "40018",
            "title": "Discrete Mathematics",
            "ects": 5,
            "terms": [2],
            "applicable_cohorts": ["c1", "j1"],
            "exam_contribution": 60,
            "coursework_contribution": 40,
            "exam_questions_total": 2,
            "exam_questions_needed": 2,
            "level": 1,
        }

        # Year 2 modules (all students)
        module_50004 = {
            "code": "50004",
            "title": "Data Structures and Algorithms",
            "ects": 7.5,
            "terms": [1],
            "applicable_cohorts": ["c2", "j2"],
            "exam_contribution": 60,
            "coursework_contribution": 40,
            "exam_questions_total": None,
            "exam_questions_needed": None,
            "level": 2,
        }

        module_50005 = {
            "code": "50005",
            "title": "Object-Oriented Design",
            "ects": 7.5,
            "terms": [1, 2],
            "applicable_cohorts": ["c2", "j2"],
            "exam_contribution": 50,
            "coursework_contribution": 50,
            "exam_questions_total": None,
            "exam_questions_needed": None,
            "level": 2,
        }

        module_50003 = {
            "code": "50003",
            "title": "Database Systems",
            "ects": 6.0,
            "terms": [1],
            "applicable_cohorts": ["c2", "j2"],
            "exam_contribution": 70,
            "coursework_contribution": 30,
            "exam_questions_total": None,
            "exam_questions_needed": None,
            "level": 2,
        }

        module_50002 = {
            "code": "50002",
            "title": "Software Engineering Principles",
            "ects": 7.5,
            "terms": [2],
            "applicable_cohorts": ["c2", "j2"],
            "exam_contribution": 40,
            "coursework_contribution": 60,
            "exam_questions_total": None,
            "exam_questions_needed": None,
            "level": 2,
        }

        # Year 3 modules
        module_60001 = {
            "code": "60001",
            "title": "Advanced Algorithms",
            "ects": 7.5,
            "terms": [1],
            "applicable_cohorts": ["c3"],
            "exam_contribution": 70,
            "coursework_contribution": 30,
            "exam_questions_total": None,
            "exam_questions_needed": None,
            "level": 3,
        }

        module_60004 = {
            "code": "60004",
            "title": "Software Engineering Group Project",
            "ects": 7.5,
            "terms": [1, 2],
            "applicable_cohorts": ["c3"],
            "exam_contribution": 0,
            "coursework_contribution": 100,
            "exam_questions_total": None,
            "exam_questions_needed": None,
            "level": 3,
        }

        module_60002 = {
            "code": "60002",
            "title": "Security Engineering",
            "ects": 6.0,
            "terms": [1],
            "applicable_cohorts": ["c3"],
            "exam_contribution": 60,
            "coursework_contribution": 40,
            "exam_questions_total": None,
            "exam_questions_needed": None,
            "level": 3,
        }

        module_60003 = {
            "code": "60003",
            "title": "Advanced Databases",
            "ects": 6.0,
            "terms": [2],
            "applicable_cohorts": ["c3"],
            "exam_contribution": 60,
            "coursework_contribution": 40,
            "exam_questions_total": None,
            "exam_questions_needed": None,
            "level": 3,
        }

        # Personal tutor objects
        tutor_adumble = {
            "login": "adumble",
            "lastname": "Dumbledore",
            "firstname": "Albus",
        }
        tutor_mmcgonag = {
            "login": "mmcgonag",
            "lastname": "McGonagall",
            "firstname": "Minerva",
        }
        tutor_rlupin = {"login": "rlupin", "lastname": "Lupin", "firstname": "Remus"}
        tutor_psprout = {
            "login": "psprout",
            "lastname": "Sprout",
            "firstname": "Pomona",
        }
        tutor_ssnape = {"login": "ssnape", "lastname": "Snape", "firstname": "Severus"}
        tutor_fflitwick = {
            "login": "fflitwick",
            "lastname": "Flitwick",
            "firstname": "Filius",
        }

        FAKE_STUDENT_INFO = {
            # Third-year MEng Computing students (mc3)
            "hpotter": {
                "login": "hpotter",
                "email": "harry.potter23@imperial.ac.uk",
                "firstname": "Harry",
                "lastname": "Potter",
                "salutation": "Mr",
                "year": year,
                "role_in_department": "student",
                "cohort": "c3",
                "cid": "01234567",
                "studentstatus": "Normal",
                "degree_year": "mc3",
                "modules": [module_60001, module_60004, module_60002, module_60003],
                "modules_helped": [module_40009, module_40018],
                "personal_tutor": tutor_adumble,
            },
            "hgranger": {
                "login": "hgranger",
                "email": "hermione.granger23@imperial.ac.uk",
                "firstname": "Hermione",
                "lastname": "Granger",
                "salutation": "Ms",
                "year": year,
                "role_in_department": "student",
                "cohort": "c3",
                "cid": "01234568",
                "studentstatus": "Normal",
                "degree_year": "mc3",
                "modules": [module_60001, module_60004, module_60002, module_60003],
                "modules_helped": [module_40009, module_40018],
                "personal_tutor": tutor_mmcgonag,
            },
            "rweasley": {
                "login": "rweasley",
                "email": "ron.weasley23@imperial.ac.uk",
                "firstname": "Ron",
                "lastname": "Weasley",
                "salutation": "Mr",
                "year": year,
                "role_in_department": "student",
                "cohort": "c3",
                "cid": "01234569",
                "studentstatus": "Normal",
                "degree_year": "mc3",
                "modules": [module_60001, module_60004, module_60002, module_60003],
                "modules_helped": [],
                "personal_tutor": tutor_rlupin,
            },
            "nlongbott": {
                "login": "nlongbott",
                "email": "neville.longbottom23@imperial.ac.uk",
                "firstname": "Neville",
                "lastname": "Longbottom",
                "salutation": "Mr",
                "year": year,
                "role_in_department": "student",
                "cohort": "c3",
                "cid": "01234570",
                "studentstatus": "Normal",
                "degree_year": "mc3",
                "modules": [module_60001, module_60004, module_60002, module_60003],
                "modules_helped": [],
                "personal_tutor": tutor_psprout,
            },
            "llovegood": {
                "login": "llovegood",
                "email": "luna.lovegood23@imperial.ac.uk",
                "firstname": "Luna",
                "lastname": "Lovegood",
                "salutation": "Ms",
                "year": year,
                "role_in_department": "student",
                "cohort": "c3",
                "cid": "01234571",
                "studentstatus": "Normal",
                "degree_year": "mc3",
                "modules": [module_60001, module_60004, module_60002, module_60003],
                "modules_helped": [],
                "personal_tutor": tutor_psprout,
            },
            # Second-year MEng Computing students (mc2)
            "gweasley": {
                "login": "gweasley",
                "email": "ginny.weasley24@imperial.ac.uk",
                "firstname": "Ginny",
                "lastname": "Weasley",
                "salutation": "Ms",
                "year": year,
                "role_in_department": "student",
                "cohort": "c2",
                "cid": "01234572",
                "studentstatus": "Normal",
                "degree_year": "mc2",
                "modules": [module_50004, module_50005, module_50003, module_50002],
                "modules_helped": [],
                "personal_tutor": tutor_rlupin,
            },
            "dmalfoy": {
                "login": "dmalfoy",
                "email": "draco.malfoy24@imperial.ac.uk",
                "firstname": "Draco",
                "lastname": "Malfoy",
                "salutation": "Mr",
                "year": year,
                "role_in_department": "student",
                "cohort": "c2",
                "cid": "01234573",
                "studentstatus": "Normal",
                "degree_year": "mc2",
                "modules": [module_50004, module_50005, module_50003, module_50002],
                "modules_helped": [],
                "personal_tutor": tutor_ssnape,
            },
            # Second-year BEng Computing students (bc2)
            "sfinnigan": {
                "login": "sfinnigan",
                "email": "seamus.finnigan24@imperial.ac.uk",
                "firstname": "Seamus",
                "lastname": "Finnigan",
                "salutation": "Mr",
                "year": year,
                "role_in_department": "student",
                "cohort": "c2",
                "cid": "01234574",
                "studentstatus": "Normal",
                "degree_year": "bc2",
                "modules": [module_50004, module_50005, module_50002],
                "modules_helped": [],
                "personal_tutor": tutor_fflitwick,
            },
            "dthomas": {
                "login": "dthomas",
                "email": "dean.thomas24@imperial.ac.uk",
                "firstname": "Dean",
                "lastname": "Thomas",
                "salutation": "Mr",
                "year": year,
                "role_in_department": "student",
                "cohort": "c2",
                "cid": "01234575",
                "studentstatus": "Normal",
                "degree_year": "bc2",
                "modules": [module_50004, module_50005, module_50002],
                "modules_helped": [],
                "personal_tutor": tutor_fflitwick,
            },
            # Second-year MEng Computing with AI student (mcai2)
            "cchang": {
                "login": "cchang",
                "email": "cho.chang24@imperial.ac.uk",
                "firstname": "Cho",
                "lastname": "Chang",
                "salutation": "Ms",
                "year": year,
                "role_in_department": "student",
                "cohort": "c2",
                "cid": "01234576",
                "studentstatus": "Normal",
                "degree_year": "mcai2",
                "modules": [module_50004, module_50003, module_50002],
                "modules_helped": [],
                "personal_tutor": tutor_adumble,
            },
            # First-year BEng Computing students (bc1)
            "ccreevey": {
                "login": "ccreevey",
                "email": "colin.creevey25@imperial.ac.uk",
                "firstname": "Colin",
                "lastname": "Creevey",
                "salutation": "Mr",
                "year": year,
                "role_in_department": "student",
                "cohort": "c1",
                "cid": "01234581",
                "studentstatus": "Normal",
                "degree_year": "bc1",
                "modules": [module_40009, module_40016, module_40018],
                "modules_helped": [],
                "personal_tutor": tutor_fflitwick,
            },
            "dcreevey": {
                "login": "dcreevey",
                "email": "dennis.creevey25@imperial.ac.uk",
                "firstname": "Dennis",
                "lastname": "Creevey",
                "salutation": "Mr",
                "year": year,
                "role_in_department": "student",
                "cohort": "c1",
                "cid": "01234582",
                "studentstatus": "Normal",
                "degree_year": "bc1",
                "modules": [module_40009, module_40016, module_40018],
                "modules_helped": [],
                "personal_tutor": tutor_fflitwick,
            },
            # First-year MEng Computing students (mc1)
            "lbrown": {
                "login": "lbrown",
                "email": "lavender.brown25@imperial.ac.uk",
                "firstname": "Lavender",
                "lastname": "Brown",
                "salutation": "Ms",
                "year": year,
                "role_in_department": "student",
                "cohort": "c1",
                "cid": "01234583",
                "studentstatus": "Normal",
                "degree_year": "mc1",
                "modules": [module_40009, module_40016, module_40018],
                "modules_helped": [],
                "personal_tutor": tutor_psprout,
            },
            "ppatil": {
                "login": "ppatil",
                "email": "parvati.patil25@imperial.ac.uk",
                "firstname": "Parvati",
                "lastname": "Patil",
                "salutation": "Ms",
                "year": year,
                "role_in_department": "student",
                "cohort": "c1",
                "cid": "01234584",
                "studentstatus": "Normal",
                "degree_year": "mc1",
                "modules": [module_40009, module_40016, module_40018],
                "modules_helped": [],
                "personal_tutor": tutor_psprout,
            },
        }

        return AppSchemasCustomPeopleDetailsStudentDetails(
            response=DummyResponse(
                content=json.dumps(
                    list(FAKE_STUDENT_INFO.values())
                    if usernames is None
                    else [
                        FAKE_STUDENT_INFO[username]
                        for username in usernames
                        if username in FAKE_STUDENT_INFO
                    ]
                ).encode()
            )
        )
