"""Classe de teste para a raspagem de exportação."""


import unittest
from unittest.mock import Mock, patch
from pathlib import Path
from requests.exceptions import Timeout
from bs4 import BeautifulSoup

from src.raspagem.exportacao_raspagem import ExportacaoRaspagem
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser



class TestComportamentoExportacaoRaspagem(unittest.TestCase):
    """Cenários de comportamento da raspagem de exportação."""

    def setUp(self):
        """Dado um HTML de exportação salvo localmente"""
        html_file_path = (
            Path(__file__).parent
            / "sources"
            / "ano=2023&opcao=opt_06&subopcao=subopt_01.html"
        )
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()

    def test_quando_html_200_entao_html_e_titulo_sao_armazenados(self):
        """Cenário: Requisição 200 bem-sucedida armazena HTML"""
        mock_response = Mock(status_code=200, text=self.mock_html_content)

        with patch("requests.get", return_value=mock_response):
            raspagem = ExportacaoRaspagem(2023, "subopt_01")
            raspagem.buscar_html()

        self.assertIsNotNone(raspagem.html)
        self.assertIn("Banco de dados de uva, vinho e derivados", raspagem.html.title.string)

    def test_quando_status_404_entao_excecao_apropriada_e_html_vazio(self):
        """Cenário: Requisição com erro 404"""
        mock_response = Mock(status_code=404, text=self.mock_html_content)

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(ErroRequisicao) as context:
                raspagem = ExportacaoRaspagem(2023, "subopt_01")
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Failed to fetch HTML. Status code: 404")

    def test_quando_status_500_entao_excecao_apropriada_e_html_vazio(self):
        """Cenário: Requisição com erro 500"""
        mock_response = Mock(status_code=500, text=self.mock_html_content)

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(ErroRequisicao) as context:
                raspagem = ExportacaoRaspagem(2023, "subopt_01")
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Failed to fetch HTML. Status code: 500")

    def test_quando_timeout_entao_excecao_com_mensagem_timeout(self):
        """Cenário: Timeout na requisição"""
        with patch("requests.get", side_effect=Timeout):
            with self.assertRaises(TimeoutRequisicao) as context:
                raspagem = ExportacaoRaspagem(2023, "subopt_01")
                raspagem.buscar_html()
        print("Mensagem da exceção capturada:", repr(str(context.exception)))

        self.assertEqual(str(context.exception), "Request timed out")

    def test_quando_parser_executado_em_html_valido_entao_dados_extraidos_completamente(self):
        """Cenário: Parser bem-sucedido extrai países e totais"""
        raspagem = ExportacaoRaspagem(2023, "subopt_01")
        raspagem.html = BeautifulSoup(self.mock_html_content, "html.parser")
        dados = raspagem.parser_html()

        self.assertIn("paises", dados)
        self.assertIn("total", dados)
        self.assertEqual(dados["total"]["quantidade"], 5538888.0)
        self.assertEqual(dados["total"]["valor"], 8923076.0)

        self.assertEqual(len(dados["paises"]), 141)

        self.assertEqual(dados["paises"][0]["pais"], "Afeganistão")
        self.assertEqual(dados["paises"][0]["quantidade_kg"], 0.0)
        self.assertEqual(dados["paises"][0]["valor_us"], 0.0)

        self.assertEqual(dados["paises"][1]["pais"], "África do Sul")
        self.assertEqual(dados["paises"][1]["quantidade_kg"], 117.0)
        self.assertEqual(dados["paises"][1]["valor_us"], 698.0)

        self.assertEqual(dados["paises"][-1]["pais"], "Vietnã")
        self.assertEqual(dados["paises"][-1]["quantidade_kg"], 72.0)
        self.assertEqual(dados["paises"][-1]["valor_us"], 128.0)
