# 🤖 Automated AI/ML News Aggregator

An automated data pipeline that fetches the latest AI/ML research and news, summarizes them using the Gemini AI API, and delivers them directly to a Telegram chat. 

## ✨ Features
- **Automated Scraping:** Fetches top daily articles via RSS feeds (e.g., ArXiv AI papers).
- **Smart Summarization:** Uses Google's `gemini-2.5-flash` model to generate crisp, 3-bullet-point technical summaries.
- **Duplicate Prevention:** Integrated SQLite database acts as a memory layer to ensure no article is sent twice.
- **Telegram Delivery:** Seamlessly delivers formatted alerts directly to mobile.
- **CI/CD Automation:** Fully automated via GitHub Actions (Runs daily at 8:00 AM IST without any manual intervention).

## 🛠️ Tech Stack
- **Language:** Python
- **AI Processing:** Google Gemini API
- **Database:** SQLite
- **Automation:** GitHub Actions (Cron Jobs)
- **Libraries:** `feedparser`, `google-generativeai`, `requests`, `python-dotenv`

## 🚀 How It Works
1. GitHub Actions triggers `main.py` every morning.
2. The script parses the target RSS feed for new items.
3. It checks the SQLite database to filter out previously processed links.
4. New links are sent to the Gemini API for a quick technical breakdown.
5. The final summarized report is pushed via the Telegram Bot API.