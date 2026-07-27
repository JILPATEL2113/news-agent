"""
Poora pipeline ek saath chalata hai: news -> script -> video -> YouTube upload.
Isi file ko GitHub Actions daily cron se run karega.
"""
import datetime
from news_fetcher import fetch_top_headlines
from script_generator import generate_script
from video_generator import assemble_video
from youtube_uploader import upload_video


def run():
    print("Step 1: Top headlines fetch ho rahi hain...")
    articles = fetch_top_headlines(country="in", page_size=6)
    print(f"  {len(articles)} articles mile.")

    print("Step 2: Hinglish script AI se generate ho raha hai...")
    segments = generate_script(articles)
    print(f"  {len(segments)} segments ban gaye.")

    print("Step 3: Video ban raha hai (ismein time lagega)...")
    video_path = assemble_video(segments)
    print(f"  Video ready: {video_path}")

    print("Step 4: YouTube pe upload ho raha hai...")
    today = datetime.date.today().strftime("%d %b %Y")
    title = f"Aaj Ki Top Headlines | {today}"
    description = (
        "Daily automated news roundup - AI se generate hua hai.\n\n"
        + "\n".join(f"- {a['title']} ({a['source']})" for a in articles)
        + "\n\n#news #india #dailynews #headlines"
    )
    video_id = upload_video(
        video_path=video_path,
        title=title,
        description=description,
        tags=["news", "india", "daily news", "top headlines", "hindi news"],
        privacy="public",  # testing ke waqt "private" rakho
    )
    print(f"Done! https://youtu.be/{video_id}")


if __name__ == "__main__":
    run()
