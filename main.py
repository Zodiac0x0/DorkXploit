# main.py
import os
import argparse
from core.DuckDuckDork import DuckDuckGoDorker
from core.Google_Dork import GoogleDorker
from core.Bing_Dork import BingDorker
from colorama import init, Fore, Style
import logging
import re
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)] %(message)s",

)
banner = f"""
        ██████╗  ██████╗ ██████╗ ██╗  ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
        ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
        ██║  ██║██║   ██║██████╔╝█████╔╝  ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
        ██║  ██║██║   ██║██╔══██╗██╔═██╗  ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
        ██████╔╝╚██████╔╝██║  ██║██║  ██╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
        ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
        DorkSniper - Automate your Google Dorking like a pro!"""

init()

async def load_dorks(filename="data/dorks.txt", target="example.com"):
    """
    Load dorks from a file and return them as a list and replace from exmaple.com to the target
        Args:
            filename:
                The path to the file containing the dorks.
            target:
                The target domain to replace in the dorks.
        Return:
            A list of dorks with the target domain.
    """
    dorks = []
    try:
        with open(filename,'r') as f :
            dorks = [line.strip().replace("example.com", target) for line in f if line.strip()]
        logging.info(f"Loaded {len(dorks)} dorks for Target {target}")
    except Exception as e:
        logging.error(f"Error loading dorks: {e}")
        return 
    except FileNotFoundError:
        logging.error(f"File {filename} not found")
        return
    return dorks

def get_target_domain():
    """
        Get the target domain from the user input
    """
    parser = argparse.ArgumentParser(description="Dorking tool for bug bounty reconnaissance")
    parser.add_argument("-t","--target", help="Target domain (e.g., google.com)", default=None)
    parser.add_argument("-o","--output",help="Save the ouput in a file",default='result/result.txt',required=False)
    args = parser.parse_args()

    if args.target:
        return args.target
    else:
        target = input(f"{Fore.YELLOW}[INPUT] Enter the target domain (e.g., google.com): {Style.RESET_ALL}").strip()
        while not target:
            target = input(f"{Fore.RED}[ERROR] Target cannot be empty. Enter the target domain: {Style.RESET_ALL}").strip()
        return target


def save_results(target, dork, engine_name, results):
    """
    Save the results in a file
        Args:
            target: 
                take the target domain from get_target_domain function
            dork:
                take the dork from load_dorks function
            engine_name:
                take the engines from core file
            results:
                take the results from core file
        Return:
            Saved file in result directory
    """
    if not os.path.exists("result"):
        os.makedirs("result")
    
    clean_dork = re.sub(r'[^\w-]', '_', dork) 
    filename = f"result/{engine_name}_{target}_{clean_dork}.txt"
    
    with open(filename, 'w') as f:
        for result in results:
            f.write(result + '\n')
    
    logging.info(f"{Fore.GREEN}[SAVED] Results saved to {filename}{Style.RESET_ALL}")


def main():
    target = get_target_domain()
    print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
    time.sleep(3)
    # Initialize search engines
    engines = {
        "DuckDuckGo": DuckDuckGoDorker(),
        "Google": GoogleDorker(),
        "Bing": BingDorker()
    }

    dorks = load_dorks(target=target)
    if not dorks:
        logging.error(f"{Fore.RED}[EXIT] No dorks to process. Exiting.{Style.RESET_ALL}")
        return

    # Run each dork on each engine
    for dork in dorks:
        logging.info(f"\n{Fore.MAGENTA}=== Processing dork: {dork} ==={Style.RESET_ALL}")
        for engine_name, engine in engines.items():
            logging.info(f"{Fore.CYAN}[INFO] Running on {engine_name}{Style.RESET_ALL}")
            results = engine.search(dork)
            if results:
                save_results(target, dork, engine_name, results)

if __name__ == "__main__":
    main()