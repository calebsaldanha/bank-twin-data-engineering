# Tarefa 1: Modelagem de Negócio e Esquema Relacional

## O Problema
Em um ambiente bancário real, os dados são altamente fragmentados. A equipe de Marketing olha para cliques, a de Risco olha para faturas, e a de Contas olha para saldos. O desafio desta etapa foi desenhar uma arquitetura de dados (Single Source of Truth) que unisse a jornada completa do cliente, permitindo rastrear o impacto de uma campanha de aquisição até a inadimplência futura.

## A Solução (Design do Banco)
Optamos por um modelo relacional robusto no PostgreSQL, utilizando o `cliente_id` como chave primária central. O ecossistema foi dividido em domínios:
1. **Domínio de Cadastro:** Tabela `clientes` com segmentação de renda (Massificado a Private).
2. **Domínio Transacional:** Tabelas `contas` e `transacoes_conta` para simular liquidez e uso de limites.
3. **Domínio de Crédito (Lending):** Tabelas `contratos_credito`, `parcelas_credito` e `reorganizacao_renegociacao` para mapear a esteira de risco, aging (dias de atraso) e quebras de acordo.
4. **Domínio de Growth:** Tabelas `campanhas_marketing`, `interacoes_campanha` e `eventos_navegacao` para telemetria de app e funil de mídia paga.

## Destaque Técnico
A separação granular entre `contratos` (a fotografia do empréstimo) e `parcelas` (o filme do pagamento) permite futuras modelagens de Análise de Sobrevivência (Survival Analysis) para prever em qual mês exato o cliente tende a entrar em default.
