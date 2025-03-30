# core/base_engien.py
import time
from fake_useragent import UserAgent

class BaseSearchEngine:
    def __init__(self, delay=2, proxies=None):
        self.headers = {"User-Agent": UserAgent().random}
        self.base_url = ''
        self.delay = delay
        self.proxies = proxies

    def search(self, dork):
        time.sleep(self.delay)
        pass