const databaseSchema = {
    'campanhas_marketing': {
        desc: 'Registro de investimentos e canais de marketing.',
        columns: [
            { name: 'campanha_id', type: 'SERIAL (PK)', desc: 'ID único da campanha.' },
            { name: 'nome_campanha', type: 'VARCHAR(100)', desc: 'Nome descritivo da ação.' },
            { name: 'objetivo', type: 'VARCHAR(50)', desc: 'Objetivo macro da campanha.' },
            { name: 'canal', type: 'VARCHAR(50)', desc: 'Origem da mídia (Google, Meta).' },
            { name: 'custo_clique_estimado', type: 'DECIMAL(10,4)', desc: 'CPC médio simulado.' },
            { name: 'data_inicio', type: 'DATE', desc: 'Data de início.' }
        ]
    },
    'clientes': {
        desc: 'Cadastro mestre de clientes e segmentação.',
        columns: [
            { name: 'cliente_id', type: 'SERIAL (PK)', desc: 'ID único.' },
            { name: 'nome', type: 'VARCHAR(100)', desc: 'Nome do cliente.' },
            { name: 'cpf', type: 'VARCHAR(14)', desc: 'Documento único.' },
            { name: 'data_nascimento', type: 'DATE', desc: 'Data de nascimento.' },
            { name: 'renda_declarada', type: 'DECIMAL(15,2)', desc: 'Renda informada no cadastro.' },
            { name: 'segmento', type: 'VARCHAR(20)', desc: 'Private, Prime, Principal, Massificado.' },
            { name: 'behavior_score', type: 'INTEGER', desc: 'Score comportamental interno.' },
            { name: 'data_cadastro', type: 'TIMESTAMP', desc: 'Data de entrada.' }
        ]
    },
    'sessoes_dispositivos': {
        desc: 'Hardware para atribuição digital (MTA).',
        columns: [
            { name: 'dispositivo_id', type: 'UUID (PK)', desc: 'ID único do hardware.' },
            { name: 'cliente_id', type: 'INTEGER (FK)', desc: 'Cliente dono do dispositivo.' },
            { name: 'os', type: 'VARCHAR(20)', desc: 'Sistema Android/iOS.' },
            { name: 'modelo_aparelho', type: 'VARCHAR(50)', desc: 'Fabricante/Modelo do aparelho.' },
            { name: 'data_primeiro_acesso', type: 'TIMESTAMP', desc: 'Primeiro registro do aparelho.' }
        ]
    },
    'contas': {
        desc: 'Relacionamento de contas e saldos.',
        columns: [
            { name: 'conta_id', type: 'SERIAL (PK)', desc: 'ID da conta corrente.' },
            { name: 'cliente_id', type: 'INTEGER (FK)', desc: 'Dono da conta.' },
            { name: 'tipo_conta', type: 'VARCHAR(20)', desc: 'Corrente, Pagamento, etc.' },
            { name: 'data_abertura', type: 'TIMESTAMP', desc: 'Data de abertura.' },
            { name: 'saldo_atual', type: 'DECIMAL(15,2)', desc: 'Liquidez momentânea.' },
            { name: 'status', type: 'VARCHAR(20)', desc: 'Ativa / Bloqueada.' }
        ]
    },
    'cartoes': {
        desc: 'Inventário de cartões e limites.',
        columns: [
            { name: 'cartao_id', type: 'SERIAL (PK)', desc: 'ID do cartão.' },
            { name: 'conta_id', type: 'INTEGER (FK)', desc: 'Conta atrelada.' },
            { name: 'tipo_cartao', type: 'VARCHAR(20)', desc: 'Débito ou Crédito.' },
            { name: 'categoria', type: 'VARCHAR(20)', desc: 'Infinite, Platinum, etc.' },
            { name: 'limite_total', type: 'DECIMAL(15,2)', desc: 'Limite aprovado total.' },
            { name: 'limite_disponivel', type: 'DECIMAL(15,2)', desc: 'Limite restante.' },
            { name: 'status', type: 'VARCHAR(20)', desc: 'Ativo / Cancelado.' }
        ]
    },
    'investimentos_posicao': {
        desc: 'Carteira de ativos e perfil de risco.',
        columns: [
            { name: 'investimento_id', type: 'SERIAL (PK)', desc: 'ID da posição.' },
            { name: 'cliente_id', type: 'INTEGER (FK)', desc: 'Investidor.' },
            { name: 'tipo_ativo', type: 'VARCHAR(50)', desc: 'CDB, Ações, FIIs.' },
            { name: 'valor_aplicado', type: 'DECIMAL(15,2)', desc: 'Montante original.' },
            { name: 'valor_atual', type: 'DECIMAL(15,2)', desc: 'Posição mercadológica.' },
            { name: 'perfil_risco', type: 'VARCHAR(20)', desc: 'Conservador, Arrojado, etc.' }
        ]
    },
    'eventos_app': {
        desc: 'Logs de telemetria e jornada Multi-Click.',
        columns: [
            { name: 'evento_id', type: 'SERIAL (PK)', desc: 'ID do log.' },
            { name: 'dispositivo_id', type: 'UUID (FK)', desc: 'Hardware que gerou a ação.' },
            { name: 'cliente_id', type: 'INTEGER (FK)', desc: 'Cliente associado.' },
            { name: 'campanha_id', type: 'INTEGER (FK)', desc: 'Ação de marketing vinculada.' },
            { name: 'sessao_id', type: 'UUID', desc: 'ID da sessão do usuário.' },
            { name: 'tipo_evento', type: 'VARCHAR(50)', desc: 'Tipo (click, login, view).' },
            { name: 'data_evento', type: 'TIMESTAMP', desc: 'Carimbo de tempo.' },
            { name: 'metadados', type: 'JSONB', desc: 'JSON adicional flexível.' }
        ]
    },
    'transacoes_cartao': {
        desc: 'Fatos transacionais categorizados por MCC.',
        columns: [
            { name: 'transacao_id', type: 'SERIAL (PK)', desc: 'ID do fato transacional.' },
            { name: 'cartao_id', type: 'INTEGER (FK)', desc: 'Cartão usado.' },
            { name: 'data_transacao', type: 'TIMESTAMP', desc: 'Data da compra.' },
            { name: 'valor', type: 'DECIMAL(15,2)', desc: 'Montante transacionado.' },
            { name: 'estabelecimento', type: 'VARCHAR(100)', desc: 'Local da compra.' },
            { name: 'mcc_grupo', type: 'VARCHAR(50)', desc: 'Categoria do gasto (Mercado, Lazer, etc).' },
            { name: 'tipo_transacao', type: 'VARCHAR(20)', desc: 'Online / Presencial.' }
        ]
    },
    'contratos_credito': {
        desc: 'Operações de crédito ativo e garantias.',
        columns: [
            { name: 'contrato_id', type: 'SERIAL (PK)', desc: 'ID do contrato.' },
            { name: 'conta_id', type: 'INTEGER (FK)', desc: 'Conta debitada.' },
            { name: 'tipo_produto', type: 'VARCHAR(50)', desc: 'Auto, Imob, Consignado.' },
            { name: 'valor_contratado', type: 'DECIMAL(15,2)', desc: 'Montante original.' },
            { name: 'taxa_juros_mes', type: 'DECIMAL(5,2)', desc: 'Taxa aplicada.' },
            { name: 'data_contratacao', type: 'DATE', desc: 'Data de assinatura.' }
        ]
    },
    'parcelas_credito': {
        desc: 'Aging de pagamentos e análise de atrasos.',
        columns: [
            { name: 'parcela_id', type: 'SERIAL (PK)', desc: 'ID da parcela.' },
            { name: 'contrato_id', type: 'INTEGER (FK)', desc: 'Contrato de origem.' },
            { name: 'numero_parcela', type: 'INTEGER', desc: 'Número da prestação (1/48, etc).' },
            { name: 'valor_parcela', type: 'DECIMAL(15,2)', desc: 'Valor devido.' },
            { name: 'data_vencimento', type: 'DATE', desc: 'Data limite.' },
            { name: 'data_pagamento', type: 'DATE', desc: 'Pagamento efetivo.' },
            { name: 'status_pagamento', type: 'VARCHAR(20)', desc: 'Pago / Atraso.' }
        ]
    },
    // NOVAS TABELAS: PIPELINE EXÓGENO
    'macroeconomia': {
        desc: 'Indicadores macroeconômicos oficiais (Selic, IPCA, Dólar).',
        columns: [
            { name: 'data', type: 'DATE (PK)', desc: 'Data de referência da medição.' },
            { name: 'selic_meta', type: 'DECIMAL(5,2)', desc: 'Taxa Selic Meta anual.' },
            { name: 'selic_diaria', type: 'DECIMAL(8,6)', desc: 'Taxa Selic Diária convertida.' },
            { name: 'ipca_mensal', type: 'DECIMAL(5,2)', desc: 'Variação mensal do IPCA.' },
            { name: 'ipca_acumulado', type: 'DECIMAL(5,2)', desc: 'IPCA acumulado últimos 12 meses.' },
            { name: 'usd_ptax_compra', type: 'DECIMAL(10,4)', desc: 'Cotação de compra USD PTAX (Bacen).' },
            { name: 'usd_ptax_venda', type: 'DECIMAL(10,4)', desc: 'Cotação de venda USD PTAX (Bacen).' }
        ]
    },
    'feriados': {
        desc: 'Calendário de Feriados e Sazonalidades.',
        columns: [
            { name: 'data', type: 'DATE (PK)', desc: 'Data do evento/feriado.' },
            { name: 'nome', type: 'VARCHAR(100)', desc: 'Nome ou descrição do feriado.' },
            { name: 'tipo', type: 'VARCHAR(50)', desc: 'Nacional, Estadual ou Bancário.' }
        ]
    },
    'google_trends': {
        desc: 'Tendências de buscas relativas ao mercado financeiro.',
        columns: [
            { name: 'data', type: 'DATE (PK)', desc: 'Data de referência da coleta.' },
            { name: 'termo_busca', type: 'VARCHAR(100)', desc: 'Termo (ex: financiamento, desemprego).' },
            { name: 'indice', type: 'INTEGER', desc: 'Índice de popularidade (0-100).' }
        ]
    }
};

function loadTable(tableName) {
    const table = databaseSchema[tableName];
    if (!table) return;
    
    // Verifica se a tabela pertence ao schema exogenas ou public
    const schemaName = ['macroeconomia', 'feriados', 'google_trends'].includes(tableName) ? 'exogenas' : 'public';
    
    document.getElementById('table-title').innerText = `${schemaName}.${tableName}`;
    document.getElementById('table-desc').innerText = table.desc;
    
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = table.columns.map(col => `
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
            <td style="padding: 10px; font-weight: 600;">${col.name}</td>
            <td style="padding: 10px; font-family: monospace; font-size: 0.85rem; color: var(--accent);">${col.type}</td>
            <td style="padding: 10px; font-size: 0.9rem; color: var(--text-muted);">${col.desc}</td>
        </tr>
    `).join('');
}

document.addEventListener('DOMContentLoaded', () => {
    // Carrega uma tabela padrão ao abrir o site
    loadTable('clientes');
    
    // Configura Botões de Artigos
    document.querySelectorAll('.read-more-btn').forEach(btn => {
        btn.onclick = () => {
            document.querySelector('.articles-grid').style.display = 'none';
            document.getElementById('article1').style.display = 'block';
        };
    });
    
    document.querySelectorAll('.close-article').forEach(btn => {
        btn.onclick = () => {
            document.getElementById('article1').style.display = 'none';
            document.querySelector('.articles-grid').style.display = 'grid';
        };
    });

    // Configura Modais
    document.querySelectorAll('.open-modal-btn').forEach(btn => {
        btn.onclick = () => { 
            const modal = document.getElementById(btn.dataset.modal);
            if (modal) modal.style.display = 'flex'; 
        };
    });
    
    document.querySelectorAll('.close-modal-btn').forEach(btn => {
        btn.onclick = () => { btn.closest('.modal-overlay').style.display = 'none'; };
    });
});
