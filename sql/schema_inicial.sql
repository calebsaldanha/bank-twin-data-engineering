DROP TABLE IF EXISTS transacoes_cartao;
DROP TABLE IF EXISTS parcelas_credito;
DROP TABLE IF EXISTS contratos_credito;
DROP TABLE IF EXISTS investimentos_posicao;
DROP TABLE IF EXISTS cartoes;
DROP TABLE IF EXISTS eventos_app;
DROP TABLE IF EXISTS contas;
DROP TABLE IF EXISTS sessoes_dispositivos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS campanhas_marketing;

CREATE TABLE campanhas_marketing (
    campanha_id SERIAL PRIMARY KEY,
    nome_campanha VARCHAR(100),
    objetivo VARCHAR(50), 
    canal VARCHAR(50),   
    custo_clique_estimado DECIMAL(10,4),
    data_inicio DATE
);

CREATE TABLE clientes (
    cliente_id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    cpf VARCHAR(14) UNIQUE,
    data_nascimento DATE,
    renda_declarada DECIMAL(15,2),
    segmento VARCHAR(20), 
    behavior_score INTEGER,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessoes_dispositivos (
    dispositivo_id UUID PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(cliente_id),
    os VARCHAR(20), 
    modelo_aparelho VARCHAR(50),
    data_primeiro_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contas (
    conta_id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(cliente_id),
    tipo_conta VARCHAR(20),
    data_abertura TIMESTAMP,
    saldo_atual DECIMAL(15,2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'Ativa'
);

CREATE TABLE cartoes (
    cartao_id SERIAL PRIMARY KEY,
    conta_id INTEGER REFERENCES contas(conta_id),
    tipo_cartao VARCHAR(20), 
    categoria VARCHAR(20), 
    limite_total DECIMAL(15,2),
    limite_disponivel DECIMAL(15,2),
    status VARCHAR(20) DEFAULT 'Ativo'
);

CREATE TABLE investimentos_posicao (
    investimento_id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(cliente_id),
    tipo_ativo VARCHAR(50), 
    valor_aplicado DECIMAL(15,2),
    valor_atual DECIMAL(15,2),
    perfil_risco VARCHAR(20)
);

CREATE TABLE eventos_app (
    evento_id SERIAL PRIMARY KEY,
    dispositivo_id UUID REFERENCES sessoes_dispositivos(dispositivo_id),
    cliente_id INTEGER REFERENCES clientes(cliente_id),
    campanha_id INTEGER REFERENCES campanhas_marketing(campanha_id),
    sessao_id UUID,
    tipo_evento VARCHAR(50),
    data_evento TIMESTAMP,
    metadados JSONB
);

CREATE TABLE transacoes_cartao (
    transacao_id SERIAL PRIMARY KEY,
    cartao_id INTEGER REFERENCES cartoes(cartao_id),
    data_transacao TIMESTAMP,
    valor DECIMAL(15,2),
    estabelecimento VARCHAR(100),
    mcc_grupo VARCHAR(50)
);

CREATE TABLE contratos_credito (
    contrato_id SERIAL PRIMARY KEY,
    conta_id INTEGER REFERENCES contas(conta_id),
    tipo_produto VARCHAR(50),
    valor_contratado DECIMAL(15,2),
    taxa_juros_mes DECIMAL(5,2),
    data_contratacao DATE
);

CREATE TABLE parcelas_credito (
    parcela_id SERIAL PRIMARY KEY,
    contrato_id INTEGER REFERENCES contratos_credito(contrato_id),
    numero_parcela INTEGER,
    valor_parcela DECIMAL(15,2),
    data_vencimento DATE,
    data_pagamento DATE,
    status_pagamento VARCHAR(20)
);
