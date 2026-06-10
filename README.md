# Análise de Comentários do YouTube via Redes Textuais

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange?style=flat-square)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![Licença](https://img.shields.io/badge/Licença-Acadêmica-green?style=flat-square)](https://github.com)

> **Investigação comparativa de estratégias de modelagem de redes textuais em comentários do YouTube**

---

## Contextualização

Este projeto de **Iniciação Científica** investiga e compara duas estratégias de modelagem de redes textuais aplicadas a comentários de vídeos do YouTube:

- **Rede de co-ocorrência** — nós são palavras, arestas representam co-ocorrência léxica
- **Rede de similaridade semântica** — nós são comentários, arestas representam proximidade semântica via embeddings

A literatura apresenta lacunas quanto ao impacto comparativo das diferentes abordagens de modelagem na qualidade das análises resultantes.

---

## Objetivos

### Objetivo Geral
Explorar técnicas de representação de redes textuais de forma **comparativa**, avaliando qual modelagem oferece melhor desempenho para tarefas específicas de análise.

### Objetivos Específicos
- Coletar e organizar corpus de comentários do YouTube com diversidade temática e temporal
- Implementar diferentes técnicas de modelagem de redes textuais
- Aplicar métricas de análise de redes (centralidade, modularidade, densidade)
- Rotular comunidades automaticamente com pipeline LLM
- Conduzir análises exploratórias comparativas entre as duas estratégias de rede
- Comparar resultados e elaborar diretrizes metodológicas

---

## Dashboard de Progresso

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ANDAMENTO DO PROJETO 2025/2026                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1  Coleta e Organização de Dados               ████████████ 100%  │
│  2  Limpeza e Pré-processamento                 ████████████ 100%  │
│  3  Rede de Co-ocorrência                       ████████████ 100%  │
│  4  Detecção e Análise de Comunidades           ████████████ 100%  │
│  5  Embeddings Semânticos                       ████████████ 100%  │
│  6  Rede de Similaridade Semântica              ████████░░░░  70%  │
│  7  Análise Comparativa de Modelagens           ░░░░░░░░░░░░   0%  │
│  8  Redação e Apresentação Final                ░░░░░░░░░░░░   0%  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Pipeline Completo

Para cada vídeo, a sequência de execução é:

```
1. youtube_scratch.py
        ↓ comentarios_bruto_{VIDEO}.csv

2a. clean_data.py              → comentarios_processados_{VIDEO}.csv  (embeddings)
2b. clean_data_lemmatized.py   → comentarios_lematizados_{VIDEO}.csv  (co-ocorrência)

3. embedding.py                → ChromaDB (coleção CHROMA_COLLECTION)

4. cooccurrence_network.ipynb  → grafo_coocorrencia_{VIDEO_ID}.gexf
                                  comunidades_coocorrencia_{VIDEO_ID}.csv
                                  distribuicao_grau_coocorrencia_{VIDEO_ID}.png

5. similarity_network_faiss.ipynb → grafo_similaridade_faiss_{VIDEO_ID}.gexf
                                     comunidades_similaridade_faiss_{VIDEO_ID}.csv
                                     distribuicao_grau_similaridade_faiss_{VIDEO_ID}.png
```

Para trocar de vídeo, alterar no `.env`: `DEFAULT_INPUT`, `DEFAULT_OUTPUT`, `CLEAN_COMMENTS_PATH`, `LEMMATIZED_PATH`, `CHROMA_COLLECTION`, e `VIDEO_ID1`.

---

## Corpus

| Vídeo | Tema | Comentários |
|:---|:---|:---:|
| Debate Presidencial Band 2022 | Bolsonaro pergunta a Lula sobre corrupção na Petrobras | 53.831 |
| Cortando a placa | Reação à remoção de placa de Bolsonaro | — |
| Chico Buarque | Manifestação cultural | — |

---

## Estrutura do Projeto

```
ic_pet/
├── README.md
├── requirements.txt
├── .env                                    (não versionado)
│
├── python_scripts/
│   ├── data_mining/
│   │   └── youtube_scratch.py             coleta via YouTube Data API v3
│   ├── pre_processing/
│   │   ├── clean_data.py                  limpeza para embeddings (NLTK)
│   │   └── clean_data_lemmatized.py       lematização para rede de co-ocorrência (SpaCy)
│   └── text_network/
│       ├── embedding.py                   gera embeddings e armazena no ChromaDB
│       ├── testing.py                     valida conexão ao ChromaDB
│       ├── cooccurrence_network.ipynb     rede de co-ocorrência de palavras
│       ├── similarity_network_faiss.ipynb rede de similaridade semântica (FAISS, escala grande)
│       └── similarity_network.ipynb       rede de similaridade semântica (sklearn, amostra)
│
├── data/
│   ├── raw/                               CSVs brutos coletados
│   ├── processed/                         CSVs processados e lematizados
│   └── chromadb/                          vector store persistente
│
└── wtdcc_2025/
    ├── poster_wtdcc_eduarda_lopes.pdf
    └── resumo_wtdcc_2025.pdf
```

---

## Arquitetura das Redes

### Rede de Co-ocorrência (`cooccurrence_network.ipynb`)

| Parâmetro | Valor |
|:---|:---:|
| Nós | palavras (lemas) |
| Arestas | co-ocorrência em comentários |
| MIN_EDGE_WEIGHT | 15 |
| TOP_N_NODES | 200 |
| Detecção de comunidades | Leiden (ModularityVertexPartition, seed=42) |
| Rotulação | flan-t5-base + mDeBERTa zero-shot |

**Resultado (vídeo 1):** 200 nós, 10.564 arestas, modularidade 0,0859, 4 comunidades

### Rede de Similaridade Semântica (`similarity_network_faiss.ipynb`)

| Parâmetro | Valor |
|:---|:---:|
| Nós | comentários (texto completo) |
| Arestas | similaridade cosseno ≥ threshold |
| Threshold padrão | 0,85 |
| Busca de vizinhos | FAISS top-K (K=50) |
| Detecção de comunidades | Leiden (ModularityVertexPartition, seed=42) |
| Rotulação | flan-t5-base + mDeBERTa zero-shot |

---

## Pré-processamento

Dois pipelines distintos porque cada rede exige um tipo diferente de input:

| Script | Ferramenta | Output | Uso |
|:---|:---|:---|:---|
| `clean_data.py` | NLTK | texto limpo sem stopwords | embeddings semânticos |
| `clean_data_lemmatized.py` | SpaCy `pt_core_news_sm` | lemas sem verbos genéricos | rede de co-ocorrência |

Os embeddings precisam do texto natural completo para capturar contexto semântico. A rede de co-ocorrência precisa de lemas limpos para que as conexões entre palavras sejam significativas.

---

## Rotulação Automática de Comunidades

Pipeline LLM em 2 etapas aplicado em ambas as redes:

1. **Text Generation** (`google/flan-t5-base`) — dado os termos/comentários mais centrais da comunidade, gera um rótulo temático livre
2. **Zero-Shot Classification** (`MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`) — valida o rótulo candidato contra categorias temáticas

---

## Variáveis de Ambiente (`.env`)

```bash
API_KEY=...
VIDEO_ID1=...   # debate presidencial
VIDEO_ID2=...   # cortando a placa
VIDEO_ID3=...   # chico buarque

LOCAL=.../data/raw/comentarios_bruto.csv
DEFAULT_INPUT=.../data/raw/comentarios_bruto.csv
DEFAULT_OUTPUT=.../data/processed/comentarios_processados.csv
CLEAN_COMMENTS_PATH=.../data/processed/comentarios_processados.csv
LEMMATIZED_PATH=.../data/processed/comentarios_lematizados.csv
DATA_PATH=.../data/chromadb/
CHROMA_COLLECTION=communities_collection_video1
```

---

## Instalação

```bash
# 1. Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Baixar modelo SpaCy para português
python -m spacy download pt_core_news_sm

# 4. Configurar .env com as variáveis acima
```

### Dependências principais

```
pandas / numpy          manipulação de dados
nltk                    tokenização e stopwords
spacy                   lematização (pt_core_news_sm)
sentence-transformers   embeddings semânticos
chromadb                vector store
networkx                construção e análise de grafos
leidenalg / igraph      detecção de comunidades
faiss-cpu               busca aproximada de vizinhos
transformers            rotulação LLM
matplotlib              visualizações
```

---

## Resultados (vídeo 1 — Debate Band 2022)

### Rede de Co-ocorrência
Identificadas 4 comunidades léxicas no corpus:
- Ataques a Políticos (~50% da rede)
- Pauta Econômica/Social
- Discurso Moralizante
- Mobilização Ideológica

O debate foi usado como palanque político: aproximadamente metade das discussões desviou do tema oficial (corrupção na Petrobras) para ataques diretos a candidatos.

### Rede de Similaridade
Em desenvolvimento — pipeline implementado, aguardando execução sobre os 3 vídeos.

---

## Apresentações

| Evento | Ano | Arquivo |
|:---|:---:|:---|
| WTDCC 2025 | 2025 | `wtdcc_2025/poster_wtdcc_eduarda_lopes.pdf` |
| WI-IAT / Webmedia | 2026 | em elaboração |

---

## Referências

BLONDEL, Vincent D. et al. *Fast unfolding of communities in large networks.* Journal of Statistical Mechanics, v. 2008, n. 10, 2008.

TRAAG, V. A.; WALTMAN, L.; VAN ECK, N. J. *From Louvain to Leiden: guaranteeing well-connected communities.* Scientific Reports, v. 9, n. 5233, 2019.

REIMERS, Nils; GUREVYCH, Iryna. *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP, 2019.

BIRD, Steven; KLEIN, Ewan; LOPER, Edward. *NLTK Documentation – Portuguese HOWTO.*

GOOGLE DEVELOPERS. *YouTube Data API v3 – Comments.*

SICSS. *Text Networks.* 2018.

VEGA, Diego; MAGNANI, Matteo. *Foundations of Temporal Text Networks.* Applied Network Science, v. 3, n. 25, 2018.

---

## 📄 Licenças

Este projeto está sendo desenvolvido como parte de pesquisa acadêmica e com apoio da Universidade Federal de Uberlândia e do YouTube Researcher Program.

Para mais informações ou colaborações, entre em contato através do repositório.
