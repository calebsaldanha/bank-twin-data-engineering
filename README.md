# Bank Digital Twin: Synthetic Data Engineering

Este repositorio contem a infraestrutura e os pipelines de simulacao em Python para a criacao de um "Gemeo Digital" bancario. O objetivo arquitetural e gerar um banco de dados relacional robusto populado com 50.000 clientes sinteticos e milhoes de eventos transacionais.

Diferente de geradores de dados aleatorios estaticos, este pipeline injeta vieses causais rigorosos (como a correlacao matematica entre segmento de renda, limites concedidos e probabilidade de inadimplencia temporal). Isso o torna a materia-prima ideal para o desenvolvimento de modelos de Data Science e Machine Learning.

## Stack Tecnologica
- Orquestracao e Infraestrutura: Docker, Docker Compose
- Banco de Dados: PostgreSQL 15
- Pipeline de Dados: Python 3.11 (Pandas, Numpy, SQLAlchemy, Faker)

## Arquitetura de Simulacao (3 Camadas)
Para garantir a integridade referencial, a injecao foi dividida em tres scripts sequenciais (src/):

1. Camada 1 (Dimensoes): simulate_data_layer1.py
2. Camada 2 (Lending & Accounts): simulate_data_layer2.py
3. Camada 3 (Fatos & Telemetria): simulate_data_layer3.py

## Como Replicar Localmente

### Passo 1: Configuracao de Seguranca (.env)
Renomeie o arquivo .env.example para .env e preencha com as suas credenciais locais do PostgreSQL.

### Passo 2: Subir a Infraestrutura (PostgreSQL)
    docker compose up -d

### Passo 3: Executar a Ingestao de Dados
    pip install pandas numpy sqlalchemy psycopg2-binary faker python-dotenv
    python src/simulate_data_layer1.py
    python src/simulate_data_layer2.py
    python src/simulate_data_layer3.py
