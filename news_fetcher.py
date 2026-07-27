"""
News fetch karta hai India ke top headlines - NewsAPI.org se (free tier).
Free API key yahan se lo: https://newsapi.org/register
"""
import os
import requests


def fetch_top_headlines(country="in", category=None, page_size=6):
    """
    NewsAPI se top headlines fetch karta hai.
    Returns list of dicts: [{title, description, source, url}, ...]
    """
    api_key = os.environ["NEWS_API_KEY"]
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": country,
        "pageSize": page_size,
        "apiKey": api_key,
    }
    if category:
        params["category"] = category

    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    articles = []
    for a in data.get("articles", []):
        if not a.get("title") or a.get("title") == "[Removed]":
            continue
        articles.append(
            {
                "title": a["title"],
                "description": a.get("description") or "",
                "source": a.get("source", {}).get("name", ""),
                "url": a.get("url", ""),
            }
        )
    return articles


if __name__ == "__main__":
    for item in fetch_top_headlines():
        print("-", item["title"])
