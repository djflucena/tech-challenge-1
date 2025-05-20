"""Classe de teste para a raspagem de exportação."""

from tests.raspagens.base_test_raspagem import BaseTestRaspagem
from src.raspagem.exportacao_raspagem import ExportacaoRaspagem
from bs4 import BeautifulSoup
from pathlib import Path


class TestExportacaoRaspagem(BaseTestRaspagem):
    raspagem_class = ExportacaoRaspagem
    kwargs = {"ano": 2023, "subopcao": "subopt_01"}

    def setUp(self):
        super().setUp()
        html_file_path = Path(__file__).parent / "sources" / "ano=2023&opcao=opt_06&subopcao=subopt_01.html"
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()

    def test_parser_extrai_dados(self):
        raspagem = self.raspagem_class(**self.kwargs)
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
