from src.repositories.importacao_repository import ImportacaoRepository
from src.raspagem.importacao_raspagem import ImportacaoRaspagem

class ImportacaoService:

    def __init__(self):
        self.importacao_repository = ImportacaoRepository()
    
    def get_opcao_por_ano(self, ano: int, subopcao: str):
        try:
            importacao_raspagem = ImportacaoRaspagem(ano,subopcao)
            importacao_raspagem.buscar_html()
            dados = importacao_raspagem.parser_html()
            self.importacao_repository.salvar_ou_atualizar(dados, ano, subopcao)
        except Exception as e:
            print("Erro ao buscar dados")
        return self.importacao_repository.get_opcao_por_ano(ano, subopcao)
