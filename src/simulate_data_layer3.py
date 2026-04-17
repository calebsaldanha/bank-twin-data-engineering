import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import uuid

load_dotenv()
engine = create_engine(os.environ.get("DATABASE_URL"))

def simulate_layer_3():
    print("Iniciando Camada 3: Atribuicao Multi-Click e Transacional...")
    
    # Carregar dados necessarios
    df_clientes = pd.read_sql("SELECT cliente_id, segmento, data_cadastro FROM clientes", engine)
    df_dispositivos = pd.read_sql("SELECT dispositivo_id, cliente_id FROM sessoes_dispositivos", engine)
    df_campanhas = pd.read_sql("SELECT campanha_id FROM campanhas_marketing", engine)
    df_cartoes = pd.read_sql("SELECT cartao_id, conta_id FROM cartoes", engine)
    
    if df_clientes.empty or df_campanhas.empty:
        print("Erro: Faltam dados das camadas anteriores.")
        return

    # --- A. EVENTOS DE MARKETING (Jornada Multi-Click) ---
    eventos = []
    print("Gerando jornadas de marketing pre-conversao...")
    
    for _, row in df_clientes.iterrows():
        d_id = df_dispositivos[df_dispositivos['cliente_id'] == row['cliente_id']]['dispositivo_id'].iloc[0]
        data_conv = row['data_cadastro']
        
        # Gerar de 2 a 5 cliques antes da conta
        num_cliques = np.random.randint(2, 6)
        for i in range(num_cliques):
            sessao = str(uuid.uuid4())
            # Cliques ocorrem entre 1 e 15 dias antes da conversao
            data_clique = data_conv - timedelta(days=np.random.randint(1, 15), minutes=np.random.randint(0, 1440))
            
            eventos.append({
                'dispositivo_id': d_id,
                'cliente_id': None, # Ainda nao era cliente no clique
                'campanha_id': int(df_campanhas.sample(1)['campanha_id'].iloc[0]),
                'sessao_id': sessao,
                'tipo_evento': 'click_ad',
                'data_evento': data_clique,
                'metadados': '{"canal_origem": "paid_media"}'
            })
            
        # Evento de Login Pos-Conversao
        eventos.append({
            'dispositivo_id': d_id,
            'cliente_id': row['cliente_id'],
            'campanha_id': None,
            'sessao_id': str(uuid.uuid4()),
            'tipo_evento': 'app_login',
            'data_evento': data_conv + timedelta(hours=1),
            'metadados': '{"status": "first_access"}'
        })

    pd.DataFrame(eventos).to_sql('eventos_app', engine, if_exists='append', index=False)

    # --- B. TRANSAÇÕES DE CARTÃO (Consumo) ---
    transacoes = []
    mccs = ['Alimentacao', 'Transporte', 'Lazer', 'Saude', 'Servicos', 'Viagens']
    print("Gerando transacoes financeiras...")

    for _, row in df_cartoes.iterrows():
        # Recuperar segmento do cliente dono da conta
        # Simplificando: clientes private gastam mais
        num_tx = np.random.randint(10, 31)
        for _ in range(num_tx):
            valor = round(np.random.exponential(150.0), 2)
            transacoes.append({
                'cartao_id': row['cartao_id'],
                'data_transacao': datetime.now() - timedelta(days=np.random.randint(0, 30)),
                'valor': valor,
                'estabelecimento': 'Estabelecimento ' + str(np.random.randint(1, 500)),
                'mcc_grupo': np.random.choice(mccs),
                'tipo_transacao': np.random.choice(['Presencial', 'E-commerce'], p=[0.6, 0.4])
            })
            
    pd.DataFrame(transacoes).to_sql('transacoes_cartao', engine, if_exists='append', index=False)
    print(f"Sucesso: {len(eventos)} eventos e {len(transacoes)} transacoes criadas.")

if __name__ == "__main__":
    simulate_layer_3()
