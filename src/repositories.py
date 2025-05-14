class ProducaoRepository:
    """
        Repository para Produção de vinhos, sucos e derivados do Rio Grande do Sul.
    """
    def __init__(self):
        self.dados = None

    def get_por_ano(self, ano: int):
        """
            Retorna a produção de vinhos, sucos e derivados do Rio Grande do Sul por ano.
        """
        return self.dados
        
    def salvar(self, dados):
        """
            Salva os dados de produção de vinhos, sucos e derivados do Rio Grande do Sul.
        """
        # Implementar lógica de salvamento no banco de dados ou outro armazenamento
        self.dados = dados