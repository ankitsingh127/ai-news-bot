import sqlite3

# This will create a file named 'ai_news.db' in your main project folder
DB_PATH = "ai_news.db"

def init_db():
    """Creates the database and the table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # We make 'link' UNIQUE so the database automatically rejects duplicates
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            published TEXT
        )
    ''')
    conn.commit()
    conn.close()

def is_duplicate(link: str) -> bool:
    """Checks if an article link is already in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM articles WHERE link = ?", (link,))
    result = cursor.fetchone()
    
    conn.close()
    return result is not None

def insert_article(title: str, link: str, published: str) -> bool:
    """Inserts a new article. Returns True if successful, False if duplicate."""
    if is_duplicate(link):
        return False
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO articles (title, link, published) VALUES (?, ?, ?)",
            (title, link, published)
        )
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        # Extra safety net in case of a collision
        success = False 
    finally:
        conn.close()
        
    return success

# --- Testing Block ---
if __name__ == "__main__":
    print("--- Setting up Database ---")
    init_db()
    print("Database initialized!")
    
    test_title = "Dummy AI Research Paper"
    test_link = "https://arxiv.org/abs/dummy"
    test_date = "2026-05-28"
    
    print("\n1. Inserting article for the first time:")
    if insert_article(test_title, test_link, test_date):
        print("✅ Success! Article added.")
    else:
        print("❌ Failed or Duplicate.")
        
    print("\n2. Trying to insert the exact same article again:")
    if insert_article(test_title, test_link, test_date):
        print("❌ Wait, this shouldn't happen!")
    else:
        print("✅ Blocked! Duplicate prevented successfully.")