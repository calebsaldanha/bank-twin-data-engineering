import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
engine = create_engine(os.environ.get("DATABASE_URL"))

def simulate_layer_2():
    print("Iniciando Camada 2: Gerando Contas, Cartoes e Investimentos...")
    
    # Carregar clientes existentes
    df_clientes = pd.read_sql("SELECT cliente_id, segmento, renda_declarada FROM clientes", engine)
    
    if df_clientes.empty:
        print("Erro: Nenhum cliente encontrado. Rode a Camada 1 primeiro.")
        return

    # --- A. GERAR CONTAS ---
    contas = []
    for _, row in df_clientes.iterrows():
        contas.append({
            'cliente_id': row['cliente_id'],
            'tipo_conta': 'Corrente',
            'data_abertura': datetime.now() - timedelta(days=np.random.randint(30, 730)),
            'saldo_atual': round(np.random.uniform(0, float(row['renda_declarada']) * 2), 2),
            'status': 'Ativa'
        })
    df_contas_final = pd.DataFrame(contas)
    df_contas_final.to_sql('contas', engine, if_exists='append', index=False)
    
    # Recuperar IDs de contas para vincular cartoes
    df_contas_db = pd.read_sql("SELECT conta_id, cliente_id FROM contas", engine)
    df_map = df_contas_db.merge(df_clientes, on='cliente_id')

    # --- B. GERAR CARTÕES (Respeitando Segmento) ---
    cartoes = []
    for _, row in df_map.iterrows():
        # Lógica de Categoria por Segmento
        if row['segmento'] == 'Private': cat = 'Infinite'; lim = 100000.0
        elif row['segmento'] == 'Prime': cat = 'Black'; lim = 50000.0
        elif row['segmento'] == 'Principal': cat = 'Platinum'; lim = 15000.0
        else: cat = 'Standard'; lim = 2000.0
        
        cartoes.append({
            'conta_id': row['conta_id'],
            'tipo_cartao': 'Multiplo',
            'categoria': cat,
            'limite_total': lim,
            'limite_disponivel': round(lim * np.random.uniform(0.1, 0.9), 2),
            'status': 'Ativo'
        })
    pd.DataFrame(cartoes).to_sql('cartoes', engine, if_exists='append', index=False)

    # --- C. GERAR INVESTIMENTOS ---
    investimentos = []
    # Apenas 40% dos clientes investem (simulando realidade)
    for _, row in df_clientes.sample(frac=0.4).iterrows():
        perfil = np.random.choice(['Conservador', 'Moderado', 'Arrojado'], p=[0.5, 0.3, 0.2])
        tipo = np.random.choice(['Renda Fixa', 'Acoes', 'FIIs', 'Tesouro'], p=[0.6, 0.15, 0.1, 0.15])
        
        val_app = round(float(row['renda_declarada']) * np.random.uniform(1, 10), 2)
        investimentos.append({
            'cliente_id': row['cliente_id'],
            'tipo_ativo': tipo,
            'valor_aplicado': val_app,
            'valor_atual': round(val_app * np.random.uniform(0.95, 1.2), 2),
            'perfil_risco': perfil
        })
    pd.DataFrame(investimentos).to_sql('investimentos_posicao', engine, if_exists='append', index=False)

    print(f"Sucesso: {len(df_contas_final)} contas e {len(cartoes)} cartoes criados.")

if __name__ == "__main__":
    simulate_layer_2()
