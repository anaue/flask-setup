from unittest import TestCase
from unittest.mock import patch
from crawler import Crawler
from web import Web
from thirdparty.captcha import Captcha
import time
from xhtml2pdf import pisa

class CrawlerTest(TestCase):
    def setUp(self):
        self.crawler = Crawler(False)

    @patch.object(Web, 'load_captcha_form_page')
    @patch.object(Web, 'get_encoded_captcha_image', return_value="img_data")
    @patch.object(Web, 'get_encoded_base64_cookies', return_value="cookies")
    def test_get_encoded_captcha_data(self, mock_base64_cookies, mock_get_captcha_image, mock_load_page):
        c = Crawler()
        img_data, cookies = c.get_encoded_captcha_data()

        mock_base64_cookies.assert_called_once()
        mock_get_captcha_image.assert_called_once()
        mock_load_page.assert_called_once()

        self.assertTrue(img_data == "img_data")
        self.assertTrue(cookies == "cookies")

    @patch.object(Captcha, 'solve', return_value="solved")
    @patch.object(Web, 'load_captcha_form_page')
    @patch.object(Web, 'get_captcha_image', return_value=b"img_data")
    @patch.object(Web, 'get_encoded_base64_cookies', return_value="cookies")
    def test_get_solved_captcha_text(self, mock_base64_cookies, mock_get_captcha_image, mock_load_page, mock_captcha_solve):
        c = Crawler()
        captcha_text, cookies = c.get_solved_captcha_text()

        mock_base64_cookies.assert_called_once()
        mock_get_captcha_image.assert_called_once()
        mock_load_page.assert_called_once()
        mock_captcha_solve.assert_called_once()

        self.assertTrue(captcha_text == "solved")
        self.assertTrue(cookies == "cookies")

    @patch.object(Web, 'set_encoded_base64_cookies')
    @patch.object(Web, 'send_cpf_captcha_form')
    @patch.object(Web, 'load_certificate_page')
    @patch.object(Web, 'is_in_certificate_page', return_value=True)
    @patch.object(Web, 'get_certificate_content', return_value="content")
    @patch.object(Web, 'save_html_page')
    @patch.object(pisa, "CreatePDF")
    def test_get_certificate(self, mock_create_pdf, mock_save_html, mock_certificate_content, mock_is_certificate, mock_certificate_form, mock_captcha_form, mock_base64_cookies):
        mock_create_pdf.err.return_value = False

        with patch.object(time, 'sleep') as mock_sleep:
            c = Crawler()
            file_path = c.get_certificate("cpf", "captcha_text", "cookies")

        mock_save_html.assert_called_once()
        mock_certificate_content.assert_called_once()
        mock_is_certificate.assert_called_once()
        mock_certificate_form.assert_called_once()
        mock_captcha_form.assert_called_once()
        mock_base64_cookies.assert_called_once()

        mock_sleep.assert_called()

        self.assertTrue(file_path != "")
