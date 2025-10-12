import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env (contains your GOOGLE_API_KEY)
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Use the correct model name (no "models/" prefix needed)
model = genai.GenerativeModel("models/gemini-2.5-pro")

# Generate text
response = model.generate_content("Write a short greeting message.")

print(response.text)
