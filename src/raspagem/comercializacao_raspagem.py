"""Classe abstrata para raspagem de dados de comércio exterior: Importação e Exportação."""

from src.raspagem.vitivinicultura_raspagem import VitiviniculturaRaspagem


class ComercializacoRaspagem(VitiviniculturaRaspagem):
    """
    Classe responsável por realizar a raspagem de dados
    da comercialização de vinhos, sucos e derivados do Rio Grande do Sul.
    """

    def __init__(self, ano: int):
        super().__init__()
        self.ano = ano
        self.construir_url()

    def construir_url(self):
        self.url = self.url + f"?opcao=opt_04&ano={self.ano}"
