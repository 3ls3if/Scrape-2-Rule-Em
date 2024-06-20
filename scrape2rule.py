import requests
from bs4 import BeautifulSoup
import re
from email_crawler import EmailCrawler
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import os
from urllib.parse import urlparse



def banner():
    light_green = '\033[92m'  # ANSI code for green (as a close approximation of light green)
    reset = '\033[0m'
    red = '\033[91m'

    print(f"""
            {light_green}
            ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗    ██████╗     ██████╗ ██╗   ██╗██╗     ███████╗    ███████╗███╗   ███╗
            ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝    ╚════██╗    ██╔══██╗██║   ██║██║     ██╔════╝    ██╔════╝████╗ ████║
            ███████╗██║     ██████╔╝███████║██████╔╝█████╗       █████╔╝    ██████╔╝██║   ██║██║     █████╗      █████╗  ██╔████╔██║
            ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝      ██╔═══╝     ██╔══██╗██║   ██║██║     ██╔══╝      ██╔══╝  ██║╚██╔╝██║
            ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗    ███████╗    ██║  ██║╚██████╔╝███████╗███████╗    ███████╗██║ ╚═╝ ██║
            ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝    ╚══════╝    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝    ╚══════╝╚═╝     ╚═╝

            {reset}
                                                                {red}  By @3ls3if {reset}

    """)


def clear_screen():
    # Check the operating system
    if os.name == 'nt':
        # For Windows
        os.system('cls')
    else:
        # For macOS and Linux
        os.system('clear')



def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_html(html):
    return BeautifulSoup(html, 'html.parser')


def extract_emails(url):
    
    try:
        crawler = EmailCrawler(url, max_pages=10)
        emails = crawler.crawl()
        
        parsed_url = urlparse(url)
        
        domain = parsed_url.netloc
        
        domain2 = domain.replace(".", "_") 
        
        emails = pd.read_csv(domain2+".csv")
        
        clear_screen()
        banner()
        print("\n[+] Emails Found: \n")
        print(emails)
    
    except Exception as e:
        print(e)
    
    return
    
    

def extract_links(soup):
    links = set()
    for a_tag in soup.find_all('a', href=True):
        links.add(a_tag['href'])
    return links


def extract_js_files(soup):
    js_files = set()
    for script_tag in soup.find_all('script', src=True):
        js_files.add(script_tag['src'])
    return js_files


def extract_html_forms(soup):
    forms = soup.find_all('form')
    return forms


def extract_sensitive_contents(soup):
    sensitive_keywords = ['password', 'secret', 'token', 'aws_access_key_id', 'aws_secret_access_key', 's3:', 'google_api_key']
    sensitive_contents = []
    for text in soup.stripped_strings:
        for keyword in sensitive_keywords:
            if keyword in text.lower():
                sensitive_contents.append(text)
    return sensitive_contents


def display_menu():
    clear_screen()
    banner()
    print("\n [+] Select the type of data to scrape: \n")
    print(" [1] Emails")
    print(" [2] Links")
    print(" [3] JavaScript files")
    print(" [4] HTML forms")
    print(" [5] Sensitive contents")
    print("[99] Exit")


def main():
    clear_screen()
    banner()
    url = input("\n [+] Enter the URL of the website (https://example.com): ")
    html = fetch_html(url)
    soup = parse_html(html)

    while True:
        display_menu()
        choice = input("\n [+] Enter your choice (1-5): ")

        if choice == '1':
            extract_emails(url)
            input("\n[+] Press Enter to continue...")
            
        elif choice == '2':
            clear_screen()
            banner()
            links = extract_links(soup)
            print("\n[*] Links found:\n")
            for link in links:
                print(link)
            input("\n[+] Press Enter to continue...")
            
        elif choice == '3':
            clear_screen()
            banner()
            js_files = extract_js_files(soup)
            print("\n[*]JavaScript files found:\n")
            for js_file in js_files:
                print(js_file)
            input("\n[+] Press Enter to continue...")
            
        elif choice == '4':
            clear_screen()
            banner()
            html_forms = extract_html_forms(soup)
            print("\n[*] HTML forms found: \n")
            for html_form in html_forms:
                print(html_forms)
            input("\n[+] Press Enter to continue...")
            
        elif choice == '5':
            clear_screen()
            banner()
            sensitive_contents = extract_sensitive_contents(soup)
            print("\n[+] Sensitive contents found:\n")
            for content in sensitive_contents:
                print(content)
            input("\n[+] Press Enter to continue...")
            
        elif choice == '99':
            clear_screen()
            banner()
            print("\n[-] Exiting the program.\n")
            break
        else:
            clear_screen()
            banner()
            print("\n[!] Invalid choice. Please try again.\n")
        print("-" * 80)

if __name__ == '__main__':
    main()