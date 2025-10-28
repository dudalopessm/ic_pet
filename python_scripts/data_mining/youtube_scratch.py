from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import pandas as pd

load_dotenv()

api_key = os.getenv("API_KEY")

youtube = build("youtube", "v3", developerKey=api_key)


def get_video_comments(VIDEO_ID, max_comments=None):
    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet", videoId=VIDEO_ID, maxResults=100, pageToken=next_page_token
        )
        response = request.execute()
        for item in response["items"]:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comment = snippet["textDisplay"]
            date = snippet["publishedAt"]
            comments.append((comment, date))
            if max_comments and len(comments) >= max_comments:
                break
        if max_comments and len(comments) >= max_comments:
            break
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    print(f"Total de comentários: {len(comments)}")
    return comments


comentarios = get_video_comments(VIDEO_ID=os.getenv("VIDEO_ID"))

df = pd.DataFrame(comentarios, columns=["comment", "date"])

csv_path = os.getenv("LOCAL")
csv_dir = os.path.dirname(csv_path)
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print("Comentários salvos em " + csv_path)
