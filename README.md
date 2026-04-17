# Bank Digital Twin - Data Engineering & Marketing Attribution

Este repositório contém a infraestrutura e a lógica de simulação para um **Gêmeo Digital Bancário**. O projeto foi desenhado para gerar dados sintéticos de alta fidelidade, permitindo o desenvolvimento de modelos complexos de Data Science em um ambiente de banco digital.

## ��� Objetivos do Projeto
- **Atribuição Multi-Click (MTA):** Rastrear jornadas de marketing desde o clique anônimo (via `dispositivo_id`) até a conversão e uso do produto.
- **Realismo Transacional:** Simular mais de 1 milhão de transações financeiras com variabilidade de comportamento por segmento (Massificado, Principal, Prime, Private).
- **Ecossistema de Crédito:** Gerar contratos de empréstimos, financiamentos e fluxos de parcelas para estudos de risco e inadimplência.

## ��� Tecnologias Utilizadas
- **Database:** PostgreSQL (rodando em Docker)
- **Engine de Dados:** Python 3.x (SQLAlchemy, Pandas, Faker)
- **Arquitetura:** Ingestão em camadas (Layers) para garantir integridade referencial.

## ���️ Estrutura das Camadas (Data Layers)
1. **Camada 1 (Dimensões):** Cadastro de clientes, mapeamento de dispositivos únicos e criação de campanhas de marketing multicanal.
2. **Camada 2 (Produtos):** Abertura de contas, emissão de cartões (variabilidade de 0 a 3 cartões por cliente), posições de investimentos e contratos de crédito.
3. **Camada 3 (Fatos):** Log de eventos de app (jornada de cliques) e transações de cartão de crédito/débito com categorias MCC.

## ��� Volumetria do Dataset
| Entidade | Volume |
| :--- | :--- |
| **Clientes** | 50.000 |
| **Transações** | +1.100.000 |
| **Eventos de Marketing** | +440.000 |
| **Contratos de Crédito** | +19.000 |
| **Investimentos** | 70% de penetração |

## ���️ Como Executar
1. Certifique-se de ter o Docker instalado.
2. Configure o arquivo `.env` com sua `DATABASE_URL`.
3. Suba o container: `docker-compose up -d`.
4. Execute o orquestrador de schema: `python src/apply_schema.py`.
5. Popule as camadas em ordem: `python src/simulate_data_layer1.py`, `layer2`, `layer_credit` e `layer3`.

---
**Desenvolvido por Caleb Saldanha** *Analista de Modelagem e Entusiasta de Data Science.*
