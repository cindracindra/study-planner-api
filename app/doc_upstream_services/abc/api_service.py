from app.doc_upstream_services.abc.deserialisation import deserialize_or_502
from app.doc_upstream_services.abc.schemas import (
    RestrictedStudentPersonalDetails,
)
from app.doc_upstream_services.base_service import DocUpstreamService
from app.protocols import AbcUpstreamService


class AbcAPIService(DocUpstreamService, AbcUpstreamService):
    def get_student(
        self,
        year: str,
        login: str,
        proxied_user: str | None = None,
    ) -> RestrictedStudentPersonalDetails:
        res = self.make_request(
            f"/{year}/students/{login}",
            proxied_user=proxied_user,
        )
        return deserialize_or_502(res, RestrictedStudentPersonalDetails)
