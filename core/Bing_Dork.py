# core.Bing_Dork.py
import requests
from bs4 import BeautifulSoup
from core.base_engien import *
from colorama import init, Fore, Style

# Initialize colorama
init()

class BingDorker(BaseSearchEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(delay=2,*args, **kwargs)
        self.base_url = "https://www.bing.com/search?q="

    def search(self, dork):
        try:
            url = self.base_url + dork.replace(' ', '+')
            print(f"{Fore.CYAN}[INFO] Searching Bing with dork: {dork}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}[URL] Fetching: {url}{Style.RESET_ALL}")
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"{Fore.RED}[-] Failed to fetch results - Status: {response.status_code}{Style.RESET_ALL}")
                return []

            print(f"{Fore.GREEN}[+] Successfully fetched results - Status: {response.status_code}{Style.RESET_ALL}")
            soup = BeautifulSoup(response.text, "html.parser")
            results = []

            for link in soup.find_all("a", class_="result__a"):
                href = link.get("href")
                if href and "http" in href:
                    results.append(href)
                    print(f"{Fore.GREEN}[FOUND] {href}{Style.RESET_ALL}")

            print(f"{Fore.YELLOW}[SUMMARY] Found {len(results)} results{Style.RESET_ALL}")
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[ERROR] Request failed: {str(e)}{Style.RESET_ALL}")
            return []
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Unexpected error: {str(e)}{Style.RESET_ALL}")
            return []
