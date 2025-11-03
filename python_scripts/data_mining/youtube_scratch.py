from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

load_dotenv()

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

def save_csv(df, csv_path_base, csv_dir, nome_sufixo, colunas_para_salvar):
    final_path = csv_path_base.replace(".csv", nome_sufixo + ".csv")

    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    try:
        df.to_csv(final_path, columns=colunas_para_salvar, index=False, encoding="utf-8-sig")
        print(f"Arquivo salvo com sucesso em: {final_path}")
        return final_path
    except KeyError:
        print(f"Erro ao salvar CSV")
        return None

csv_path = os.getenv("LOCAL")
csv_dir = os.path.dirname(csv_path)

print(f"Iniciando coleta de dados...")
raw_comments = get_video_comments(VIDEO_ID=os.getenv("VIDEO_ID1"))
df = pd.DataFrame(raw_comments, columns=["comment", "date"])
print(f"Total de comentários capturados: {len(df)}")

save_csv(df, csv_path, csv_dir, nome_sufixo="_bruto", colunas_para_salvar=['date', 'comment'])