from abc import ABC, abstractmethod
from src.utils import extrair_numeros

from bs4 import BeautifulSoup
import requests

from src.config import URL_SITE_EMBRAPA

class ComercioExteriorRaspagemAbstract(ABC):
    
    def __init__(self):
        self.url = URL_SITE_EMBRAPA
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
            
            rodape_quantidade = extrair_numeros(data_table.find('tfoot').findChildren('td')[1].string.strip())
            rodape_valor = extrair_numeros(data_table.find('tfoot').findChildren('td')[2].string.strip())

            paises = []
            for tr in data_table.find('tbody').find_all('tr'):
                pais = {}
                tds = tr.find_all('td')
                pais['pais'] = tds[0].string.strip()
                pais['quantidade_kg'] = extrair_numeros(tds[1].string.strip())
                pais['valor_us'] = extrair_numeros(tds[2].string.strip())
                paises.append(pais)
        except Exception as e:
            raise Exception(f"Erro ao processar o html: {e}")
        return {
            "paises":paises,
            "total": {
                "quantidade": rodape_quantidade,
                "valor": rodape_valor
            }
        }