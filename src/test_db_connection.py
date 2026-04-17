from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd

# String de conexão apontando para a porta 5432 que o Docker abriu
DATABASE_URL = os.environ.get("DATABASE_URL")

def testar_conexao():
    try:
        print("Iniciando conexão com o Gêmeo Digital (PostgreSQL no Docker)...")
        engine = create_engine(DATABASE_URL)
        
        # Busca todas as tabelas criadas automaticamente pelo nosso arquivo .sql
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        """
        
        with engine.connect() as conn:
            df_tabelas = pd.read_sql(text(query), conn)
            
        print("\nConexão estabelecida com sucesso!")
        print(f"Encontramos {len(df_tabelas)} tabelas prontas para uso:")
        for _, row in df_tabelas.iterrows():
            print(f" - {row['table_name']}")
            
    except Exception as e:
        print("\nErro ao conectar. O contêiner do Docker está rodando?")
        print(f"Detalhes do erro: {repr(e)}")

if __name__ == "__main__":
    testar_conexao()
