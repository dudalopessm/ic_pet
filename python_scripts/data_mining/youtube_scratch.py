from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

load_dotenv(override=True)

api_key = os.getenv("API_KEY")

youtube = build("youtube", "v3", developerKey=api_key)

def _fetch_replies(top_level_comment_id, comments, max_comments):
    replies_page_token = None
    while True:
        try:
            response = youtube.comments().list(
                part="snippet",
                parentId=top_level_comment_id,
                maxResults=100,
                textFormat="plainText",
                pageToken=replies_page_token
            ).execute()
        except Exception as e:
            print(f"Erro: {e}\nIgnorando respostas deste comentário e continuando...")
            break

        for reply_item in response["items"]:
            snippet = reply_item["snippet"]
            comments.append((snippet["textDisplay"], snippet["publishedAt"]))
            if max_comments and len(comments) >= max_comments:
                return

        replies_page_token = response.get("nextPageToken")
        if not replies_page_token:
            break


def _process_page(items, comments, max_comments):
    for item in items:
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append((snippet["textDisplay"], snippet["publishedAt"]))

        if max_comments and len(comments) >= max_comments:
            return True

        if item["snippet"]["totalReplyCount"] > 0:
            _fetch_replies(item["snippet"]["topLevelComment"]["id"], comments, max_comments)
            if max_comments and len(comments) >= max_comments:
                return True

    return False


def get_video_comments(video_id, max_comments=None):
    comments = []
    next_page_token = None

    while True:
        try:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                order="time",
                textFormat="plainText",
                pageToken=next_page_token
            ).execute()
        except HttpError as e:
            print(f"Erro: {e}\nCausa provável: Cota da API excedida ou vídeo/comentários indisponíveis.\nSalvando progresso parcial...")
            break
        except Exception as e:
            print(f"Erro: {e}\nSalvando progresso parcial...")
            break

        if _process_page(response["items"], comments, max_comments):
            break

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    print(f"Coleta finalizada ou interrompida. Total de comentários capturados: {len(comments)}")
    return comments

def save_csv(df, csv_path_base, csv_dir, nome_sufixo, colunas_para_salvar):
    final_path = csv_path_base.replace(".csv", nome_sufixo + ".csv")

    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    try:
        df.to_csv(final_path, columns=colunas_para_salvar, index=False, encoding="utf-8-sig")
        print(f"Arquivo salvo com sucesso em: {final_path}")
        return final_path
    except KeyError:
        print("Erro ao salvar CSV")
        return None

csv_path = os.getenv("LOCAL")
csv_dir = os.path.dirname(csv_path)

print("Iniciando coleta de dados...")
raw_comments = get_video_comments(video_id=os.getenv("VIDEO_ID2"))
df = pd.DataFrame(raw_comments, columns=["comment", "date"])
print(f"Total de comentários capturados: {len(df)}")

save_csv(df, csv_path, csv_dir, nome_sufixo="_bruto_aruan", colunas_para_salvar=['date', 'comment'])
