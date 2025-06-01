
# Tech Challenge 1

# API Pública de Vitivinicultura - Embrapa

Esta API pública tem como objetivo disponibilizar, em tempo real, os dados de vitivinicultura 
fornecidos pela Embrapa Uva e Vinho. Os dados abrangem as seguintes áreas:

- Produção e comercialização de vinhos e derivados
- Processamento - quantidade de uvas processadas
- Importação e exportação de derivados de uva


## 📌 Funcionalidades

- 🔍 Consulta em tempo real dos dados de vitivinicultura
- 📦 API RESTful com endpoints padronizados
- 📊 Filtros por ano
- 📁 Respostas em formato JSON


## 🚀 Tecnologias Utilizadas

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


## 📁 Estrutura do Projeto

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


## ⚙️ Instalação

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

## ▶️ Execução

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


## 📤 Endpoints Principais

| Método | Rota                | Descrição                                                |
| ------ | ------------------- | -------------------------------------------------------- |
| GET    | `/producao/`        | Retorna dados de produção de vinhos, sucos e derivados   |
| GET    | `/processamento/`   | Dados sobre a quantidade de uvas processadas             |
| GET    | `/comercializacao/` | Dados de comercialização de vinhos, sucos e derivados    |
| GET    | `/importacao/`      | Dados de importação de derivados de uva                  |
| GET    | `/exportacao/`      | Dados de exportação de derivados de uva                  |


⚠️ As rotas aceitam filtros por ano.


## 🗄️ Acesso ao Banco de Dados

Seguem orientações para configuração e uso da base de dados PostgreSQL.

### 🔐 Acessar o banco de dados PostgreSQL

Para acessar a instância do banco de dados PostgreSQL no container:

```bash
docker exec -it tech-challenge-1_db_1 psql -U postgres -d vitivinicultura
```

### 🛠️ Comandos úteis no `psql`

No prompt do `psql`, você pode executar os seguintes comandos:

```sql
\dn \\ -- Listar esquemas

\dt vitivinicultura.* \\ -- Listar tabelas no esquema "vitivinicultura"

\dv vitivinicultura.* \\ -- Listar visões (views) no esquema "vitivinicultura"

\d+ vitivinicultura.* \\ -- Ver todas as tabelas, views, colunas e tipos no esquema "vitivinicultura"

```

Esses comandos são úteis para inspecionar a estrutura do banco, validar dados e depurar problemas
durante o desenvolvimento da API.
