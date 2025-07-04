import unittest
from unittest.mock import patch
from src.services.processamento_service import ProcessamentoService
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser


class TestComportamentoProcessamentoService(unittest.TestCase):
    def setUp(self):
        self.ano = 2023
        self.subopcao = "subopt_01"

        

    @patch("src.services.processamento_service.ProcessamentoRaspagem")
    @patch("src.services.processamento_service.ProcessamentoRepository")
    def test_quando_dados_validos_entao_salva_raw_e_final(self, mock_repo_final, mock_raspagem):
        """Cenário: Dados disponíveis e válidos"""
        instance = mock_raspagem.return_value
        instance.buscar_html.return_value = None
        instance.parser_html.return_value = {"Total": 123, "Cultivar": []}

        service = ProcessamentoService()
        service.get_por_ano(self.ano, self.subopcao)

        instance.buscar_html.assert_called_once()
        instance.parser_html.assert_called_once()
        mock_repo_final.return_value.salvar_ou_atualizar.assert_called_once()

    @patch("src.services.processamento_service.ProcessamentoRaspagem", side_effect=TimeoutRequisicao())
    @patch("src.services.processamento_service.ProcessamentoRepository")
    def test_quando_timeout_entao_retorna_dados_locais(self, mock_repo_final, _):
        """Cenário: Timeout na raspagem"""
        service = ProcessamentoService()
        with patch.object(service, "get_por_ano", return_value="dados locais") as fallback:
            resultado = service.get_por_ano(self.ano, self.subopcao)
            fallback.assert_called_once_with(self.ano, self.subopcao)
            self.assertEqual(resultado, "dados locais")

    @patch("src.services.processamento_service.ProcessamentoRaspagem")
    @patch("src.services.processamento_service.ProcessamentoRepository")
    def test_quando_status_http_erro_entao_retorna_dados_locais(self, mock_repo_final, mock_raspagem):
        """Cenário: Status HTTP 404/500 na raspagem"""
        instance = mock_raspagem.return_value
        instance.buscar_html.side_effect = ErroRequisicao(500)

        service = ProcessamentoService()
        with patch.object(service, "get_por_ano", return_value="dados locais") as fallback:
            resultado = service.get_por_ano(self.ano, self.subopcao)
            fallback.assert_called_once_with(self.ano, self.subopcao)
            self.assertEqual(resultado, "dados locais")

    @patch("src.services.processamento_service.ProcessamentoRaspagem")
    @patch("src.services.processamento_service.ProcessamentoRepository")
    def test_quando_falha_no_parser_entao_retorna_dados_locais(self, mock_repo_final, mock_raspagem):
        """Cenário: Falha ao interpretar HTML"""
        instance = mock_raspagem.return_value
        instance.buscar_html.return_value = None
        instance.parser_html.side_effect = ErroParser("falha no parser")

        service = ProcessamentoService()
        with patch.object(service, "get_por_ano", return_value="dados locais") as fallback:
            resultado = service.get_por_ano(self.ano, self.subopcao)
            fallback.assert_called_once_with(self.ano, self.subopcao)
            self.assertEqual(resultado, "dados locais")
