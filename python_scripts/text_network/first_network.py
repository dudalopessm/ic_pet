import pandas as pd
import networkx as nx
from itertools import combinations
from dotenv import load_dotenv
import os
import spacy

load_dotenv()

COMMENT_COLUMN = "comment"
CLEAN_COMMENTS_PATH = os.getenv("CLEAN_COMMENTS_PATH")

df = pd.read_csv(CLEAN_COMMENTS_PATH)
print("Lendo csv...")
comments = df[COMMENT_COLUMN].astype(str).tolist()

nlp = spacy.load("pt_core_news_sm")

def tokenize(text):
    doc = nlp(text)
    return [token.lemma_.lower() for token in doc if token.text.strip() != ""]

G = nx.Graph()

print("Populando grafo...")
for comment in comments:
    palavras = tokenize(comment)
    palavras = [p for p in palavras if len(p) > 1]  # remove tokens de um caractere

    for w1, w2 in combinations(palavras, 2): # para cada palavra combinada duas a duas -> pega todas as palavras
        if G.has_edge(w1, w2): # se já tiverem aparecido juntas, o peso é incrementado
            G[w1][w2]["weight"] += 1
        else:
            G.add_edge(w1, w2, weight=1) # se não, uma aresta é criada com peso 1

print("Removendo arestas com peso < 2...") # destaca pares de palavras que realmente se repetem em vários comentários = threshold filtering
edges_to_remove = [(u, v) for u, v, w in G.edges(data="weight") if w < 2]
G.remove_edges_from(edges_to_remove)

print("Removendo nós com grau < 2...") # elimina palavras isoladas/pouco citadas
nodes_to_remove = [n for n, d in G.degree() if d < 2]
G.remove_nodes_from(nodes_to_remove)


max_weight = max([G[u][v]["weight"] for u, v in G.edges()]) # peso máximo utilizado para normalização

# normalização para 0 - 1: peso_normal = peso_anterior / peso máximo

print("Normalizando pesos...")
for u, v in G.edges():
    G[u][v]["norm_weight"] = G[u][v]["weight"] / max_weight # normaliza cada peso de aresta

nx.write_gexf(G, "coocorrencia_normalizada.gexf") # exportação em Gephi para visualização

print("Rede exportada para 'coocorrencia_normalizada.gexf'.")