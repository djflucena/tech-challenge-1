
# Tech Challenge 1

# API Pública de Vitivinicultura - Embrapa

Esta API pública tem como objetivo disponibilizar, em tempo real, os dados de vitivinicultura 
fornecidos pela Embrapa Uva e Vinho. Os dados abrangem as seguintes áreas:

- Produção e comercialização de vinhos e derivados
- Processamento - quantidade de uvas processadas
- Importação e exportação de derivados de uva


## Funcionalidades

- Consulta em tempo real dos dados de vitivinicultura
- API RESTful com endpoints padronizados
- Filtros por ano
- Respostas em formato JSON


## Tecnologias Utilizadas

- Python 3.11+
- FastAPI
- Alembic
- BeautifulSoup
- Uvicorn
- Unittest
- Requests
- Pydantic
- PostgreSQL
- SQLAlchemy


## Visão Geral do Projeto

### ⚙️ Funcionamento Geral da API

![API Vitivinicultura-visao-geral-2 drawio](https://github.com/user-attachments/assets/de8530e8-f041-4488-8d12-37a953d2de4f)

O funcionamento da API segue a seguinte lógica:

1. **Consulta primária ao site da Embrapa**  
   Ao receber uma requisição, a API tenta acessar o site da Embrapa para realizar a raspagem (_web scraping_) dos dados de vitivinicultura.

2. **Raspagem bem-sucedida**  
   Se a raspagem for concluída com sucesso:
   - Os dados extraídos são imediatamente retornados ao cliente solicitante.
   - Simultaneamente, a API tenta armazenar os dados em um banco de dados local, com o objetivo de manter uma cópia para eventuais usos futuros (mecanismo de _fallback_).

3. **Falha na raspagem — uso de fallback**  
   Caso ocorra uma falha na raspagem (por exemplo, indisponibilidade do site da Embrapa ou erro de rede):
   - A API busca os dados previamente armazenados no banco de dados.
     - **Se os dados estiverem disponíveis no banco:** eles são retornados ao cliente como resposta à requisição.
     - **Se os dados não estiverem disponíveis:** a API informa ao cliente que não foi possível recuperar os dados solicitados no momento.


## Arquitetura do Projeto

![API Vitivinicultura-arquitetura-3 drawio](https://github.com/user-attachments/assets/021ebbaf-a08a-49be-b798-bdd079e963e4)


## Estrutura do Projeto

Estrutura com os principais módulos e arquivos do projeto.

```
tech-challenge-1
├── alembic/
├── docker/
├── logs/
├── README.md
├── requirements.txt
├── src/
│   └── config/
│   └── filters/
│   └── raspagem/
│   └── respositories/
│   └── schemas/
│   └── services/
│   └── database.py
│   └── main.py
│   └── utils.py
└── tests/
    └── raspagens/
    └── services/

```

## Estrutura dos Principais Módulos

![API Vitivinicultura-heranca-classes-atualizada drawio](https://github.com/user-attachments/assets/d12f71c5-9a21-4d8d-885a-d7c8b636ee68)


## Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/djflucena/tech-challenge-1.git
cd tech-challenge-1/
```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

### 4. Construa e inicie os containers Docker
```bash
docker-compose build --no-cache
docker-compose up -d
```

### 6. Aplique as migrações do banco de dados
```bash
alembic upgrade head
```

## Execução

```bash
fastapi dev src/main.py
```
A API estará disponível em: http://127.0.0.1:8000

Documentação interativa (Swagger): http://127.0.0.1:8000/docs


## 🧪 Testes

Para rodar os testes automatizados:
```bash
python -m unittest
```

Os testes cobrem:

- Respostas dos endpoints
- Coleta e estruturação de dados da Embrapa
- Validação de erros e respostas inválidas


## Endpoints Principais

| Método | Rota                | Descrição                                                |
| ------ | ------------------- | -------------------------------------------------------- |
| GET    | `/producao/`        | Retorna dados de produção de vinhos, sucos e derivados   |
| GET    | `/processamento/`   | Dados sobre a quantidade de uvas processadas             |
| GET    | `/comercializacao/` | Dados de comercialização de vinhos, sucos e derivados    |
| GET    | `/importacao/`      | Dados de importação de derivados de uva                  |
| GET    | `/exportacao/`      | Dados de exportação de derivados de uva                  |


⚠️ As rotas aceitam filtros por ano.


## Acesso ao Banco de Dados

Seguem orientações para configuração e uso da base de dados PostgreSQL.

### Acessar o banco de dados PostgreSQL

Para acessar a instância do banco de dados PostgreSQL no container:

```bash
docker exec -it tech-challenge-1_db_1 psql -U postgres -d vitivinicultura
```

### Comandos úteis no `psql`

No prompt do `psql`, você pode executar os seguintes comandos:

```sql
\dn \\ -- Listar esquemas

\dt vitivinicultura.* \\ -- Listar tabelas no esquema "vitivinicultura"

\dv vitivinicultura.* \\ -- Listar visões (views) no esquema "vitivinicultura"

\d+ vitivinicultura.* \\ -- Ver todas as tabelas, views, colunas e tipos no esquema "vitivinicultura"

```

Esses comandos são úteis para inspecionar a estrutura do banco, validar dados e depurar problemas
durante o desenvolvimento da API.
