from dotenv import load_dotenv
import os

load_dotenv()

WS_HOST = os.environ.get("WS_HOST", "localhost")
WS_PORT = int(os.environ.get("WS_PORT", 8080))
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
MAX_CONNECTIONS = int(os.environ.get("MAX_CONNECTIONS", 1000))
FIBONACCI_CACHE_SIZE = int(os.environ.get("FIBONACCI_CACHE_SIZE", 100))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
