import requests
from gatet import _get_next_proxy, PROXIES_LIST, _build_proxy_dict

print("=" * 60)
print("🔍 gatet.py ရဲ့ proxy တွေ တကယ်သုံးနေလား စစ်ဆေး")
print("=" * 60)

# ၁။ မူလ IP (proxy မပါဘဲ)
try:
    direct_ip = requests.get("https://api.ipify.org?format=json", timeout=10).json()["ip"]
    print(f"\n🌐 မူလ IP (proxy မပါ): {direct_ip}")
except Exception as e:
    print(f"\n❌ မူလ IP မရ: {e}")
    direct_ip = None

# ၂။ gatet.py ရဲ့ proxy တွေနဲ့ IP စစ်
print(f"\n📋 Proxy {len(PROXIES_LIST)} ခုကို စစ်မယ်...\n")

working = 0
failed = 0

for i, proxy_str in enumerate(PROXIES_LIST, 1):
    proxy = _build_proxy_dict(proxy_str)
    try:
        r = requests.get("https://api.ipify.org?format=json",
                         proxies=proxy, timeout=15)
        proxy_ip = r.json()["ip"]

        # မူလ IP နဲ့ တူ/မတူ စစ်
        if direct_ip and proxy_ip == direct_ip:
            status = "⚠️ မူလ IP နဲ့ တူနေတယ် — proxy အလုပ်မလုပ်ဘူး!"
            failed += 1
        else:
            status = "✅ Proxy အလုပ်လုပ်တယ် (IP မတူ)"
            working += 1

        print(f"[{i}] {proxy_str.split(':')[0]}")
        print(f"    Proxy IP: {proxy_ip}")
        print(f"    {status}\n")
    except Exception as e:
        failed += 1
        print(f"[{i}] {proxy_str.split(':')[0]}")
        print(f"    ❌ မရ: {type(e).__name__}: {str(e)[:80]}\n")

# ၃။ အနှစ်ချုပ်
print("=" * 60)
print("📊 အနှစ်ချုပ်")
print("=" * 60)
print(f"✅ Working: {working}/{len(PROXIES_LIST)}")
print(f"❌ Failed : {failed}/{len(PROXIES_LIST)}")
print("=" * 60)