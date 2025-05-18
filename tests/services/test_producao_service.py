import unittest
from unittest.mock import patch
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser
from src.services.producao_services import ProducaoService


class TestComportamentoProducaoService(unittest.TestCase):
    def setUp(self):
        self.ano = 2023

    @patch("src.services.producao_services.ProducaoRaspagem")
    @patch("src.services.producao_services.RawRepository")
    @patch("src.services.producao_services.ProducaoRepository")
    def test_quando_dados_validos_entao_salva_raw_e_final(self, mock_repo_final, mock_repo_raw, mock_raspagem):
        """Cenário: Dados disponíveis e válidos"""
        instance = mock_raspagem.return_value
        instance.buscar_html.return_value = None
        instance.parser_html.return_value = {"Total": 123, "Produto": []}

        service = ProducaoService()
        service.get_por_ano(self.ano)

        instance.buscar_html.assert_called_once()
        instance.parser_html.assert_called_once()
        mock_repo_raw.return_value.upsert.assert_called_once()
        mock_repo_final.return_value.salvar_ou_atualizar.assert_called_once()

    @patch("src.services.producao_services.ProducaoRaspagem", side_effect=TimeoutRequisicao())
    @patch("src.services.producao_services.ProducaoRepository")
    def test_quando_timeout_entao_retorna_dados_locais(self, mock_repo_final, _):
        """Cenário: Timeout na raspagem"""
        service = ProducaoService()
        with patch.object(service.producao_repository, "get_por_ano", return_value="dados locais") as fallback:
            resultado = service.get_por_ano(self.ano)
            fallback.assert_called_once_with(self.ano)
            self.assertEqual(resultado, "dados locais")

    @patch("src.services.producao_services.ProducaoRaspagem")
    @patch("src.services.producao_services.ProducaoRepository")
    def test_quando_status_http_erro_entao_retorna_dados_locais(self, mock_repo_final, mock_raspagem):
        """Cenário: Status HTTP 404/500 na raspagem"""
        instance = mock_raspagem.return_value
        instance.buscar_html.side_effect = ErroRequisicao(404)

        service = ProducaoService()
        with patch.object(service.producao_repository, "get_por_ano", return_value="dados locais") as fallback:
            resultado = service.get_por_ano(self.ano)
            fallback.assert_called_once_with(self.ano)
            self.assertEqual(resultado, "dados locais")

    @patch("src.services.producao_services.ProducaoRaspagem")
    @patch("src.services.producao_services.ProducaoRepository")
    def test_quando_falha_no_parser_entao_retorna_dados_locais(self, mock_repo_final, mock_raspagem):
        """Cenário: Falha ao interpretar HTML"""
        instance = mock_raspagem.return_value
        instance.buscar_html.return_value = None
        instance.parser_html.side_effect = ErroParser("falha no parser")

        service = ProducaoService()
        with patch.object(service.producao_repository, "get_por_ano", return_value="dados locais") as fallback:
            resultado = service.get_por_ano(self.ano)
            fallback.assert_called_once_with(self.ano)
            self.assertEqual(resultado, "dados locais")
