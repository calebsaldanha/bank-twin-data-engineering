-- ==============================================================================
-- 1. DADOS MESTRES E CADASTRO (CLIENTES)
-- ==============================================================================
CREATE TABLE clientes (
    cliente_id SERIAL PRIMARY KEY,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    renda_declarada DECIMAL(15, 2),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    segmento VARCHAR(20) CHECK (segmento IN ('Massificado', 'Principal', 'Prime', 'Private')),
    behavior_score INT, -- Score interno atualizado mensalmente (0 a 1000)
    data_abertura_conta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- 2. CONTAS CORRENTES E TRANSAÇÕES
-- ==============================================================================
CREATE TABLE contas (
    conta_id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(cliente_id),
    saldo_atual DECIMAL(15, 2) DEFAULT 0.00,
    limite_cheque_especial DECIMAL(15, 2) DEFAULT 0.00, -- Limite de Crédito da Conta (Lime)
    status VARCHAR(20) DEFAULT 'Ativa'
);

CREATE TABLE transacoes_conta (
    transacao_id SERIAL PRIMARY KEY,
    conta_id INT REFERENCES contas(conta_id),
    data_hora TIMESTAMP NOT NULL,
    valor DECIMAL(15, 2) NOT NULL,
    tipo_transacao VARCHAR(50), -- Ex: PIX_IN, PIX_OUT, TED, BOLETO, DEBITO
    localidade_cidade VARCHAR(100),
    localidade_estado VARCHAR(2),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    dispositivo_origem VARCHAR(50) -- Ex: App iOS, App Android, Web Banking
);

-- ==============================================================================
-- 3. CRÉDITO, EMPRÉSTIMOS E RENEGOCIAÇÃO (LENDING)
-- ==============================================================================
CREATE TABLE contratos_credito (
    contrato_id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(cliente_id),
    tipo_produto VARCHAR(50), 
    -- Ex: 'CredPessoal', 'CredConsignado', 'CredAuto', 'CredImob', 'AntecipaFGTS', 'ChequeEspecial_Lim'
    valor_financiado DECIMAL(15, 2) NOT NULL,
    taxa_juros_mensal DECIMAL(5, 4) NOT NULL,
    prazo_meses INT NOT NULL,
    data_contratacao TIMESTAMP NOT NULL,
    status VARCHAR(30) -- 'Ativo', 'Quitado', 'Inadimplente', 'Renegociado'
);

CREATE TABLE parcelas_credito (
    parcela_id SERIAL PRIMARY KEY,
    contrato_id INT REFERENCES contratos_credito(contrato_id),
    numero_parcela INT NOT NULL,
    data_vencimento DATE NOT NULL,
    data_pagamento DATE,
    valor_parcela DECIMAL(15, 2) NOT NULL,
    dias_atraso INT DEFAULT 0
);

CREATE TABLE reorganizacao_renegociacao (
    renegociacao_id SERIAL PRIMARY KEY,
    contrato_original_id INT REFERENCES contratos_credito(contrato_id),
    novo_contrato_id INT REFERENCES contratos_credito(contrato_id),
    data_hora TIMESTAMP NOT NULL,
    desconto_principal DECIMAL(15, 2) DEFAULT 0.00,
    desconto_juros DECIMAL(15, 2) DEFAULT 0.00,
    valor_total_renegociado DECIMAL(15, 2) NOT NULL,
    status_acordo VARCHAR(30) -- 'Promessa_Pagamento', 'Quebra_Acordo', 'Efetivado'
);

-- ==============================================================================
-- 4. MARKETING, GROWTH E AQUISIÇÃO
-- ==============================================================================
CREATE TABLE campanhas_marketing (
    campanha_id SERIAL PRIMARY KEY,
    nome_campanha VARCHAR(200),
    canal VARCHAR(50), -- Ex: 'Web_Search', 'Meta_Ads', 'TikTok', 'Email_CRM', 'App_Push', 'TV_Off', 'Agencia_Off'
    produto_alvo VARCHAR(50), -- Ex: 'CredPessoal', 'Cartao_Prime', 'Renegociacao'
    investimento_diario DECIMAL(15, 2),
    data_inicio DATE NOT NULL,
    data_fim DATE
);

CREATE TABLE interacoes_campanha (
    interacao_id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(cliente_id), -- Pode ser NULL se for lead não logado
    campanha_id INT REFERENCES campanhas_marketing(campanha_id),
    data_hora TIMESTAMP NOT NULL,
    tipo_interacao VARCHAR(30), -- 'Impressao', 'Clique', 'Conversao_Offline'
    custo_estimado DECIMAL(10, 4)
);

-- ==============================================================================
-- 5. NAVEGAÇÃO E TELEMETRIA (APP E WEB)
-- ==============================================================================
CREATE TABLE eventos_navegacao (
    evento_id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(cliente_id),
    session_id VARCHAR(100) NOT NULL,
    plataforma VARCHAR(20), -- 'App_iOS', 'App_Android', 'Web_Desktop', 'Web_Mobile'
    data_hora TIMESTAMP NOT NULL,
    produto_contexto VARCHAR(50), -- A tela que o usuário está (Ex: 'CredPessoal', 'Renegociacao', 'Cartao_Alta_Renda')
    evento_nome VARCHAR(100), 
    -- Nomenclaturas Específicas:
    -- 'view_tela_limites', 'click_banner_emprestimo', 'scroll_oferta_renegociacao'
    -- 'init_checkout_credito', 'simulate_tax_auto', 'error_validation_renda'
    -- 'click_botao_contratar', 'success_proposal'
    tempo_tela_segundos INT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8)
);
