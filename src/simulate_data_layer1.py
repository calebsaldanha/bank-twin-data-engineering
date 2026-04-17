import pandas as pd
import numpy as np
from faker import Faker
from sqlalchemy import create_engine, text
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')
Faker.seed(42)
np.random.seed(42)

DATABASE_URL = "postgresql://caleb:adminpassword@127.0.0.1:5433/bank_twin"
engine = create_engine(DATABASE_URL)

def limpar_base_antiga():
    print("Limpando dados antigos de teste...")
    # Correção: O engine.begin() já gerencia a transação e o commit automaticamente
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE clientes CASCADE;"))
        conn.execute(text("TRUNCATE TABLE campanhas_marketing CASCADE;"))

def gerar_clientes(n=50000):
    print(f"A gerar {n} clientes sintéticos (Isso pode levar cerca de 30-60 segundos)...")
    clientes = []
    
    for _ in range(n):
        rand_renda = np.random.random()
        if rand_renda < 0.60:
            renda = round(np.random.uniform(1500, 5000), 2)
            segmento = 'Massificado'
        elif rand_renda < 0.85:
            renda = round(np.random.uniform(5001, 15000), 2)
            segmento = 'Principal'
        elif rand_renda < 0.98:
            renda = round(np.random.uniform(15001, 40000), 2)
            segmento = 'Prime'
        else:
            renda = round(np.random.uniform(40001, 150000), 2)
            segmento = 'Private'
            
        score_base = np.random.normal(loc=600, scale=150)
        if segmento in ['Prime', 'Private']:
            score_base += 100
        behavior_score = int(np.clip(score_base, 0, 1000))
        
        data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=80)
        dias_conta = random.randint(30, 1800)
        data_abertura = datetime.now() - timedelta(days=dias_conta)
        cpf = str(random.randint(10000000000, 99999999999))
        
        clientes.append({
            'cpf': cpf,
            'data_nascimento': data_nascimento,
            'renda_declarada': renda,
            'cidade': fake.city(),
            'estado': fake.estado_sigla(),
            'segmento': segmento,
            'behavior_score': behavior_score,
            'data_abertura_conta': data_abertura
        })
        
    df_clientes = pd.DataFrame(clientes)
    print("A inserir 50.000 clientes no PostgreSQL...")
    df_clientes.to_sql('clientes', engine, if_exists='append', index=False)
    print("Clientes inseridos com sucesso!")

def gerar_campanhas():
    print("A gerar histórico de campanhas de marketing...")
    produtos = ['CredPessoal', 'Cartao_Prime', 'Renegociacao', 'Conta_Massificado', 'CredAuto']
    canais = ['Meta_Ads', 'TikTok', 'Google_Search', 'Email_CRM', 'App_Push']
    campanhas = []
    
    for i in range(1, 51):
        canal = random.choice(canais)
        produto = random.choice(produtos)
        
        if canal in ['Meta_Ads', 'Google_Search', 'TikTok']:
            investimento = round(np.random.uniform(1000, 10000), 2)
        else:
            investimento = round(np.random.uniform(100, 500), 2)
            
        dias_atras = random.randint(30, 365)
        data_inicio = datetime.now() - timedelta(days=dias_atras)
        duracao = random.randint(5, 45)
        data_fim = data_inicio + timedelta(days=duracao)
        
        campanhas.append({
            'nome_campanha': f"Campanha_{produto}_{canal}_Q{random.randint(1,4)}",
            'canal': canal,
            'produto_alvo': produto,
            'investimento_diario': investimento,
            'data_inicio': data_inicio.date(),
            'data_fim': data_fim.date()
        })
        
    df_campanhas = pd.DataFrame(campanhas)
    df_campanhas.to_sql('campanhas_marketing', engine, if_exists='append', index=False)
    print("Campanhas inseridas com sucesso!")

if __name__ == "__main__":
    limpar_base_antiga()
    gerar_clientes(50000)
    gerar_campanhas()
