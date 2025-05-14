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
        response = requests.get(f"{self.url}?ano={ano}", timeout=100)
        if response.status_code == 200:
            self.html = BeautifulSoup(response.text, 'html.parser')
        else:
            raise Exception(f"Failed to fetch HTML. Status code: {response.status_code}")

    def converter_dados(self):
        data_table = self.html.find('table', class_='tb_base tb_dados')
        table_header_coluna_esquerda = data_table.find('thead').findChildren('th')[0].string.strip()
        table_footer_total_text = data_table.find('tfoot').findChildren('td')[0].string.strip()
        table_footer_total_val = data_table.find('tfoot').findChildren('td')[1].string.strip()

        produtos = []
        """for td in data_table.find('tbody').find_all('td'):
            if "tb_item" in td['class']:
                
            elif "tb_subitem" in td['class']:
                print("aqui")"""
        return {
            table_header_coluna_esquerda: produtos,
            table_footer_total_text: extrair_numeros(table_footer_total_val),
        }
        """{
            "Produto": [
                {
                    "VINHO DE MESA": "217208604",
                    "TIPOS": [
                        {"Tinto": 174224052},
                        {"Branco": 748400},
                        {"Rosado": 42236152}
                    ]
                },
                {
                    "VINHO FINO DE MESA (VINIFERA)": "23899346",
                    "TIPOS": [
                        {"Tinto": 7591557},
                        {"Branco": 15562889},
                        {"Rosado": 744900}
                    ]
                },
                {
                    "SUCO": "1097771",
                    "TIPOS": [
                        {"Suco de uva integral": 1097771},
                        {"Suco de uva concentrado": 0},
                        {"Suco de uva adoçado": 0},
                        {"Suco de uva orgânico": 0},
                        {"Suco de uva reconstituído": 0}
                    ]
                }
            ],
            "Total": 256370050
        }"""
    