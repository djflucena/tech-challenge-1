
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



## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI**
- **Alembic** (para migrações de banco)
- **BeautifulSoup** (para web scraping)
- **Uvicorn** (servidor ASGI)
- **Unittest** (testes automatizados)
- **Requests** (para requisições HTTP)
- **Pydantic** (validação de dados)
- **PostgreSQL** (banco de dados relacional)
- **SQLAlchemy** (ORM)


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

* **Clone o repositório:**  

```bash
git clone https://github.com/djflucena/tech-challenge-1.git
cd tech-challenge-1/
```

## Modos de execução

### 1. 🐳 Execução com Docker

* **Construir e iniciar os containers Docker:**  

```bash
docker-compose build --no-cache
docker-compose up -d
```

### 2. 💻 Execução Local

1. **Criar e ativar ambiente virtual:**  

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

3. **Iniciar o PostgreSQL localmente**

* Garantir que DATABASE_URL aponte para o banco local  

4. **Aplicar migrações alembic:**

```bash
alembic upgrade head
```

5. **Executar a API:**

```bash
fastapi dev src/main.py
```

## Disponibilidade da API:

* 🚀 A API estará disponível em: http://127.0.0.1:8000  
* 📚 Documentação Swagger: http://127.0.0.1:8000/docs  


## 🧪 Testes

* Para rodar os testes automatizados:
```bash
python -m unittest
```

**Os testes cobrem:**

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


## 🔍 Acesso ao Banco de Dados

**É possível acessar o banco de dados tanto no ambiente **Dockerizado** quanto no **ambiente local**, dependendo de como a aplicação foi executada.**

### 1. 🐳 Banco de Dados no Docker

Se você estiver rodando com Docker, o PostgreSQL estará dentro do container. Para acessá-lo:  

```bash
docker exec -it tech-challenge-1_db_1 psql -U postgres -d vitivinicultura
```

### 2. 💻 Banco de Dados Local

Se estiver rodando a aplicação localmente com um PostgreSQL instalado na máquina:  
* Conectar ao banco local (ajuste as credenciais conforme sua DATABASE_URL)  

```bash
psql -U seu_usuario -d vitivinicultura -h localhost -W
```

> Substitua `seu_usuario` pelo usuário correto configurado no seu PostgreSQL local.


### 🧰 Comandos úteis no `psql`

Após conectar ao banco, você pode usar os seguintes comandos para inspecionar a estrutura e os dados:  

```sql
\dn \\ -- Listar esquemas

\dt vitivinicultura.* \\ -- Listar tabelas no esquema "vitivinicultura"

\dv vitivinicultura.* \\ -- Listar visões (views) no esquema "vitivinicultura"

\d+ vitivinicultura.* \\ -- Ver todas as tabelas, views, colunas e tipos no esquema "vitivinicultura"
```

Esses comandos são úteis para validar a estrutura do banco, verificar registros e depurar problemas durante o desenvolvimento ou testes da API.
