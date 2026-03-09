from typing import Protocol

from app.doc_upstream_services.response_wrappers import UpstreamResponse


class Authenticator(Protocol):
    def authenticate(self, username: str, password: str) -> dict | None:
        """An authenticator can authenticate"""


class AbcUpstreamService(Protocol):
    """
    The ABC API service is the only API that gets mocked in dev.
    This interface ensures type compatibility between the real and the mock connectors.
    """

    def student_info(
        self,
        usernames: list[str] | None,
        year: str,
        cohorts: list[str] | None = None,
        proxied_user: str | None = None,
    ) -> UpstreamResponse:
        """ABC API can provide a student's personal information"""
