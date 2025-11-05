from dotenv import load_dotenv
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm import tqdm

load_dotenv()

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

stopwords_portugues = set(stopwords.words('portuguese'))

def cleaning_comments(text):
    if not isinstance(text, str) or not text.strip():
        return ""
    
    lower_text = text.lower()
    tokens = word_tokenize(lower_text, language='portuguese')
    filtred_tokens = [
        palavra for palavra in tokens 
        if palavra.isalnum() and palavra not in stopwords_portugues
    ]
    return " ".join(filtred_tokens)

def clean_and_save(input_csv, output_csv):
    print(f"Lendo arquivo: {input_csv}")
    df = pd.read_csv(input_csv)
    print(f"Total de comentários carregados: {len(df)}")
    
    print("\nRemovendo stopwords...")
    tqdm.pandas(desc="Processando")
    df['clean_comment'] = df['comment'].progress_apply(cleaning_comments)

    df_clean = df[df['clean_comment'].str.len() > 0].copy()
    print(f"Total final após remoção de stopwords: {len(df_clean)}")

    df_clean = df_clean.drop(columns=['comment'])
    df_clean = df_clean.rename(columns={'clean_comment': 'comment'})
    
    print(f"\nSalvando arquivo limpo em: {output_csv}")
    df_clean.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"Arquivo salvo com sucesso")

clean_and_save(os.getenv("DEFAULT_INPUT"), os.getenv("DEFAULT_OUTPUT"))