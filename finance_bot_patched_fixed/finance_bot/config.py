import os
from dotenv import load_dotenv

load_dotenv()  # 👈 ВАЖНО

TOKEN = os.getenv("TG_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "TG_BOT_TOKEN environment variable is not set. "
        "Create .env with TG_BOT_TOKEN=... and restart the bot."
    )
