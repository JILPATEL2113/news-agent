"""
YouTube Data API v3 se video upload karta hai.
Pehli baar local machine pe ek interactive login karke 'token.json' banana
padega (README dekho), uske baad GitHub Actions me wahi token.json secret
ke roop me reuse hota hai (auto-refresh hota rahega).
"""
import os
import json
import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def _get_credentials():
    token_json = os.environ["YOUTUBE_TOKEN_JSON"]  # poore token.json ka content, ek env var me
    creds = Credentials.from_authorized_user_info(json.loads(token_json), SCOPES)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return creds


def upload_video(video_path, title, description, tags=None, category_id="25", privacy="public"):
    """
    category_id 25 = News & Politics
    privacy: "public" | "unlisted" | "private"
    """
    creds = _get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Upload progress: {int(status.progress() * 100)}%")

    print(f"Upload complete! Video ID: {response['id']}")
    return response["id"]


if __name__ == "__main__":
    today = datetime.date.today().strftime("%d %b %Y")
    upload_video(
        video_path="output/final_video.mp4",
        title=f"Aaj Ki Top Headlines | {today}",
        description="Daily automated news update. #news #india #headlines",
        tags=["news", "india", "daily news", "top headlines"],
    )
