import unittest
from requests.exceptions import Timeout
from unittest.mock import Mock, patch

from bs4 import BeautifulSoup

from src.raspagem.importacao_raspagem import ImportacaoRaspagem
from pathlib import Path

class TestImportacaoRaspagem(unittest.TestCase):

    def setUp(self):
        html_file_path = Path(__file__).parent / "sources" / "ano=1970&opcao=opt_05&subopcao=subopt_01.html"
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()
        return super().setUp()

    def test_buscar_html_sucesso(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            raspagem = ImportacaoRaspagem(1970, 'subopt_01')
            raspagem.buscar_html()
            self.assertIsNotNone(raspagem.html)
            self.assertIn("Banco de dados de uva, vinho e derivados", raspagem.html.title.string)
    
    def test_buscar_html_request_404(self):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(Exception) as context:
                raspagem = ImportacaoRaspagem(1970, 'subopt_01')
                raspagem.buscar_html()
                self.assertIsNone(raspagem.html)
                self.assertEqual(context.msg, "Failed to fetch HTML. Status code: 404")
    
    def test_buscar_html_request_500(self):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(Exception) as context:
                raspagem = ImportacaoRaspagem(1970, 'subopt_01')
                raspagem.buscar_html()
                self.assertIsNone(raspagem.html)
                self.assertEqual(context.msg, "Failed to fetch HTML. Status code: 500")
    
    def test_buscar_html_request_timeout(self):
        with patch("requests.get", side_effect=Timeout):
            with self.assertRaises(Exception) as context:
                raspagem = ImportacaoRaspagem(1970, 'subopt_01')
                raspagem.buscar_html()
                self.assertIsNone(raspagem.html)
                self.assertEqual(context.msg, "Request timed out")

    def test_parser_html_sucesso(self):
        raspagem = ImportacaoRaspagem(1970, 'subopt_01')
        raspagem.html = BeautifulSoup(self.mock_html_content, 'html.parser')
        dados = raspagem.parser_html()

        self.assertIn("paises", dados)
        self.assertIn("total", dados)
        self.assertEqual(dados["total"]["quantidade"], 1444578.0)
        self.assertEqual(dados["total"]["valor"], 883886.0)
        self.assertEqual(len(dados["paises"]), 69.0)
        self.assertEqual(dados["paises"][0]["pais"], "Africa do Sul")
        self.assertEqual(dados["paises"][0]["quantidade_kg"], 0.0)
        self.assertEqual(dados["paises"][0]["valor_us"], 0.0)
        self.assertEqual(dados["paises"][1]["pais"], "Alemanha")
        self.assertEqual(dados["paises"][1]["quantidade_kg"], 52297.0)
        self.assertEqual(dados["paises"][1]["valor_us"],30498.0)
        self.assertEqual(dados["paises"][68]["pais"], "Outros")
        self.assertEqual(dados["paises"][68]["quantidade_kg"], 5508.0)
        self.assertEqual(dados["paises"][68]["valor_us"],4255.0)