# core/base_engien.py
import time
import requests
import logging

class BaseSearchEngine:
    def __init__(self, delay=1, user_agent=None):
        self.delay = delay
        self.user_agent = user_agent or "Mozilla/5.0 (compatible; DorkScanner/1.0)"
    
    def fetch_results(self, url):
        logging.debug(f"Sleeping for {self.delay} seconds before request...")
        time.sleep(self.delay)
        headers = {"User-Agent": self.user_agent}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"[ERROR] Failed to fetch {url}: {e}")
            return None
