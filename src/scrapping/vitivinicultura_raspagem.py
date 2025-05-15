from abc import ABC, abstractmethod
from src.utils import extrair_numeros

from bs4 import BeautifulSoup
import requests

class VitiviniculturaRaspagem(ABC):
    
    def __init__(self):
        self.url = None
        self.html = None

    @abstractmethod
    def construir_url(self):
        pass

    def buscar_html(self) -> None:
        try:
            response = requests.get(self.url, timeout=100)
            if response.status_code == 200:
                self.html = BeautifulSoup(response.text, 'html.parser')
            else:
                raise Exception(f"Failed to fetch HTML. Status code: {response.status_code}")
        except TimeoutError:
            raise Exception("Request timed out")

    def parser_html(self):
        try:
            data_table = self.html.find('table', class_='tb_base tb_dados')
            table_header_coluna_esquerda = data_table.find('thead').findChildren('th')[0].string.strip()
            table_footer_total_text = data_table.find('tfoot').findChildren('td')[0].string.strip()
            table_footer_total_val = extrair_numeros(data_table.find('tfoot').findChildren('td')[1].string.strip())

            produtos = []
            id_item_corrente = None
        
            for tr in data_table.find('tbody').find_all('tr'):
                tds = tr.find_all('td')
                if tds[0]['class'][0] == "tb_item":
                    item = self.__extrair_item(tds)
                    item["TIPOS"] = []
                    id_item_corrente = list(item.keys())[0]
                    produtos.append(item)
                elif tds[0]['class'][0] == "tb_subitem":
                    subitem = self.__extrair_item(tds)
                    item_corrente = self.__procurar_item_id(produtos, id_item_corrente)
                    if item_corrente != -1:
                        produtos[item_corrente]["TIPOS"].append(subitem)
        except Exception as e:
            raise Exception(f"Erro ao processar o html")
        return {
            table_header_coluna_esquerda: produtos,
            table_footer_total_text: table_footer_total_val,
        }
    
    def __extrair_item(self, tds=[]) -> dict:
        item = {}
        item[tds[0].string.strip()] = extrair_numeros(tds[1].string.strip())
        return item
    
    def __procurar_item_id(self, produtos, id_item_corrente) -> int:
        for id, produto in enumerate(produtos):
            if list(produto.keys())[0] == id_item_corrente:
                return id
        return -1