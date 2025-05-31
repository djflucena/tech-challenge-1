"""Classe de Teste para a classe ProducaoRaspagem."""

from tests.raspagens.base_test_raspagem import BaseTestRaspagem
from src.raspagem.producao_raspagem import ProducaoRaspagem
from bs4 import BeautifulSoup
from pathlib import Path


class TestProducaoRaspagem(BaseTestRaspagem):
    raspagem_class = ProducaoRaspagem
    kwargs = {"ano": 1970, 'subopcao': None}

    def setUp(self):
        super().setUp()
        html_file_path = Path(__file__).parent / "sources" / "ano=1970&opcao=opt_02.html"
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()

    def test_parser_extrai_dados_estruturados(self):
        raspagem = self.raspagem_class(**self.kwargs)
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

