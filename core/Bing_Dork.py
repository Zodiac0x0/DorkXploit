# core/Bing_Dork.py
import requests
from bs4 import BeautifulSoup
from core.base_engien import BaseSearchEngine
from colorama import init, Fore, Style

init()

class BingDorker(BaseSearchEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://www.bing.com/search?q="

    def search(self, dork):
        try:
            url = self.base_url + dork.replace(' ', '+')
            print(f"{Fore.CYAN}[INFO] Searching Bing with dork: {dork}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}[URL] Fetching: {url}{Style.RESET_ALL}")
            
            html = self.fetch_results(url)
            if not html:
                print(f"{Fore.RED}[-] Failed to fetch results{Style.RESET_ALL}")
                return []

            print(f"{Fore.GREEN}[+] Successfully fetched results{Style.RESET_ALL}")
            soup = BeautifulSoup(html, "html.parser")
            results = []
            for link in soup.select("a[href^='http']"):  # Adjust selector as needed
                href = link.get("href")
                if href:
                    results.append(href)
                    print(f"{Fore.GREEN}[FOUND] {href}{Style.RESET_ALL}")
            
            print(f"{Fore.YELLOW}[SUMMARY] Found {len(results)} results{Style.RESET_ALL}")
            return results
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Unexpected error: {str(e)}{Style.RESET_ALL}")
            return []