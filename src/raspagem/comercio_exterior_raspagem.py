"""Classe abstrata para raspagem de dados de comércio exterior: Importação e Exportação."""
from abc import abstractmethod

from src.raspagem.base_raspagem import BaseRaspagem
from src.raspagem.raspagem_exceptions import ErroParser
from src.utils import extrair_numeros
from src.utils import remover_acentos

class ComercioExteriorRaspagem(BaseRaspagem):
    """
        Classe abstrata para raspagem de dados de comércio exterior: Importação e Exportação.
    """
    @abstractmethod
    def construir_url(self):
        """
        Método abstrato para construir a URL de acordo com o tipo de consulta.
        """


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
                pais["pais"] = remover_acentos(tds[0].string.strip())  # type: ignore
                pais["quantidade_kg"] = extrair_numeros(tds[1].string.strip())  # type: ignore
                pais["valor_us"] = extrair_numeros(tds[2].string.strip())  # type: ignore
                paises.append(pais)

        except Exception as e:
            raise ErroParser(f"Erro ao processar o HTML: {e}") from e

        return {
            "paises": paises,
            "total": {"quantidade": rodape_quantidade, "valor": rodape_valor},
        }
