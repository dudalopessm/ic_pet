import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()

print("Carregando modelo...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

data_path = os.getenv("DATA_PATH")

client = chromadb.PersistentClient(path=data_path)

collection = client.get_collection(name="communities_collection")

print(f"Conectado. A coleção tem {collection.count()} documentos.")

texto_busca = "lula ladrão"
vetor_busca = model.encode([texto_busca])

results = collection.query(
    query_embeddings=vetor_busca,
    n_results=3,
    include=["documents", "metadatas", "distances"]
)

for i, doc in enumerate(results['documents'][0]):
    print(f"\nResultado {i+1}:")
    print(f"Texto: {doc}")
    print(f"Distância: {results['distances'][0][i]:.4f}")
    print(f"Índice original: {results['metadatas'][0][i]['index']}")