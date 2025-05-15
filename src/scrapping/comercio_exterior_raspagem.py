"""Classe abstrata para raspagem de dados de comércio exterior: Importação e Exportação."""
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

from src.utils import extrair_numeros
from src.config import URL_SITE_EMBRAPA

class ComercioExteriorRaspagemAbstract(ABC):
    """
        Classe abstrata para raspagem de dados de comércio exterior: Importação e Exportação.
    """
    def __init__(self):
        self.url: str = URL_SITE_EMBRAPA
        self.html: BeautifulSoup

    @abstractmethod
    def construir_url(self):
        """
        Método abstrato para construir a URL de acordo com o tipo de consulta.
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
                raise Exception(f"Failed to fetch HTML. Status code: {response.status_code}")
        except TimeoutError as e:
            raise Exception("Request timed out") from e

    def parser_html(self):
        """
        Método para processar o HTML e extrair os dados desejados.
        """
        try:
            data_table = self.html.find("table", class_="tb_base tb_dados")

            rodape_quantidade = extrair_numeros(
                data_table.find("tfoot").findChildren("td")[1].string.strip())  # type: ignore
            rodape_valor = extrair_numeros(
                data_table.find("tfoot").findChildren("td")[2].string.strip())  # type: ignore

            paises = []
            for tr in data_table.find("tbody").find_all("tr"):  # type: ignore
                pais = {}
                tds = tr.find_all("td")  # type: ignore
                pais["pais"] = tds[0].string.strip()  # type: ignore
                pais["quantidade_kg"] = extrair_numeros(tds[1].string.strip())  # type: ignore
                pais["valor_us"] = extrair_numeros(tds[2].string.strip())  # type: ignore
                paises.append(pais)
        except Exception as e:
            raise Exception(f"Erro ao processar o html: {e}") from e
        return {
            "paises": paises,
            "total": {"quantidade": rodape_quantidade, "valor": rodape_valor},
        }
