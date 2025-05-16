"""Service para processamento de vinhos, sucos e derivados
    do Rio Grande do Sul."""
# src/services/processamento.py

from src.repositories.processamento_repository import ProcessamentoRepository
from src.raspagem.processamento_raspagem import ProcessamentoRaspagem

class ProcessamentoService:
    """
    Service para processamento de uvas viníferas, americanas,
    de mesa e sem classificação no Rio Grande do Sul.
    """

    def __init__(self):
        self._repo = ProcessamentoRepository()

    def get_por_ano(self, ano: int, subopcao: str):
        """
        Tenta raspar; em falha, retorna o que estiver salvo.
        """
        try:
            raspagem = ProcessamentoRaspagem(ano, subopcao)
            raspagem.buscar_html()
            dados = raspagem.parser_html()
            self._repo.salvar_ou_atualizar(dados, ano, subopcao)
        except Exception as e:
            print(f"[warn] erro na raspagem: {e}")
        return self._repo.get_por_ano(ano, subopcao)
