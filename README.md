# Daily News Video Agent

Roz automatic: News fetch → Hinglish script (AI) → Voice-over → Stock footage →
Video assemble → YouTube upload. GitHub Actions par free me chalta hai, aapke
computer ki zaroorat nahi (setup ke ek step ke alawa).

## Kya-kya chahiye (sab free tier mein available hai)

| Service | Kis liye | Free limit |
|---|---|---|
| [NewsAPI.org](https://newsapi.org/register) | Top headlines | 100 requests/day |
| [Anthropic Console](https://console.anthropic.com/) | Hinglish script likhna | Pay-as-you-go, bahut sasta (~₹1-2/video) |
| [Pexels API](https://www.pexels.com/api/) | Stock video clips | Free, unlimited |
| YouTube Data API (Google Cloud) | Auto-upload | 10,000 units/day free (1 upload ~1600 units) |

## Setup Steps

### 1. Repo GitHub par push karo
```bash
git init
git add .
git commit -m "Daily news video agent"
git remote add origin <tumhara-repo-url>
git push -u origin main
```

### 2. API keys lo
- **NewsAPI**: signup karo, dashboard se key copy karo.
- **Anthropic**: [console.anthropic.com](https://console.anthropic.com) par API key banao.
- **Pexels**: [pexels.com/api](https://www.pexels.com/api/) par free signup, key milegi.

### 3. YouTube OAuth setup (thoda lamba hai, ek hi baar karna hai)
1. [Google Cloud Console](https://console.cloud.google.com/) par naya project banao.
2. "YouTube Data API v3" enable karo (APIs & Services → Library).
3. OAuth consent screen banao (External, Testing mode chalega).
4. Credentials → Create Credentials → OAuth client ID → "Desktop app".
5. JSON download karo, naam do `client_secret.json`, `src/` folder me daalo.
6. Apne computer par:
   ```bash
   cd src
   pip install -r ../requirements.txt
   python get_youtube_token.py
   ```
   Browser khulega, apne uss Google account se login karo jispe YouTube channel hai.
7. `token.json` ban jayegi - iska pura content copy kar lo.

### 4. GitHub Secrets add karo
Repo → Settings → Secrets and variables → Actions → "New repository secret":

| Secret name | Value |
|---|---|
| `NEWS_API_KEY` | NewsAPI wali key |
| `ANTHROPIC_API_KEY` | Anthropic console wali key |
| `PEXELS_API_KEY` | Pexels wali key |
| `YOUTUBE_TOKEN_JSON` | token.json ka **pura content** (paste as-is) |

### 5. Test run karo
Repo → Actions tab → "Daily News Video Upload" → "Run workflow" (manual trigger).
Pehli baar test karne ke liye `src/main.py` me `privacy="public"` ko
`privacy="private"` kar do, taaki galti se live na chala jaye.

### 6. Schedule check karo
`.github/workflows/daily_upload.yml` me cron time set hai **subah 7:30 AM IST**.
Badalna ho to `cron: "0 2 * * *"` line edit karo — [crontab.guru](https://crontab.guru)
se time calculate kar sakte ho (GitHub Actions UTC time use karta hai).

## Important Notes
- **YouTube token expire ho sakta hai** agar OAuth app "Testing" mode me hai
  (7 din me expire hota hai). Consent screen ko "In production" karo taaki
  token har baar auto-refresh hota rahe, expire na ho.
- Video quality/style badalne ke liye `src/video_generator.py` me resolution,
  font, ya voice (`VOICE` variable) change kar sakte ho.
- News category badalni ho to `main.py` me `fetch_top_headlines(category="business")`
  jaisa kuch pass karo (options: business, entertainment, health, science, sports, technology).
- **Copyright dhyan rakhna**: Pexels clips free-to-use hain, lekin news content
  khud AI-summarized/paraphrased hai — kisi article ko word-for-word copy mat karna.

## Local test (bina upload ke)
```bash
cd src
export NEWS_API_KEY=xxx ANTHROPIC_API_KEY=xxx PEXELS_API_KEY=xxx
python -c "from news_fetcher import fetch_top_headlines; from script_generator import generate_script; import json; print(json.dumps(generate_script(fetch_top_headlines()), indent=2, ensure_ascii=False))"
```
