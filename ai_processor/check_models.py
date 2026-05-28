import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("--- Checking Available Models ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
    print("---------------------------------")
except Exception as e:
    print(f"Error fetching models: {e}")