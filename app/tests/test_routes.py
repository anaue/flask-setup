from unittest import TestCase
from unittest.mock import patch
from fastapi.testclient import TestClient
import tempfile
import services
from main import app


class MainTest(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch.object(services, 'settings_list_mock')
    def test_root_redirect(self, mock_settings_list_mock):
        mock_settings_list_mock.return_value = {"data": [{"id": 123, "name": "setting 123"}]}
        response = self.client.get("/")
        self.assertTrue(response.status_code == 200)
        mock_settings_list_mock.assert_called_once()

    @patch.object(services, 'settings_list_mock')
    def test_api_mock_call(self, mock_settings_list_mock):
        mock_settings_list_mock.return_value = {"data": [{"id": 123, "name": "setting 123"}]}
        response = self.client.get("/api/mock")
        self.assertTrue(response.status_code == 200)
        mock_settings_list_mock.assert_called_once()

    @patch.object(services, 'load_settings_list')
    def test_load_settings_list_call(self, mock_load_settings_list):
        mock_load_settings_list.return_value = {"data": [{"id": 123, "name": "setting 123"}]}
        response = self.client.get("/api/config")
        self.assertTrue(response.status_code == 200)
        mock_load_settings_list.assert_called_once()

    @patch.object(services, 'get_setting')
    def test_get_setting_call(self, mock_get_setting):
        mock_get_setting.return_value = {"id": 123, "name": "setting 123"}
        response = self.client.get("/api/settings/123")
        self.assertTrue(response.status_code == 200)
        mock_get_setting.assert_called_once()
