import unittest
from unittest.mock import Mock, patch

from src.raspagem_service import ProducaoRaspagem
from pathlib import Path

class TestProducaoRaspagem(unittest.TestCase):

    def setUp(self):
        html_file_path = Path(__file__).parent / "sources" / "ano=1970&opcao=opt_02.html"
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()
        return super().setUp()

    def test_buscar_html(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            raspagem = ProducaoRaspagem()
            raspagem.buscar_html(2022)
            self.assertIsNotNone(raspagem.html)
            self.assertIn("Banco de dados de uva, vinho e derivados", raspagem.html.title.string)
