import pytest
from unittest.mock import Mock, patch
import json

from app.utils.sync_helpers import get_module_list, create_missing_ratings


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
