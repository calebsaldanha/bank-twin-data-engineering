import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
engine = create_engine(os.environ.get("DATABASE_URL"))

def simulate_layer_2_refined():
    df_clientes = pd.read_sql("SELECT cliente_id, segmento, renda_declarada FROM clientes", engine)
    df_contas = pd.read_sql("SELECT conta_id, cliente_id FROM contas", engine)
    
    # 1. Limpar cartoes existentes para refazer a distribuicao
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM cartoes"))

    # 2. Nova Logica de Cartoes (Variabilidade)
    df_map = df_contas.merge(df_clientes, on='cliente_id')
    cartoes = []
    
    for _, row in df_map.iterrows():
        # Definir quantidade de cartoes (15% nenhum, 60% um, 20% dois, 5% tres)
        qtd = np.random.choice([0, 1, 2, 3], p=[0.15, 0.60, 0.20, 0.05])
        
        for _ in range(qtd):
            if row['segmento'] == 'Private': cat, lim = 'Infinite', 120000.0
            elif row['segmento'] == 'Prime': cat, lim = 'Black', 60000.0
            elif row['segmento'] == 'Principal': cat, lim = 'Platinum', 18000.0
            else: cat, lim = 'Standard', 3000.0
            
            cartoes.append({
                'conta_id': row['conta_id'],
                'tipo_cartao': np.random.choice(['Debito', 'Multiplo'], p=[0.3, 0.7]),
                'categoria': cat,
                'limite_total': lim,
                'limite_disponivel': round(lim * np.random.uniform(0.1, 0.95), 2),
                'status': 'Ativo'
            })
            
    if cartoes:
        pd.DataFrame(cartoes).to_sql('cartoes', engine, if_exists='append', index=False, chunksize=5000)
    print(f"Refinamento de cartoes concluido: {len(cartoes)} gerados.")

from sqlalchemy import text
if __name__ == "__main__":
    simulate_layer_2_refined()
