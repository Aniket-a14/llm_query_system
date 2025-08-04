import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)  # ✅ Proper setup

def get_supported_model(preferred="gemini-1.5-pro-latest"):
    try:
        models = [m.name for m in genai.list_models()]
        for m in models:
            if preferred in m:
                return m
        return models[0] if models else preferred
    except Exception as e:
        print(f"Error listing models: {e}")
        return preferred

GEMINI_MODEL = get_supported_model()
print("Model in use:", GEMINI_MODEL)
