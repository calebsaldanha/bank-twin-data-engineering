from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.environ.get("DATABASE_URL"))

def clean():
    # TRUNCATE CASCADE apaga a tabela e todas as referencias em outras tabelas
    queries = [
        "TRUNCATE TABLE transacoes_cartao CASCADE;",
        "TRUNCATE TABLE parcelas_credito CASCADE;",
        "TRUNCATE TABLE contratos_credito CASCADE;",
        "TRUNCATE TABLE cartoes CASCADE;"
    ]
    with engine.begin() as conn:
        for q in queries:
            conn.execute(text(q))
    print("Tabelas de produtos e fatos limpas com sucesso.")

if __name__ == "__main__":
    clean()
