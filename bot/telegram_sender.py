import os
import requests
from dotenv import load_dotenv
from database.db_manager import add_user

load_dotenv()

# Ab humein TELEGRAM_CHAT_ID ki yahan hardcoded zaroorat nahi hai
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def fetch_new_subscribers():
    """
    Checks Telegram for recent messages to find new users who sent /start.
    Saves their chat_id to the database.
    """
    if not BOT_TOKEN:
        print("Error: Bot token missing in .env file.")
        return

    print("Checking Telegram for new subscribers...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            # Extract results (messages sent to the bot)
            for result in data.get("result", []):
                # Ensure the message contains text
                if "message" in result and "text" in result["message"]:
                    text = result["message"]["text"]
                    chat_id = str(result["message"]["chat"]["id"])
                    
                    # If the user sent /start, save them to the DB
                    if text == "/start":
                        add_user(chat_id)
        else:
            print(f"Failed to fetch updates: {response.text}")
    except Exception as e:
        print(f"Error connecting to Telegram API: {e}")

def send_telegram_message(text: str, chat_id: str) -> bool:
    """
    Sends a text message to a specific Telegram chat_id.
    """
    if not BOT_TOKEN:
        return False
        
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to send to {chat_id}: {response.text}")
            return False
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

# --- Testing Block ---
if __name__ == "__main__":
    print("--- Testing Subscriber Fetching ---")
    fetch_new_subscribers()
    print("Check complete!")