from src.config import BANCO_DE_DADOS


class ImportacaoRepository:

    def get_opcao_por_ano(self, ano: int, subopcao: str):
        return BANCO_DE_DADOS[ano][subopcao]

    def salvar_ou_atualizar(self, dados, ano, subopcao):
        if ano not in BANCO_DE_DADOS:
            BANCO_DE_DADOS[ano] = {}
        if subopcao not in BANCO_DE_DADOS[ano]:
            BANCO_DE_DADOS[ano][subopcao] = {}
        BANCO_DE_DADOS[ano][subopcao] = dados