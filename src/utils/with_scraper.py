from settings import SCRAPER_API_KEY


def with_scraper_api(url: str) -> str:
    return f'https://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url={url}'
