import unittest
from unittest.mock import Mock, patch

from bs4 import BeautifulSoup

from src.scrapping.producao_raspagem import ProducaoRaspagem
from pathlib import Path

class TestProducaoRaspagem(unittest.TestCase):

    def setUp(self):
        html_file_path = Path(__file__).parent / "sources" / "ano=1970&opcao=opt_02.html"
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()
        return super().setUp()

    def test_buscar_html_sucesso(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            raspagem = ProducaoRaspagem()
            raspagem.buscar_html(1970)
            self.assertIsNotNone(raspagem.html)
            self.assertIn("Banco de dados de uva, vinho e derivados", raspagem.html.title.string)
    
    def test_buscar_html_request_404(self):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(Exception) as context:
                raspagem = ProducaoRaspagem()
                raspagem.buscar_html(1970)
                self.assertIsNone(raspagem.html)
                self.assertEqual(context.msg, "Failed to fetch HTML. Status code: 404")

    def test_converter_dados(self):
        raspagem = ProducaoRaspagem()
        raspagem.html = BeautifulSoup(self.mock_html_content, 'html.parser')
        dados = raspagem.converter_dados()

        self.assertIn("Produto", dados)
        self.assertIn("Total", dados)
        self.assertEqual(dados["Total"], 256370050)
        self.assertEqual(len(dados["Produto"]), 4)
        self.assertIn("VINHO DE MESA", dados["Produto"][0])
        self.assertIn("VINHO FINO DE MESA (VINIFERA)", dados["Produto"][1])
        self.assertIn("SUCO", dados["Produto"][2])
        self.assertIn("DERIVADOS)", dados["Produto"][3])
        self.assertEqual(dados["Produto"][0]["VINHO DE MESA"], 217208604)
        self.assertEqual(dados["Produto"][1]["VINHO FINO DE MESA (VINIFERA)"], 23899346)
        self.assertEqual(dados["Produto"][2]["SUCO"], 1097771)
        self.assertEqual(dados["Produto"][3]["DERIVADOS"], 14164329)
