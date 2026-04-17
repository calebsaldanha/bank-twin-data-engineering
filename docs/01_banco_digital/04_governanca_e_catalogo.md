# Tarefa 4: Estratégia de Catálogo de Dados e Metadados

## O Problema
Em ecossistemas com múltiplos domínios (Finanças, Esportes, Saúde), a descoberta de dados torna-se um gargalo. Cientistas de Dados gastam 80% do tempo entendendo o que cada coluna significa.

## A Solução
Implementação de um **Data Catalog** integrado ao portfólio. Inspirado em ferramentas como o Google Cloud Dataplex, este catálogo serve como a interface de entrada para qualquer análise técnica.

## Componentes do Catálogo
1. **Dicionário de Dados Operacional:** Descrição técnica de cada coluna, tipo de dado (Integer, Float, String) e restrições (Primary Key, Foreign Key).
2. **Linhagem de Dados (Data Lineage):** Mapeamento de como o dado flui da simulação em Python (`simulate_data.py`) até as tabelas finais no PostgreSQL.
3. **Data Quality Score:** Indicadores de preenchimento (null rate) e validade estatística.
4. **Data Preview & Sandbox:** Interface interativa para visualização de amostras reais e execução de consultas SQL exploratórias via navegador.

## Valor para o Negócio (Stakeholders)
O catálogo reduz o tempo de *Onboarding* de novos analistas e garante que as métricas de negócio (ex: o que é considerado um 'Atraso de Crédito') sejam consistentes em todos os dashboards e modelos.
