class RaspagemErro(Exception):
    """
    Exceção base para erros de raspagem de dados.
    Todas as exceções específicas devem herdar desta.
    """
    pass


class ErroRequisicao(RaspagemErro):
    """
    Erro ao obter resposta HTTP com status diferente de 200.
    """
    def __init__(self, status_code: int):
        super().__init__(f"Failed to fetch HTML. Status code: {status_code}")
        self.status_code = status_code


class TimeoutRequisicao(RaspagemErro):
    """
    Timeout na tentativa de acessar a URL.
    """
    def __init__(self):
        super().__init__("Request timed out")


class ErroParser(RaspagemErro):
    """
    Erro ao interpretar o conteúdo HTML durante o parser.
    """
    def __init__(self, detalhe: str = "Erro ao processar HTML."):
        super().__init__(detalhe)
