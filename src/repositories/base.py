# src/repositories/base.py
from typing import Any, Optional
from src.config import BANCO_DE_DADOS

class BaseRepository:
    def __init__(self, categoria: str, has_subopcao: bool = True):
        if categoria not in BANCO_DE_DADOS:
            raise ValueError(f"Categoria inválida: {categoria!r}")
        self._repo = BANCO_DE_DADOS[categoria]
        self._has_subopcao = has_subopcao

    def get_por_ano(
        self,
        ano: int,
        subopcao: Optional[str] = None
    ) -> Any:
        """
        Se has_subopcao=True, retorna repo[ano][subopcao].
        Se has_subopcao=False, ignora subopcao e retorna repo[ano].
        """
        if self._has_subopcao:
            if subopcao is None:
                raise ValueError("Esta categoria exige subopcao")
            return self._repo.get(ano, {}).get(subopcao)
        else:
            # subopcao é ignorado
            return self._repo.get(ano)

    def salvar_ou_atualizar(
        self,
        dados: Any,
        ano: int,
        subopcao: Optional[str] = None
    ) -> None:
        """
        Se has_subopcao=True, faz self._repo[ano][subopcao] = dados.
        Se has_subopcao=False, faz self._repo[ano] = dados.
        """
        if self._has_subopcao:
            if subopcao is None:
                raise ValueError("Esta categoria exige subopcao")
            ano_dict = self._repo.setdefault(ano, {})
            ano_dict[subopcao] = dados
        else:
            # subopcao é ignorado
            self._repo[ano] = dados
