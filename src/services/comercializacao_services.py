from src.raspagem.comercializacao_raspagem import ComercializacoRaspagem
from src.repositories.comercializacao_repository import ComercializacaoRepository

class ComercializacaoService:
    """
        Service para comercialização de vinhos, sucos e derivados 
        do Rio Grande do Sul.
    """
    def __init__(self):
        self.comercializacao_repository = ComercializacaoRepository()

    def get_por_ano(self, ano: int):
        """
            Retorna a comercialização de vinhos, sucos e derivados 
            do Rio Grande do Sul por ano.
        """
        try:
            comercializacao_raspagem = ComercializacoRaspagem(ano)
            comercializacao_raspagem.buscar_html()
            dados = comercializacao_raspagem.parser_html()
            
            self.comercializacao_repository.salvar_ou_atualizar(dados, ano)
        except Exception as e:
            print("Erro ao buscar dados")
        return self.comercializacao_repository.get_por_ano(ano)

