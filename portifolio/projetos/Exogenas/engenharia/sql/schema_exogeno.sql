-- Criação do Schema isolado para garantir governança
CREATE SCHEMA IF NOT EXISTS exogenas;

-- Tabela Macroeconômica (Granularidade Mensal/Diária)
CREATE TABLE IF NOT EXISTS exogenas.macroeconomia (
    data DATE PRIMARY KEY,
    selic_meta DECIMAL(5,2),
    ipca_mensal DECIMAL(5,2),
    ibc_br DECIMAL(10,2),
    usd_brl_fechamento DECIMAL(5,4)
);

-- Tabela de Feriados (Granularidade Diária)
CREATE TABLE IF NOT EXISTS exogenas.feriados (
    data DATE PRIMARY KEY,
    nome_feriado VARCHAR(100),
    tipo VARCHAR(50) -- Nacional, Estadual, Facultativo
);

-- Tabela de Comportamento/Busca (Granularidade Semanal/Diária)
CREATE TABLE IF NOT EXISTS exogenas.google_trends (
    data DATE,
    termo_busca VARCHAR(100),
    indice_volume INTEGER,
    PRIMARY KEY (data, termo_busca)
);
