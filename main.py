# main.py
import os
import argparse
from colorama import init, Fore, Style
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor

from utils.color import Colors
from core.DuckDuckDork import DuckDuckGoDorker
from core.Google_Dork import GoogleDorker
from core.Bing_Dork import BingDorker
from core.Shodan_Scan import ShodanScanner



logging.basicConfig(
    level=logging.INFO,)
banner = f"""
{Colors.CYAN}

        ██████╗  ██████╗ ██████╗ ██╗  ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
        ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
        ██║  ██║██║   ██║██████╔╝█████╔╝  ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
        ██║  ██║██║   ██║██╔══██╗██╔═██╗  ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
        ██████╔╝╚██████╔╝██║  ██║██║  ██╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
        ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝  
        {Colors.RESET}
        {Colors.MAGENTA}[!] Coded By: Omar Islam{Colors.RESET}
        """
init()

def argp():
    parser = argparse.ArgumentParser(description="Dorking tool for reconnaissance it search on (Google, Bing, Duckduckgo)")

    parser.add_argument("--url", help="Target domain",dest='url',required=True,type=str)
    parser.add_argument("--save", help="Save the output in a file (default: result/result.txt)", 
                        default="result/result.txt", type=str,dest='search')
    parser.add_argument("--dorks",help="Path to the list of dorks file",required=True,type=str)
    parser.add_argument("--thread",help="Number of threads for the processing",dest='thread',default=10,type=int)
    parser.add_argument("--shodan-api", help="Shodan API key for scanning")
    parser.add_argument("--verbose",help="Enable verbose mode for more detailed output", action="store_true")
    parser.add_argument("--engine",help="Choose spacific engine to search with",choices=['Google','Bing',"DuckDuckgo"],dest='engine')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug(f"{Colors.GREEN}Verbose mode enabled.{Colors.RESET}")
    if not args.dorks:
        logging.error(f"{Colors.RED}[-] Please provide the dorks file path.{Colors.RESET}")
        exit()
    return args

def load_dorks(dork_file,target):
    """
    Load dorks from a file and replace 'exmaple.com' to the target domain
        Args:
            target:
                The target domain to replace in the dorks.
        Return:
            A list of dorks with the target domain.
    """
    try:
        with open(dork_file, 'r') as f:
            return [line.strip().replace("example.com", target) for line in f if line.strip()]
    except FileNotFoundError:
        logging.error(f"{Colors.RED}File {dork_file} not found{Colors.RESET}")
    except Exception as e:
        logging.error(f"{Colors.RED}Error loading dorks: {e}{Colors.RESET}")
    return []


def save_results(target, engine_name, results):
    """
    Save the results in a file
        Args:
            target: 
                take the target domain from get_target_domain function
            engine_name:
                take the engines from core file
            results:
                take the results from core file
        Return:
            Saved file in the same directory
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{engine_name}_{target}.txt")
    with open(path, 'w') as f:
        for result in results:
            f.write(str(result) + '\n')
    logging.info(f"{Colors.GREEN}[SAVED] Results saved to {path}{Colors.RESET}")

def select_engine(args):
    engines = {
        "DuckDuckGo": DuckDuckGoDorker(),
        "Google": GoogleDorker(),
        "Bing": BingDorker()
    }

    target = args.url
    dorks = load_dorks(args.dorks, target)
    if not dorks:
        logging.error(f"{Colors.RED}[EXIT] No dorks to process.{Colors.RESET}")
        return

    engine_name = args.engine
    engine = engines.get(engine_name)
    if not engine:
        logging.error(f"{Colors.RED}[ERROR] Invalid engine selected.{Colors.RESET}")
        return

    for dork in dorks:
        results = engine.search(dork)
        if results:
            logging.info(f"{Colors.BLUE}Saving...{Colors.RESET}")
            save_results(target, dork, engine_name, results)

def shodan_api(args):
    if args.shodan_api:
        logging.info(f"{Colors.YELLOW}Scanning Shodan...{Style.RESET_ALL}")
        sh = ShodanScanner(api_key=args.shodan_api)
        results = sh.scan(args.url)
        if results:
            logging.info(f"{Colors.GREEN}Results found. Saving...{Style.RESET_ALL}")
            save_results(args.url, "Shodan", results)
        else:
            logging.warning(f"{Colors.RED}No Shodan Results Found for {args.url}{Style.RESET_ALL}")
    else:
        logging.error(f"{Colors.RED}[ERROR] Shodan API key not provided.{Style.RESET_ALL}")

def run_each_eng(args):
    engines = {
        "DuckDuckGo": DuckDuckGoDorker(),
        "Google": GoogleDorker(),
        "Bing": BingDorker()
    }

    dorks = load_dorks(args.dorks, args.url)
    if not dorks:
        return

    for dork in dorks:
        logging.info(f"\n{Colors.MAGENTA}=== Processing dork: {dork} ==={Style.RESET_ALL}")
        for name, engine in engines.items():
            results = engine.search(dork)
            if results:
                logging.info(f"{Colors.GREEN}Saving...{Colors.RESET}")
                save_results(args.url, name, results)

def threads():
    engines = {
        "DuckDuckGo": DuckDuckGoDorker(),
        "Google": GoogleDorker(),
        "Bing": BingDorker()
    }
    dorks = load_dorks(args.dorks,args.url)   
    try:    
        with ThreadPoolExecutor(max_workers=args.thread or 10) as executor:
            lst = []
            for dork in dorks:
                for engine_name, engine in engines.items():
                    logging.info(f"{Fore.BLUE}[INFO] Running on {engine_name}{Style.RESET_ALL}")
                    future = executor.submit(engine.search, dork)
                    lst.append((future, engine_name, dork))
            for res, engine_name ,dork in lst:
                result = res.result()  
                if result:
                    save_results(args.url, engine_name, result) 
    except Exception as e:
        logging.error(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        logging.critical(f'{Fore.RED}Critical error: The system cannot continue due to {e}')
    
if __name__ == "__main__":
    print(banner)
    time.sleep(1)

    args = argp()

    if args.thread:
        threads()

    if args.engine:
        select_engine(args)
    else:
        run_each_eng(args)
    if args.use_shodan:
        shodan_api(args)