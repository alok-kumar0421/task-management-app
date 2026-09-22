import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    PORT = int(os.environ.get("PORT", 5000))
    GMAIL_TOKEN_JSON = os.environ.get("GMAIL_TOKEN_JSON")
