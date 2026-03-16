import sqlite3
import random

def gerar_dados_autoparts(n=2000):
    pecas = ["CABO ACEL", "CABO F", "RETENTOR DT", "AMORT", "FILTRO OLEO", "PASTILHA TRAV", "BUCHA SUSP", "BOMBA AGUA", "KIT EMBREAG", "SUP PARACH", "PARACH", "RESERV", "EMBLEMA"]

    montadoras = ["GM", "VW", "FT", "FD", "TY", "RN", "HD", "HY", "MT", "PT", "CT"]

    modelos = {
        "GM": ["SONIC", "ONIX", "CORSA", "S10", "PRISMA", "CELTA", "CRUZE", "TRACKER"],
        "VW": ["GOL", "POLO", "AMAROK", "GOLF", "SAVEIRO", "VIRTUS", "T-CROSS", "VOYAGE"],
        "FT": ["UNO", "PALIO", "STRADA", "TORO", "ARGO", "MOBI", "CRONOS", "SIENA"],
        "FD": ["KA", "FIESTA", "RANGER", "FOCUS", "ECOSPORT", "F1000", "FUSION"],
        "TY": ["COROLLA", "HILUX", "ETIOS", "YARIS", "SW4", "RAV4"],
        "RN": ["SANDERO", "LOGAN", "DUSTER", "KWID", "OROCH", "MASTER", "CAPTUR"],
        "HD": ["CIVIC", "FIT", "HRV", "CITY", "CRV", "WRV"],
        "HY": ["HB20", "CRETA", "TUCSON", "I30", "SANTA FE", "HR"],
        "MT": ["L200", "PAJERO", "ASX", "OUTLANDER", "TR4"],
        "PT": ["208", "308", "2008", "PARTNER", "EXPERT"],
        "CT": ["C3", "C4 CACTUS", "C3 PICASSO", "JUMPER", "BERLINGO"]
    }
    lados = ["ESQ", "DIR", "DT", "TR", "CENTRAL", "ESQ/DIR"]

    populando = []
    for i in range(n):
        m = random.choice(montadoras)
        mod = random.choice(modelos[m])
        p = random.choice(pecas)
        ano = f"{random.randint(90, 99):02d}/{random.randint(00, 24):02d}" 
        lado = random.choice(lados)
        
        descricao = f"{p} {m} {mod} {ano} {lado}"
        
        quantidade = random.randint(1, 100)
        
        loc = f"S{random.randint(1,9)}R{random.randint(1,20)}C{random.randint(1,15)}L{random.randint(1,10)}"
        
        populando.append((descricao, quantidade, loc))
    
    return populando

def inserir_no_banco():
    conn = sqlite3.connect('produtos_autopecas.db')
    cursor = conn.cursor()

    dados = gerar_dados_autoparts(2000)


    cursor.executemany('''
        INSERT OR IGNORE INTO produtos (ds_produto, qt_produto, ds_local)
        VALUES (?, ?, ?)
    ''', dados)

    conn.commit()
    conn.close()
    print(f"2000 itens inseridos no SQLite com sucesso!")

if __name__ == "__main__":
    inserir_no_banco()