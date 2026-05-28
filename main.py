import time
from scrapers.rss_scraper import fetch_rss_news
from database.db_manager import init_db, insert_article, get_all_users
from ai_processor.summarizer import summarize_news
from bot.telegram_sender import send_telegram_message, fetch_new_subscribers

# 🌍 MULTI-SOURCE FEEDS (The "Whole Internet" approach)
RSS_FEEDS = [
    # 1. Google News (Aggregates ALL general websites/news for "Artificial Intelligence" in last 24h)
    "https://news.google.com/rss/search?q=Artificial+Intelligence+when:24h&hl=en-US&gl=US&ceid=US:en",
    # 2. TechCrunch (For startup/industry AI news)
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    # 3. ArXiv (For hardcore research papers)
    "http://export.arxiv.org/rss/cs.AI"
]

def main():
    print("🚀 Starting AI News Aggregator Pipeline...")
    
    # 1. Initialize DB (Tables: articles, users)
    init_db()
    
    # 2. ⚡ Check for new users who pressed /start in the last 24 hours
    fetch_new_subscribers()
    
    # 3. Get the list of all subscribed users from the database
    subscribers = get_all_users()
    if not subscribers:
        print("No subscribers found in database. Exiting...")
        return
        
    print(f"Total active subscribers: {len(subscribers)}")
    new_articles_count = 0

    # 4. ⚡ LOOP THROUGH ALL FEEDS IN THE INTERNET
    for feed_url in RSS_FEEDS:
        print(f"\n📡 Fetching news from {feed_url[:40]}...")
        
        # Har website se top 2 latest khabre uthayenge taaki spam na ho
        articles = fetch_rss_news(feed_url, max_items=2) 
        
        if not articles:
            print("No articles found in this feed today.")
            continue

        # 5. Process each article one by one
        for article in articles:
            title = article['title']
            link = article['link']
            published = article['published']
            
            # 6. Check Database to prevent sending duplicate news
            if insert_article(title, link, published):
                new_articles_count += 1
                print(f"\n📰 Processing: {title}")
                print("🧠 Generating Gemini Summary...")
                
                summary = summarize_news(title, link)
                telegram_msg = f"🗞️ {title}\n\n{summary}\n\n🔗 Read Full: {link}"
                
                print("📲 Broadcasting to all subscribers...")
                
                # 7. ⚡ BROADCAST LOOP: Send the message to EVERY user in the database
                for chat_id in subscribers:
                    send_telegram_message(telegram_msg, chat_id)
                    # Small delay to avoid Telegram blocking us for spamming too fast
                    time.sleep(1) 
                    
                # Extra delay before processing the next article
                time.sleep(3)
            else:
                print(f"⏩ Skipped (Already sent): {title}")

    print(f"\n✅ Pipeline Complete! Delivered {new_articles_count} fresh updates from the internet to {len(subscribers)} users.")

if __name__ == "__main__":
    main()