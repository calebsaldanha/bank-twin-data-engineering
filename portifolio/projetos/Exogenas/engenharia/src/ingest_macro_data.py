import pandas as pd
import requests
from sqlalchemy import create_engine
import os
from datetime import datetime

# Configuração via Variáveis de Ambiente
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASS = os.getenv('DB_PASS', 'adminpassword')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '5433')
DB_NAME = os.getenv('DB_NAME', 'macro_db')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def get_banco_central_data(codigo_bcb):
    # Janela segura de 5 anos para evitar o limite de dias exatos do BCB
    data_inicial = (pd.Timestamp.now() - pd.DateOffset(years=5)).strftime('%d/%m/%Y')
    data_final = pd.Timestamp.now().strftime('%d/%m/%Y')
    
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb}/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise ConnectionError(f"A API do BCB falhou com status {response.status_code}: {response.text}")
        
    try:
        data = response.json()
    except ValueError:
        raise ValueError(f"O servidor do BCB não enviou um JSON válido. Resposta bruta: '{response.text[:200]}...'")
    
    # Se a API retornar um dicionário isolado em vez de lista
    if isinstance(data, dict):
        if 'data' not in data:
            raise ValueError(f"Resposta inesperada da API: {data}")
        data = [data]
        
    df = pd.DataFrame(data)
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['valor'] = df['valor'].astype(float)
    return df

def get_ptax():
    url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='12-31-2024'&$top=1000&$format=json"
    response = requests.get(url)
    data = response.json()['value']
    df = pd.DataFrame(data)
    df['data'] = pd.to_datetime(df['dataHoraCotacao'])
    return df[['data', 'cotacaoCompra', 'cotacaoVenda']]

def ingest_macroeconomia():
    print("Iniciando extração de dados Macroeconômicos (Janela Móvel Segura de 5 anos)...")
    
    try:
        print("Buscando série 432 (Selic Meta) do Banco Central...")
        df_selic_meta = get_banco_central_data(432)
        df_selic_meta.rename(columns={'valor': 'selic_meta'}, inplace=True)
        
        print("Buscando série 433 (IPCA Mensal) do Banco Central...")
        df_ipca = get_banco_central_data(433)
        df_ipca.rename(columns={'valor': 'ipca_mensal'}, inplace=True)
        
        # Criar um DataFrame unificado
        df_macro = pd.merge(df_selic_meta, df_ipca, on='data', how='outer')
        
        print("Salvando macroeconomia no banco de dados...")
        df_macro.to_sql('macroeconomia', engine, schema='exogenas', if_exists='replace', index=False)
        print("Dados macroeconômicos injetados com sucesso!")
        
    except Exception as e:
        print(f"Falha ao extrair dados macroeconômicos: {e}")

def ingest_feriados(ano):
    print(f"Buscando feriados de {ano} na Brasil API...")
    url = f"https://brasilapi.com.br/api/feriados/v1/{ano}"
    response = requests.get(url)
    
    if response.status_code == 200:
        df_feriados = pd.DataFrame(response.json())
        df_feriados['data'] = pd.to_datetime(df_feriados['date'])
        df_feriados.rename(columns={'name': 'nome_feriado', 'type': 'tipo'}, inplace=True)
        df_feriados = df_feriados[['data', 'nome_feriado', 'tipo']]
        
        print("Salvando feriados no banco de dados...")
        try:
            df_feriados.to_sql('feriados', engine, schema='exogenas', if_exists='append', index=False)
            print(f"Feriados de {ano} injetados com sucesso!")
        except Exception as e:
            if "duplicate key value" in str(e):
                print(f"Aviso: Os feriados de {ano} já estão cadastrados na base de dados.")
            else:
                print(f"Erro ao inserir feriados: {e}")
    else:
        print(f"Erro ao buscar feriados da Brasil API. Status: {response.status_code}")

if __name__ == "__main__":
    ingest_macroeconomia()
    
    ano_atual = datetime.now().year
    ingest_feriados(ano_atual - 1)
    ingest_feriados(ano_atual)
