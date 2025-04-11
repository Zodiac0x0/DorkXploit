# core/Bing_Dork.py
import logging
from bs4 import BeautifulSoup
from core.base_engien import BaseSearchEngine
from utils.color import Colors

logger = logging.getLogger(__name__)

class BingDorker(BaseSearchEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://www.bing.com/search?q="

    def search(self, dork):
        try:
            url = self.base_url + dork.replace(' ', '+')
            logger.info(f"{Colors.CYAN}[INFO] Searching Bing with dork: {dork}{Colors.RESET}")
            logger.info(f"{Colors.BLUE}[URL] Fetching: {url}{Colors.RESET}")

            html = self.fetch_results(url)
            if not html:
                logger.error(f"{Colors.RED}[-] Failed to fetch results{Colors.RESET}")
                return []

            logger.info(f"{Colors.GREEN}[+] Successfully fetched results{Colors.RESET}")
            soup = BeautifulSoup(html, "html.parser")
            results = []
            for link in soup.select("a[href^='http']"):
                href = link.get("href")
                if href:
                    results.append(href)
                    logger.info(f"{Colors.GREEN}[FOUND] {href}{Colors.RESET}")

            logger.info(f"{Colors.YELLOW}[SUMMARY] Found {len(results)} results{Colors.RESET}")
            return results
        except Exception as e:
            logger.exception(f"{Colors.RED}[ERROR] Unexpected error: {str(e)}{Colors.RESET}")
            return []
