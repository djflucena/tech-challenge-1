"""Service para exportação de vinhos, sucos e derivados
    do Rio Grande do Sul."""
from src.repositories.exportacao_repository import ExportacaoRepository
from src.raspagem.exportacao_raspagem import ExportacaoRaspagem
from src.repositories.raw_repository import RawRepository

class ExportacaoService:
    """Service para exportação de vinhos, sucos e derivados
    do Rio Grande do Sul."""

    def __init__(self):
        self._repo_raw = RawRepository()
        self.exportacao_repository = ExportacaoRepository()

    def get_por_ano(self, ano: int, subopcao: str):
        """Retorna a exportação de vinhos, sucos e derivados"""
        try:
            exportacao_raspagem = ExportacaoRaspagem(ano, subopcao)
            exportacao_raspagem.buscar_html()
            dados = exportacao_raspagem.parser_html()

            self._repo_raw.upsert(
                endpoint="exportacao",
                ano=ano,
                subopcao=subopcao,
                payload=dados
            )
            
            self.exportacao_repository.salvar_ou_atualizar(dados, ano, subopcao)
        except Exception:
            print("Erro ao buscar dados")
        return self.exportacao_repository.get_por_ano(ano, subopcao)
