# 🤖 AI/ML News Broadcast Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Gemini AI](https://img.shields.io/badge/AI-Google_Gemini_2.5-orange.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-green.svg)
![Telegram API](https://img.shields.io/badge/Delivery-Telegram_Bot-blue.svg)

An end-to-end, scalable data pipeline that aggregates the latest Artificial Intelligence and Machine Learning research, processes the text using Large Language Models (LLMs), and broadcasts structured summaries to multiple subscribers via a Telegram Bot.

## 🏗️ System Architecture

1. **Data Ingestion:** Extracts daily XML/RSS feeds from research repositories (e.g., ArXiv).
2. **State Management:** Interacts with a SQLite database to maintain a history of processed URLs, ensuring zero duplicate processing.
3. **Dynamic User Management:** Automatically fetches new bot subscribers via Telegram's `getUpdates` API and registers their Chat IDs into the database.
4. **AI Processing:** Routes new content to the Google Gemini 2.5 Flash API with a custom system prompt to generate concise, 3-bullet-point technical summaries.
5. **Broadcast Delivery:** Pushes the final formatted payload to all registered subscribers via Telegram webhooks in a controlled loop.
6. **Orchestration:** Scheduled via GitHub Actions (Cron Jobs) to run daily at 8:00 AM IST with zero manual intervention.

## ✨ Key Engineering Features
- **Idempotent Execution:** Database layer guarantees that multiple runs don't result in duplicate alerts.
- **Auto-Scaling Audience:** Seamlessly handles new users. Anyone who sends `/start` to the bot is automatically enrolled for the next daily broadcast.
- **Prompt Engineering:** Optimized system instructions for the LLM to extract only high-value information (Context, Importance, Impact).
- **Secure Secrets Management:** API keys and tokens are strictly handled via environment variables and GitHub Secrets.
- **Serverless Cloud Deployment:** Completely cloud-native execution without requiring a dedicated 24/7 hosting server.

## 🛠️ Technology Stack
- **Core:** Python
- **Libraries:** `feedparser`, `requests`, `google-generativeai`, `python-dotenv`
- **Database:** SQLite3 (Relational Database)
- **CI/CD & Automation:** GitHub Actions Workflows

## 🚀 Local Setup & Installation

If you want to run or test this pipeline locally:

1. **Clone the repository:**
   `git clone https://github.com/ankitsingh127/ai-news-aggregator.git`
   `cd ai-news-aggregator`

2. **Set up the virtual environment:**
   `python -m venv venv`
   `venv\Scripts\activate`

3. **Install dependencies:**
   `pip install -r requirements.txt`

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your keys:
   `GEMINI_API_KEY=your_gemini_api_key_here`
   `TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here`

5. **Test the Pipeline:**
   Ensure you have sent `/start` to your Telegram Bot, then run:
   `python main.py`

## 🔮 Future Scope
- Integrating **Playwright** to scrape dynamic, non-RSS websites.
- Adding categorized subscriptions (e.g., users can type `/nlp` or `/vision` to get specific news).
- Migrating SQLite to PostgreSQL for larger subscriber bases.
