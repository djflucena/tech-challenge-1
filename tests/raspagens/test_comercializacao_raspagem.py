import unittest
from requests.exceptions import Timeout
from unittest.mock import Mock, patch

from bs4 import BeautifulSoup
from requests import HTTPError

from src.raspagem.comercializacao_raspagem import ComercializacoRaspagem
from pathlib import Path

class TestComercializacoRaspagem(unittest.TestCase):

    def setUp(self):
        html_file_path = Path(__file__).parent / "sources" / "ano=2023&opcao=opt_04.html"
        with html_file_path.open("r", encoding="utf-8") as file:
            self.mock_html_content = file.read()
        return super().setUp()

    def test_buscar_html_sucesso(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            raspagem = ComercializacoRaspagem(2003)
            raspagem.buscar_html()
            self.assertIsNotNone(raspagem.html)
            self.assertIn("Banco de dados de uva, vinho e derivados", raspagem.html.title.string)
    
    def test_buscar_html_request_404(self):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(Exception) as context:
                raspagem = ComercializacoRaspagem()
                raspagem.buscar_html(2023)
                self.assertIsNone(raspagem.html)
                self.assertEqual(context.msg, "Failed to fetch HTML. Status code: 404")
    
    def test_buscar_html_request_500(self):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = self.mock_html_content

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(Exception) as context:
                raspagem = ComercializacoRaspagem()
                raspagem.buscar_html(2003)
                self.assertIsNone(raspagem.html)
                self.assertEqual(context.msg, "Failed to fetch HTML. Status code: 500")
    
    def test_buscar_html_request_timeout(self):
        with patch("requests.get", side_effect=Timeout):
            with self.assertRaises(Exception) as context:
                raspagem = ComercializacoRaspagem()
                raspagem.buscar_html(2023)
                self.assertIsNone(raspagem.html)
                self.assertEqual(context.msg, "Request timed out")

    def test_parser_html_sucesso(self):
        raspagem = ComercializacoRaspagem(2023)
        raspagem.html = BeautifulSoup(self.mock_html_content, 'html.parser')
        dados = raspagem.parser_html()

        # Verificações gerais
        self.assertIn("Produto", dados)
        self.assertIn("Total", dados)
        self.assertEqual(dados["Total"], 472291085)  # Total geral

        # Quantidade de categorias principais
        self.assertEqual(len(dados["Produto"]), 9)  # Número de categorias principais

        # Categorias e quantidades principais
        self.assertIn("VINHO DE MESA", dados["Produto"][0])
        self.assertIn("VINHO FINO DE MESA", dados["Produto"][1])
        self.assertIn("VINHO FRIZANTE", dados["Produto"][2])
        self.assertIn("VINHO ORGÂNICO", dados["Produto"][3])
        self.assertIn("VINHO ESPECIAL", dados["Produto"][4])
        self.assertIn("ESPUMANTES", dados["Produto"][5])
        self.assertIn("SUCO DE UVAS", dados["Produto"][6])
        self.assertIn("SUCO DE UVAS CONCENTRADO", dados["Produto"][7])
        self.assertIn("OUTROS PRODUTOS COMERCIALIZADOS", dados["Produto"][8])

        # Valores principais
        self.assertEqual(dados["Produto"][0]["VINHO DE MESA"], 187016848)
        self.assertEqual(dados["Produto"][1]["VINHO FINO DE MESA"], 18589310)
        self.assertEqual(dados["Produto"][2]["VINHO FRIZANTE"], 2843600)
        self.assertEqual(dados["Produto"][3]["VINHO ORGÂNICO"], 9123)
        self.assertEqual(dados["Produto"][4]["VINHO ESPECIAL"], 0)  # '-' foi convertido para 0
        self.assertEqual(dados["Produto"][5]["ESPUMANTES"], 29381635)
        self.assertEqual(dados["Produto"][6]["SUCO DE UVAS"], 166708720)
        self.assertEqual(dados["Produto"][7]["SUCO DE UVAS CONCENTRADO"], 37852507)
        self.assertEqual(dados["Produto"][8]["OUTROS PRODUTOS COMERCIALIZADOS"], 29889342)

        # Subitens (TIPOS) por categoria
        self.assertEqual(len(dados["Produto"][0]["TIPOS"]), 3)  # VINHO DE MESA
        self.assertEqual(len(dados["Produto"][1]["TIPOS"]), 3)  # VINHO FINO DE MESA
        self.assertEqual(len(dados["Produto"][2]["TIPOS"]), 0)  # VINHO FRIZANTE (sem subitens)
        self.assertEqual(len(dados["Produto"][3]["TIPOS"]), 0)  # VINHO ORGÂNICO (sem subitens)
        self.assertEqual(len(dados["Produto"][4]["TIPOS"]), 3)  # VINHO ESPECIAL
        self.assertEqual(len(dados["Produto"][5]["TIPOS"]), 3)  # ESPUMANTES
        self.assertEqual(len(dados["Produto"][6]["TIPOS"]), 5)  # SUCO DE UVAS
        self.assertEqual(len(dados["Produto"][7]["TIPOS"]), 0)  # SUCO DE UVAS CONCENTRADO (sem subitens)
        self.assertEqual(len(dados["Produto"][8]["TIPOS"]), 36) # OUTROS PRODUTOS COMERCIALIZADOS

        # Exemplos de subitens
        self.assertEqual(list(dados["Produto"][0]["TIPOS"][0].values())[0], 165097539)  # VINHO DE MESA - Tinto
        self.assertEqual(list(dados["Produto"][0]["TIPOS"][1].values())[0], 2520748)    # VINHO DE MESA - Rosado
        self.assertEqual(list(dados["Produto"][0]["TIPOS"][2].values())[0], 19398561)   # VINHO DE MESA - Branco

        self.assertEqual(list(dados["Produto"][1]["TIPOS"][0].values())[0], 12450606)  # VINHO FINO DE MESA - Tinto
        self.assertEqual(list(dados["Produto"][1]["TIPOS"][1].values())[0], 1214583)   # VINHO FINO DE MESA - Rosado
        self.assertEqual(list(dados["Produto"][1]["TIPOS"][2].values())[0], 4924121)   # VINHO FINO DE MESA - Branco

        self.assertEqual(list(dados["Produto"][4]["TIPOS"][0].values())[0], 0)  # VINHO ESPECIAL - Tinto
        self.assertEqual(list(dados["Produto"][4]["TIPOS"][1].values())[0], 0)  # VINHO ESPECIAL - Rosado
        self.assertEqual(list(dados["Produto"][4]["TIPOS"][2].values())[0], 0)  # VINHO ESPECIAL - Branco

        self.assertEqual(list(dados["Produto"][5]["TIPOS"][0].values())[0], 9771698)   # ESPUMANTES - Espumante Moscatel
        self.assertEqual(list(dados["Produto"][5]["TIPOS"][1].values())[0], 19609379)  # ESPUMANTES - Espumante
        self.assertEqual(list(dados["Produto"][5]["TIPOS"][2].values())[0], 558)       # ESPUMANTES - Espumante Orgânico

        self.assertEqual(list(dados["Produto"][6]["TIPOS"][0].values())[0], 129419407) # SUCO DE UVAS - Suco Natural Integral
        self.assertEqual(list(dados["Produto"][6]["TIPOS"][1].values())[0], 128599)    # SUCO DE UVAS - Suco Adoçado
        self.assertEqual(list(dados["Produto"][6]["TIPOS"][2].values())[0], 34402925)  # SUCO DE UVAS - Suco Reprocessado/reconstituído
        self.assertEqual(list(dados["Produto"][6]["TIPOS"][3].values())[0], 932154)    # SUCO DE UVAS - Suco Orgânico
        self.assertEqual(list(dados["Produto"][6]["TIPOS"][4].values())[0], 1825635)   # SUCO DE UVAS - Outros sucos de uvas

        # Um exemplo de "OUTROS PRODUTOS COMERCIALIZADOS"
        self.assertEqual(list(dados["Produto"][8]["TIPOS"][0].values())[0], 8152)      # Outros vinhos (sem informação detalhada)
        self.assertEqual(list(dados["Produto"][8]["TIPOS"][1].values())[0], 0)         # Agrin (fermentado, acético misto)
        self.assertEqual(list(dados["Produto"][8]["TIPOS"][2].values())[0], 111)       # Aguardente de vinho 50°gl