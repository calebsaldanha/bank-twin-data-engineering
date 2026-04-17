# Tarefa 2: Orquestração de Infraestrutura com Docker

## O Problema
Instalar bancos de dados fisicamente no sistema operacional da máquina (bare-metal) gera problemas de dependências, conflitos de portas com projetos legados e dificulta a reprodutibilidade do projeto por outros desenvolvedores ou recrutadores.

## A Solução
Implementação de uma arquitetura baseada em contêineres utilizando **Docker** e **Docker Compose**.

## Implementação Técnica
* **Imagem Base:** Utilização da imagem oficial `postgres:15-alpine` por ser leve e otimizada.
* **Mapeamento de Portas:** O banco foi exposto intencionalmente na porta `5433` (e não na padrão `5432`) para mitigar conflitos com qualquer instância nativa do Windows operando no host local.
* **Persistência de Dados (Volumes):** Criação de um volume nomeado (`postgres_data`) para garantir que os 50.000 clientes e os milhões de registros gerados não sejam perdidos caso o contêiner seja reiniciado ou derrubado (`docker compose down`).
* **Automação:** O arquivo `schema_inicial.sql` foi mapeado via bind mount para a pasta de *entrypoint* do Docker, garantindo que as 9 tabelas sejam criadas automaticamente no instante em que o banco sobe pela primeira vez.
