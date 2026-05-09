# Case Study: Bank Digital Twin & Big Data Simulation

Este projeto consiste no desenvolvimento de um motor de simulacao de dados bancarios de alta fidelidade, projetado para suportar o treinamento de modelos de Machine Learning, analises de risco de credito e modelos de atribuicao de marketing (MTA).

## Desafio de Engenharia
O principal desafio foi criar um ambiente que simulasse a complexidade de um banco real, saindo de modelos lineares para uma estrutura de dados densa e interdependente, garantindo integridade referencial em uma base de larga escala.

## Destaques Tecnicos
- Escalabilidade: Geracao de 50.000 clientes e mais de 1.1 milhao de transacoes financeiras.
- Variabilidade de Produto: Simulacao de distribuicao nao-linear de cartoes (0 a 3 por cliente) e produtos de credito diversificados.
- Atribuicao Multi-Click: Implementacao de logica de rastreio via dispositivo_id, permitindo unir eventos anonimos de marketing a conversoes de clientes.
- Integridade: Uso de SQLAlchemy e PostgreSQL com restricoes de Foreign Keys e integridade de dados financeiros.

## Metricas Finais do Dataset
- Clientes: 50.000
- Transacoes de Cartao: ~1.150.000
- Eventos de Marketing: ~450.000
- Contratos de Credito: ~19.000
- Penetracao de Investimentos: 70%

---
Desenvolvido por Caleb Saldanha
