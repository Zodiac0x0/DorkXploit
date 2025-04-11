import requests
import time
import random
import logging
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BaseSearchEngine:
    def __init__(self,delay=2,*args,**kwargs):
        self.user_agent = UserAgent()
        self.delay = delay

    def search(self, query):
        raise NotImplementedError("Subclasses must implement the search method.")

    def fetch_results(self, url, retries=3):
        """
        Args:
            url (str): 
                URL to fetch results from.
            retries (int): 
                Number of retries if the request fails.
        """
        for attempt in range(1, retries + 1):
            try:
                headers = {"User-Agent": self.user_agent.random}
                time.sleep(random.uniform(2, 5))

                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                logging.info(f"[SUCCESS] Retrieved results from {url}")
                return response.text

            except requests.exceptions.RequestException as e:
                logging.warning(f"[WARNING] Attempt {attempt} failed: {e}")
                if attempt == retries:
                    logging.error("[ERROR] Maximum retries reached, skipping request.")
                    return None