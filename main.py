import requests
import random
import asyncio

LINKS_FILE = "links.txt"
PROXIES_FILE = "proxies.txt"
TIMEOUT = 5
FETCH_TIMEOUT = 10
TEST_URL = "http://httpbin.org/ip"

seen_working = set()

open(PROXIES_FILE, "a", encoding="utf-8").close()

def get_proxy_list():
    proxy_list = []
    try:
        with open(LINKS_FILE, "r", encoding="utf-8") as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("links.txt not found")
        return []

    for url in urls:
        try:
            req = requests.get(url, timeout=FETCH_TIMEOUT)
            lines = [line.strip() for line in req.text.splitlines() if line.strip()]
            print(f"Loaded {len(lines)} proxies from {url}")
            proxy_list.extend(lines)
        except requests.RequestException:
            print(f"Error fetching {url}")
    random.shuffle(proxy_list)
    print(f"Total proxies loaded: {len(proxy_list)}")
    return proxy_list

def check_proxy(proxy):
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    try:
        response = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if response.status_code == 200:
            if proxy not in seen_working:
                seen_working.add(proxy)
                try:
                    with open(PROXIES_FILE, "a", encoding="utf-8") as file:
                        file.write(proxy + "\n")
                except Exception:
                    pass
            print(f"Proxy {proxy} is working.")
            return True
    except requests.RequestException:
        return False
    return False

async def main():
    proxy_list = await asyncio.to_thread(get_proxy_list)
    if not proxy_list:
        return
    tasks = [asyncio.create_task(asyncio.to_thread(check_proxy, proxy)) for proxy in proxy_list]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())