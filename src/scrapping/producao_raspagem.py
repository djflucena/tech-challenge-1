from src.utils import extrair_numeros

from bs4 import BeautifulSoup
import requests

class ProducaoRaspagem:
    """
        Classe responsável por realizar a raspagem de dados 
        da produção de vinhos, sucos e derivados do Rio Grande do Sul.
    """
    def __init__(self):
        """
            Inicializa a classe ProducaoRaspagem.
            Define a URL base para a raspagem de dados.
        """
        self.url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
        self.html = None

    def buscar_html(self, ano: int) -> None:
        """
            Busca o HTML da página de produção de vinhos, 
            sucos e derivados do Rio Grande do Sul.
            :param ano: Ano para o qual os dados devem ser buscados.
        """
        try:
            response = requests.get(f"{self.url}?ano={ano}", timeout=100)
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
            total_val = data_table.find('tfoot').findChildren('td')[1].string.strip()
            table_footer_total_val = float(extrair_numeros(total_val)) if total_val else 0 

            produtos = []
            id_item_corrente = None
        
            for tr in data_table.find('tbody').find_all('tr'):
                tds = tr.find_all('td')
                if tds[0]['class'][0] == "tb_item":
                    item = self.extrair_item(tds)
                    item["TIPOS"] = []
                    id_item_corrente = list(item.keys())[0]
                    print(id_item_corrente)
                    produtos.append(item)
                elif tds[0]['class'][0] == "tb_subitem":
                    subitem = self.extrair_item(tds)
                    item_corrente = self.procurar_item_id(produtos, id_item_corrente)
                    if item_corrente != -1:
                        produtos[item_corrente]["TIPOS"].append(subitem)
                    else:
                        pass
                else:
                    pass
        except Exception as e:
            raise Exception(f"Erro ao processar o html")
        return {
            table_header_coluna_esquerda: produtos,
            table_footer_total_text: table_footer_total_val,
        }
        
    def extrair_item(self, tds=[]) -> dict:
        item = {}
        val = extrair_numeros(tds[1].string.strip())
        item[tds[0].string.strip()] = float(val) if val else 0 
        return item
    
    def procurar_item_id(self, produtos, id_item_corrente) -> int:
        for id, produto in enumerate(produtos):
            if list(produto.keys())[0] == id_item_corrente:
                return id
        return -1
    