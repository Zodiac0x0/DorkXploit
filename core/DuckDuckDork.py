# core/DuckDuckDork.py
import requests
from bs4 import BeautifulSoup
from core.base_engien import BaseSearchEngine  # Fixed typo from 'base_engien'
from colorama import init, Fore, Style

# Initialize colorama
init()

class DuckDuckGoDorker(BaseSearchEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Inherit delay and user_agent from BaseSearchEngine
        self.base_url = "https://html.duckduckgo.com/html/?q="

    def search(self, dork):
        try:
            url = self.base_url + dork.replace(' ', '+')
            print(f"{Fore.CYAN}[INFO] Searching DuckDuckGo with dork: {dork}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}[URL] Fetching: {url}{Style.RESET_ALL}")
            
            # Use fetch_results from BaseSearchEngine instead of requests.get
            html = self.fetch_results(url)
            if not html:
                print(f"{Fore.RED}[-] Failed to fetch results{Style.RESET_ALL}")
                return []

            print(f"{Fore.GREEN}[+] Successfully fetched results{Style.RESET_ALL}")
            soup = BeautifulSoup(html, "html.parser")
            results = []

            for link in soup.find_all("a", class_="result__a"):
                href = link.get("href")
                if href and "http" in href:
                    results.append(href)
                    print(f"{Fore.GREEN}[FOUND] {href}{Style.RESET_ALL}")

            print(f"{Fore.YELLOW}[SUMMARY] Found {len(results)} results{Style.RESET_ALL}")
            return results
            
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Unexpected error: {str(e)}{Style.RESET_ALL}")
            return []