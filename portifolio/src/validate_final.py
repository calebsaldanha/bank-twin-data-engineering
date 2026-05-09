import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.environ.get("DATABASE_URL"))

def validate():
    print("\n" + "="*40)
    print("RELATORIO FINAL DE VOLUMETRIA")
    print("="*40)
    
    queries = {
        "Clientes": "SELECT COUNT(*) FROM clientes",
        "Cartões": "SELECT COUNT(*) FROM cartoes",
        "Contratos Crédito": "SELECT COUNT(*) FROM contratos_credito",
        "Parcelas": "SELECT COUNT(*) FROM parcelas_credito",
        "Transações": "SELECT COUNT(*) FROM transacoes_cartao",
        "Eventos Mkt": "SELECT COUNT(*) FROM eventos_app"
    }
    
    for nome, q in queries.items():
        with engine.connect() as conn:
            res = conn.execute(text(q)).scalar()
            print(f"{nome.ljust(20)}: {res:,}")

    print("\n" + "="*40)
    print("DISTRIBUICAO DE CARTOES (PROVA DE VARIABILIDADE)")
    print("="*40)
    dist_query = """
        SELECT qtd as num_cartoes, COUNT(*) as total_contas
        FROM (SELECT conta_id, COUNT(cartao_id) as qtd FROM contas LEFT JOIN cartoes USING(conta_id) GROUP BY 1) t
        GROUP BY 1 ORDER BY 1;
    """
    print(pd.read_sql(dist_query, engine).to_string(index=False))

if __name__ == "__main__":
    validate()
