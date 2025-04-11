from bs4 import BeautifulSoup
from core.base_engien import BaseSearchEngine
from utils.color import Colors
import logging

formatter = logging.Formatter(
    f'{Colors.YELLOW}[%(levelname)s]{Colors.RESET} {Colors.CYAN}%(message)s{Colors.RESET}'
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger("google")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)

class GoogleDorker(BaseSearchEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://www.google.com/search?q="

    def search(self, dork):
        try:
            url = self.base_url + dork.replace(' ', '+')
            logger.info(f"[GOOGLE] Searching with dork: {dork}")
            logger.debug(f"[GOOGLE] Fetching URL: {url}")

            html = self.fetch_results(url)
            if not html:
                logger.warning("[GOOGLE] Failed to fetch results")
                return []

            soup = BeautifulSoup(html, "html.parser")
            results = []
            for link in soup.select("a[href^='http']"):
                href = link.get("href")
                if href:
                    results.append(href)
                    logger.info(f"[GOOGLE] Found: {href}")
            logger.info(f"[GOOGLE] Total results: {len(results)}")
            return results
        except Exception as e:
            logger.error(f"[GOOGLE] Error: {e}")
            return []