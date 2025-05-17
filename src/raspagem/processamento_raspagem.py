""" Classe responsável por realizar a raspagem de dados da comercialização."""

from src.raspagem.vitivinicultura_raspagem import VitiviniculturaRaspagem


class ProcessamentoRaspagem(VitiviniculturaRaspagem):
    """
    Classe responsável por realizar a raspagem de dados
    da comercialização de vinhos, sucos e derivados do Rio Grande do Sul.
    """

    def __init__(self, ano: int, subopcao: str) -> None:
        super().__init__()
        self.ano = ano
        self.subopcao = subopcao
        self.construir_url()

    def construir_url(self):
        self.url = self.url + f"?ano={self.ano}&opcao=opt_03&subopcao={self.subopcao}"
