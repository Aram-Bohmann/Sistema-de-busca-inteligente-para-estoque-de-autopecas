# 🔩 Sistema de Busca Inteligente — Autopeças

> Motor de busca com fuzzy search, sinônimos automotivos e ranking por estoque, construído com Elasticsearch + Python + Streamlit.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.12.0-005571?style=flat-square&logo=elasticsearch&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-required-2496ED?style=flat-square&logo=docker&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57?style=flat-square&logo=sqlite&logoColor=white)

---

## 📌 Sobre o Projeto

Em ambientes de venda de autopeças, vendedores frequentemente buscam produtos usando siglas, abreviações e grafias inconsistentes — `AMORT`, `AMORTECEDOR`, `AMOR` referem-se à mesma peça, mas sistemas convencionais não reconhecem essa equivalência.

Este projeto resolve esse problema com um motor de busca que **pensa como um vendedor**: tolerante a erros, inteligente com sinônimos e priorizando o que está disponível em estoque.

> 💡 Estimativas em projetos similares de busca no varejo apontam para reduções acima de 80% no tempo gasto em buscas manuais após a implementação de sistemas desse tipo *(dado ilustrativo, baseado em benchmarks do setor)*.

---

## ✨ Funcionalidades

- 🔍 **Fuzzy Search** — tolera erros de digitação automaticamente
- 🔄 **Sinônimos automotivos** — mais de 40 mapeamentos (GM↔Chevrolet, FT↔Fiat, DT↔Dianteiro...)
- 📊 **Ranking por estoque** — produtos com mais unidades sobem nos resultados
- ⚡ **Latência em tempo real** — exibida a cada busca (média < 50ms)
- 🗂️ **Estoque completo** — tabela carrega automaticamente sem necessidade de pesquisa
- 🐳 **Docker** — ambiente isolado e reproduzível

---

## 🛠️ Stack Tecnológica

| Ferramenta | Versão | Função |
|---|---|---|
| Python | 3.11+ | Linguagem principal |
| Elasticsearch | 8.12.0 | Motor de busca e indexação |
| elasticsearch-py | 8.12.0 | Cliente Python para o ES |
| Streamlit | 1.x | Interface web |
| SQLite | 3.x | Banco de dados local |
| Pandas | 2.x | Transformação dos dados |
| Docker | latest | Infraestrutura do ES |
| Poetry | latest | Gerenciamento de dependências |

---

## 📁 Estrutura do Projeto

```
busca-autopecas/
│
├── app.py              # Interface Streamlit
├── sync_to_es.py       # Sincronização SQLite → Elasticsearch
├── setup_db.py         # Criação do banco SQLite
├── seed_db.py          # População com dados de exemplo
├── search_engine.py    # Lógica de busca híbrida
│
├── pyproject.toml      # Dependências (Poetry)
└── README.md
```

---

## 🚀 Como Rodar

### Pré-requisitos

- [Python 3.11+](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)

---

### 1. Clone o repositório

```bash
git clone https://github.com/Aram-Bohmann/busca-autopecas.git
cd busca-autopecas
```

### 2. Instale as dependências

```bash
poetry install
```

### 3. Suba o Elasticsearch via Docker

```bash
docker run -d \
  --name es_autopecas \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.12.0
```

> ⚠️ Aguarde ~30 segundos para o container inicializar completamente.

### 4. Configure o banco de dados

```bash
# Cria a estrutura do SQLite
poetry run python setup_db.py

# Popula com 2.000 produtos de exemplo
poetry run python seed_db.py
```

### 5. Sincronize com o Elasticsearch

```bash
poetry run python sync_to_es.py
```

Saída esperada:
```
🗑️ Índice antigo removido.
🏗️ Novo índice criado com sucesso.
✅ 2000 itens sincronizados!
```

### 6. Rode a aplicação

```bash
poetry run streamlit run app.py
```

Acesse em: **http://localhost:8501**

---

## 🔎 Exemplos de Busca

| Você digita | O sistema entende |
|---|---|
| `cabo gm sonic 15 esq` | Cabo — Chevrolet — Sonic — 2015 — Esquerdo |
| `amort vw gol 98/04` | Amortecedor — Volkswagen — Gol — 1998/2004 |
| `retentor dt fiat uno` | Retentor Dianteiro — Fiat — Uno |
| `pastilha ford ka dir` | Pastilha de Freio — Ford — Ka — Direito |
| `filtro oleo hy hb20` | Filtro de Óleo — Hyundai — HB20 |

---

## ⚙️ Como Funciona

### Analyzer customizado no Elasticsearch

O coração do sistema é um **analyzer** configurado com três filtros em cadeia:

```
Texto bruto → lowercase → asciifolding → sinônimos → tokens indexados
```

**Exemplo:**
```
"AMORT VW GOL" → ["amort", "amortecedor", "amor", "vw", "volkswagen", "volks", "gol"]
```

### Busca híbrida com ranking

```python
function_score(
    multi_match(fuzzy + sinônimos)  →  relevância textual
    ×
    field_value_factor(qt_produto)  →  boost por estoque
)
```

O resultado final combina **relevância semântica** com **disponibilidade em estoque** — peças com mais unidades sobem automaticamente.

---

## 🔄 Re-sincronização

Sempre que o catálogo de produtos for atualizado no SQLite, rode:

```bash
poetry run python sync_to_es.py
```

O script recria o índice do zero, garantindo consistência total.

---

## 👨‍💻 Desenvolvedor

**Aram Bohmann Leite da Luz**
Ciência de Dados · Full-Stack Analytics & Machine Learning · Python · SQL · Power BI · Web Dev

[![Portfólio](https://img.shields.io/badge/Portfólio-000000?style=flat-square&logo=vercel&logoColor=white)](https://aram-bohmann.github.io/Site-Portfolio/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Aram-Bohmann)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/aram-luz-1b0ab1321/)

---
