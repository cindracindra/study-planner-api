from app.doc_upstream_services.abc.deserialisation import deserialize_or_502
from app.doc_upstream_services.abc.schemas import (
    AppSchemasCustomPeopleDetailsStudentDetails,
)
from app.doc_upstream_services.base_service import DocUpstreamService
from app.protocols import AbcUpstreamService


class AbcAPIService(DocUpstreamService, AbcUpstreamService):
    def student_info(
        self,
        usernames: list[str] | None,
        year: str,
        cohorts: list[str] | None = None,
        proxied_user: str | None = None,
    ) -> list[AppSchemasCustomPeopleDetailsStudentDetails]:
        params = {"login": usernames}
        if cohorts:
            params.update(cohort=cohorts)
        return self.make_request(
            f"/{year}/students",
            params=params,
            proxied_user=proxied_user,
        )
