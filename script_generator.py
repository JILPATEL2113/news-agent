"""
Claude API se news articles ko Hinglish video script me convert karta hai.
Har news item ke liye: narration line + video keyword (stock footage search ke liye)
"""
import os
import json
import anthropic

SYSTEM_PROMPT = """Tum ek Hindi YouTube news channel ke liye script writer ho.
Tumhe news headlines diye jayenge, tumhe unse ek Hinglish (Hindi + English mix,
Roman script mein) voice-over script banana hai jo casual, engaging aur
easy-to-understand ho - jaise ek YouTuber bolta hai.

STRICT RULES:
- Sirf JSON array return karo, kuch aur text nahi.
- Har news ke liye ek object: {"narration": "...", "keyword": "..."}
- "narration": 2-3 sentences, Hinglish mein, natural bolne wale tone mein
- "keyword": 2-3 English words jo is news se related stock video dhundne ke
  liye use honge (e.g. "stock market", "parliament building", "cricket stadium")
- Ek intro line bhi add karo shuru mein (keyword: "news studio")
- Ek outro line bhi add karo end mein (keyword: "city skyline")
- Total 6-9 items honge (intro + news + outro)
"""


def generate_script(articles):
    client = anthropic.Anthropic()  # ANTHROPIC_API_KEY env var se uthayega

    news_text = "\n".join(
        f"{i+1}. {a['title']} - {a['description']}" for i, a in enumerate(articles)
    )

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Aaj ki top headlines:\n\n{news_text}\n\nAb JSON script banao.",
            }
        ],
    )

    raw = message.content[0].text.strip()
    # Agar model ne markdown fence use kiya ho to hata do
    raw = raw.replace("```json", "").replace("```", "").strip()
    segments = json.loads(raw)
    return segments


if __name__ == "__main__":
    from news_fetcher import fetch_top_headlines

    arts = fetch_top_headlines()
    segs = generate_script(arts)
    print(json.dumps(segs, indent=2, ensure_ascii=False))
