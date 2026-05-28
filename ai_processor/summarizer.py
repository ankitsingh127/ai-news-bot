import os
import google.generativeai as genai
from dotenv import load_dotenv

# Ye function .env file se humari API key securely load karega
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing! Check your .env file.")

# Gemini AI ko configure karte hain
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash')

def summarize_news(title: str, link: str) -> str:
    """
    Takes a news title and asks Gemini to generate a short, crisp summary.
    """
    prompt = f"""
    You are an expert AI/ML technical assistant. 
    I have an AI/ML news article with the following title: "{title}"
    
    Please provide:
    1. A one-sentence explanation of what this likely means.
    2. Why this is important for an AI developer/student.
    Keep the entire response under 3 short bullet points. Be concise.
    """
    
    try:
        # Calling the Gemini API
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error from AI API: {e}")
        return "Could not generate summary."

# --- Testing Block ---
if __name__ == "__main__":
    print("--- Testing Gemini AI Summarizer ---")
    
    # Ek dummy news title de kar test karte hain
    test_title = "OpenAI releases new GPT-4o model with real-time audio and vision capabilities"
    test_link = "https://dummy-link.com"
    
    print(f"Original Title: {test_title}\n")
    print("Generating summary... (Please wait a second)\n")
    
    summary = summarize_news(test_title, test_link)
    print(summary)