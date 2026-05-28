import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text: str) -> bool:
    """
    Sends a text message to the configured Telegram chat.
    Returns True if successful, False otherwise.
    """
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: Missing Telegram tokens in .env file.")
        return False
        
    # Telegram API endpoint for sending messages
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # The payload (data) we are sending
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        
    }
    
    try:
        response = requests.post(url, data=payload)
        # Check if the request was successful
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to send message: {response.text}")
            return False
    except Exception as e:
        print(f"Error connecting to Telegram API: {e}")
        return False

# --- Testing Block ---
if __name__ == "__main__":
    print("--- Testing Telegram Delivery ---")
    
    test_message = "🤖 *AI News Bot Test*\n\nBhai, ye bot mast chal raha hai! Agar ye message phone pe aa gaya, toh Step 4 clear hai."
    
    print("Sending message to Telegram...")
    if send_telegram_message(test_message):
        print("✅ Message successfully sent! Check your phone.")
    else:
        print("❌ Failed to send message.")