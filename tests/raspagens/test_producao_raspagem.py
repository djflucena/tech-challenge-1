"""Classe de Teste para a classe ProducaoRaspagem."""

from multiprocessing import context
import unittest
from unittest.mock import Mock, patch
from pathlib import Path
from requests.exceptions import Timeout
from bs4 import BeautifulSoup
from src.raspagem.producao_raspagem import ProducaoRaspagem
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser



class TestComportamentoProducaoRaspagem(unittest.TestCase):
    """Cenários de comportamento da raspagem de produção."""

    def setUp(self):
        """Dado um HTML salvo localmente para teste de produção"""
        html_file_path = (
            Path(__file__).parent / "sources" / "ano=1970&opcao=opt_02.html"
        )
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()

    def test_quando_status_200_entao_html_e_titulo_sao_armazenados(self):
        """Cenário: Requisição 200 com sucesso"""
        mock_response = Mock(status_code=200, text=self.mock_html_content)

        with patch("requests.get", return_value=mock_response):
            raspagem = ProducaoRaspagem(1970)
            raspagem.buscar_html()

        self.assertIsNotNone(raspagem.html)
        self.assertIn("Banco de dados de uva, vinho e derivados", raspagem.html.title.string)

    def test_quando_status_404_entao_excecao_com_mensagem_adequada(self):
        """Cenário: Requisição com erro 404"""
        mock_response = Mock(status_code=404, text=self.mock_html_content)

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(ErroRequisicao) as context:
                raspagem = ProducaoRaspagem(1970)
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Failed to fetch HTML. Status code: 404")

    def test_quando_status_500_entao_excecao_com_mensagem_adequada(self):
        """Cenário: Requisição com erro 500"""
        mock_response = Mock(status_code=500, text=self.mock_html_content)

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(ErroRequisicao) as context:
                raspagem = ProducaoRaspagem(1970)
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Failed to fetch HTML. Status code: 500")

    def test_quando_timeout_entao_excecao_com_mensagem_timeout(self):
        """Cenário: Timeout na requisição"""
        with patch("requests.get", side_effect=Timeout):
            with self.assertRaises(TimeoutRequisicao) as context:
                raspagem = ProducaoRaspagem(1970)
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Request timed out")

    def test_quando_parser_executado_entao_dados_estruturados_sao_extraidos(self):
        """Cenário: Parser retorna produtos, totais e tipos corretamente"""
        raspagem = ProducaoRaspagem(1970)
        raspagem.html = BeautifulSoup(self.mock_html_content, "html.parser")
        dados = raspagem.parser_html()

        self.assertIn("Produto", dados)
        self.assertIn("Total", dados)
        self.assertEqual(dados["Total"], 256370050)
        self.assertEqual(len(dados["Produto"]), 4)

        produtos = dados["Produto"]

        self.assertIn("VINHO DE MESA", produtos[0])
        self.assertIn("VINHO FINO DE MESA (VINIFERA)", produtos[1])
        self.assertIn("SUCO", produtos[2])
        self.assertIn("DERIVADOS", produtos[3])

        self.assertEqual(produtos[0]["VINHO DE MESA"], 217208604)
        self.assertEqual(produtos[1]["VINHO FINO DE MESA (VINIFERA)"], 23899346)
        self.assertEqual(produtos[2]["SUCO"], 1097771)
        self.assertEqual(produtos[3]["DERIVADOS"], 14164329)

        self.assertEqual(len(produtos[0]["TIPOS"]), 3)
        self.assertEqual(len(produtos[1]["TIPOS"]), 3)
        self.assertEqual(len(produtos[2]["TIPOS"]), 5)
        self.assertEqual(len(produtos[3]["TIPOS"]), 36)

        self.assertEqual(list(produtos[0]["TIPOS"][0].values())[0], 174224052.0)
        self.assertEqual(list(produtos[1]["TIPOS"][0].values())[0], 7591557.0)
        self.assertEqual(list(produtos[2]["TIPOS"][1].values())[0], 0)
        self.assertEqual(list(produtos[3]["TIPOS"][0].values())[0], 0)

