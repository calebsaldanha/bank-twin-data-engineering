import random
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

np.random.seed(42)

DATABASE_URL = "postgresql://caleb:adminpassword@127.0.0.1:5433/bank_twin"
engine = create_engine(DATABASE_URL)

def gerar_historico_credito():
    print("A simular Histórico de Pagamentos, Inadimplência e Renegociações...")
    
    # Carregar contratos e clientes para cruzar perfil de risco
    query = """
        SELECT c.contrato_id, c.cliente_id, c.tipo_produto, c.valor_financiado, c.prazo_meses, c.data_contratacao, cl.segmento
        FROM contratos_credito c
        JOIN clientes cl ON c.cliente_id = cl.cliente_id
    """
    df_contratos = pd.read_sql(query, engine)
    
    parcelas = []
    renegociacoes = []
    
    # Processamento iterativo otimizado
    for _, row in df_contratos.iterrows():
        # Definir probabilidade de atraso baseada no produto e segmento
        prob_atraso = 0.05
        if row['segmento'] == 'Massificado': prob_atraso += 0.15
        if row['tipo_produto'] == 'CredPessoal': prob_atraso += 0.10
        if row['tipo_produto'] == 'CredImob': prob_atraso -= 0.10
        prob_atraso = max(0.01, min(prob_atraso, 0.40))
        
        valor_parcela = row['valor_financiado'] / row['prazo_meses']
        
        # Simular os últimos 6 meses de parcelas (ou menos se contrato for recente)
        meses_ativos = min(6, row['prazo_meses'])
        
        for i in range(1, meses_ativos + 1):
            data_vencimento = row['data_contratacao'] + pd.DateOffset(months=i)
            if data_vencimento > datetime.now():
                break # Parcela no futuro
                
            is_atrasado = np.random.random() < prob_atraso
            dias_atraso = int(np.random.exponential(scale=30)) if is_atrasado else 0
            
            # Limitar atraso absurdo
            dias_atraso = min(dias_atraso, 300)
            
            data_pag = data_vencimento + timedelta(days=dias_atraso) if not (is_atrasado and dias_atraso > 90) else None
            
            parcelas.append({
                'contrato_id': row['contrato_id'],
                'numero_parcela': i,
                'data_vencimento': data_vencimento.date(),
                'data_pagamento': data_pag.date() if pd.notnull(data_pag) else None,
                'valor_parcela': round(valor_parcela, 2),
                'dias_atraso': dias_atraso
            })
            
            # Se atrasou muito, gera uma renegociação
            if dias_atraso > 60 and i == meses_ativos - 1:
                renegociacoes.append({
                    'contrato_original_id': row['contrato_id'],
                    'novo_contrato_id': None, # Simplificação temporal
                    'data_hora': datetime.now() - timedelta(days=random.randint(1, 30)),
                    'desconto_principal': round(row['valor_financiado'] * 0.1, 2),
                    'desconto_juros': 0.0,
                    'valor_total_renegociado': round(row['valor_financiado'] * 0.9, 2),
                    'status_acordo': np.random.choice(['Promessa_Pagamento', 'Quebra_Acordo', 'Efetivado'], p=[0.2, 0.3, 0.5])
                })

    print(f"A inserir {len(parcelas)} parcelas geradas...")
    pd.DataFrame(parcelas).to_sql('parcelas_credito', engine, if_exists='append', index=False, chunksize=20000)
    
    if renegociacoes:
        print(f"A inserir {len(renegociacoes)} eventos de renegociação...")
        pd.DataFrame(renegociacoes).to_sql('reorganizacao_renegociacao', engine, if_exists='append', index=False, chunksize=10000)

def gerar_eventos_app_marketing():
    print("A gerar Telemetria de App e Interações de Marketing...")
    
    df_clientes = pd.read_sql("SELECT cliente_id, segmento FROM clientes", engine)
    
    eventos = []
    
    # Simulando um recorte de sessões ativas para 30% da base (para não estourar a memória)
    clientes_ativos = df_clientes.sample(frac=0.30)
    
    for _, row in clientes_ativos.iterrows():
        n_eventos = np.random.randint(3, 15)
        session_id = f"sess_{row['cliente_id']}_{np.random.randint(1000,9999)}"
        plataforma = np.random.choice(['App_iOS', 'App_Android'])
        
        for _ in range(n_eventos):
            # Viés de navegação por segmento
            if row['segmento'] == 'Massificado':
                acoes = ['view_saldo', 'click_banner_emprestimo', 'simulate_tax_auto', 'init_checkout_credito', 'error_validation_renda']
                prob = [0.4, 0.2, 0.1, 0.1, 0.2]
            else:
                acoes = ['view_saldo', 'view_investimentos', 'click_cartao_black', 'transfer_pix_out']
                prob = [0.5, 0.3, 0.1, 0.1]
                
            evento = np.random.choice(acoes, p=prob)
            
            eventos.append({
                'cliente_id': row['cliente_id'],
                'session_id': session_id,
                'plataforma': plataforma,
                'data_hora': datetime.now() - timedelta(days=np.random.randint(1, 30), hours=np.random.randint(0, 23)),
                'produto_contexto': 'Geral' if 'view' in evento else 'Credito',
                'evento_nome': evento,
                'tempo_tela_segundos': np.random.randint(5, 120),
                'latitude': np.random.uniform(-23.6, -23.4), # Foco em SP/Barueri
                'longitude': np.random.uniform(-46.8, -46.6)
            })

    print(f"A inserir {len(eventos)} logs de navegação do App...")
    pd.DataFrame(eventos).to_sql('eventos_navegacao', engine, if_exists='append', index=False, chunksize=20000)

if __name__ == "__main__":
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE parcelas_credito CASCADE;"))
        conn.execute(text("TRUNCATE TABLE reorganizacao_renegociacao CASCADE;"))
        conn.execute(text("TRUNCATE TABLE eventos_navegacao CASCADE;"))
        
    gerar_historico_credito()
    gerar_eventos_app_marketing()
