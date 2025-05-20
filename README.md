
# Tech Challenge 1 - README.md provisório

Siga as instruções abaixo para configurar e executar o ambiente local.

## Instruções de Setup

### 1. Clonar o repositório
```bash
git clone https://github.com/djflucena/tech-challenge-1.git
cd tech-challenge-1/
```

### 2. Atualizar o repositório
```bash
git fetch origin
git pull origin main
```

### 3. Criar e ativar o ambiente virtual Python
```bash
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
```

### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

### 5. Construir e iniciar os containers Docker
```bash
docker-compose build --no-cache
docker-compose up -d
```

### 6. Aplicar migrações do banco de dados
```bash
alembic upgrade head
```

### 7. Acessar o banco de dados PostgreSQL
```bash
docker exec -it tech-challenge-1_db_1 psql -U postgres -d vitivinicultura
```

### 8. Comandos úteis no `psql`
Dentro do prompt do `psql`, você pode executar os seguintes comandos:

```sql
\dn \\ -- Listar esquemas

\dt vitivinicultura.* \\ -- Listar tabelas no esquema "vitivinicultura"

\dv vitivinicultura.* \\ -- Listar visões (views) no esquema "vitivinicultura"

\d+ vitivinicultura.* \\ -- Ver todas as tabelas, views, colunas e tipos no esquema "vitivinicultura"

```
