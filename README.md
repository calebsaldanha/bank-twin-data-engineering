# Bank Digital Twin - Data Engineering and Marketing Attribution

Este repositorio contem a infraestrutura e a logica de simulacao para um Gemeo Digital Bancario. O projeto foi desenhado para gerar dados sinteticos de alta fidelidade, permitindo o desenvolvimento de modelos complexos de Data Science em um ambiente de banco digital.

## Objetivos do Projeto
- Atribuicao Multi-Click (MTA): Rastrear jornadas de marketing desde o clique anonimo (via dispositivo_id) ate a conversao e uso do produto.
- Realismo Transacional: Simular mais de 1 milhao de transacoes financeiras com variabilidade de comportamento por segmento (Massificado, Principal, Prime, Private).
- Ecossistema de Credito: Gerar contratos de emprestimos, financiamentos e fluxos de parcelas para estudos de risco e inadimplencia.

## Tecnologias Utilizadas
- Database: PostgreSQL (Docker)
- Engine de Dados: Python 3.x (SQLAlchemy, Pandas, Faker)
- Arquitetura: Ingestao em camadas (Layers) para garantir integridade referencial.

## Estrutura das Camadas (Data Layers)
1. Camada 1 (Dimensoes): Cadastro de clientes, mapeamento de dispositivos unicos e criacao de campanhas de marketing multicanal.
2. Camada 2 (Produtos): Abertura de contas, emissao de cartoes (variabilidade de 0 a 3 cartoes por cliente), posicoes de investimentos e contratos de credito.
3. Camada 3 (Fatos): Log de eventos de app (jornada de cliques) e transacoes de cartao de credito/debito com categorias MCC.

## Volumetria Final do Dataset
| Entidade | Volume de Registros |
| :--- | :--- |
| Clientes | 50.000 |
| Cartoes | 57.630 |
| Contratos de Credito | 19.306 |
| Parcelas de Credito | 57.918 |
| Transacoes de Cartao | 1.151.762 |
| Eventos de Marketing | 449.879 |

## Como Executar
1. Certifique-se de ter o Docker instalado e o banco de dados ativo.
2. Configure o arquivo .env com a DATABASE_URL valida.
3. Execute o orquestrador de schema: python src/apply_schema.py.
4. Popule as camadas em ordem: python src/simulate_data_layer1.py, layer2, layer_credit e layer3.

---
Desenvolvido por Caleb Saldanha
Analista de Modelagem e Dados.
