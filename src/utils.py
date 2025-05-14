import re

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