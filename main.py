import time
from scrapers.rss_scraper import fetch_rss_news
from database.db_manager import init_db, insert_article
from ai_processor.summarizer import summarize_news
from bot.telegram_sender import send_telegram_message

# Hum ArXiv ki AI feed use kar rahe hain
TARGET_FEED = "http://export.arxiv.org/rss/cs.AI"

def main():
    print("🚀 Starting AI News Aggregator Pipeline...")
    
    # 1. Initialize DB (Creates table if it doesn't exist)
    init_db()
    
    # 2. Fetch the top 5 latest news articles
    print(f"Fetching news from {TARGET_FEED}...")
    articles = fetch_rss_news(TARGET_FEED, max_items=5)
    
    if not articles:
        print("No articles found today.")
        return

    new_articles_count = 0

    # 3. Process each article one by one
    for article in articles:
        title = article['title']
        link = article['link']
        published = article['published']
        
        # 4. Check Database to prevent duplicates
        if insert_article(title, link, published):
            new_articles_count += 1
            print(f"\n📰 New Article: {title}")
            print("🧠 Generating Gemini Summary...")
            
            # 5. Summarize using AI
            summary = summarize_news(title, link)
            
            # 6. Format message nicely for Telegram
            telegram_msg = f"🗞️ {title}\n\n{summary}\n\n🔗 Read Paper: {link}"
            
            # 7. Send to Telegram
            print("📲 Delivering to Telegram...")
            send_telegram_message(telegram_msg)
            
            # Small delay to avoid hitting rate limits on APIs
            time.sleep(3)
        else:
            # If insert_article returns False, it's a duplicate
            print(f"⏩ Skipped (Already processed): {title}")

    print(f"\n✅ Pipeline Complete! Delivered {new_articles_count} new updates.")

if __name__ == "__main__":
    main()