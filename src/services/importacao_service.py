"""Service para importação de vinhos, sucos e derivados
    do Rio Grande do Sul."""
from src.repositories.importacao_repository import ImportacaoRepository
from src.raspagem.importacao_raspagem import ImportacaoRaspagem


class ImportacaoService:
    """Service para importação de vinhos, sucos e derivados
    do Rio Grande do Sul."""

    def __init__(self):
        self.importacao_repository = ImportacaoRepository()

    def get_por_ano(self, ano: int, subopcao: str):
        """Retorna a importação de vinhos, sucos e derivados"""
        try:
            importacao_raspagem = ImportacaoRaspagem(ano, subopcao)
            importacao_raspagem.buscar_html()
            dados = importacao_raspagem.parser_html()
            self.importacao_repository.salvar_ou_atualizar(dados, ano, subopcao)
        except Exception:
            print("Erro ao buscar dados")
        return self.importacao_repository.get_por_ano(ano, subopcao)
