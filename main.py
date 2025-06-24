import random
import time
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

# 🧠 Simulated device profiles
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

# 📂 Load custom proxies
def get_custom_proxies():
    try:
        with open("custom_proxies.txt", "r") as f:
            custom = [line.strip() for line in f if line.strip()]
            log(f"Loaded {len(custom)} custom proxies from file")
            return custom
    except FileNotFoundError:
        log("[!] custom_proxies.txt file not found.")
        return []

# 🕹️ Simulate visit + click
def visit_and_interact(url, proxy):
    profile = random.choice(TRAFFIC_PROFILES)
    log(f"Using profile: {profile['name']} with proxy: {proxy}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                proxy={"server": proxy},
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

# 🏁 Main function
def main():
    print("=== Proxy Ad Click Bot (Custom Proxies Only) ===")
    proxies = get_custom_proxies()

    if not proxies:
        log("[!] No custom proxies found. Exiting...")
        return

    target_url = input("Enter TARGET website URL: ").strip()
    adsterra_link = input("Enter Adsterra LINK: ").strip()
    try:
        view_count = int(input("How many views/interactions to run? (e.g. 50): "))
    except ValueError:
        print("Invalid number entered. Exiting...")
        return

    for i in range(1, view_count + 1):
        proxy = random.choice(proxies)
        current_url = adsterra_link if i % 2 == 0 else target_url
        log(f"➡️ Attempt {i}/{view_count} | Target: {current_url} | Proxy: {proxy}")

        visit_and_interact(current_url, proxy)
        time.sleep(random.randint(10, 20))

if __name__ == "__main__":
    main()
