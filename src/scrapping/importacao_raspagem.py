class ImportacaoRaspagem:
    
    def __init__(self, ano: int, subopcao: str) -> None:
        self.ano = ano
        self.subopcao = subopcao
        self.html = None

    def buscar_html(self) -> None:
        pass

    def parser_html(self) -> dict:
        return {}