# libraries
import hashlib
import random
import torch
from sentence_transformers import SentenceTransformer
import pandas as pd
from dotenv import load_dotenv
import os
import chromadb
from chromadb import Settings
import numpy as np

load_dotenv()

csv_path = "C:\\duda\\faculdade\\ic_pet\\data\\processed\\comentarios_processados_debate.csv"
data_path = os.getenv("DATA_PATH")
chroma_collection = "communities_collection_debate"

# random seed
random_seed = 42
random.seed(random_seed)
np.random.seed(random_seed)

torch.manual_seed(random_seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(random_seed)

# loading sentence transformer model
model = SentenceTransformer('BAAI/bge-m3')

# loading input data
df = pd.read_csv(csv_path)
df['comment'] = df['comment'].fillna("").astype(str)
texts = df['comment'].tolist()

print("Embeddando")
# embbedings
embeddings = model.encode(texts,
                          show_progress_bar=True,
                          batch_size=16,
                          device='cpu')
print(embeddings.shape)

# armazenando em ChromaDB
client = chromadb.PersistentClient(path=data_path, settings=Settings(anonymized_telemetry=False))

collection = client.get_or_create_collection(name=chroma_collection, metadata={"hnsw:space": "cosine"})

ids = [hashlib.md5(text.encode()).hexdigest() for text in texts]
metadata = [{"date": str(df['date'].iloc[i])} for i in range(len(texts))]

# armazenando de 5000 em 5000
batch_size = 5000
total_docs = len(texts)

print("Armazenando")
for i in range(0, total_docs, batch_size):
    end_index = min(i + batch_size, total_docs) # 

    batch_texts = texts[i:end_index]
    batch_ids = ids[i:end_index]
    batch_metadata = metadata[i:end_index]
    batch_embeddings = embeddings[i:end_index].tolist()

    collection.add(
        documents=batch_texts,
        embeddings=batch_embeddings,
        metadatas=batch_metadata,
        ids=batch_ids
    )
print("Concluído")