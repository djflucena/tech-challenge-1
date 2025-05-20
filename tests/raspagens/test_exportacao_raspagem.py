"""Classe de teste para a raspagem de exportação."""
import unittest
from unittest.mock import Mock, patch
from pathlib import Path
from requests.exceptions import Timeout
from bs4 import BeautifulSoup

from src.raspagem.exportacao_raspagem import ExportacaoRaspagem
from pathlib import Path

class TestExportacaoRaspagem(unittest.TestCase):
    """Classe de teste para a raspagem de exportação."""

    def setUp(self):
        html_file_path = (
            Path(__file__).parent
            / "sources"
            / "ano=2023&opcao=opt_06&subopcao=subopt_01.html"
        )
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()
        return super().setUp()

    def test_buscar_html_sucesso(self):
        """Testa a busca de HTML com sucesso."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            raspagem = ExportacaoRaspagem(2023, "subopt_01")
            raspagem.buscar_html()
            self.assertIsNotNone(raspagem.html)
            self.assertIn(
                "Banco de dados de uva, vinho e derivados",
                raspagem.html.title.string)  # type: ignore

    def test_buscar_html_request_404(self):
        """Testa o tratamento de erro 404 na requisição."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(Exception) as context:
                raspagem = ExportacaoRaspagem(2023, "subopt_01")
                raspagem.buscar_html()
                self.assertIsNone(raspagem.html)
                self.assertEqual(context.msg, "Failed to fetch HTML. Status code: 404")

    def test_buscar_html_request_500(self):
        """Testa o tratamento de erro 500 na requisição."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(Exception) as context:
                raspagem = ExportacaoRaspagem(2023, "subopt_01")
                raspagem.buscar_html()
                self.assertIsNone(raspagem.html)
                self.assertEqual(context.msg, "Failed to fetch HTML. Status code: 500")

    def test_buscar_html_request_timeout(self):
        """Testa o tratamento de timeout na requisição."""
        with patch("requests.get", side_effect=Timeout):
            with self.assertRaises(Exception) as context:
                raspagem = ExportacaoRaspagem(2023, "subopt_01")
                raspagem.buscar_html()
                self.assertIsNone(raspagem.html)
                self.assertEqual(context.msg, "Request timed out")

    def test_parser_html_sucesso(self):
        """Testa o parser de HTML com sucesso."""
        raspagem = ExportacaoRaspagem(2023, "subopt_01")
        raspagem.html = BeautifulSoup(self.mock_html_content, "html.parser")
        dados = raspagem.parser_html()

        self.assertIn("paises", dados)
        self.assertIn("total", dados)

        self.assertEqual(dados["total"]["quantidade"], 5538888.0)
        self.assertEqual(dados["total"]["valor"], 8923076.0)

        self.assertEqual(len(dados["paises"]), 141)

        self.assertEqual(dados["paises"][0]["pais"], "Afeganistao")
        self.assertEqual(dados["paises"][0]["quantidade_kg"], 0.0)
        self.assertEqual(dados["paises"][0]["valor_us"], 0.0)

        self.assertEqual(dados["paises"][1]["pais"], "Africa do Sul")
        self.assertEqual(dados["paises"][1]["quantidade_kg"], 117.0)
        self.assertEqual(dados["paises"][1]["valor_us"], 698.0)

        self.assertEqual(dados["paises"][-1]["pais"], "Vietna")
        self.assertEqual(dados["paises"][-1]["quantidade_kg"], 72.0)
        self.assertEqual(dados["paises"][-1]["valor_us"], 128.0)