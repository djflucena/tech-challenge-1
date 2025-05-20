# src/repositories/exceptions.py

class RepositorioErro(Exception):
    """Exceção base para erros de repositório (persistência)."""
    pass


class ErroConexaoBD(RepositorioErro):
    """Falha ao conectar com o banco de dados."""
    def __init__(self, detalhe: str):
        super().__init__(f"Erro de conexão com o banco: {detalhe}")


class ErroConsultaBD(RepositorioErro):
    """Falha ao executar uma consulta (SELECT)."""
    def __init__(self, detalhe: str):
        super().__init__(f"Erro na consulta ao banco: {detalhe}")


class RegistroNaoEncontrado(RepositorioErro):
    """Quando não existe registro para os parâmetros informados."""
    def __init__(self, endpoint: str, ano: int, subopcao: str | None):
        chave = f"{endpoint}/{ano}/{subopcao or ''}"
        super().__init__(f"Nenhum registro encontrado para {chave}")
