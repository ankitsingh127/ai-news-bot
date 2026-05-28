import feedparser

def fetch_rss_news(feed_url: str, max_items: int = 5) -> list:
    """
    Fetches and parses an RSS feed, returning the top news items.
    """
    print(f"Fetching news from: {feed_url} ...")
    feed = feedparser.parse(feed_url)
    
    news_list = []
    
    # Check if the feed was successfully parsed and has entries
    if not feed.entries:
        print("No entries found or invalid feed URL.")
        return news_list
        
    # Loop through the entries up to our max_items limit
    for entry in feed.entries[:max_items]:
        news_item = {
            "title": entry.get("title", "No Title"),
            "link": entry.get("link", "No Link"),
            "published": entry.get("published", "No Date")
        }
        news_list.append(news_item)
        
    return news_list

# --- Testing Block ---
# This block only runs if you execute this file directly.
# It will NOT run when we import this function into main.py later.
if __name__ == "__main__":
    # Let's test it using ArXiv's AI/ML research paper feed
    TEST_FEED_URL = "http://export.arxiv.org/rss/cs.AI"
    
    articles = fetch_rss_news(TEST_FEED_URL, max_items=3)
    
    print("\n--- Extracted AI News ---")
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   Link: {article['link']}")
        print(f"   Date: {article['published']}\n")