import requests
import time

# ===== စစ်ချင်တဲ့ proxy စာရင်း =====
PROXIES_LIST = [
    "p102.instantproxies.com:9207:9013:wBZ6YFPOkt4b",
    "p101.instantproxies.com:9207:9012:RP1vGZQZhhlK",
    "p103.instantproxies.com:9206:9011:ufrvfyLUDAK4",
]

# စစ်ဆေးမယ့် URL — IP ကို ပြန်ပေးတဲ့ service
CHECK_URL = "https://api.ipify.org?format=json"
TIMEOUT = 15


def build_proxy_dict(proxy_str):
    """host:port:user:pass -> requests proxy dict"""
    parts = proxy_str.strip().split(":")
    if len(parts) != 4:
        return None
    host, port, user, pwd = parts
    url = f"http://{user}:{pwd}@{host}:{port}"
    return {"http": url, "https": url}


def check_proxy(proxy_str):
    """Proxy တစ်ခုကို စစ်။ dict ပြန်"""
    proxy = build_proxy_dict(proxy_str)
    if proxy is None:
        return {
            "proxy": proxy_str,
            "status": "❌ INVALID FORMAT",
            "ip": "-",
            "time": 0,
            "error": "Format မမှန် (host:port:user:pass ဖြစ်ရမယ်)",
        }

    start = time.time()
    try:
        r = requests.get(CHECK_URL, proxies=proxy, timeout=TIMEOUT)
        elapsed = time.time() - start

        if r.status_code == 200:
            try:
                ip = r.json().get("ip", "-")
            except Exception:
                ip = r.text.strip()[:30]
            return {
                "proxy": proxy_str,
                "status": "✅ WORKING",
                "ip": ip,
                "time": elapsed,
                "error": "",
            }
        else:
            return {
                "proxy": proxy_str,
                "status": f"⚠️ HTTP {r.status_code}",
                "ip": "-",
                "time": elapsed,
                "error": r.text[:100],
            }

    except requests.exceptions.ProxyError as e:
        return {"proxy": proxy_str, "status": "❌ PROXY ERROR", "ip": "-",
                "time": time.time() - start, "error": str(e)[:120]}
    except requests.exceptions.ConnectTimeout:
        return {"proxy": proxy_str, "status": "❌ CONNECT TIMEOUT", "ip": "-",
                "time": time.time() - start, "error": "Connection timeout"}
    except requests.exceptions.ReadTimeout:
        return {"proxy": proxy_str, "status": "❌ READ TIMEOUT", "ip": "-",
                "time": time.time() - start, "error": "Read timeout"}
    except requests.exceptions.SSLError as e:
        return {"proxy": proxy_str, "status": "❌ SSL ERROR", "ip": "-",
                "time": time.time() - start, "error": str(e)[:120]}
    except Exception as e:
        return {"proxy": proxy_str, "status": "❌ FAILED", "ip": "-",
                "time": time.time() - start, "error": f"{type(e).__name__}: {str(e)[:100]}"}


def main():
    print("=" * 70)
    print(f"🔍 Proxy စစ်ဆေးခြင်း — {len(PROXIES_LIST)} ခု")
    print(f"🌐 Check URL: {CHECK_URL}")
    print("=" * 70)

    working = 0
    results = []

    for i, proxy in enumerate(PROXIES_LIST, 1):
        print(f"\n[{i}/{len(PROXIES_LIST)}] စစ်နေသည်: {proxy}")
        res = check_proxy(proxy)
        results.append(res)

        if res["status"].startswith("✅"):
            working += 1
            print(f"   {res['status']} | IP: {res['ip']} | Time: {res['time']:.2f}s")
        else:
            print(f"   {res['status']} | {res['error']}")

    # ===== အနှစ်ချုပ် =====
    print("\n" + "=" * 70)
    print("📊 အနှစ်ချုပ်")
    print("=" * 70)
    print(f"✅ Working: {working}/{len(PROXIES_LIST)}")
    print(f"❌ Failed : {len(PROXIES_LIST) - working}/{len(PROXIES_LIST)}")
    print("-" * 70)

    for res in results:
        icon = "✅" if res["status"].startswith("✅") else "❌"
        print(f"{icon} {res['proxy']}")
        if res["status"].startswith("✅"):
            print(f"    IP: {res['ip']} | Time: {res['time']:.2f}s")
        else:
            print(f"    {res['status']} — {res['error']}")
    print("=" * 70)


if __name__ == "__main__":
    main()