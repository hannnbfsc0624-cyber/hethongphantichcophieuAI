import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv chưa cài cũng không sao, dùng os.environ trực tiếp

PRICE_PROVIDER = os.getenv("PRICE_PROVIDER", "mock")
PRICE_API_BASE_URL = os.getenv("PRICE_API_BASE_URL", "")

NEWS_PROVIDER = os.getenv("NEWS_PROVIDER", "mock")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "false").strip().lower() in ("1", "true", "yes")

CACHE_TTL_PRICE = int(os.getenv("CACHE_TTL_PRICE", "60"))
CACHE_TTL_NEWS = int(os.getenv("CACHE_TTL_NEWS", "300"))
CACHE_TTL_SENTIMENT = int(os.getenv("CACHE_TTL_SENTIMENT", "3600"))
CACHE_TTL_GEMINI = int(os.getenv("CACHE_TTL_GEMINI", "600"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "false").strip().lower() in ("1", "true", "yes")

CACHE_TTL_PRICE = int(os.getenv("CACHE_TTL_PRICE", "60"))
CACHE_TTL_NEWS = int(os.getenv("CACHE_TTL_NEWS", "300"))
CACHE_TTL_SENTIMENT = int(os.getenv("CACHE_TTL_SENTIMENT", "3600"))
CACHE_TTL_GEMINI = int(os.getenv("CACHE_TTL_GEMINI", "600"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "false").strip().lower() in ("1", "true", "yes")

CACHE_TTL_PRICE = int(os.getenv("CACHE_TTL_PRICE", "60"))
CACHE_TTL_NEWS = int(os.getenv("CACHE_TTL_NEWS", "300"))
CACHE_TTL_SENTIMENT = int(os.getenv("CACHE_TTL_SENTIMENT", "3600"))
CACHE_TTL_GEMINI = int(os.getenv("CACHE_TTL_GEMINI", "600"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "false").strip().lower() in ("1", "true", "yes")

CACHE_TTL_PRICE = int(os.getenv("CACHE_TTL_PRICE", "60"))
CACHE_TTL_NEWS = int(os.getenv("CACHE_TTL_NEWS", "300"))
CACHE_TTL_SENTIMENT = int(os.getenv("CACHE_TTL_SENTIMENT", "3600"))
CACHE_TTL_GEMINI = int(os.getenv("CACHE_TTL_GEMINI", "600"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "false").strip().lower() in ("1", "true", "yes")

CACHE_TTL_PRICE = int(os.getenv("CACHE_TTL_PRICE", "60"))
CACHE_TTL_NEWS = int(os.getenv("CACHE_TTL_NEWS", "300"))
CACHE_TTL_SENTIMENT = int(os.getenv("CACHE_TTL_SENTIMENT", "3600"))
CACHE_TTL_GEMINI = int(os.getenv("CACHE_TTL_GEMINI", "600"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "false").strip().lower() in ("1", "true", "yes")

CACHE_TTL_PRICE = int(os.getenv("CACHE_TTL_PRICE", "60"))
CACHE_TTL_NEWS = int(os.getenv("CACHE_TTL_NEWS", "300"))
CACHE_TTL_SENTIMENT = int(os.getenv("CACHE_TTL_SENTIMENT", "3600"))
CACHE_TTL_GEMINI = int(os.getenv("CACHE_TTL_GEMINI", "600"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "false").strip().lower() in ("1", "true", "yes")

CACHE_TTL_PRICE = int(os.getenv("CACHE_TTL_PRICE", "60"))
CACHE_TTL_NEWS = int(os.getenv("CACHE_TTL_NEWS", "300"))
CACHE_TTL_SENTIMENT = int(os.getenv("CACHE_TTL_SENTIMENT", "3600"))
CACHE_TTL_GEMINI = int(os.getenv("CACHE_TTL_GEMINI", "600"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "false").strip().lower() in ("1", "true", "yes")

CACHE_TTL_PRICE = int(os.getenv("CACHE_TTL_PRICE", "60"))
CACHE_TTL_NEWS = int(os.getenv("CACHE_TTL_NEWS", "300"))
CACHE_TTL_SENTIMENT = int(os.getenv("CACHE_TTL_SENTIMENT", "3600"))
CACHE_TTL_GEMINI = int(os.getenv("CACHE_TTL_GEMINI", "600"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "false").strip().lower() in ("1", "true", "yes")

CACHE_TTL_PRICE = int(os.getenv("CACHE_TTL_PRICE", "60"))
CACHE_TTL_NEWS = int(os.getenv("CACHE_TTL_NEWS", "300"))
CACHE_TTL_SENTIMENT = int(os.getenv("CACHE_TTL_SENTIMENT", "3600"))
CACHE_TTL_GEMINI = int(os.getenv("CACHE_TTL_GEMINI", "600"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "false").strip().lower() in ("1", "true", "yes")

CACHE_TTL_PRICE = int(os.getenv("CACHE_TTL_PRICE", "60"))
CACHE_TTL_NEWS = int(os.getenv("CACHE_TTL_NEWS", "300"))
CACHE_TTL_SENTIMENT = int(os.getenv("CACHE_TTL_SENTIMENT", "3600"))
CACHE_TTL_GEMINI = int(os.getenv("CACHE_TTL_GEMINI", "600"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "false").strip().lower() in ("1", "true", "yes")

CACHE_TTL_PRICE = int(os.getenv("CACHE_TTL_PRICE", "60"))
CACHE_TTL_NEWS = int(os.getenv("CACHE_TTL_NEWS", "300"))
CACHE_TTL_SENTIMENT = int(os.getenv("CACHE_TTL_SENTIMENT", "3600"))
CACHE_TTL_GEMINI = int(os.getenv("CACHE_TTL_GEMINI", "600"))

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

FLASK_PORT = int(os.getenv("FLASK_PORT", "8000"))
DB_PATH = os.getenv("DB_PATH", "stock_ai.db")

DEFAULT_WATCHLIST = ["FPT", "HPG", "TCB", "VCB", "VNM", "MWG", "VHM", "SSI"]
