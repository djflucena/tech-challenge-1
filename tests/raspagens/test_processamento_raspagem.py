"""Classe de teste para a raspagem de processamento."""
import unittest
from unittest.mock import Mock, patch
from pathlib import Path
from bs4 import BeautifulSoup
from requests.exceptions import Timeout

from src.raspagem.processamento_raspagem import ProcessamentoRaspagem


class TestProcessamentoRaspagem(unittest.TestCase):
    """Classe de teste para a raspagem de processamento."""

    def setUp(self):
        html_file_path = (
            Path(__file__).parent
            / "sources"
            / "ano=2023&opcao=opt_03&subopcao=subopt_01.html"
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
            raspagem = ProcessamentoRaspagem(2023, "subopt_01")
            raspagem.buscar_html()
            self.assertIsNotNone(raspagem.html)
            self.assertIn(
                "Banco de dados de uva, vinho e derivados",
                raspagem.html.title.string
            )

    def test_buscar_html_request_404(self):
        """Testa o tratamento de erro 404 na requisição."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(Exception) as context:
                raspagem = ProcessamentoRaspagem(2023, "subopt_01")
                raspagem.buscar_html()
                self.assertIsNone(raspagem.html)
            self.assertEqual(str(context.exception), "Failed to fetch HTML. Status code: 404")

    def test_buscar_html_request_500(self):
        """Testa o tratamento de erro 500 na requisição."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(Exception) as context:
                raspagem = ProcessamentoRaspagem(2023, "subopt_01")
                raspagem.buscar_html()
                self.assertIsNone(raspagem.html)
            self.assertEqual(str(context.exception), "Failed to fetch HTML. Status code: 500")

    def test_buscar_html_request_timeout(self):
        """Testa o tratamento de timeout na requisição."""
        with patch("requests.get", side_effect=Timeout):
            with self.assertRaises(Exception) as context:
                raspagem = ProcessamentoRaspagem(2023, "subopt_01")
                raspagem.buscar_html()
                self.assertIsNone(raspagem.html)
                self.assertEqual(context.msg, "Request timed out")


    def test_parser_html_sucesso(self):
        """Testa o parser de HTML com sucesso."""
        raspagem = ProcessamentoRaspagem(2023, "subopt_01")
        raspagem.html = BeautifulSoup(self.mock_html_content, "html.parser")
        dados = raspagem.parser_html()

        # Verifica se as chaves principais estão presentes
        self.assertIn("Cultivar", dados)
        self.assertIn("Total", dados)

        # Verifica o total geral
        self.assertEqual(dados["Total"], 99557416)

        # Verifica se os itens principais estão lá
        culturas = dados["Cultivar"]
        self.assertGreater(len(culturas), 0)

        # Primeiro item: TINTAS
        tinta_item = culturas[0]
        self.assertEqual(list(tinta_item.keys())[0], "TINTAS")
        self.assertEqual(tinta_item["TINTAS"], 35881118)
        self.assertIn("TIPOS", tinta_item)

        # Verifica alguns subtipos de TINTAS
        tipos_tintas = tinta_item["TIPOS"]
        self.assertGreater(len(tipos_tintas), 0)
        self.assertEqual(tipos_tintas[0]["Alicante Bouschet"], 4108858)
        self.assertEqual(tipos_tintas[1]["Ancelota"], 783688)

        # Segundo item: BRANCAS E ROSADAS
        brancas_item = culturas[1]
        self.assertEqual(list(brancas_item.keys())[0], "BRANCAS E ROSADAS")
        self.assertEqual(brancas_item["BRANCAS E ROSADAS"], 63676298)
        self.assertIn("TIPOS", brancas_item)

        # Verifica alguns subtipos de BRANCAS
        tipos_brancas = brancas_item["TIPOS"]
        self.assertGreater(len(tipos_brancas), 0)
        self.assertEqual(tipos_brancas[0]["Aliatico"], 0)
        self.assertEqual(tipos_brancas[1]["Aligote"], 0)
        self.assertEqual(tipos_brancas[-1]["Outras(3)"], 0)