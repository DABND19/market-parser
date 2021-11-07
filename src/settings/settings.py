from os import environ


SCRAPER_API_KEY = 'fa47308daf41ce270c7ab2b6f44f35fa'

BOT_TOKEN = environ.get("BOT_TOKEN")

DB_USER = environ.get("DB_USER", "postgres")
DB_PASSWORD = environ.get("DB_PASSWORD", "123456")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_PORT = environ.get("DB_PORT", "5432")
DB_NAME = environ.get("DB_NAME", "postgres")

REDIS_HOST = environ.get("REDIS_HOST", "localhost")

NGINX_HOST = environ.get("NGINX_HOST", "localhost")
NGINX_PORT = environ.get("NGINX_PORT", "8443")

try:
    from .settings_local import *
except ImportError:
    pass

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
WEBHOOK_URL = f"https://{NGINX_HOST}:{NGINX_PORT}/"