from abc import ABC, abstractmethod

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
        return {}