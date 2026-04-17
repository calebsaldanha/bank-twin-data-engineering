import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import random

# Fixando sementes para reprodutibilidade
np.random.seed(42)
random.seed(42)

DATABASE_URL = "postgresql://caleb:adminpassword@127.0.0.1:5433/bank_twin"
engine = create_engine(DATABASE_URL)

def gerar_contas():
    print("A ler dados de clientes para gerar contas...")
    df_clientes = pd.read_sql("SELECT cliente_id, segmento, renda_declarada, data_abertura_conta FROM clientes", engine)
    
    n = len(df_clientes)
    print(f"A processar contas para {n} clientes...")
    
    # Lógica de negócio vetorizada para saldos e limites (Lime)
    saldos = []
    limes = []
    
    for seg, renda in zip(df_clientes['segmento'], df_clientes['renda_declarada']):
        if seg == 'Massificado':
            saldos.append(round(max(0, np.random.normal(300, 500)), 2))
            limes.append(np.random.choice([0, 500, 1000]))
        elif seg == 'Principal':
            saldos.append(round(max(100, np.random.normal(1500, 1200)), 2))
            limes.append(np.random.choice([1000, 2000, 3000]))
        elif seg == 'Prime':
            saldos.append(round(max(1000, np.random.normal(8000, 5000)), 2))
            limes.append(np.random.choice([5000, 10000, 15000]))
        else: # Private
            saldos.append(round(max(10000, np.random.normal(50000, 30000)), 2))
            limes.append(np.random.choice([20000, 50000, 100000]))

    df_contas = pd.DataFrame({
        'cliente_id': df_clientes['cliente_id'],
        'saldo_atual': saldos,
        'limite_cheque_especial': limes,
        'status': np.random.choice(['Ativa', 'Bloqueada_Prev'], p=[0.98, 0.02], size=n)
    })
    
    print("A inserir contas no banco de dados...")
    df_contas.to_sql('contas', engine, if_exists='append', index=False, chunksize=10000)
    print("Contas inseridas com sucesso!")
    return df_clientes

def gerar_contratos(df_clientes):
    print("A simular carteira de crédito (Lending)...")
    
    produtos_credito = ['CredPessoal', 'CredAuto', 'CredImob', 'AntecipaFGTS']
    contratos = []
    
    # Vamos assumir que 65% da base tem algum produto de crédito
    clientes_com_credito = df_clientes.sample(frac=0.65, random_state=42)
    
    for _, row in clientes_com_credito.iterrows():
        # Cliente pode ter de 1 a 3 contratos
        num_contratos = np.random.choice([1, 2, 3], p=[0.7, 0.25, 0.05])
        
        for _ in range(num_contratos):
            produto = np.random.choice(produtos_credito, p=[0.5, 0.2, 0.1, 0.2])
            
            # Ajuste de valores baseado no produto e renda
            if produto == 'CredPessoal':
                valor = round(np.random.uniform(1000, row['renda_declarada'] * 3), 2)
                prazo = int(np.random.choice([12, 24, 36, 48]))
                taxa = round(np.random.uniform(0.015, 0.059), 4) # 1.5% a 5.9% ao mês
            elif produto == 'CredAuto':
                valor = round(np.random.uniform(20000, 120000), 2)
                prazo = int(np.random.choice([36, 48, 60]))
                taxa = round(np.random.uniform(0.012, 0.025), 4)
            elif produto == 'CredImob':
                valor = round(np.random.uniform(150000, 800000), 2)
                prazo = int(np.random.choice([120, 240, 360]))
                taxa = round(np.random.uniform(0.007, 0.011), 4)
            else: # AntecipaFGTS
                valor = round(np.random.uniform(500, 5000), 2)
                prazo = int(np.random.choice([1, 3, 5])) # Anos antecipados convertidos p/ simulação
                taxa = round(np.random.uniform(0.018, 0.022), 4)
                
            # Data de contratação deve ser após a abertura da conta
            dias_desde_abertura = (datetime.now() - row['data_abertura_conta']).days
            dias_atras = random.randint(1, max(2, dias_desde_abertura))
            data_contrato = datetime.now() - timedelta(days=dias_atras)
            
            # Status inicial genérico (será refinado na geração das parcelas)
            status = np.random.choice(['Ativo', 'Quitado'], p=[0.8, 0.2])
            
            contratos.append({
                'cliente_id': row['cliente_id'],
                'tipo_produto': produto,
                'valor_financiado': valor,
                'taxa_juros_mensal': taxa,
                'prazo_meses': prazo,
                'data_contratacao': data_contrato,
                'status': status
            })
            
    df_contratos = pd.DataFrame(contratos)
    print(f"A inserir {len(df_contratos)} contratos de crédito...")
    df_contratos.to_sql('contratos_credito', engine, if_exists='append', index=False, chunksize=10000)
    print("Contratos inseridos com sucesso!")

if __name__ == "__main__":
    # Garantir que não dupliquemos dados se rodarmos o script duas vezes
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE contas CASCADE;"))
        conn.execute(text("TRUNCATE TABLE contratos_credito CASCADE;"))
        
    df_cli = gerar_contas()
    gerar_contratos(df_cli)
