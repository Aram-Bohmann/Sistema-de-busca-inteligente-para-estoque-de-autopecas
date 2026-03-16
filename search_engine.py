from elasticsearch import Elasticsearch

try:
    es = Elasticsearch(
        [{"host": "localhost", "port": 9200, "scheme": "http"}]
    )
except Exception as e:
    print(f"Erro ao conectar no ES: {e}")

def busca_hibrida(query_texto):
    body = {
        "query": {
            "function_score": {
                "query": {
                    "multi_match": {
                        "query": query_texto,
                        "fields": ["ds_produto^4"],
                        "type": "best_fields",
                        "fuzziness": "AUTO",
                        "prefix_length": 2,
                        "minimum_should_match": "75%"
                    }
                },
                "functions": [
                    {
                        "field_value_factor": {
                            "field": "qt_produto",
                            "modifier": "log1p",
                            "factor": 0.5,
                            "missing": 0
                        }
                    }
                ],
                "boost_mode": "multiply"
            }
        },
        "size": 20
    }

    return es.search(index="produtos_autopecas", **body)