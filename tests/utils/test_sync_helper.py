from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch
from sqlmodel import select

from app.utils.sync_helpers import get_module_list, create_missing_ratings, needs_sync, update_sync_status
from app.models.user_sync_status import UserSyncStatus
from app.models.confidence_ratings import ConfidenceRating, ModuleRating


class TestGetModuleList:

    def test_returns_module_codes_for_valid_student(self):
        mock_response = Mock()
        mock_response.json_content = [
            {
                "login": "hpotter",
                "modules": [
                    {"code": "60001"},
                    {"code": "60002"},
                ],
            }
        ]
        with patch("app.utils.sync_helpers.get_abc_service_handler") as mock_handler:
            mock_handler.return_value.student_info.return_value = mock_response
            result = get_module_list(year="2425", username="hpotter")
        assert result == ["60001", "60002"]

    def test_returns_empty_list_for_unknown_student(self):
        mock_response = Mock()
        mock_response.json_content = []
        with patch("app.utils.sync_helpers.get_abc_service_handler") as mock_handler:
            mock_handler.return_value.student_info.return_value = mock_response
            result = get_module_list(year="2425", username="unknown")
            assert result == []

    def test_returns_empty_list_when_student_has_no_modules(self):
        mock_response = Mock()
        mock_response.json_content = [{"login": "hpotter", "modules": []}]
        with patch("app.utils.sync_helpers.get_abc_service_handler") as mock_handler:
            mock_handler.return_value.student_info.return_value = mock_response
            result = get_module_list(year="2425", username="hpotter")
            assert result == []

    def test_handles_missing_modules_key(self):
        """Should return empty list if modules key is missing."""
        mock_response = Mock()
        mock_response.json_content = [{"login": "hpotter"}]
        with patch("app.utils.sync_helpers.get_abc_service_handler") as mock_handler:
            mock_handler.return_value.student_info.return_value = mock_response
            result = get_module_list(year="2425", username="hpotter")
            assert result == []

    def test_needs_sync_returns_false_when_recently_synced(self):
        sync_status = Mock()
        sync_status.last_synced = datetime.now(timezone.utc) - timedelta(hours=1)
        assert needs_sync(sync_status) is False

    def test_create_missing_ratings_creates_confidence_rating_if_missing(self, session):
        with patch("app.utils.sync_helpers.get_module_list", return_value=["60001"]):
            create_missing_ratings(session, "2526", "hpotter", total_weeks=1)
        rating = session.exec(select(ConfidenceRating)).first()
        assert rating is not None

    def test_create_missing_ratings_returns_early_if_no_modules(self, session):
        with patch("app.utils.sync_helpers.get_module_list", return_value=[]):
            create_missing_ratings(session, "2526", "hpotter", total_weeks=11)
        ratings = session.exec(select(ModuleRating)).all()
        assert len(ratings) == 0
