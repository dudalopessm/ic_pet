from dotenv import load_dotenv
import os
import pandas as pd
import spacy
from tqdm import tqdm

load_dotenv()

VERBOS_GENERICOS = {
    "ser", "ter", "estar", "ficar", "ir", "haver", "fazer", "dizer", "achar",
    "ver", "coisa", "gente", "pra", "pro", "aí", "então", "né", "tá", "dar",
    "poder", "querer", "saber", "falar", "usar", "melhor", "pior"
}

nlp = spacy.load("pt_core_news_sm")
nlp.disable_pipes(["parser", "ner"])

def lemmatize_comment(text):
    if not isinstance(text, str) or not text.strip():
        return ""

    doc = nlp(text)
    tokens = []
    for token in doc:
        lemma = token.lemma_.lower()
        if (
            lemma not in VERBOS_GENERICOS
            and not token.is_punct
            and not token.is_space
            and len(lemma) > 2
        ):
            tokens.append(lemma)

    return " ".join(tokens)

def lemmatize_and_save(input_csv, output_csv):
    print(f"Lendo arquivo: {input_csv}")
    df = pd.read_csv(input_csv)
    print(f"Total de comentários carregados: {len(df)}")

    tqdm.pandas(desc="Lematizando")
    df['lemmatized'] = df['comment'].progress_apply(lemmatize_comment)

    df_clean = df[df['lemmatized'].str.len() > 0].copy()
    print(f"Total final após lematização: {len(df_clean)}")

    df_clean = df_clean.drop(columns=['comment'])
    df_clean = df_clean.rename(columns={'lemmatized': 'comment'})

    print(f"\nSalvando arquivo lematizado em: {output_csv}")
    df_clean.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print("Arquivo salvo com sucesso")

lemmatize_and_save("C:\\duda\\faculdade\\ic_pet\\data\\raw\\comentarios_bruto_gillete.csv", "C:\\duda\\faculdade\\ic_pet\\data\\processed\\comentarios_lematizados_gillete.csv")
