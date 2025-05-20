"""Classe de Teste para a classe ComercializacoRaspagem."""
import unittest
from unittest.mock import Mock, patch
from pathlib import Path
from requests.exceptions import Timeout
from bs4 import BeautifulSoup
from src.raspagem.comercializacao_raspagem import ComercializacoRaspagem

class TestComercializacoRaspagem(unittest.TestCase):
    """Classe de Teste para a classe ComercializacoRaspagem."""

    def setUp(self):
        html_file_path = (
            Path(__file__).parent / "sources" / "ano=2023&opcao=opt_04.html"
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
            raspagem = ComercializacoRaspagem(2003)
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
                raspagem = ComercializacoRaspagem(2003)
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
                raspagem = ComercializacoRaspagem(2003)
                raspagem.buscar_html()
                self.assertIsNone(raspagem.html)
                self.assertEqual(context.msg, "Failed to fetch HTML. Status code: 500")

    def test_buscar_html_request_timeout(self):
        """Testa o tratamento de erro de timeout na requisição."""
        with patch("requests.get", side_effect=Timeout):
            with self.assertRaises(Exception) as context:
                raspagem = ComercializacoRaspagem(2023)
                raspagem.buscar_html()
                self.assertIsNone(raspagem.html)
                self.assertEqual(context.msg, "Request timed out")

    def test_parser_html_sucesso(self):
        """Testa o parser de HTML com sucesso."""
        raspagem = ComercializacoRaspagem(2023)
        raspagem.html = BeautifulSoup(self.mock_html_content, "html.parser")
        dados = raspagem.parser_html()

        # Verificações gerais
        self.assertIn("Produto", dados)
        self.assertIn("Total", dados)
        self.assertEqual(dados["Total"], 472291085)
        self.assertEqual(len(dados["Produto"]), 9)

        categorias = [
            "VINHO DE MESA", "VINHO FINO DE MESA", "VINHO FRIZANTE", "VINHO ORGANICO",
            "VINHO ESPECIAL", "ESPUMANTES", "SUCO DE UVAS",
            "SUCO DE UVAS CONCENTRADO", "OUTROS PRODUTOS COMERCIALIZADOS"
        ]
        for i, nome in enumerate(categorias):
            self.assertIn(nome, dados["Produto"][i])

        self.assertEqual(dados["Produto"][0]["VINHO DE MESA"], 187016848)
        self.assertEqual(dados["Produto"][1]["VINHO FINO DE MESA"], 18589310)
        self.assertEqual(dados["Produto"][4]["VINHO ESPECIAL"], 0)
        self.assertEqual(dados["Produto"][6]["SUCO DE UVAS"], 166708720)
        self.assertEqual(len(dados["Produto"][0]["TIPOS"]), 3)
        self.assertEqual(list(dados["Produto"][0]["TIPOS"][0].values())[0], 165097539)  # VINHO DE MESA - Tinto
        self.assertEqual(list(dados["Produto"][8]["TIPOS"][2].values())[0], 111)  # Aguardente de vinho 50°gl