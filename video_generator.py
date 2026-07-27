"""
1. Har segment ka Hinglish narration -> voice-over (edge-tts, free, Hindi voice)
2. Har segment ke keyword se Pexels se stock video clip download
3. moviepy se sab jodkar final video banata hai, saath mein captions bhi burn-in
"""
import os
import asyncio
import requests
import edge_tts
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips,
    TextClip,
    CompositeVideoClip,
)

VOICE = "hi-IN-MadhurNeural"  # Hindi male voice, Hinglish text ko naturally padh leta hai
WORK_DIR = "work"


def _ensure_dir():
    os.makedirs(WORK_DIR, exist_ok=True)


async def _tts_to_file(text, out_path):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(out_path)


def generate_voiceover(text, index):
    _ensure_dir()
    out_path = os.path.join(WORK_DIR, f"audio_{index}.mp3")
    asyncio.run(_tts_to_file(text, out_path))
    return out_path


def download_stock_clip(keyword, index):
    """Pexels API se keyword ke hisaab se ek vertical/horizontal video clip download karta hai."""
    _ensure_dir()
    api_key = os.environ["PEXELS_API_KEY"]
    resp = requests.get(
        "https://api.pexels.com/videos/search",
        headers={"Authorization": api_key},
        params={"query": keyword, "per_page": 5, "orientation": "landscape"},
        timeout=20,
    )
    resp.raise_for_status()
    videos = resp.json().get("videos", [])
    out_path = os.path.join(WORK_DIR, f"clip_{index}.mp4")

    if not videos:
        return None

    # sabse achi quality wali file dhundo (~HD)
    files = sorted(videos[0]["video_files"], key=lambda f: f.get("width", 0))
    best = next((f for f in files if f.get("width", 0) >= 1280), files[-1])

    with requests.get(best["link"], stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)

    return out_path


def build_segment_clip(video_path, audio_path, caption_text):
    audio = AudioFileClip(audio_path)
    video = VideoFileClip(video_path).without_audio()

    # audio duration ke hisaab se video ko loop/trim karo
    duration = audio.duration
    if video.duration < duration:
        loops = int(duration // video.duration) + 1
        video = concatenate_videoclips([video] * loops)
    video = video.subclip(0, duration).resize(height=1080).set_audio(audio)

    caption = (
        TextClip(
            caption_text,
            fontsize=42,
            color="white",
            font="DejaVu-Sans-Bold",
            method="caption",
            size=(int(video.w * 0.85), None),
            stroke_color="black",
            stroke_width=2,
        )
        .set_position(("center", "bottom"))
        .set_duration(duration)
        .margin(bottom=60, opacity=0)
    )

    return CompositeVideoClip([video, caption])


def assemble_video(segments, output_path="output/final_video.mp4"):
    """
    segments: list of {"narration": str, "keyword": str}
    Har segment ke liye TTS + stock clip banata hai, phir sab jod deta hai.
    """
    os.makedirs("output", exist_ok=True)
    clips = []

    for i, seg in enumerate(segments):
        print(f"[{i+1}/{len(segments)}] Voice-over generate ho raha hai...")
        audio_path = generate_voiceover(seg["narration"], i)

        print(f"[{i+1}/{len(segments)}] Stock clip download ho raha hai ({seg['keyword']})...")
        video_path = download_stock_clip(seg["keyword"], i)
        if video_path is None:
            print(f"  -> koi clip nahi mila '{seg['keyword']}' ke liye, skip.")
            continue

        clips.append(build_segment_clip(video_path, audio_path, seg["narration"]))

    if not clips:
        raise RuntimeError("Koi bhi segment clip nahi ban paya.")

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
    return output_path
