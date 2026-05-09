import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.environ.get("DATABASE_URL"))

def run_validation():
    tabelas = ['clientes', 'contas', 'cartoes', 'investimentos_posicao', 'contratos_credito', 'parcelas_credito']
    print("\nVOLUMETRIA ATUALIZADA")
    with engine.connect() as conn:
        for t in tabelas:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar()
            print(f"{t.ljust(20)}: {count:,}")

    print("\nDISTRIBUICAO DE CARTOES POR CONTA")
    df_cards = pd.read_sql("""
        SELECT qtd_cartoes, COUNT(*) as total_contas
        FROM (SELECT conta_id, COUNT(cartao_id) as qtd_cartoes FROM contas LEFT JOIN cartoes USING(conta_id) GROUP BY 1) t
        GROUP BY 1 ORDER BY 1
    """, engine)
    print(df_cards.to_string(index=False))

    print("\nMIX DE PRODUTOS DE CREDITO")
    df_cred = pd.read_sql("SELECT tipo_produto, COUNT(*) as total FROM contratos_credito GROUP BY 1", engine)
    print(df_cred.to_string(index=False))

if __name__ == "__main__":
    run_validation()
