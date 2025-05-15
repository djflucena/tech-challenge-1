from src.config import BANCO_DE_DADOS

class ComercializacaoRepository:
    def get_por_ano(self, ano: int):
        try:
            return BANCO_DE_DADOS[ano]
        except KeyError:
            raise Exception(f"Dados não encontrados para o ano {ano}")
        
    def salvar_ou_atualizar(self, dados, ano):
        BANCO_DE_DADOS[ano] = dados