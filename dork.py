import requests
import argparse
from bs4 import BeautifulSoup
import urllib.parse
from colorama import Fore, Style, init
from time import sleep
from tqdm import tqdm
import signal
import sys

init(autoreset=True)

found_links = set()
output_file = None

def banner():
    print(f"""
{Fore.RED}===========================================
{Fore.GREEN}   Bing Dorker - Red Team Edition
{Fore.GREEN}   Author: github.com/idhin
{Fore.CYAN}   Real-time saving | Multiple pages support
{Fore.RED}===========================================

{Fore.YELLOW}DISCLAIMER:
Use only for legal and authorized purposes.
All consequences of misuse are your own responsibility.

{Fore.RESET}
""")


def handle_exit(signum, frame):
    print(f"\n{Fore.RED}[!] Interrupted! Saving collected links before exit...")
    save_links()
    sys.exit(0)

def save_links():
    if output_file:
        with open(output_file, 'a') as f:
            for link in found_links:
                f.write(link + '\n')
        print(f"{Fore.YELLOW}[*] Total saved: {len(found_links)} link(s)")

def bing_search(query, pages=1):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    for page in range(pages):
        offset = page * 10
        url = f"https://www.bing.com/search?q={urllib.parse.quote_plus(query)}&first={offset + 1}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[!] Request error: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('li', class_='b_algo')

        for result in results:
            a_tag = result.find('a')
            if a_tag and a_tag.get('href'):
                raw_url = a_tag.get('href')
                if "bing.com/ck/a?" in raw_url:
                    parsed_url = urllib.parse.urlparse(raw_url)
                    query_params = urllib.parse.parse_qs(parsed_url.query)
                    if 'u' in query_params:
                        link = urllib.parse.unquote(query_params['u'][0])
                    else:
                        link = raw_url
                else:
                    link = raw_url

                if link not in found_links:
                    found_links.add(link)
                    print(f"{Fore.GREEN}[+] Found: {Style.RESET_ALL}{link}")
                    with open(output_file, 'a') as f:
                        f.write(link + '\n')
        sleep(0.3)

def main():
    global output_file
    banner()

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    parser = argparse.ArgumentParser(description='Bing Dorking Script')
    parser.add_argument('-l', '--list', dest='dork_list', required=True, help='Path to the dork list file')
    parser.add_argument('-o', '--output', dest='output_file', required=True, help='Output file to save results')
    parser.add_argument('-p', '--pages', dest='pages', type=int, default=1, help='Number of pages per dork (default: 1)')
    args = parser.parse_args()

    output_file = args.output_file

    try:
        with open(args.dork_list, 'r') as f:
            queries = [q.strip() for q in f.readlines() if q.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Dork list file not found!")
        return

    print(f"{Fore.CYAN}[+] Processing {len(queries)} dork(s) x {args.pages} page(s) each...\n")

    for query in tqdm(queries, desc="Searching", ncols=80, colour='GREEN'):
        bing_search(query, pages=args.pages)
        sleep(0.2)

    print(f"\n{Fore.YELLOW}[✓] Finished. Total links found: {len(found_links)}")
    print(f"{Fore.BLUE}[-] Saved to: {output_file}")

if __name__ == "__main__":
    main()