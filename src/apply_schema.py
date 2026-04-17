import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.environ.get("DATABASE_URL"))

def apply():
    with open('sql/schema_inicial.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    # engine.begin() garante o commit automatico na versao 2.0+ do SQLAlchemy
    # e funciona como uma transacao segura em versoes anteriores
    with engine.begin() as conn:
        conn.execute(text(sql))
    print("Schema SQL aplicado com sucesso.")

if __name__ == "__main__":
    apply()
