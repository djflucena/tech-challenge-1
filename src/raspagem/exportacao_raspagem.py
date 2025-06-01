"""Classe responsável por realizar a raspagem de dados de exportação."""

from src.raspagem.comercio_exterior_raspagem import ComercioExteriorRaspagem


class ExportacaoRaspagem(ComercioExteriorRaspagem):
    """Classe responsável por realizar a raspagem de dados de
    exportação de vinhos, sucos e derivados do Rio Grande do Sul."""

    def __init__(self, ano: int, subopcao: str) -> None:
        super().__init__()
        self.ano = ano
        self.subopcao = subopcao
        self.construir_url()

    def construir_url(self):
        self.url = self.url + f"?ano={self.ano}&opcao=opt_06&subopcao={self.subopcao}"
