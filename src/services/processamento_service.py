"""Service para processamento de vinhos, sucos e derivados
    do Rio Grande do Sul."""

from src.repositories.processamento_repository import ProcessamentoRepository
from src.raspagem.processamento_raspagem import ProcessamentoRaspagem
from src.repositories.raw_repository import RawRepository

class ProcessamentoService:
    """
    Service para processamento de uvas viníferas, americanas,
    de mesa e sem classificação no Rio Grande do Sul.
    """

    def __init__(self):
        self._repo_raw = RawRepository()
        self._repo = ProcessamentoRepository()

    def get_por_ano(self, ano: int, subopcao: str):
        """
        Tenta raspar; em falha, retorna o que estiver salvo.
        """
        try:
            raspagem = ProcessamentoRaspagem(ano, subopcao)
            raspagem.buscar_html()
            dados = raspagem.parser_html()
  
            self._repo_raw.upsert(
                endpoint="processamento",
                ano=ano,
                subopcao=subopcao,
                payload=dados
            )

            self._repo.salvar_ou_atualizar(dados, ano, subopcao)
        except Exception:
            print("Erro ao buscar dados")
        return self._repo.get_por_ano(ano, subopcao)
