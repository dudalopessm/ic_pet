from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

load_dotenv()

# só necessário na primeira vez
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Baixando stopwords...")
    nltk.download('stopwords')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Baixando tokenizador punkt...")
    nltk.download('punkt')

api_key = os.getenv("API_KEY")

youtube = build("youtube", "v3", developerKey=api_key)


def get_video_comments(VIDEO_ID, max_comments=None):
    comments = []
    next_page_token = None
    stop = False

    while True:
        try:
            request = youtube.commentThreads().list(
            part="snippet", 
            videoId=VIDEO_ID, 
            maxResults=100,  
            order="time", 
            textFormat="plainText",
            pageToken=next_page_token
        )
            response = request.execute()
        except HttpError as e:
            print(f"Erro: {e}")
            print("Causa provável: Cota da API excedida ou vídeo/comentários indisponíveis.")
            print("Salvando progresso parcial...")
            stop = True
        except Exception as e:
            print(f"Erro: {e}")
            print("Salvando progresso parcial...")
            stop = True

        if stop == True:
            break

        for item in response["items"]:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comment = snippet["textDisplay"]
            date = snippet["publishedAt"]
            comments.append((comment, date))

            if max_comments and len(comments) >= max_comments:
                stop = True
                break

            topLevelCommentId = item["snippet"]["topLevelComment"]["id"]

            if item["snippet"]["totalReplyCount"] > 0:
                replies_page_token = None

                while True:
                    try:
                        request_reply = youtube.comments().list(
                        part="snippet",
                        parentId=topLevelCommentId,
                        maxResults=100,
                        textFormat="plainText",
                        pageToken=replies_page_token
                    )
                        response_reply = request_reply.execute()
                    except HttpError as e:
                        print(f"Erro: {e}")
                        print("Ignorando respostas deste comentário e continuando...")
                        break 
                    except Exception as e:
                        print(f"!!! ERRO INESPERADO (Chamada de Respostas) !!!")
                        print(f"Erro: {e}")
                        print("Ignorando respostas deste comentário e continuando...")
                        break

                    for reply_item in response_reply["items"]:
                        reply_snippet = reply_item["snippet"]
                        comment = reply_snippet["textDisplay"]
                        date = reply_snippet["publishedAt"]
                        comments.append((comment, date))

                        if max_comments and len(comments) >= max_comments:
                            stop = True
                            break

                    if stop == True:
                        break

                    replies_page_token = response_reply.get("nextPageToken")
                    if not replies_page_token:
                        break

                if stop == True:
                    break
        if stop == True:
            break

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    print(f"Coleta finalizada ou interrompida. Total de comentários capturados: {len(comments)}")
    return comments

print(f"Iniciando coleta de dados...")
raw_comments = get_video_comments(VIDEO_ID=os.getenv("VIDEO_ID"))

df = pd.DataFrame(raw_comments, columns=["comment", "date"])
print(f"Total de comentários capturados: {len(df)}")

def data_cleaning(df):
    laughs = r'^((k+)|(ha)+|(rs)+|\s+)+$'
    laughs_index = df['comment'].str.match(laughs, case=False, na=False)

    emojis_and_blank = (
        r'^['
        r'\s'                     # Blank spaces
        r'\U0001F600-\U0001F64F'  # Emoticons
        r'\U0001F300-\U0001F5FF'  # Symbols & Pictographs
        r'\U0001F680-\U0001F6FF'  # Transport & Map Symbols
        r'\U0001F1E0-\U0001F1FF'  # Flags (iOS)
        r'\U00002702-\U000027B0'
        r'\U000024C2-\U0001F251'
        r']+$'
    )
    emojis_blank_index = df['comment'].str.match(emojis_and_blank, na=False)

    remove = laughs_index | emojis_blank_index

    new_df = df[~remove].copy()

    print(f"Total de comentários após filtro: {len(new_df)}")
    return new_df

df = data_cleaning(df)

stopwords_portugues = set(stopwords.words('portuguese'))

def cleaning_comments(text):
    if not isinstance(text, str):
        return ""

    lower_text = text.lower()
    tokens = word_tokenize(lower_text, language='portuguese')
    filtred_tokens = [
        palavra for palavra in tokens 
        if palavra.isalnum() and palavra not in stopwords_portugues
    ]

    return " ".join(filtred_tokens)

df['clean_comment'] = df['comment'].apply(cleaning_comments)


def save_csv(df, csv_path, csv_dir):
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    columns = ['date', 'comment', 'clean_comment']
    df.to_csv(csv_path, columns=columns, index=False, encoding="utf-8-sig")
    print("Comentários salvos em " + csv_path)
    return csv_path

csv_path = os.getenv("LOCAL")
csv_dir = os.path.dirname(csv_path)

save_csv(df, csv_path, csv_dir)