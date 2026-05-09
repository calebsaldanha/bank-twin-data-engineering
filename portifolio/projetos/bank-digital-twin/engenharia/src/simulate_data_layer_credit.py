import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
engine = create_engine(os.environ.get("DATABASE_URL"))

def simulate_credit():
    df_clientes = pd.read_sql("SELECT cliente_id, segmento, renda_declarada FROM clientes", engine)
    df_contas = pd.read_sql("SELECT conta_id, cliente_id FROM contas", engine)
    df_map = df_contas.merge(df_clientes, on='cliente_id')
    
    contratos = []
    parcelas = []
    
    print("Gerando contratos de credito diversificados...")
    
    for _, row in df_map.iterrows():
        # Probabilidade de ter credito baseada no segmento
        prob = {'Massificado': 0.3, 'Principal': 0.5, 'Prime': 0.4, 'Private': 0.2}
        if np.random.random() > prob[row['segmento']]:
            continue
            
        # Definir produto por segmento
        if row['segmento'] in ['Private', 'Prime']:
            produto = np.random.choice(['Imobiliario', 'Auto', 'Pessoal'], p=[0.4, 0.4, 0.2])
        else:
            produto = np.random.choice(['Consignado', 'Pessoal', 'Auto'], p=[0.5, 0.4, 0.1])
            
        valor = float(row['renda_declarada']) * np.random.randint(5, 50)
        taxa = np.random.uniform(0.8, 3.5)
        data_c = datetime.now().date() - timedelta(days=np.random.randint(30, 365))
        
        contratos.append({
            'conta_id': row['conta_id'],
            'tipo_produto': produto,
            'valor_contratado': round(valor, 2),
            'taxa_juros_mes': round(taxa, 2),
            'data_contratacao': data_c
        })

    df_contratos = pd.DataFrame(contratos)
    df_contratos.to_sql('contratos_credito', engine, if_exists='append', index=False)
    
    # Gerar parcelas para os contratos criados
    df_c_db = pd.read_sql("SELECT contrato_id, valor_contratado, data_contratacao FROM contratos_credito", engine)
    for _, c in df_c_db.iterrows():
        num_p = np.random.choice([12, 24, 48, 360])
        val_p = float(c['valor_contratado']) / num_p
        
        for p in range(1, 4): # Gerar as primeiras 3 parcelas para teste
            data_v = c['data_contratacao'] + timedelta(days=30*p)
            parcelas.append({
                'contrato_id': c['contrato_id'],
                'numero_parcela': p,
                'valor_parcela': round(val_p, 2),
                'data_vencimento': data_v,
                'data_pagamento': data_v if np.random.random() > 0.1 else None,
                'status_pagamento': 'Pago' if np.random.random() > 0.1 else 'Atraso'
            })
            
    pd.DataFrame(parcelas).to_sql('parcelas_credito', engine, if_exists='append', index=False, chunksize=5000)
    print(f"Credito concluido: {len(contratos)} contratos gerados.")

if __name__ == "__main__":
    simulate_credit()
