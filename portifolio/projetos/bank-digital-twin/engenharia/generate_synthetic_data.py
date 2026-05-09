import random
import pandas as pd
from sqlalchemy import create_engine, text
from faker import Faker
import uuid
import json

fake = Faker('pt_BR')
engine = create_engine("postgresql://caleb:adminpassword@127.0.0.1:5433/bank_twin")

N_CLIENTES = 50000
BATCH_SIZE = 10000

# Mapa de Métricas e Telas por Produto
FUNIS_APP = {
    "Abertura_Conta": ["Início_Onboarding", "Dados_Pessoais", "Envio_Documentos", "Selfie", "Aprovação_Conta"],
    "Cartao": ["Menu_Cartões", "Fatura_Detalhe", "Ajuste_Limite", "Gerar_Cartão_Virtual", "Bloqueio_Temporário"],
    "Emprestimo_Pessoal": ["Menu_Empréstimos", "Simulação_Valor", "Escolha_Parcelas", "Resumo_Taxas", "Assinatura_Contrato"],
    "Credito_Consignado": ["Menu_Consignado", "Vincular_INSS", "Consulta_Margem", "Simulação_Consignado", "Aprovação_INSS"],
    "Credito_Parcelado": ["Fatura_Detalhe", "Opções_Parcelamento", "Simulação_Parcelamento", "Confirmação_Parcelamento_Fatura"],
    "Investimentos": ["Home_Investimentos", "Perfil_Investidor", "Catálogo_CDB", "Home_Broker_Ações", "Confirmação_Ordem"]
}

def reset_db():
    print("Recriando o schema do banco de dados...")
    with engine.begin() as conn:
        with open('database_schema.sql', 'r') as f:
            conn.execute(text(f.read()))

def generate_campanhas():
    campanhas = [
        # Campanhas Gerais e outros produtos
        {"nome_campanha": "Ágora Investimentos - CDB 110%", "objetivo": "Conversão", "canal": "LinkedIn", "custo_clique_estimado": 2.50, "data_inicio": "2025-03-01"},
        {"nome_campanha": "Empréstimo Consignado INSS", "objetivo": "Retenção", "canal": "SMS", "custo_clique_estimado": 0.40, "data_inicio": "2025-02-15"},
        {"nome_campanha": "Antecipação 13º Salário", "objetivo": "Conversão", "canal": "Push App", "custo_clique_estimado": 0.30, "data_inicio": "2025-06-01"},
        {"nome_campanha": "Open Finance - Traga seus dados", "objetivo": "Engajamento", "canal": "Email", "custo_clique_estimado": 0.80, "data_inicio": "2025-04-10"},
        {"nome_campanha": "Financiamento Auto Veículos", "objetivo": "Conversão", "canal": "Google Ads", "custo_clique_estimado": 3.10, "data_inicio": "2025-05-20"},
        {"nome_campanha": "Seguro de Vida Proteção", "objetivo": "Cross-sell", "canal": "Banner App", "custo_clique_estimado": 0.10, "data_inicio": "2025-07-01"},
        {"nome_campanha": "Programa Indique e Ganhe", "objetivo": "Aquisição", "canal": "WhatsApp", "custo_clique_estimado": 0.50, "data_inicio": "2025-08-15"},
        {"nome_campanha": "Crédito Pessoal - Taxas Reduzidas", "objetivo": "Conversão", "canal": "Email", "custo_clique_estimado": 0.90, "data_inicio": "2025-09-01"},
        
        # Foco Forte em Cartões (Inspirado no portfólio real)
        {"nome_campanha": "Cartão Neo Zero Anuidade", "objetivo": "Aquisição", "canal": "Instagram", "custo_clique_estimado": 1.20, "data_inicio": "2025-01-10"},
        {"nome_campanha": "Cartão Visa Infinite - Acesso Sala VIP", "objetivo": "Aquisição", "canal": "LinkedIn", "custo_clique_estimado": 3.50, "data_inicio": "2025-01-20"},
        {"nome_campanha": "Cartão Elo Nanquim - Pontos Livelo", "objetivo": "Cross-sell", "canal": "Email", "custo_clique_estimado": 1.80, "data_inicio": "2025-02-05"},
        {"nome_campanha": "Upgrade de Cartão - Platinum", "objetivo": "Retenção", "canal": "Push App", "custo_clique_estimado": 0.60, "data_inicio": "2025-04-01"},
        {"nome_campanha": "Cartão Like - 5% Cashback em Apps", "objetivo": "Aquisição", "canal": "Instagram", "custo_clique_estimado": 1.10, "data_inicio": "2025-05-15"},
        {"nome_campanha": "Aumento de Limite Pré-Aprovado", "objetivo": "Engajamento", "canal": "SMS", "custo_clique_estimado": 0.20, "data_inicio": "2025-07-10"},
        {"nome_campanha": "Cartão Universitário - Limite Inicial", "objetivo": "Aquisição", "canal": "TikTok", "custo_clique_estimado": 0.85, "data_inicio": "2025-02-20"},
        {"nome_campanha": "Cartão Signature - Seguro Viagem", "objetivo": "Conversão", "canal": "Google Ads", "custo_clique_estimado": 2.10, "data_inicio": "2025-10-05"},
        {"nome_campanha": "Black Friday - Limite em Dobro", "objetivo": "Engajamento", "canal": "Push App", "custo_clique_estimado": 0.45, "data_inicio": "2025-11-01"}
    ]
    pd.DataFrame(campanhas).to_sql('campanhas_marketing', engine, if_exists='append', index=False)

def generate_massive_data():
    print(f"\nIniciando geração de {N_CLIENTES} clientes com Mapeamento de Eventos e Campanhas de Cartões...")
    
    ufs = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE', 'CE', 'DF', 'ES', 'GO']
    estados_civis = ['Solteiro', 'Casado', 'Divorciado', 'Viúvo']
    mcc_grupos = ['Alimentação', 'Transporte', 'Saúde', 'Educação', 'Lazer', 'Serviços', 'Varejo']
    
    for batch_start in range(1, N_CLIENTES + 1, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE - 1, N_CLIENTES)
        size = batch_end - batch_start + 1
        
        print(f" -> Processando Lote {batch_start} a {batch_end}...")
        
        # 1. CLIENTES
        clientes = []
        for i in range(size):
            renda = random.choices([2500, 5500, 12000, 25000], weights=[0.5, 0.3, 0.15, 0.05])[0] + random.uniform(0, 1000)
            base_score = 400 if renda < 5000 else 650 if renda < 15000 else 800
            
            clientes.append({
                "nome": fake.name(),
                "cpf": str(random.randint(10000000000, 99999999999)),
                "data_nascimento": fake.date_of_birth(minimum_age=18, maximum_age=85),
                "estado_civil": random.choice(estados_civis),
                "uf_residencia": random.choice(ufs),
                "renda_declarada": round(renda, 2),
                "score_serasa": min(1000, max(0, base_score + random.randint(-150, 150))),
                "segmento": "Classic" if renda < 5000 else "Exclusive" if renda < 12000 else "Prime",
                "behavior_score": random.randint(300, 950)
            })
        pd.DataFrame(clientes).to_sql('clientes', engine, if_exists='append', index=False)
        client_ids = list(range(batch_start, batch_end + 1))
        
        # 2. CONTAS E CARTÕES
        contas, cartoes = [], []
        for cid in client_ids:
            contas.append({"cliente_id": cid, "tipo_conta": random.choice(["Corrente", "Poupança"]), "data_abertura": fake.date_time_between(start_date="-2y", end_date="now"), "saldo_atual": round(random.uniform(100, 50000), 2), "status": "Ativa"})
        pd.DataFrame(contas).to_sql('contas', engine, if_exists='append', index=False)
        
        for conta_id in client_ids:
            cartoes.append({"conta_id": conta_id, "tipo_cartao": random.choice(["Múltiplo", "Crédito"]), "categoria": random.choice(["Gold", "Platinum", "Black", "Infinite", "Nanquim"]), "limite_total": round(random.uniform(1000, 30000), 2), "limite_disponivel": round(random.uniform(500, 30000), 2), "status": "Ativo"})
        pd.DataFrame(cartoes).to_sql('cartoes', engine, if_exists='append', index=False)
        
        # 3. TRANSAÇÕES
        transacoes = []
        for cartao_id in client_ids:
            for _ in range(random.randint(5, 15)):
                transacoes.append({"cartao_id": cartao_id, "data_transacao": fake.date_time_between(start_date="-1y", end_date="now"), "valor": round(random.uniform(10, 1000), 2), "estabelecimento": f"Loja {random.randint(1, 200)}", "mcc_grupo": random.choice(mcc_grupos), "tipo_transacao": random.choice(["Crédito", "Débito"])})
        pd.DataFrame(transacoes).to_sql('transacoes_cartao', engine, if_exists='append', index=False)
        
        # 4. SESSÕES E EVENTOS APP
        sessoes, eventos = [], []
        for cid in client_ids:
            disp_id = str(uuid.uuid4())
            sessoes.append({"dispositivo_id": disp_id, "cliente_id": cid, "os": random.choice(["iOS", "Android"]), "modelo_aparelho": random.choice(["iPhone 13", "Galaxy S21", "Moto G", "Xiaomi 11"])})
            
            jornadas_cliente = random.sample(list(FUNIS_APP.keys()), random.randint(1, 3))
            
            for jornada in jornadas_cliente:
                sessao_id = str(uuid.uuid4())
                telas_jornada = FUNIS_APP[jornada]
                passos_dados = random.randint(1, len(telas_jornada))
                data_sessao = fake.date_time_between(start_date="-30d", end_date="now")
                
                # Sorteia entre nulo (orgânico) ou uma das 17 campanhas
                campanha_origem = random.choice([None, random.randint(1, 17)]) 
                
                for passo in range(passos_dados):
                    eventos.append({
                        "dispositivo_id": disp_id, 
                        "cliente_id": cid, 
                        "campanha_id": campanha_origem,
                        "sessao_id": sessao_id, 
                        "tipo_evento": telas_jornada[passo], 
                        "data_evento": data_sessao + pd.Timedelta(minutes=passo*1.5),
                        "metadados": json.dumps({"jornada": jornada, "passo_funil": passo + 1, "completou_funil": passo == len(telas_jornada)-1})
                    })
                    
        pd.DataFrame(sessoes).to_sql('sessoes_dispositivos', engine, if_exists='append', index=False)
        pd.DataFrame(eventos).to_sql('eventos_app', engine, if_exists='append', index=False)
        
        # 5. INVESTIMENTOS E CRÉDITO
        investimentos, contratos, parcelas = [], [], []
        for cid in random.sample(client_ids, int(size * 0.2)):
            investimentos.append({"cliente_id": cid, "tipo_ativo": random.choice(["CDB", "LCI", "Tesouro Direto", "Ações"]), "valor_aplicado": round(random.uniform(1000, 100000), 2), "valor_atual": round(random.uniform(900, 110000), 2), "perfil_risco": random.choice(["Conservador", "Moderado", "Arrojado"])})
        if investimentos: pd.DataFrame(investimentos).to_sql('investimentos_posicao', engine, if_exists='append', index=False)
        
        start_contract_id = int((batch_start - 1) * 0.3) + 1
        for i, conta_id in enumerate(random.sample(client_ids, int(size * 0.3))):
            contrato_id = start_contract_id + i
            contratos.append({"conta_id": conta_id, "tipo_produto": random.choice(["Empréstimo Pessoal", "Consignado INSS", "Crédito Parcelado", "Financiamento Auto"]), "valor_contratado": round(random.uniform(5000, 50000), 2), "taxa_juros_mes": round(random.uniform(1.5, 5.0), 2), "data_contratacao": fake.date_between(start_date="-1y", end_date="today")})
            for p in range(1, 13):
                parcelas.append({"contrato_id": contrato_id, "numero_parcela": p, "valor_parcela": round(random.uniform(500, 5000), 2), "data_vencimento": fake.date_between(start_date="-11m", end_date="+1m"), "status_pagamento": random.choice(["Pago", "Atrasado", "Pendente"])})
        if contratos:
            pd.DataFrame(contratos).to_sql('contratos_credito', engine, if_exists='append', index=False)
            pd.DataFrame(parcelas).to_sql('parcelas_credito', engine, if_exists='append', index=False)

if __name__ == "__main__":
    reset_db()
    generate_campanhas()
    generate_massive_data()
    print("\n✅ Sucesso: Base gerada com métricas de App Analytics e foco reforçado em Cartões!")
