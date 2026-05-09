# Macroeconomic Data Pipeline (Central Data Hub)

Este repositório faz parte da arquitetura do meu **Central Data Hub**, atuando como o motor de ingestão de dados exógenos. Ele coleta, processa e armazena indicadores macroeconômicos e sazonalidades para alimentar modelos de **Data Science, Inferência Causal e Machine Learning**.

## Arquitetura e Fontes de Dados
O pipeline consome dados de APIs públicas e os consolida em um banco de dados PostgreSQL (`macro_db`), projetado para ser cruzado com dados transacionais privados via processos de ELT.

* **Banco Central do Brasil (BCB):** * Taxa Selic Meta (Série 432).
    * IPCA Mensal (Série 433).
    * *Regra de Negócio:* Para garantir resiliência e respeitar os limites de paginação da API do BCB, o pipeline extrai uma **janela móvel histórica dos últimos 5 anos** em cada execução.
* **Brasil API:**
    * Calendário de Feriados Nacionais.
    * *Regra de Negócio:* Atualização idempotente dos feriados do ano corrente e do ano anterior, evitando duplicidade de chaves primárias.

## Stack Tecnológico
* **Linguagem:** Python 3
* **Manipulação de Dados:** Pandas
* **Banco de Dados:** PostgreSQL (via Docker) e SQLAlchemy
* **Automação:** Windows Task Scheduler / Cron

## Configuração e Automação Local
A execução está automatizada para rodar diariamente em *batch*. O script `run_pipeline.bat` (ignorado no versionamento por questões de segurança) carrega as variáveis de ambiente com as credenciais do banco e invoca o ambiente virtual:

    DB_USER=seu_usuario
    DB_PASS=sua_senha
    DB_HOST=127.0.0.1
    DB_PORT=5433
    DB_NAME=macro_db

A automação é garantida via agendamento do sistema operacional (D-1), rodando silenciosamente nas madrugadas para atualizar o fechamento das taxas diárias.
