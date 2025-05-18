"""
Classe abstrata para raspagem de dados de vitivinicultura:
Produção, Processamento e Comercialização
"""

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
from src.utils import extrair_numeros
from src.config import URL_SITE_EMBRAPA
from requests.exceptions import Timeout
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser


class VitiviniculturaRaspagem(ABC):
    """
    Classe abstrata para raspagem de dados de vitivinicultura:
    Produção, Processamento e Comercialização.
    """

    def __init__(self):
        self.url: str = URL_SITE_EMBRAPA
        self.html: BeautifulSoup

    @abstractmethod
    def construir_url(self):
        """
        Método abstrato para construir a URL específica da raspagem.
        Cada subclasse deve implementar este método.
        """

    def buscar_html(self) -> None:
        """
        Método para buscar o HTML da página.
        """
        try:
            response = requests.get(self.url, timeout=100)
            if response.status_code == 200:
                self.html = BeautifulSoup(response.text, "html.parser")
            else:
                raise ErroRequisicao(response.status_code)
        except Timeout as e:
            raise TimeoutRequisicao()
        

    def parser_html(self) -> dict:
        """
        Método para processar o HTML e extrair os dados relevantes.
        """
        try:
            data_table = self.html.find("table", class_="tb_base tb_dados")
            table_header_coluna_esquerda = data_table.find("thead").findChildren("th")[0].string.strip()  # type: ignore
            table_footer_total_text = data_table.find("tfoot").findChildren("td")[0].string.strip()  # type: ignore
            table_footer_total_val = extrair_numeros(
                data_table.find("tfoot").findChildren("td")[1].string.strip())  # type: ignore

            produtos = []
            id_item_corrente = None

            for tr in data_table.find("tbody").find_all("tr"):  # type: ignore
                tds = tr.find_all("td")  # type: ignore
                if tds[0]["class"][0] == "tb_item":  # type: ignore
                    item = self.__extrair_item(tds)
                    item["TIPOS"] = []
                    id_item_corrente = list(item.keys())[0]
                    produtos.append(item)
                elif tds[0]["class"][0] == "tb_subitem":  # type: ignore
                    subitem = self.__extrair_item(tds)
                    item_corrente = self.__procurar_item_id(produtos, id_item_corrente)
                    if item_corrente != -1:
                        produtos[item_corrente]["TIPOS"].append(subitem)
        except Exception as e:
            raise ErroParser("Erro ao processar o HTML") from e
        return {
            table_header_coluna_esquerda: produtos,
            table_footer_total_text: table_footer_total_val,
        }

    def __extrair_item(self, tds: list) -> dict:
        item = dict()
        item[tds[0].string.strip()] = extrair_numeros(tds[1].string.strip())
        return item

    def __procurar_item_id(self, produtos, id_item_corrente) -> int:
        for index, produto in enumerate(produtos):
            if list(produto.keys())[0] == id_item_corrente:
                return index
        return -1
