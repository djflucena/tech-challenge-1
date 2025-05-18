"""Classe de teste para a raspagem de processamento."""
import unittest
from unittest.mock import Mock, patch
from pathlib import Path
from bs4 import BeautifulSoup
from requests.exceptions import Timeout

from src.raspagem.processamento_raspagem import ProcessamentoRaspagem
from src.raspagem.raspagem_exceptions import ErroParser, ErroRequisicao,TimeoutRequisicao

class TestComportamentoProcessamentoRaspagem(unittest.TestCase):
    """Cenários de comportamento da raspagem de processamento."""

    def setUp(self):
        """Dado um HTML salvo localmente para teste de processamento"""
        html_file_path = (
            Path(__file__).parent
            / "sources"
            / "ano=2023&opcao=opt_03&subopcao=subopt_01.html"
        )
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()

    def test_quando_status_200_entao_html_e_titulo_sao_armazenados(self):
        """Cenário: Requisição 200 com sucesso"""
        mock_response = Mock(status_code=200, text=self.mock_html_content)

        with patch("requests.get", return_value=mock_response):
            raspagem = ProcessamentoRaspagem(2023, "subopt_01")
            raspagem.buscar_html()

        self.assertIsNotNone(raspagem.html)
        self.assertIn("Banco de dados de uva, vinho e derivados", raspagem.html.title.string)

    def test_quando_status_404_entao_excecao_com_mensagem_adequada(self):
        """Cenário: Requisição 404 retorna erro tratado"""
        mock_response = Mock(status_code=404, text=self.mock_html_content)

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(ErroRequisicao) as context:
                raspagem = ProcessamentoRaspagem(2023, "subopt_01")
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Failed to fetch HTML. Status code: 404")

    def test_quando_status_500_entao_excecao_com_mensagem_adequada(self):
        """Cenário: Requisição 500 retorna erro tratado"""
        mock_response = Mock(status_code=500, text=self.mock_html_content)

        with patch("requests.get", return_value=mock_response):
           with self.assertRaises(ErroRequisicao) as context:
                raspagem = ProcessamentoRaspagem(2023, "subopt_01")
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Failed to fetch HTML. Status code: 500")

    def test_quando_timeout_entao_excecao_com_mensagem_timeout(self):
        """Cenário: Timeout na requisição"""
        with patch("requests.get", side_effect=Timeout):
            with self.assertRaises(TimeoutRequisicao) as context:
                raspagem = ProcessamentoRaspagem(2023, "subopt_01")
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Request timed out")

    def test_quando_parser_executado_entao_dados_processados_e_categorizados(self):
        """Cenário: Parser retorna dados estruturados por cultivar"""
        raspagem = ProcessamentoRaspagem(2023, "subopt_01")
        raspagem.html = BeautifulSoup(self.mock_html_content, "html.parser")
        dados = raspagem.parser_html()

        # Chaves principais
        self.assertIn("Cultivar", dados)
        self.assertIn("Total", dados)
        self.assertEqual(dados["Total"], 99557416)

        culturas = dados["Cultivar"]
        self.assertGreater(len(culturas), 0)

        # TINTAS
        tinta_item = culturas[0]
        self.assertEqual(list(tinta_item.keys())[0], "TINTAS")
        self.assertEqual(tinta_item["TINTAS"], 35881118)
        self.assertIn("TIPOS", tinta_item)

        tipos_tintas = tinta_item["TIPOS"]
        self.assertGreater(len(tipos_tintas), 0)
        self.assertEqual(tipos_tintas[0]["Alicante Bouschet"], 4108858)
        self.assertEqual(tipos_tintas[1]["Ancelota"], 783688)

        # BRANCAS E ROSADAS
        brancas_item = culturas[1]
        self.assertEqual(list(brancas_item.keys())[0], "BRANCAS E ROSADAS")
        self.assertEqual(brancas_item["BRANCAS E ROSADAS"], 63676298)
        self.assertIn("TIPOS", brancas_item)

        tipos_brancas = brancas_item["TIPOS"]
        self.assertGreater(len(tipos_brancas), 0)
        self.assertEqual(tipos_brancas[0]["Aliatico"], 0)
        self.assertEqual(tipos_brancas[1]["Aligote"], 0)
        self.assertEqual(tipos_brancas[-1]["Outras(3)"], 0)
