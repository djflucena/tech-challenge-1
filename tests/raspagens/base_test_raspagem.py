import unittest
from unittest.mock import patch, Mock
from requests.exceptions import Timeout
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao

class BaseTestRaspagem(unittest.TestCase):
    """
    Classe base reutilizável para testes de raspagem.
    Subclasses devem definir:
      - self.raspagem_class
      - self.kwargs (ex: {"ano": 2023, "subopcao": "subopt_01"})
    """

    raspagem_class = None
    kwargs = {}

    def setUp(self):
        # se ninguém sobrescreveu raspagem_class, pule todos os testes deste base
        if self.raspagem_class is None:
            self.skipTest("BaseTestRaspagem: pulando testes abstratos")

    def simulate_response(self, status_code=200, text="<html><title>Banco de dados de uva</title></html>"):
        return Mock(status_code=status_code, text=text)

    def test_html_200_retorna_titulo(self):
        mock_response = self.simulate_response()

        with patch("requests.get", return_value=mock_response):
            raspagem = self.raspagem_class(**self.kwargs)
            raspagem.buscar_html()

        self.assertIsNotNone(raspagem.html)
        self.assertIn("Banco de dados de uva", raspagem.html.title.string)

    def test_status_404_lanca_erro_requisicao(self):
        mock_response = self.simulate_response(status_code=404)

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(ErroRequisicao) as context:
                raspagem = self.raspagem_class(**self.kwargs)
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Failed to fetch HTML. Status code: 404")

    def test_status_500_lanca_erro_requisicao(self):
        mock_response = self.simulate_response(status_code=500)

        with patch("requests.get", return_value=mock_response):
            with self.assertRaises(ErroRequisicao) as context:
                raspagem = self.raspagem_class(**self.kwargs)
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Failed to fetch HTML. Status code: 500")

    def test_timeout_lanca_timeout_requisicao(self):
        with patch("requests.get", side_effect=Timeout):
            with self.assertRaises(TimeoutRequisicao) as context:
                raspagem = self.raspagem_class(**self.kwargs)
                raspagem.buscar_html()

        self.assertEqual(str(context.exception), "Request timed out")