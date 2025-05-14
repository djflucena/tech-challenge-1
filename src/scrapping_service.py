class RaspagemService:
    def __init__(self, url):
        self.url = url
        self.html = None

    def buscar_dados(self):
        self.html = "Fetched data from URL"

    def converter_dados(self):
        return {
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
        }
    