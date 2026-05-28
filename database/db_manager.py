import sqlite3

DB_PATH = "ai_news.db"

def init_db():
    """Creates the database and tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table for Articles (Old one)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            published TEXT
        )
    ''')
    
    # NEW Table for Users/Subscribers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            chat_id TEXT PRIMARY KEY
        )
    ''')
    
    conn.commit()
    conn.close()

# --- ARTICLE FUNCTIONS ---
def is_duplicate(link: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM articles WHERE link = ?", (link,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def insert_article(title: str, link: str, published: str) -> bool:
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
        success = False 
    finally:
        conn.close()
    return success

# --- USER FUNCTIONS (NEW) ---
def add_user(chat_id: str) -> bool:
    """Adds a new user to the database. Returns True if new, False if already exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (chat_id) VALUES (?)", (str(chat_id),))
        conn.commit()
        success = True
        print(f"New subscriber added: {chat_id}")
    except sqlite3.IntegrityError:
        success = False # User is already in the database
    finally:
        conn.close()
    return success

def get_all_users() -> list:
    """Returns a list of all subscribed chat_IDs."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

# --- Testing Block ---
if __name__ == "__main__":
    init_db()
    print("Database updated with Users table!")