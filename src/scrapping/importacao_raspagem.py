from src.scrapping.comercio_exterior_raspagem import ComercioExteriorRaspagemAbstract

class ImportacaoRaspagem(ComercioExteriorRaspagemAbstract):
    
    def __init__(self, ano: int, subopcao: str) -> None:
        super().__init__()
        self.ano = ano
        self.subopcao = subopcao
        self.construir_url()

    def construir_url(self):
        self.url = self.url + f"?ano={self.ano}&opcao=opt_05&subopcao={self.subopcao}"