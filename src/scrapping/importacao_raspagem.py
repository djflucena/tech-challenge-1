from src.scrapping.comercio_exterior_raspagem import ComercioExteriorRaspagemAbstract

class ImportacaoRaspagem(ComercioExteriorRaspagemAbstract):
    
    def __init__(self, ano: int, subopcao: str) -> None:
        super().__init__()
        self.ano = ano
        self.subopcao = subopcao
        self.html = None

    def construir_url(self):
        pass

    def buscar_html(self) -> None:
        pass

    def parser_html(self) -> dict:
        return {}