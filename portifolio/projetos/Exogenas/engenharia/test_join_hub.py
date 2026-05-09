import pandas as pd
from sqlalchemy import create_engine
import warnings

warnings.filterwarnings('ignore')

print("--- [TESTE DE INTEGRAÇÃO DO CENTRAL DATA HUB] ---")

# Credenciais mapeadas do Docker
DB_USER = 'caleb'
DB_PASS = 'adminpassword'
DB_HOST = '127.0.0.1'
DB_PORT = '5433'

# Engine para ambos os bancos
engine_bank = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/bank_twin")
engine_macro = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/macro_db")

try:
    # 1. Extração Exógena
    df_macro = pd.read_sql("SELECT data, selic_meta, ipca_mensal FROM exogenas.macroeconomia", engine_macro)
    df_feriados = pd.read_sql("SELECT data, nome_feriado FROM exogenas.feriados", engine_macro)
    
    df_macro['data'] = pd.to_datetime(df_macro['data'])
    df_feriados['data'] = pd.to_datetime(df_feriados['data'])
    
    # 2. Extração Transacional
    # Caso a tabela não se chame 'transacoes_cartao', este passo vai falhar e avisar
    query_trans = "SELECT DATE(data_transacao) as data, COUNT(*) as qtd, SUM(valor) as volume FROM public.transacoes_cartao GROUP BY 1 LIMIT 20"
    df_trans = pd.read_sql(query_trans, engine_bank)
    df_trans['data'] = pd.to_datetime(df_trans['data'])
    
    # 3. JOIN Analítico
    df_hub = pd.merge(df_trans, df_macro, on='data', how='left')
    df_hub = pd.merge(df_hub, df_feriados, on='data', how='left')
    df_hub['nome_feriado'] = df_hub['nome_feriado'].fillna('Dia Útil')
    
    print("\n[SUCESSO] O Data Hub está unindo as tabelas com sucesso:")
    print(df_hub.sort_values('data').tail(5))
    print("\n--- Estrutura Final pronta para Modelagem ---")

except Exception as e:
    print(f"\n[ERRO NA INTEGRAÇÃO]: {e}")
    print("Possível causa: Verifique se a tabela 'transacoes_cartao' existe no banco 'bank_twin'.")
