import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load your API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create model object (✅ Correct format for latest API)
model = genai.GenerativeModel("models/gemini-2.5-pro")

# Generate text
response = model.generate_content("Hello Gemini! How are you today?")
print(response.text)


