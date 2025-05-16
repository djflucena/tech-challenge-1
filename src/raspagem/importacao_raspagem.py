"""Classe abstrata para raspagem de dados de comércio exterior: Importação e Exportação."""

from src.raspagem.comercio_exterior_raspagem import ComercioExteriorRaspagemAbstract


class ImportacaoRaspagem(ComercioExteriorRaspagemAbstract):
    """Classe responsável por realizar a raspagem de dados de
    importação de vinhos, sucos e derivados do Rio Grande do Sul."""

    def __init__(self, ano: int, subopcao: str) -> None:
        super().__init__()
        self.ano = ano
        self.subopcao = subopcao
        self.construir_url()

    def construir_url(self):
        self.url = self.url + f"?ano={self.ano}&opcao=opt_05&subopcao={self.subopcao}"
