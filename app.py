import streamlit as st
import time
import pandas as pd
from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])

st.set_page_config(page_title="Autopeças", layout="wide", page_icon="🔩")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* Reset e base */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section[data-testid="stMain"] > div {
    background-color: #F5F2EB !important;
}

[data-testid="stHeader"] { background: transparent !important; }

/* Esconde elementos desnecessários do Streamlit */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

/* Tipografia global */
html, body, [data-testid="stAppViewContainer"] * {
    font-family: 'DM Mono', monospace;
    color: #1a1a1a;
}

/* ── HEADER ─────────────────────────────────── */
.header-wrap {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding: 2.5rem 0 1rem 0;
    border-bottom: 2px solid #1a1a1a;
    margin-bottom: 2rem;
}
.header-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.8rem;
    letter-spacing: -2px;
    line-height: 1;
    color: #1a1a1a;
}
.header-title span { color: #C1440E; }
.header-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 2px;
    padding-bottom: 6px;
}

/* ── INPUT ──────────────────────────────────── */
[data-testid="stTextInput"] {
    margin-bottom: 0.5rem;
}
[data-testid="stTextInput"] label { display: none; }
[data-testid="stTextInput"] input {
    background: #FFFFFF !important;
    border: 2px solid #1a1a1a !important;
    border-radius: 0px !important;
    color: #1a1a1a !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1rem !important;
    padding: 14px 18px !important;
    box-shadow: 4px 4px 0px #1a1a1a !important;
    transition: box-shadow 0.15s ease !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #C1440E !important;
    box-shadow: 4px 4px 0px #C1440E !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: #aaa !important;
    font-style: italic;
}

/* ── BADGE DE STATUS ────────────────────────── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 0.6rem 0;
    margin-bottom: 1rem;
    border-bottom: 1px solid #ddd;
}
.badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    padding: 3px 10px;
    border-radius: 0;
    border: 1px solid;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.badge-orange { color: #C1440E; border-color: #C1440E; background: #fff3ef; }
.badge-gray   { color: #666;    border-color: #ccc;    background: #f9f9f9; }
.badge-green  { color: #1a6b3a; border-color: #1a6b3a; background: #edf7f1; }

/* ── DATAFRAME ──────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 2px solid #1a1a1a !important;
    box-shadow: 5px 5px 0px #1a1a1a;
}
[data-testid="stDataFrame"] * {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}

/* ── AVISO ──────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 0 !important;
    border: 1px solid #C1440E !important;
    background: #fff3ef !important;
    font-family: 'DM Mono', monospace !important;
}
</style>
""", unsafe_allow_html=True)


# ── Funções ES ────────────────────────────────────────────────────────────────
def buscar_todos():
    return es.search(index="produtos_autopecas", **{
        "query": {"match_all": {}},
        "size": 1000,
        "sort": [{"id_produto": {"order": "asc"}}]
    })

def busca_hibrida(query_texto):
    return es.search(index="produtos_autopecas", **{
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
                "functions": [{"field_value_factor": {
                    "field": "qt_produto", "modifier": "log1p", "factor": 0.5, "missing": 0
                }}],
                "boost_mode": "multiply"
            }
        },
    })

def hits_to_df(hits):
    return pd.DataFrame([{
        "ID":       h["_source"]["id_produto"],
        "Produto":  h["_source"]["ds_produto"],
        "Estoque":  h["_source"]["qt_produto"],
        "Endereço": h["_source"]["ds_local"]
    } for h in hits])


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-wrap">
    <div class="header-title">AUTO<span>PEÇAS</span><br>ESTOQUE</div>
    <div class="header-sub">Busca inteligente · fuzzy + sinônimos</div>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
query = st.text_input("", placeholder="cabo gm sonic 2015  ·  retentor dt gol  ·  amort vw 98/04")

# ── Resultados ────────────────────────────────────────────────────────────────
if query:
    t0 = time.time()
    try:
        res = busca_hibrida(query)
        latency = (time.time() - t0) * 1000
        hits = res["hits"]["hits"]

        st.markdown(f"""
        <div class="status-bar">
            <span class="badge badge-orange">⌕ {len(hits)} resultado(s)</span>
            <span class="badge badge-gray">⏱ {latency:.1f} ms</span>
        </div>
        """, unsafe_allow_html=True)

        if not hits:
            st.warning("Nenhum resultado. Tente termos mais genéricos.")
        else:
            st.dataframe(hits_to_df(hits), use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Erro na busca: {e}")

else:
    t0 = time.time()
    try:
        res = buscar_todos()
        latency = (time.time() - t0) * 1000
        hits = res["hits"]["hits"]

        st.markdown(f"""
        <div class="status-bar">
            <span class="badge badge-green">● estoque completo</span>
            <span class="badge badge-gray">{len(hits)} itens</span>
            <span class="badge badge-gray">⏱ {latency:.1f} ms</span>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(hits_to_df(hits), use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Erro ao carregar estoque: {e}")