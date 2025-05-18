"""Classe de teste para a raspagem de importação."""
from tests.raspagens.base_test_raspagem import BaseTestRaspagem
from src.raspagem.importacao_raspagem import ImportacaoRaspagem
from bs4 import BeautifulSoup
from pathlib import Path


class TestImportacaoRaspagem(BaseTestRaspagem):
    raspagem_class = ImportacaoRaspagem
    kwargs = {"ano": 1970, "subopcao": "subopt_01"}

    def setUp(self):
        super().setUp()
        html_file_path = Path(__file__).parent / "sources" / "ano=1970&opcao=opt_05&subopcao=subopt_01.html"
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()

    def test_parser_extrai_dados_de_paises(self):
        raspagem = self.raspagem_class(**self.kwargs)
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

