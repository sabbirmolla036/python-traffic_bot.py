import random
import time
import requests
from datetime import datetime
from playwright.sync_api import sync_playwright

# 🔘 Selectors to simulate ad clicks
CLICK_SELECTORS = [
    "button[onclick='openLinks()']",
    "button:has-text('Watch Movie')",
    "a.button",
    "button.btn-primary",
    "#main-cta",
    "a[href*='click']"
]

# 🧠 Simulated device profiles (added Chrome Mobile)
TRAFFIC_PROFILES = [
    {
        "name": "Android + Facebook",
        "user_agent": "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36",
        "viewport": {"width": 360, "height": 740},
        "is_mobile": True,
        "has_touch": True,
        "referer": "https://m.facebook.com/"
    },
    {
        "name": "iPhone + Instagram",
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "viewport": {"width": 375, "height": 812},
        "is_mobile": True,
        "has_touch": True,
        "referer": "https://l.instagram.com/"
    },
    {
        "name": "iPhone + TikTok",
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 TikTok/18.2.0",
        "viewport": {"width": 375, "height": 812},
        "is_mobile": True,
        "has_touch": True,
        "referer": "https://www.tiktok.com/"
    },
    {
        "name": "Android + Chrome",
        "user_agent": "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.131 Mobile Safari/537.36",
        "viewport": {"width": 412, "height": 823},
        "is_mobile": True,
        "has_touch": True,
        "referer": "https://www.google.com/"
    }
]

# 📝 Logger
def log(msg):
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}")

# 🌐 Proxy sources
def get_proxyscrape_proxies():
    try:
        url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=3000"
        response = requests.get(url, timeout=10)
        proxies = [p.strip() for p in response.text.splitlines() if p.strip()]
        log(f"Fetched {len(proxies)} proxies from ProxyScrape")
        return proxies
    except Exception as e:
        log(f"[!] ProxyScrape error: {e}")
        return []

def get_geonode_proxies():
    try:
        url = "https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=lastChecked&sort_type=desc&protocols=http"
        response = requests.get(url, timeout=10)
        data = response.json()
        proxies = [f"{item['ip']}:{item['port']}" for item in data.get("data", []) if item.get("ip") and item.get("port")]
        log(f"Fetched {len(proxies)} proxies from Geonode")
        return proxies
    except Exception as e:
        log(f"[!] Geonode error: {e}")
        return []

def get_custom_proxies():
    try:
        with open("custom_proxies.txt", "r") as f:
            custom = [line.strip() for line in f if line.strip()]
            log(f"Loaded {len(custom)} custom proxies from file")
            return custom
    except FileNotFoundError:
        log("No custom proxy file found (custom_proxies.txt)")
        return []

# 🧪 Test if a proxy works
def is_proxy_working(proxy: str) -> bool:
    try:
        resp = requests.get("http://httpbin.org/ip",
                            proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                            timeout=5)
        return resp.status_code == 200
    except:
        return False

# 🎭 Simulate visit
def visit_and_interact(url, proxy):
    profile = random.choice(TRAFFIC_PROFILES)
    log(f"Using profile: {profile['name']} with proxy: {proxy}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                proxy={"server": f"http://{proxy}"},
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )

            context = browser.new_context(
                user_agent=profile["user_agent"],
                viewport=profile["viewport"],
                is_mobile=profile["is_mobile"],
                has_touch=profile["has_touch"],
                extra_http_headers={"Referer": profile["referer"]}
            )

            page = context.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_load_state('networkidle')
            log(f"[✓] Visited: {url} with {profile['name']}")

            for _ in range(random.randint(2, 5)):
                page.mouse.wheel(0, random.randint(200, 600))
                time.sleep(random.uniform(1.5, 2.5))

            for selector in CLICK_SELECTORS:
                try:
                    page.wait_for_selector(selector, timeout=3000)
                    page.click(selector)
                    log(f"[🖱️] Clicked on: {selector}")
                    break
                except:
                    continue

            time.sleep(random.uniform(6, 12))
            browser.close()
            log("[🚪] Browser session closed\n")
            return True
    except Exception as e:
        log(f"[X] Failed with proxy {proxy}: {e}")
        return False

# 🏁 Main Routine
def main():
    print("=== Proxy Ad Click Bot ===")
    print("1. Use FREE proxies (ProxyScrape + Geonode)")
    print("2. Use CUSTOM proxies (from custom_proxies.txt)")
    choice = input("Choose option (1 or 2): ").strip()

    if choice == "1":
        proxies = get_proxyscrape_proxies() + get_geonode_proxies()
    elif choice == "2":
        proxies = get_custom_proxies()
    else:
        print("Invalid choice. Exiting...")
        return

    target_url = input("Enter TARGET website URL: ").strip()
    adsterra_link = input("Enter Adsterra LINK: ").strip()
    try:
        view_count = int(input("How many views/interactions to run? (e.g. 50): "))
    except ValueError:
        print("Invalid number entered. Exiting...")
        return

    log(f"Total proxies fetched: {len(proxies)}")
    log("Checking working proxies...")
    working_proxies = [p for p in proxies if is_proxy_working(p)]
    log(f"✔ {len(working_proxies)} working proxies found")

    if not working_proxies:
        log("[!] No working proxies available. Exiting...")
        return

    for i in range(1, view_count + 1):
        if not working_proxies:
            log("[!] Proxy list exhausted.")
            break

        proxy = random.choice(working_proxies)
        current_url = adsterra_link if i % 2 == 0 else target_url
        log(f"➡️ Attempt {i}/{view_count} | Target: {current_url} | Proxy: {proxy}")

        success = visit_and_interact(current_url, proxy)
        if not success:
            working_proxies.remove(proxy)
            continue

        time.sleep(random.randint(10, 20))

if __name__ == "__main__":
    main()
