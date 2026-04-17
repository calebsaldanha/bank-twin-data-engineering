# Tarefa 3: Geração de Dados Sintéticos e Vieses Causais

## O Problema
Bancos de dados sintéticos tradicionais costumam gerar dados puramente aleatórios (ruído branco). Para estudos avançados de Machine Learning e Inferência Causal, é obrigatório que os dados contenham correlações reais (vieses estatísticos). Se o modelo não tiver sinal, ele não aprenderá nada.

## A Solução
Desenvolvimento de um pipeline em Python utilizando `Faker`, `Pandas` e `Numpy` dividido em 3 camadas de injeção de dados, garantindo a integridade referencial e o cruzamento estatístico das variáveis.

## Vieses (Biases) Programados na Base
Para simular a complexidade de um banco real, os seguintes cenários foram injetados nos dados:
1. **Viés de Risco vs. Segmento:** Clientes do segmento *Massificado* receberam uma probabilidade matematicamente superior de gerar atrasos (aging > 60 dias) em produtos de Crédito Pessoal, espelhando o risco real de mercado sem garantias.
2. **Viés de Engajamento Digital:** A telemetria da tabela `eventos_navegacao` foi roteada pelo perfil socioeconômico. Clientes *Prime/Private* geram mais logs de visualização de investimentos e uso de cartões premium, enquanto a base massificada gera mais cliques em banners de simulação de empréstimo e renegociação de dívidas.
3. **Escala e Vetorização:** O código foi otimizado para gerar 50.000 clientes e o respectivo histórico transacional (atingindo centenas de milhares de linhas) em poucos segundos, demonstrando eficiência em processamento de dados massivos.
