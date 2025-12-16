# 📊 Análise de Comentários do YouTube via Redes Textuais

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange?style=flat-square)]()
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)]()
[![Licença](https://img.shields.io/badge/Licença-Acadêmica-green?style=flat-square)]()

> **Investigação comparativa de estratégias de modelagem de redes textuais em comentários do YouTube com foco em análise de opinião e padrões discursivos**

---

## 🎯 Contextualização

Este projeto de **Iniciação Científica** investiga diferentes estratégias de modelagem de redes textuais aplicadas a comentários de vídeos do YouTube, com foco em mineração de opinião e análise exploratória. A literatura apresenta lacunas quanto ao impacto comparativo das diferentes abordagens de modelagem na qualidade das análises resultantes.

## 📋 Objetivos

### 🎓 Objetivo Geral
Explorar técnicas de representação de redes textuais de forma **comparativa**, avaliando qual modelagem oferece melhor desempenho para tarefas específicas de análise.

### 🔍 Objetivos Específicos
- ✅ Coletar e organizar corpus de comentários do YouTube com diversidade temática e temporal
- ⏳ Implementar diferentes técnicas de modelagem de redes textuais (variando unidade de análise, tipo de aresta e janela de contexto)
- ⏳ Aplicar métricas de análise de redes (centralidade, modularidade, densidade)
- ⏳ Avaliar desempenho em tarefas de mineração de opinião
- ⏳ Conduzir análises exploratórias para identificação de comunidades léxicas e padrões discursivos
- ⏳ Comparar resultados e elaborar diretrizes metodológicas

---

## 📊 Dashboard de Progresso

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ANDAMENTO DO PROJETO 2025                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1️⃣  Coleta e Organização de Dados               ████████████ 100% │
│  2️⃣  Limpeza e Pré-processamento                 ████████████ 100% │
│  3️⃣  Primeira Rede Textual (Co-ocorrência)       ████████████ 100% │
│  4️⃣  Análise de Comunidades                       ████████████ 100% │
│  5️⃣  Implementação de Redes Alternativas         ████░░░░░░░░  40% │
│  6️⃣  Análise Comparativa de Modelagens           ░░░░░░░░░░░░   0% │
│  7️⃣  Mineração de Opinião & Avaliação             ░░░░░░░░░░░░   0% │
│  8️⃣  Redação e Apresentação Final                 ░░░░░░░░░░░░   0% │
│                                                                     │
│  Total: 37.5% do projeto                                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

✅ CONCLUÍDO     ⏳ EM DESENVOLVIMENTO     ⏹️  PLANEJADO
```

---

## 🛠️ Metodologia

### Técnicas de Modelagem
- **Unidades de análise**: palavras vs sentenças
- **Tipos de aresta**: co-ocorrência, dependência sintática, distância lexical
- **Janelas de contexto**: variações de tamanho

### Tarefas de Avaliação
- Mineração de opinião (polaridade, subjetividade)
- Análise exploratória (comunidades léxicas, padrões discursivos)

---

## 📈 Etapa 1: Coleta e Pré-processamento dos Dados

### 📑 Seleção do Corpus

Inicialmente, buscou-se um conjunto de dados volumoso em tema polêmico no YouTube. O vídeo "‹ CORTANDO O BOTÃO DO YOUTUBE ›" (29M visualizações, 582K comentários) mostrou-se inviável devido às limitações de quota da API.

**Corpus Final Selecionado:**

| Propriedade | Valor |
|:---|:---|
| **Título** | Bolsonaro pergunta para Lula sobre corrupção na Petrobras \| Band Eleições - Debate Presidencial 2022 |
| **Canal** | Band Jornalismo |
| **Visualizações** | 9,6 milhões |
| **Comentários Coletados** | 53.831 |
| **Data** | 2022 |
| **Justificativa** | Tema inerentemente polarizado garante opiniões divergentes |

### ✅ Configuração do Ambiente

- ✓ Ambiente virtual Python
- ✓ Dependências instaladas (NLTK, SpaCy, NetworkX, Pandas, etc)
- ✓ Arquivo `.env` com credenciais e caminhos
- ✓ Conectividade com YouTube Data API v3

### 📥 Etapa 1.1: Extração dos Dados

**Arquivo:** [`python_scripts/data_mining/youtube_scratch.py`](python_scripts/data_mining/youtube_scratch.py)

Implementação utilizando **YouTube Data API v3**:

```
┌──────────────────────────────────────────────────────┐
│  1. Recuperação de Comentários Principais           │
│     └─► commentThreads().list()                     │
│         └─ Metadados: autor, data, conteúdo         │
├──────────────────────────────────────────────────────┤
│  2. Recuperação de Respostas (Replies)              │
│     └─► comments().list()                           │
│         └─ Associação com comentário pai            │
├──────────────────────────────────────────────────────┤
│  3. Armazenamento em DataFrame Pandas               │
├──────────────────────────────────────────────────────┤
│  4. Exportação para CSV                             │
│     📄 comentarios_bruto.csv (53.831 rows)          │
└──────────────────────────────────────────────────────┘

RESULTADO: ✅ 53.831 comentários recuperados
```

### 🔧 Etapa 1.2: Limpeza e Pré-processamento

**Arquivo:** [`python_scripts/pre_processing/clean_data.py`](python_scripts/pre_processing/clean_data.py)

Tratamento com **NLTK (Natural Language Toolkit)**:

#### Pipeline de Limpeza

| # | Etapa | Ferramenta | Resultado |
|:---:|:---|:---|:---|
| 1 | Normalização | `lower()` | Uniformização de texto |
| 2 | Tokenização | `word_tokenize()` | Segmentação em palavras |
| 3 | Remove Stopwords | 207 palavras PT-BR | Eliminação de ruído semântico |
| 4 | Filtragem | `isalnum()` | Apenas tokens válidos |
| 5 | Validação | Checagem de vazios | Garantia de integridade |

**Resultado:** ✅ `comentarios_processados.csv` (53.831 linhas)

#### ⚠️ Limitações Conhecidas

Após limpeza, permanecem:
- Menções a usuários (@username)
- Comentários spam (aleatórios)

*Avaliação: Presença não prejudica análises subsequentes*

---

## 🕸️ Etapa 2-4: Modelagem de Redes Textuais

### 1️⃣ Primeira Rede: Co-ocorrência Simples

**Arquivo:** [`python_scripts/text_network/first_network.py`](python_scripts/text_network/first_network.py)

Prototipagem estabelecendo bases metodológicas:

```
ENTRADA: comentarios_processados.csv (53.831)
    │
    ├─► SpaCy pt_core_news_sm
    │   • Lematização de tokens
    │   • Exclusão de tokens < 2 caracteres
    │
    ├─► Construção do Grafo
    │   • Grafo não-direcionado (NetworkX)
    │   • Aresta = co-ocorrência de palavras
    │   • Peso = frequência conjunta
    │   • Método: itertools.combinations()
    │
    ├─► Filtragem de Ruído
    │   • Remove: peso < 2, grau < 2
    │   • Normaliza pesos para [0, 1]
    │
    └─► SAÍDA: coocorrencia_normalizada.gexf
        (Pronto para Gephi)
```

**Status:** ✅ Concluído

---

### Apresentação WTDCC 2025

**Arquivo:** [`python_scripts/text_network/poster_network.ipynb`](python_scripts/text_network/poster_network.ipynb)

Versão aprimorada com critérios rigorosos:

#### 📊 Configuração

| Parâmetro | Valor | Objetivo |
|:---|:---:|:---|
| **MIN_EDGE_WEIGHT** | 15 | Conexões fortes apenas |
| **TOP_N_NODES** | 200 | Termos principais |
| **Algoritmo** | Louvain | Detecção de comunidades |
| **Resolução** | 1.0 | Granularidade equilibrada |

#### 🔬 Pipeline Completo

1. Lematização otimizada
2. Filtragem manual de ruídos
3. Remoção de duplicatas intra-comentário
4. Construção incremental de grafo
5. Corte de conexões fracas
6. Seleção por centralidade de grau
7. Extração de componente gigante conexo

#### 📈 Resultados Finais

| Métrica | Valor |
|:---|:---:|
| **Nós** | 200 |
| **Arestas** | 10.564 |
| **Modularidade** | 0,0859 |
| **Comunidades** | 4 |
| **Densidade** | Alta |

#### 🎨 Comunidades Identificadas

```
┌─────────────────────────────────────────────────┐
│     ESTRUTURA DO DEBATE (4 COMUNIDADES)         │
├─────────────────────────────────────────────────┤
│                                                 │
│ 🟢 VERDE: Ataques a Políticos                   │
│    └─ Crítica focada em figura política         │
│                                                 │
│ 🟣 ROXO: Pauta Econômica/Social                │
│    └─ Preocupações do cenário nacional          │
│                                                 │
│ 🟠 LARANJA: Discurso Moralizante               │
│    └─ Opinião favorável a candidato específico  │
│                                                 │
│ 🔵 AZUL: Mobilização Ideológica                │
│    └─ Discussão sobre corrupção (tema central)  │
│                                                 │
│ ⚠️  ~50% da rede dominada por grupo que          │
│    desvirtua tema para ataque político          │
│                                                 │
└─────────────────────────────────────────────────┘
```

#### 💡 Interpretação dos Achados

O vídeo sobre corrupção foi usado como **palanque político**:

- ✘ Desvirtua tema principal do debate
- ✘ Concentra-se em ataque ao político interrogado
- ✘ Defende outro político de forma moralizante
- ✘ Marginaliza pauta econômica/social

**Conclusão:** O debate foi apropriado por grupo dominante para disseminação de opiniões sobre candidatos presidenciais.

**Status:** ✅ Concluído e documentado

---

### 3️⃣ Embeddings Semânticos (EM DESENVOLVIMENTO)

**Arquivo:** [`python_scripts/text_network/embedding.py`](python_scripts/text_network/embedding.py)

Representações contínuas dos textos:

#### 🎯 Abordagem

```python
from sentence_transformers import SentenceTransformer

# Modelo multilíngue
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings = model.encode(comentarios)
```

#### 📌 Objetivos

- [ ] Criar vetores de similaridade semântica
- [ ] Clustering de opiniões por tema
- [ ] Base para redes de dependência semântica
- [ ] Análise de evolução de tópicos

#### 🗄️ Armazenamento

- **Banco:** ChromaDB (vector store)
- **Persistência:** `data/chroma.sqlite3`
- **Indexação:** Automática com vetores

**Status:** ⏳ Em desenvolvimento

---

## 📋 Estrutura do Projeto

```
📦 ic/
├── 📄 README.md (este arquivo)
├── 📄 plano_ic.pdf
├── 🐍 python_scripts/
│   ├── data_mining/
│   │   └── youtube_scratch.py          ✅ Coleta de dados
│   ├── pre_processing/
│   │   └── clean_data.py               ✅ Limpeza
│   └── text_network/
│       ├── embedding.py                ⏳ Em desenvolvimento
│       ├── first_network.py            ✅ Primeira rede
│       ├── poster_network.ipynb        ✅ Rede refinada
│       └── testing.py                  🧪 Testes
├── 📊 data/
│   ├── chroma.sqlite3                  (vector store)
│   ├── comentarios_bruto.csv           (53.831 comentários)
│   ├── comentarios_processados.csv     (53.831 limpos)
│   ├── grafo_poster.gexf               (rede visualizável)
│   └── f0c2082e-75b1.../              (cache Chroma)
└── 🎓 wtdcc_2025/                       (conferência)
```

---

## 🔧 Instalação e Configuração

### 📋 Dependências do Projeto

Todas as bibliotecas necessárias estão listadas em [`requirements.txt`](requirements.txt) com suas versões específicas:

```
python-dotenv          # Variáveis de ambiente
pandas                 # Manipulação de dados
tqdm                   # Barras de progresso
nltk                   # NLP em português
spacy                  # Lematização
pt_core_news_sm        # Modelo SpaCy PT
google-api-python-client  # API do YouTube
networkx               # Análise de redes
python-louvain         # Detecção de comunidades
sentence-transformers  # Embeddings
chromadb               # Vector store
matplotlib             # Visualizações
```

### 🚀 Passo a Passo de Instalação

#### 1. Clone o Repositório

```bash
cd /home/eduarda/faculdade/ic
```

#### 2. Crie um Ambiente Virtual

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Instale as Dependências do requirements.txt

```bash
# Upgrade do pip (recomendado)
pip install --upgrade pip

# Instalação de todas as bibliotecas
pip install -r requirements.txt
```

#### 4. Baixe o Modelo SpaCy para Português

```bash
python -m spacy download pt_core_news_sm
```

#### 5. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com:

```bash
API_KEY=seu_api_key_aqui
VIDEO_ID=id_do_video
CLEAN_COMMENTS_PATH=./data/comentarios_processados.csv
DATA_PATH=./data/
```

### ✅ Verificação da Instalação

Para verificar se tudo foi instalado corretamente:

```bash
python -c "import pandas; import nltk; import spacy; import networkx; print('✅ Todas as bibliotecas instaladas com sucesso!')"
```

### 📦 Arquivo requirements.txt

O arquivo [`requirements.txt`](requirements.txt) contém:

- **Versões específicas** de cada biblioteca para garantir compatibilidade
- **Comentários organizados** por categoria (dados, NLP, redes, etc)
- **Notas importantes** sobre downloads adicionais necessários

Para adicionar novas dependências, edite o arquivo e reinstale:

```bash
pip install -r requirements.txt
```

---

### Análise Comparativa

- [ ] Métricas estruturais de redes
- [ ] Centralidade, clusterização, diâmetro
- [ ] Comparação de resultados entre modelagens
- [ ] Tabelas e gráficos comparativos

### Mineração de Opinião

- [ ] Análise de polaridade
- [ ] Detecção de subjetividade
- [ ] Correlação com estrutura de rede
- [ ] Avaliação de desempenho

### Redação Final

- [ ] Integração de resultados
- [ ] Elaboração de diretrizes metodológicas
- [ ] Documentação final
- [ ] Apresentação/Publicação

---

## 📚 Referências

AGGARWAL, Tushar. *NetworkX: A comprehensive guide to mastering network analysis with Python.* Medium, 2023.

BIRD, Steven; KLEIN, Ewan; LOPER, Edward. *NLTK Documentation – Portuguese HOWTO.* [https://www.nltk.org/howto/portuguese_en.html](https://www.nltk.org/howto/portuguese_en.html)

BLONDEL, Vincent D. et al. *Fast unfolding of communities in large networks.* Journal of Statistical Mechanics, v. 2008, n. 10, 2008.

CARVALHO, André C. P. L. F. de; MENEZES, Ângelo G.; BONIDIA, Robson P. *Ciência de Dados: Fundamentos e Aplicações.* 1. ed. LTC, 2024.

GOOGLE DEVELOPERS. *YouTube Data API v3 – Comments.* [https://developers.google.com/youtube/v3/docs/comments/list](https://developers.google.com/youtube/v3/docs/comments/list)

SICSS. *Text Networks.* [https://sicss.io/2018/materials/day3-text-analysis/text-networks/](https://sicss.io/2018/materials/day3-text-analysis/text-networks/)

VEGA, Diego; MAGNANI, Matteo. *Foundations of Temporal Text Networks.* Applied Network Science, v. 3, n. 25, 2018. DOI: [10.1007/s41109-018-0082-3](https://doi.org/10.1007/s41109-018-0082-3)

---

## 📄 Licenças

Este projeto está sendo desenvolvido como parte de pesquisa acadêmica e com apoio da Universidade Federal de Uberlândia e do YouTube Researcher Program.

Para mais informações ou colaborações, entre em contato através do repositório.