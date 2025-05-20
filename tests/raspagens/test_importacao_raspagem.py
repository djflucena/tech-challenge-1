"""Classe de teste para a raspagem de importação."""
import unittest
from unittest.mock import Mock, patch
from pathlib import Path
from requests.exceptions import Timeout
from bs4 import BeautifulSoup

from src.raspagem.importacao_raspagem import ImportacaoRaspagem


class TestComportamentoImportacaoRaspagem(unittest.TestCase):
    """Cenários de comportamento da raspagem de importação."""

    def setUp(self):
        """Dado um HTML salvo localmente para testes de importação"""
        html_file_path = (
            Path(__file__).parent
            / "sources"
            / "ano=1970&opcao=opt_05&subopcao=subopt_01.html"
        )
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()

    def test_quando_html_200_entao_html_e_titulo_sao_armazenados(self):
        """Cenário: Requisição 200 com sucesso armazena o HTML"""
        mock_response = Mock(status_code=200, text=self.mock_html_content)

        with patch("requests.get", return_value=mock_response):
            raspagem = ImportacaoRaspagem(1970, "subopt_01")
            raspagem.buscar_html()

        self.assertIsNotNone(raspagem.html)
        self.assertIn("Banco de dados de uva, vinho e derivados", raspagem.html.title.string)

    def test_quando_status_404_entao_excecao_com_mensagem_apropriada(self):
        """Cenário: Requisição com erro 404"""
        mock_response = Mock(status_code=404, text=self.mock_html_content)

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(Exception) as context:
                raspagem = ImportacaoRaspagem(1970, "subopt_01")
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Failed to fetch HTML. Status code: 404")

    def test_quando_status_500_entao_excecao_com_mensagem_apropriada(self):
        """Cenário: Requisição com erro 500"""
        mock_response = Mock(status_code=500, text=self.mock_html_content)

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(Exception) as context:
                raspagem = ImportacaoRaspagem(1970, "subopt_01")
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Failed to fetch HTML. Status code: 500")

    def test_quando_timeout_entao_excecao_com_mensagem_timeout(self):
        """Cenário: Timeout na requisição"""
        with patch("requests.get", side_effect=Timeout):
            with self.assertRaises(Exception) as context:
                raspagem = ImportacaoRaspagem(1970, "subopt_01")
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Request timed out")

    def test_quando_parser_executado_entao_dados_de_paises_sao_extraidos(self):
        """Cenário: Parser com HTML válido retorna totais e lista de países"""
        raspagem = ImportacaoRaspagem(1970, "subopt_01")
        raspagem.html = BeautifulSoup(self.mock_html_content, "html.parser")
        dados = raspagem.parser_html()

        self.assertIn("paises", dados)
        self.assertIn("total", dados)

        self.assertEqual(dados["total"]["quantidade"], 1444578.0)
        self.assertEqual(dados["total"]["valor"], 883886.0)
        self.assertEqual(len(dados["paises"]), 69)

        self.assertEqual(dados["paises"][0]["pais"], "Africa do Sul")
        self.assertEqual(dados["paises"][0]["quantidade_kg"], 0.0)
        self.assertEqual(dados["paises"][0]["valor_us"], 0.0)

        self.assertEqual(dados["paises"][1]["pais"], "Alemanha")
        self.assertEqual(dados["paises"][1]["quantidade_kg"], 52297.0)
        self.assertEqual(dados["paises"][1]["valor_us"], 30498.0)

        self.assertEqual(dados["paises"][68]["pais"], "Outros")
        self.assertEqual(dados["paises"][68]["quantidade_kg"], 5508.0)
        self.assertEqual(dados["paises"][68]["valor_us"], 4255.0)

