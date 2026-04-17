import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
engine = create_engine(os.environ.get("DATABASE_URL"))

def simulate_layer_2():
    df_clientes = pd.read_sql("SELECT cliente_id, segmento, renda_declarada FROM clientes", engine)
    
    # 1. Contas (100% dos clientes)
    contas = [{
        'cliente_id': row['cliente_id'],
        'tipo_conta': 'Corrente',
        'data_abertura': datetime.now() - timedelta(days=np.random.randint(10, 700)),
        'saldo_atual': round(np.random.uniform(0, float(row['renda_declarada']) * 1.5), 2),
        'status': 'Ativa'
    } for _, row in df_clientes.iterrows()]
    pd.DataFrame(contas).to_sql('contas', engine, if_exists='append', index=False, chunksize=5000)
    
    # 2. Cartoes (100% das contas)
    df_contas = pd.read_sql("SELECT conta_id, cliente_id FROM contas", engine)
    df_map = df_contas.merge(df_clientes, on='cliente_id')
    
    cartoes = []
    for _, row in df_map.iterrows():
        if row['segmento'] == 'Private': cat, lim = 'Infinite', 120000.0
        elif row['segmento'] == 'Prime': cat, lim = 'Black', 60000.0
        elif row['segmento'] == 'Principal': cat, lim = 'Platinum', 18000.0
        else: cat, lim = 'Standard', 3000.0
        
        cartoes.append({
            'conta_id': row['conta_id'],
            'tipo_cartao': 'Multiplo',
            'categoria': cat,
            'limite_total': lim,
            'limite_disponivel': round(lim * np.random.uniform(0.05, 0.95), 2),
            'status': 'Ativo'
        })
    pd.DataFrame(cartoes).to_sql('cartoes', engine, if_exists='append', index=False, chunksize=5000)

    # 3. Investimentos (70% de penetracao)
    invest_list = []
    for _, row in df_clientes.sample(frac=0.7).iterrows():
        perfil = np.random.choice(['Conservador', 'Moderado', 'Arrojado'], p=[0.4, 0.4, 0.2])
        tipo = np.random.choice(['Renda Fixa', 'Acoes', 'FIIs', 'Tesouro'], p=[0.5, 0.2, 0.15, 0.15])
        val_app = round(float(row['renda_declarada']) * np.random.uniform(2, 20), 2)
        invest_list.append({
            'cliente_id': row['cliente_id'],
            'tipo_ativo': tipo,
            'valor_aplicado': val_app,
            'valor_atual': round(val_app * np.random.uniform(0.9, 1.3), 2),
            'perfil_risco': perfil
        })
    pd.DataFrame(invest_list).to_sql('investimentos_posicao', engine, if_exists='append', index=False, chunksize=5000)
    print("Camada 2 concluida.")

if __name__ == "__main__":
    simulate_layer_2()
