"""Testes para a classe ComercializacaoRaspagem, responsável por raspar dados de uma página HTML."""

from tests.raspagens.base_test_raspagem import BaseTestRaspagem
from src.raspagem.comercializacao_raspagem import ComercializacaoRaspagem
from bs4 import BeautifulSoup
from pathlib import Path


class TestComercializacaoRaspagem(BaseTestRaspagem):
    raspagem_class = ComercializacaoRaspagem
    kwargs = {"ano": 2023}

    def setUp(self):
        super().setUp()
        html_file_path = Path(__file__).parent / "sources" / "ano=2023&opcao=opt_04.html"
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()

    def test_quando_parser_executado_em_html_valido_entao_dados_extraidos_corretamente(self):
        raspagem = self.raspagem_class(**self.kwargs)
        raspagem.html = BeautifulSoup(self.mock_html_content, "html.parser")
        dados = raspagem.parser_html()

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
        self.assertEqual(list(dados["Produto"][0]["TIPOS"][0].values())[0], 165097539)
        self.assertEqual(list(dados["Produto"][8]["TIPOS"][2].values())[0], 111)

    
    def test_quando_parser_executado_em_html_valido_entao_dados_extraidos_corretamente(self):
        """Cenário: Parser bem-sucedido extrai os dados corretamente"""
        raspagem = ComercializacaoRaspagem(2023)
        raspagem.html = BeautifulSoup(self.mock_html_content, "html.parser")
        dados = raspagem.parser_html()

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
