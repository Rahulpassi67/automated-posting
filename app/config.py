
import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)

# Application settings
APP_NAME = os.getenv("APP_NAME", "Dxora")
APP_ENV = os.getenv("APP_ENV", "development")

DEBUG = os.getenv("DEBUG", "false").lower() in (
    "true", "1", "yes"
)

# FastAPI server settings
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Facebook Pages settings
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")

# Threads settings
THREADS_USER_ID = os.getenv("THREADS_USER_ID")
THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN")

# Bluesky settings
BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")

# Mastodon settings
MASTODON_BASE_URL = os.getenv("MASTODON_BASE_URL")
MASTODON_ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")

# Telegram settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")