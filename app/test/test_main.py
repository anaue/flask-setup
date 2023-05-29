from unittest import TestCase
from unittest.mock import patch
from fastapi.testclient import TestClient
import tempfile
from crawler import Crawler
from main import app


class MainTest(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch.object(Crawler, 'get_encoded_captcha_data')
    def test_root_redirect(self, mock_get_encoded_captcha_data):
        mock_get_encoded_captcha_data.return_value = ("", None)
        response = self.client.get("/")
        self.assertTrue(response.status_code == 200)
        mock_get_encoded_captcha_data.amock_ssert_called_once()

    @patch.object(Crawler, 'get_encoded_captcha_data')
    def test_htmlform(self, mock_get_encoded_captcha_data):
        mock_get_encoded_captcha_data.return_value = ("", None)
        response = self.client.get("/form")
        self.assertTrue(response.status_code == 200)
        mock_get_encoded_captcha_data.amock_ssert_called_once()

    @patch.object(Crawler, 'get_encoded_captcha_data')
    def test_error_htmlform_with_image_not_loaded(self, mock_get_encoded_captcha_data):
        mock_get_encoded_captcha_data.return_value = (None, None)
        response = self.client.get("/form")
        self.assertTrue(response.status_code == 500)
        mock_get_encoded_captcha_data.amock_ssert_called_once()

    @patch.object(Crawler, 'get_certificate')
    def test_error_certificate_internal_error(self, mock_get_certificate):
        mock_get_certificate.return_value = ""
        response = self.client.get("/certificate?cpf=ni&captcha=txt")
        self.assertTrue(response.status_code == 500)
        mock_get_certificate.assert_called_once()

    @patch.object(Crawler, 'get_certificate')
    def test_error_certificate_unprocessable_error(self, mock_get_certificate):
        mock_get_certificate.return_value = ""
        response = self.client.get("/certificate")
        self.assertTrue(response.status_code == 422)
        mock_get_certificate.assert_not_called()

    @patch.object(Crawler, 'get_certificate')
    def test_certificate_load(self, mock_get_certificate):
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as result_file:
            result_file.write(b"123")
            mock_get_certificate.return_value = result_file.name

        response = self.client.get("/certificate?cpf=ni&captcha=txt")
        self.assertTrue(response.status_code == 200)
        mock_get_certificate.assert_called_once()

    def test_htmlform_only_cpf(self):
        response = self.client.get("/form/cpf")
        self.assertTrue(response.status_code == 200)

    @patch.object(Crawler, 'get_certificate')
    @patch.object(Crawler, 'get_solved_captcha_text')
    def test_certificate_load_only_cpf(self, mock_get_solved_captcha_text, mock_get_certificate):
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as result_file:
            result_file.write(b"123")
            mock_get_certificate.return_value = result_file.name
        mock_get_solved_captcha_text.return_value = ("123", "cookies")

        response = self.client.get("/certificate/cpf?cpf=cpf123")
        self.assertTrue(response.status_code == 200, "http response failed with status_code " + str(response.status_code))
        mock_get_certificate.assert_called_once_with("cpf123", "123", "cookies")
        mock_get_solved_captcha_text.assert_called_once()

