class ImportacaoRepository:

    def get_opcao_por_ano(self, ano: int, subopcao: str):
        return {
            "produtos": [
                {
                    "pais": "Alemanha",
                    "quantidade_kg": 52297,
                    "valor_us": 30498
                },
            ],
            "total": {
                "quantidade": 1444578,
                "valor": 883886
            }
        }