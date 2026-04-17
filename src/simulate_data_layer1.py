import pandas as pd
import numpy as np
from faker import Faker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime, timedelta

load_dotenv()
fake = Faker('pt_BR')
engine = create_engine(os.environ.get("DATABASE_URL"))

def simulate_layer_1():
    print("Gerando Campanhas, Clientes e Dispositivos...")
    
    canais = ['Google Search', 'Meta Ads', 'LinkedIn', 'Email Marketing', 'YouTube']
    objetivos = ['Abertura Conta', 'Upgrade Cartao', 'Investimento', 'Credito Pessoal']
    
    campanhas = []
    for i in range(20):
        obj = np.random.choice(objetivos)
        campanhas.append({
            'nome_campanha': f"Campanha_{obj}_{i}",
            'objetivo': obj,
            'canal': np.random.choice(canais),
            'custo_clique_estimado': round(np.random.uniform(0.5, 5.0), 4),
            'data_inicio': fake.date_between(start_date='-1y', end_date='today')
        })
    pd.DataFrame(campanhas).to_sql('campanhas_marketing', engine, if_exists='append', index=False)
    
    clientes = []
    for _ in range(1000):
        renda = np.random.exponential(5000) + 1500
        if renda > 25000: segmento = 'Private'
        elif renda > 12000: segmento = 'Prime'
        elif renda > 5000: segmento = 'Principal'
        else: segmento = 'Massificado'
        
        clientes.append({
            'nome': fake.name(),
            'cpf': fake.cpf(),
            'data_nascimento': fake.date_of_birth(minimum_age=18, maximum_age=85),
            'renda_declarada': round(renda, 2),
            'segmento': segmento,
            'behavior_score': np.random.randint(300, 1000)
        })
    pd.DataFrame(clientes).to_sql('clientes', engine, if_exists='append', index=False)
    
    # Vinculando dispositivos
    ids_clientes = pd.read_sql("SELECT cliente_id FROM clientes", engine)['cliente_id'].tolist()
    dispositivos = [{
        'dispositivo_id': str(uuid.uuid4()),
        'cliente_id': c_id,
        'os': np.random.choice(['Android', 'iOS'], p=[0.7, 0.3]),
        'modelo_aparelho': fake.word(),
        'data_primeiro_acesso': datetime.now() - timedelta(days=np.random.randint(1, 365))
    } for c_id in ids_clientes]
    pd.DataFrame(dispositivos).to_sql('sessoes_dispositivos', engine, if_exists='append', index=False)
    
    print("Sucesso na Camada 1.")

if __name__ == "__main__":
    simulate_layer_1()
