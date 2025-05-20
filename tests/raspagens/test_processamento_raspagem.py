"""Classe de teste para a raspagem de processamento."""
from tests.raspagens.base_test_raspagem import BaseTestRaspagem
from src.raspagem.processamento_raspagem import ProcessamentoRaspagem
from bs4 import BeautifulSoup
from pathlib import Path


class TestProcessamentoRaspagem(BaseTestRaspagem):
    raspagem_class = ProcessamentoRaspagem
    kwargs = {"ano": 2023, "subopcao": "subopt_01"}

    def setUp(self):
        super().setUp()
        html_file_path = Path(__file__).parent / "sources" / "ano=2023&opcao=opt_03&subopcao=subopt_01.html"
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()

    def test_parser_extrai_dados_categorizados(self):
        raspagem = self.raspagem_class(**self.kwargs)
        raspagem.html = BeautifulSoup(self.mock_html_content, "html.parser")
        dados = raspagem.parser_html()

        self.assertIn("Cultivar", dados)
        self.assertIn("Total", dados)
        self.assertEqual(dados["Total"], 99557416)

        culturas = dados["Cultivar"]
        self.assertGreater(len(culturas), 0)

        tinta_item = culturas[0]
        self.assertEqual(list(tinta_item.keys())[0], "TINTAS")
        self.assertEqual(tinta_item["TINTAS"], 35881118)
        self.assertIn("TIPOS", tinta_item)

        tipos_tintas = tinta_item["TIPOS"]
        self.assertGreater(len(tipos_tintas), 0)
        self.assertEqual(tipos_tintas[0]["Alicante Bouschet"], 4108858)
        self.assertEqual(tipos_tintas[1]["Ancelota"], 783688)

        brancas_item = culturas[1]
        self.assertEqual(list(brancas_item.keys())[0], "BRANCAS E ROSADAS")
        self.assertEqual(brancas_item["BRANCAS E ROSADAS"], 63676298)
        self.assertIn("TIPOS", brancas_item)

        tipos_brancas = brancas_item["TIPOS"]
        self.assertGreater(len(tipos_brancas), 0)
        self.assertEqual(tipos_brancas[0]["Aliatico"], 0)
        self.assertEqual(tipos_brancas[1]["Aligote"], 0)
        self.assertEqual(tipos_brancas[-1]["Outras(3)"], 0)

