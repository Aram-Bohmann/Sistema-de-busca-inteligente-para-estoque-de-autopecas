import sqlite3
from elasticsearch import Elasticsearch, helpers

# 1. Configuração revisada (Garantindo que o JSON esteja perfeito)
MAPPING = {
    "settings": {
        "analysis": {
            "filter": {
                "meus_sinonimos": {
                    "type": "synonym",
                    "synonyms": [
                        "gm, chevrolet, chevrole",
                        "vw, volkswagen, volks",
                        "ft, fiat",
                        "fd, ford",
                        "ty, toyota, toy",
                        "rn, renault, reno",
                        "hd, honda",
                        "hy, hyundai",
                        "mt, mitsubishi, mit",
                        "pt, peugeot, pejo",
                        "ct, citroen, citroen",
                        "retentor, vedador, gaxeta, ret",
                        "amor, amortecedor, amort",
                        "cabo acel, cabo acelerador",
                        "cabo f, cabo freio, cabo de mao",
                        "filtro oleo, filtro de oleo, elemento lubrificante",
                        "pastilha trav, pastilha de freio, pastilha",
                        "bucha susp, bucha suspensao",
                        "bomba agua, bomba d'agua, bba agua",
                        "kit embreag, kit embreagem, plato e disco",
                        "sup parach, suporte parachoques, suporte",
                        "parach, parachoque, para-choque",
                        "reserv, reservatorio, expansao",
                        "emblema, logo, logomarca, grade",
                        "dt, dianteiro, frente, frontal, dianteira, diant",
                        "tr, traseiro, tras, retaguarda",
                        "esq, esquerdo, motorista",
                        "dir, direito, passageiro",
                        "par, ambos os lados, bilateral, esq dir",
                        "central, meio, intermediario",
                        "90, 1990", "91, 1991", "92, 1992", "93, 1993", "94, 1994", 
                        "95, 1995", "96, 1996", "97, 1997", "98, 1998", "99, 1999",
                        "00, 2000", "01, 2001", "02, 2002", "03, 2003", "04, 2004", 
                        "05, 2005", "06, 2006", "07, 2007", "08, 2008", "09, 2009",
                        "10, 2010", "11, 2011", "12, 2012", "13, 2013", "14, 2014", 
                        "15, 2015", "16, 2016", "17, 2017", "18, 2018", "19, 2019",
                        "20, 2020", "21, 2021", "22, 2022", "23, 2023", "24, 2024", "25, 2025"
                    ]
                }
            },
            "analyzer": {
                "meu_analisador": {
                    "tokenizer": "standard",
                    "filter": ["lowercase", "asciifolding", "meus_sinonimos"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "id_produto": { "type": "keyword" },
            "ds_produto": { "type": "text", "analyzer": "meu_analisador" },
            "qt_produto": { "type": "integer" },
            "ds_local": { "type": "keyword" }
        }
    }
}

def sincronizar():
    # Conexão simplificada para Docker local
    es = Elasticsearch(
        [{"host": "localhost", "port": 9200, "scheme": "http"}]
    )

    try:
        # Tenta deletar o índice antigo (se existir)
        if es.indices.exists(index="produtos_autopecas"):
            es.indices.delete(index="produtos_autopecas")
            print("Índice antigo removido.")

        # Cria o índice com as configurações de sinônimos
        es.indices.create(index="produtos_autopecas", body=MAPPING)
        print("Novo índice criado com sucesso.")

        # Conecta no SQLite
        conn = sqlite3.connect('produtos_autopecas.db')
        cursor = conn.cursor()
        
        # Ajuste os nomes das colunas conforme o seu SQLite
        cursor.execute("SELECT id_produto, ds_produto, qt_produto, ds_local FROM produtos")
        rows = cursor.fetchall()

        acoes = [
            {
                "_index": "produtos_autopecas",
                "_source": {
                    "id_produto": r[0],
                    "ds_produto": r[1],
                    "qt_produto": r[2],
                    "ds_local": r[3]
                }
            }
            for r in rows
        ]

        if acoes:
            helpers.bulk(es, acoes)
            print(f"{len(acoes)} itens sincronizados!")
        else:
            print("O SQLite parece estar vazio. Rode o seed_db.py primeiro.")

        conn.close()

    except Exception as e:
        print(f"❌ Erro durante a sincronização: {e}")

if __name__ == "__main__":
    sincronizar()