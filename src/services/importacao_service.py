from src.repositories.importacao_repository import ImportacaoRepository

class ImportacaoService:

    def __init__(self):
        self.importacao_repository = ImportacaoRepository()
    
    def get_opcao_por_ano(self, ano: int, subopcao: str):
        try:
            pass
            # importacao_raspagem = ImportacaoRaspagem(ano)
        except Exception as e:
            print("Erro ao buscar dados")
        return self.importacao_repository.get_opcao_por_ano(ano, subopcao)
