import re
import unicodedata

def extrair_numeros(input_string) -> float:
    """
    Extracts and returns only the numbers from the given string.

    Args:
        input_string (str): The input string.

    Returns:
        str: A string containing only the numbers from the input.
    """
    val = re.sub(r'\D', '', input_string)
    return float(val) if val else 0 

def remover_acentos(texto: str) -> str:
    """
    Remove os acentos de todos os caracteres na string fornecida.

    Esta função normaliza a string usando a forma de decomposição NFD (Normalization Form D),
    onde caracteres acentuados são representados como a combinação de sua base e um diacrítico.
    Em seguida, filtra todos os caracteres de categoria 'Mn' (Mark, Nonspacing), que incluem
    acentos gráficos e outros modificadores invisíveis.

    Parâmetros:
        texto (str): A string de entrada que pode conter caracteres acentuados.

    Retorna:
        str: Uma nova string com os mesmos caracteres do input, porém sem acentuação.
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )