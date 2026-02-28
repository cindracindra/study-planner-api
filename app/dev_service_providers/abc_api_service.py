import json
from dataclasses import dataclass

from fastapi import HTTPException
from starlette import status

from app.doc_upstream_services.abc.schemas import (
    RestrictedStudentPersonalDetails,
    RoleInDepartment,
    Person,
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
    def get_student(
        self, year: str, login: str, proxied_user: str | None = None
    ) -> RestrictedStudentPersonalDetails:
        """Return fake student data for testing."""
        fake_students = {
            "hpotter": RestrictedStudentPersonalDetails(
                login="hpotter",
                email="harry.potter23@imperial.ac.uk",
                lastname="Potter",
                firstname="Harry",
                salutation="Mr",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c3",
                cid="01234567",
                exam_class="mc3",
                degree_code="mc",
                degree_year="mc3",
                student_status="Normal",
                entry_year=2023,
                fee_status="Home",
                personal_tutor=Person(
                    login="adumble", lastname="Dumbledore", firstname="Albus"
                ),
            ),
            "hgranger": RestrictedStudentPersonalDetails(
                login="hgranger",
                email="hermione.granger23@imperial.ac.uk",
                lastname="Granger",
                firstname="Hermione",
                salutation="Ms",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c3",
                cid="01234568",
                exam_class="mc3",
                degree_code="mc",
                degree_year="mc3",
                student_status="Normal",
                entry_year=2023,
                fee_status="Home",
                personal_tutor=Person(
                    login="mmcgonag", lastname="McGonagall", firstname="Minerva"
                ),
            ),
            "rweasley": RestrictedStudentPersonalDetails(
                login="rweasley",
                email="ron.weasley23@imperial.ac.uk",
                lastname="Weasley",
                firstname="Ron",
                salutation="Mr",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c3",
                cid="01234569",
                exam_class="mc3",
                degree_code="mc",
                degree_year="mc3",
                student_status="Normal",
                entry_year=2023,
                fee_status="Home",
                personal_tutor=Person(
                    login="rlupin", lastname="Lupin", firstname="Remus"
                ),
            ),
            "nlongbott": RestrictedStudentPersonalDetails(
                login="nlongbott",
                email="neville.longbottom23@imperial.ac.uk",
                lastname="Longbottom",
                firstname="Neville",
                salutation="Mr",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c3",
                cid="01234570",
                exam_class="mc3",
                degree_code="mc",
                degree_year="mc3",
                student_status="Normal",
                entry_year=2023,
                fee_status="Home",
                personal_tutor=Person(
                    login="psprout", lastname="Sprout", firstname="Pomona"
                ),
            ),
            "llovegood": RestrictedStudentPersonalDetails(
                login="llovegood",
                email="luna.lovegood23@imperial.ac.uk",
                lastname="Lovegood",
                firstname="Luna",
                salutation="Ms",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c3",
                cid="01234571",
                exam_class="mc3",
                degree_code="mc",
                degree_year="mc3",
                student_status="Normal",
                entry_year=2023,
                fee_status="Home",
                personal_tutor=Person(
                    login="psprout", lastname="Sprout", firstname="Pomona"
                ),
            ),
            "gweasley": RestrictedStudentPersonalDetails(
                login="gweasley",
                email="ginny.weasley24@imperial.ac.uk",
                lastname="Weasley",
                firstname="Ginny",
                salutation="Ms",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c2",
                cid="01234572",
                exam_class="mc2",
                degree_code="mc",
                degree_year="mc2",
                student_status="Normal",
                entry_year=2024,
                fee_status="Home",
                personal_tutor=Person(
                    login="rlupin", lastname="Lupin", firstname="Remus"
                ),
            ),
            "dmalfoy": RestrictedStudentPersonalDetails(
                login="dmalfoy",
                email="draco.malfoy24@imperial.ac.uk",
                lastname="Malfoy",
                firstname="Draco",
                salutation="Mr",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c2",
                cid="01234573",
                exam_class="mc2",
                degree_code="mc",
                degree_year="mc2",
                student_status="Normal",
                entry_year=2024,
                fee_status="Home",
                personal_tutor=Person(
                    login="ssnape", lastname="Snape", firstname="Severus"
                ),
            ),
            "sfinnigan": RestrictedStudentPersonalDetails(
                login="sfinnigan",
                email="seamus.finnigan24@imperial.ac.uk",
                lastname="Finnigan",
                firstname="Seamus",
                salutation="Mr",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c2",
                cid="01234574",
                exam_class="bc2",
                degree_code="bc2",
                degree_year="bc2",
                student_status="Normal",
                entry_year=2024,
                fee_status="Home",
                personal_tutor=Person(
                    login="fflitwick", lastname="Flitwick", firstname="Filius"
                ),
            ),
            "dthomas": RestrictedStudentPersonalDetails(
                login="dthomas",
                email="dean.thomas24@imperial.ac.uk",
                lastname="Thomas",
                firstname="Dean",
                salutation="Mr",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c2",
                cid="01234575",
                exam_class="bc2",
                degree_code="bc",
                degree_year="bc2",
                student_status="Normal",
                entry_year=2024,
                fee_status="Home",
                personal_tutor=Person(
                    login="fflitwick", lastname="Flitwick", firstname="Filius"
                ),
            ),
            "cchang": RestrictedStudentPersonalDetails(
                login="cchang",
                email="cho.chang24@imperial.ac.uk",
                lastname="Chang",
                firstname="Cho",
                salutation="Ms",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c2",
                cid="01234576",
                exam_class="mcai2",
                degree_code="mcai",
                degree_year="mcai2",
                student_status="Normal",
                entry_year=2024,
                fee_status="Home",
                personal_tutor=Person(
                    login="adumble", lastname="Dumbledore", firstname="Albus"
                ),
            ),
            "ccreevey": RestrictedStudentPersonalDetails(
                login="ccreevey",
                email="colin.creevey25@imperial.ac.uk",
                lastname="Creevey",
                firstname="Colin",
                salutation="Mr",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c1",
                cid="01234581",
                exam_class="bc1",
                degree_code="bc",
                degree_year="bc1",
                student_status="Normal",
                entry_year=2025,
                fee_status="Home",
                personal_tutor=Person(
                    login="fflitwick", lastname="Flitwick", firstname="Filius"
                ),
            ),
            "dcreevey": RestrictedStudentPersonalDetails(
                login="dcreevey",
                email="dennis.creevey25@imperial.ac.uk",
                lastname="Creevey",
                firstname="Dennis",
                salutation="Mr",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c1",
                cid="01234582",
                exam_class="bc1",
                degree_code="bc",
                degree_year="bc1",
                student_status="Normal",
                entry_year=2025,
                fee_status="Home",
                personal_tutor=Person(
                    login="fflitwick", lastname="Flitwick", firstname="Filius"
                ),
            ),
            "lbrown": RestrictedStudentPersonalDetails(
                login="lbrown",
                email="lavender.brown25@imperial.ac.uk",
                lastname="Brown",
                firstname="Lavender",
                salutation="Ms",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c1",
                cid="01234583",
                exam_class="mc1",
                degree_code="mc",
                degree_year="mc1",
                student_status="Normal",
                entry_year=2025,
                fee_status="Home",
                personal_tutor=Person(
                    login="psprout", lastname="Sprout", firstname="Pomona"
                ),
            ),
            "ppatil": RestrictedStudentPersonalDetails(
                login="ppatil",
                email="parvati.patil25@imperial.ac.uk",
                lastname="Patil",
                firstname="Parvati",
                salutation="Ms",
                year=year,
                role_in_department=RoleInDepartment.student,
                cohort="c1",
                cid="01234584",
                exam_class="mc1",
                degree_code="mc",
                degree_year="mc1",
                student_status="Normal",
                entry_year=2025,
                fee_status="Home",
                personal_tutor=Person(
                    login="psprout", lastname="Sprout", firstname="Pomona"
                ),
            ),
        }

        if login not in fake_students:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found",
            )

        return fake_students[login]
