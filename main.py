# main.py
import os
import argparse
from core.DuckDuckDork import DuckDuckGoDorker
from core.Google_Dork import GoogleDorker
from core.Bing_Dork import BingDorker
from core.Shodan_Scan import ShodanScanner
from colorama import init, Fore, Style
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor
import socket


logging.basicConfig(
    level=logging.INFO,)
banner = f"""
{Fore.CYAN}
        ██████╗  ██████╗ ██████╗ ██╗  ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
        ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
        ██║  ██║██║   ██║██████╔╝█████╔╝  ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
        ██║  ██║██║   ██║██╔══██╗██╔═██╗  ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
        ██████╔╝╚██████╔╝██║  ██║██║  ██╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
        ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝  
        {Style.RESET_ALL}
        {Fore.MAGENTA}[!] Coded By: Omar Islam{Style.RESET_ALL}
        """
init()

def argp():
    parser = argparse.ArgumentParser(description="Dorking tool for reconnaissance it search on (Google, Bing, Duckduckgo)")

    parser.add_argument("--url", help="Target domain (e.g., google.com)",dest='url',required=True,type=str)
    parser.add_argument("--save", help="Save the output in a file (default: result/result.txt)", 
                        default="result/result.txt", type=str,dest='search')
    parser.add_argument("--dorks",help="Path to the list of dorks file",required=True,type=str)
    parser.add_argument("--thread",help="Number of threads for the processing",dest='thread',default=10,type=int)
    parser.add_argument("--use-shodan", action="store_true", help="Enable Shodan scanning if API key is provided.")
    parser.add_argument("--shodan-api", help="Shodan API key for scanning")
    parser.add_argument("--verbose",help="Enable verbose mode for more detailed output", action="store_true")
    parser.add_argument("--engine",help="Choose spacific engine to search with",choices=['Google','Bing',"DuckDuckgo"],dest='engine')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug(f"{Fore.GREEN}Verbose mode enabled.{Style.RESET_ALL}")

    if args.use_shodan and not args.shodan_api:
        logging.error(f"{Fore.RED}Shodan scanning requires an API key. Use --shodan-api <API_KEY>.{Style.RESET_ALL}")
        exit(1)
    return args

def load_dorks(filename, target="example.com"):
    """
    Load dorks from a file and replace 'exmaple.com' to the target domain
        Args:
            filename:
                The path to the file containing the dorks.
            target:
                The target domain to replace in the dorks.
        Return:
            A list of dorks with the target domain.
    """
    try:
        with open(filename,'r') as f :
            return [line.strip().replace('example.com',target) for line in f if line.strip()]
    
    except FileNotFoundError:
        logging.error(f"File {filename} not found")
        return []
    except Exception as e:
        logging.error(f"Error loading dorks: {e}")
        return []

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
    if not os.path.exists("results"):
        os.makedirs("results")
    
    clean_dork = re.sub(r'[^\w-]', '_', dork)

    filename = f"results/{engine_name}_{target}_{clean_dork}.txt"
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, filename)

    
    with open(my_file, 'w') as f:
        for result in results:
            f.write(str(result) + '\n')
    
    logging.info(f"{Fore.GREEN}[SAVED] Results saved to {filename}{Style.RESET_ALL}")

def select_engine():
    engines = {
        "DuckDuckGo": DuckDuckGoDorker(),
        "Google": GoogleDorker(),
        "Bing": BingDorker()
    }
    args = argp()
    target = args.url
    sel_eng = args.engine
    dorks = load_dorks(target=target)
    if not dorks:
        logging.error(f"{Fore.RED}[EXIT] No dorks to process. Exiting.{Style.RESET_ALL}")
        return
    
    engine = engines.get(sel_eng) if sel_eng else None
    try:
        if sel_eng:
            if sel_eng not in engines:
                logging.error(f"{Fore.RED}[ERROR] Engine not found. Please select from the following engines:")
                return
        engine = engines[sel_eng]
        try:
            for dork in dorks:
                results = engine.search(dork)
                if results:
                    logging.info(f"{Fore.BLUE}Saving...{Style.RESET_ALL}")
                    save_results(target, dork, sel_eng, results)
                    logging.info(f"{Fore.YELLOW}Saved")
        except Exception as e:
            logging.error(f"{Fore.RED}[EXIT] Error processing dork with {sel_eng}: {e}{Style.RESET_ALL}")
            return
    except Exception as e:
        logging.error(f"{Fore.RED}[EXIT] Error processing dork with {sel_eng}: {e}{Style.RESET_ALL}")
        return

def shodan_api():
    args = argp()
    shodan_api = args.shodan_api
    target = args.url

    if shodan_api:
        logging.info(f'{Fore.YELLOW}Scanning Shodan...!{Style.RESET_ALL}')
        sh = ShodanScanner(api_key=shodan_api)
        results = sh.scan(target)

        if results:
            logging.info(f"{Fore.GREEN}Found Some Results and Saving it...{Style.RESET_ALL}")
            save_results(results, "Shodan", target, "Shodan API")
        else:
            logging.warning(f"{Fore.RED}No Shodan Results Found for {target}{Style.RESET_ALL}")
    else:
        logging.error(f"{Fore.RED}[ERROR] Shodan API key not provided. Exiting.{Style.RESET_ALL}")

def run_each_eng():
    args = argp()
    target = args.url

    engines = {
        "DuckDuckGo": DuckDuckGoDorker(),
        "Google": GoogleDorker(),
        "Bing": BingDorker()
}

    dorks = load_dorks(target=target)

    for dork in dorks:
        logging.info(f"\n{Fore.MAGENTA}=== Processing dork: {dork} ==={Style.RESET_ALL}")
        for engine_name, engine in engines.items():
            logging.info(f"{Fore.BLUE}[INFO] Running on {engine_name}{Style.RESET_ALL}")
            results = engine.search(dork)
            if results:
                save_results(target, dork, engine_name, results)

def threads():
    args = argp()
    target = args.url
    thread = args.threads
    engines = {
        "DuckDuckGo": DuckDuckGoDorker(),
        "Google": GoogleDorker(),
        "Bing": BingDorker()
    }
    dorks = load_dorks(target=target)   
    try:
        dorks = load_dorks(target)
        logging.debug("Loaded dorks: %s", dorks)
        with ThreadPoolExecutor(max_workers=thread or 10) as executor:
            lst = []
            for dork in dorks:
                for engine_name,engine in engines.items():
                    logging.info(f"{Fore.BLUE}[INFO] Running on {engine_name}{Style.RESET_ALL}")
                    future = executor.submit(engine.search, dork)
                    lst.append((future,engine_name))
                for res , engine_name in lst:
                    result = future.result()
                    if result:
                        logging.info(f"{Fore.GREEN}Result founded for {target} using {engine_name}")
                        save_results(target, dork, engine_name, result)
                    else:
                        logging.warning(f"{Fore.RED}No results for {target} using {engine_name}")
    except Exception as e:
        logging.error(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        logging.critical(f'{Fore.RED}Critical error: The system cannot continue due to {e}')
def main():
    args = argp()
    print(banner)
    time.sleep(2)
    if args.dorks:
        load_dorks(filename=args.dorks,target=args.url)
    elif args.dorks is None:
        raise ValueError("You should add a Dorks File")
    if args.engine:
        select_engine(args)
    else:
        run_each_eng(args)
    if args.use_shodan:
        shodan_api(args)
    
if __name__ == "__main__":
    main()