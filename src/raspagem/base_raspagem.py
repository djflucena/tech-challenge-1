import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from http import HTTPStatus
from requests.exceptions import Timeout

from src.config import URL_SITE_EMBRAPA
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser


class BaseRaspagem(ABC):
    
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
            if response.status_code == HTTPStatus.OK:
                self.html = BeautifulSoup(response.text, "html.parser")
            else:
                raise ErroRequisicao(response.status_code)
        except Timeout as e:
            raise TimeoutRequisicao()
