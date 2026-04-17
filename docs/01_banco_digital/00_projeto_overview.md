# Gêmeo Digital Bancário: Arquitetura e Engenharia de Dados Sintéticos

## 1. Definição do Escopo
O projeto visa criar um ecossistema de dados completo que simula a operação de uma grande instituição financeira brasileira. O objetivo é fornecer uma base rica e correlacionada para estudos de **Ciência de Dados, Inferência Causal e Modelagem de Risco**.

### Áreas Cobertas:
* **Cadastro:** Dados demográficos e segmentação (Massificado, Principal, Prime, Private).
* **Core Banking:** Contas correntes e transacional (PIX, TED, limites de crédito).
* **Lending (Crédito):** Contratos de Empréstimo Pessoal, Auto, Imobiliário e Antecipação de FGTS.
* **Cobrança/Renegociação:** Ciclo de atraso, renegociações e acordos.
* **Marketing & Growth:** Campanhas multicanal (Meta, TikTok, Google) e telemetria de navegação no App.

## 2. Escolha e Metodologia de Dados
Para garantir veracidade analítica, a geração de dados (50.000 clientes) não foi aleatória, mas baseada em **vieses estatísticos (Biases)**:
* **Correlação Renda-Segmento:** Limites de crédito e saldos são proporcionais à renda e ao segmento.
* **Vieses de Risco:** Probabilidades de inadimplência maiores no segmento Massificado e em produtos de crédito pessoal sem garantia.
* **Telemetria Comportamental:** Logs de navegação variam conforme o interesse do segmento (ex: Prime foca em Investimentos, Massificado em Crédito/Renegociação).

## 3. Stack Tecnológica
* **Infraestrutura:** Docker Desktop (Isolamento de ambiente).
* **Banco de Dados:** PostgreSQL 15 (Motor relacional).
* **Linguagem:** Python 3.11.
* **Bibliotecas Principais:**
    * `SQLAlchemy`: ORM e gestão de conexões.
    * `Pandas` & `Numpy`: Vetorização e manipulação massiva de dados.
    * `Faker`: Geração de entidades brasileiras realistas (CPF, nomes, cidades).

## 4. Dicionário de Tabelas (Esquema Relacional)
O banco está estruturado em 9 tabelas principais:
1.  `clientes`: Dados mestre e score comportamental.
2.  `contas`: Saldos e limites de Cheque Especial (Lime).
3.  `transacoes_conta`: Histórico de movimentações com geolocalização.
4.  `contratos_credito`: Detalhes de taxas, prazos e produtos contratados.
5.  `parcelas_credito`: Fluxo de pagamentos e dias de atraso (Aging).
6.  `reorganizacao_renegociacao`: Acordos de dívidas e quebras de promessa.
7.  `campanhas_marketing`: Investimentos e canais de aquisição.
8.  `interacoes_campanha`: Cliques e impressões vinculados a clientes.
9.  `eventos_navegacao`: Logs de botões e telas acessadas no App.

## 5. Método de Criação
A base foi construída em um pipeline de 3 camadas:
* **Camada 1 (Dimensões):** Criação de entidades independentes.
* **Camada 2 (Contratos):** Vinculação de produtos financeiros aos clientes.
* **Camada 3 (Eventos):** Geração de fatos temporais (pagamentos e cliques) com milhões de registros.
