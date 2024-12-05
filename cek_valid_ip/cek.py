from curl_cffi import requests as curl_requests
from colorama import Fore, Style, init
from datetime import datetime
import time


init(autoreset=True)

print(f"{Fore.YELLOW}===========================")
print(f"{Fore.YELLOW} CEK AKUN VALID IP NODEPAY ")
print(f"{Fore.YELLOW}===========================\n")

with open('tokens.txt', 'r') as file:
    tokens = file.readlines()

tokens = [token.strip() for token in tokens]

print(f"{Fore.MAGENTA}Jumlah Akun: {len(tokens)}\n")

url = "https://api.nodepay.org/api/network/device-networks"
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
    "Authorization": "Bearer {token}",
    "Content-Type": "application/json",
    #"Cookie": "__cf_bm=YvjchKo1EAcHYQ7XQxVV_mG6DETxise_qeqayq8H3Ro-1733368102-1.0.1.1-fAzoYodtQFO_QOSKtmczoNQnJbw9Pqi62mBEdSYrE0B_k9UDfD0J.RbGYcTEJ5so8APXC2hOGpb0ZZzUdz5NqA",
    "Origin": "https://app.nodepay.ai",
    "Priority": "u=1, i",
    "Referer": "https://app.nodepay.ai/",
    "Sec-CH-UA": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "Sec-CH-UA-Mobile": "?1",
    "Sec-CH-UA-Platform": "\"Android\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
}

params = {
    "page": 0,
    "limit": 10,
    "active": "true"
}

line_count = 0

# Baca cookie dari file cookies.txt
with open('cookies.txt', 'r') as cookie_file:
    cookie_value = cookie_file.read().strip()

# Perbarui header Cookie dengan nilai dari cookies.txt
headers["Cookie"] = cookie_value

try:
    for index, token in enumerate(tokens):
        token_display = token[:4] + '*' * 10 + token[-4:]
        
        print(f"{Fore.CYAN}{'='*20}")
        print(f"{Fore.GREEN}Processing Akun: {token_display} ({index + 1}/{len(tokens)})")
        print(f"{Fore.CYAN}{'='*20}")
        
        headers["Authorization"] = f"Bearer {token}"
        
        response = curl_requests.get(url, headers=headers, params=params, impersonate="chrome110")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if response.status_code == 200:
            data = response.json()
            
            if data["success"]:
                devices = data["data"]
                print(f"{current_time} - Total devices: {len(devices)}")
                line_count += 1
                
                for device in devices:
                    ip_address = device.get("ip_address")
                    ip_score = device.get("ip_score", 0)
                    total_points = device.get("total_points", 0)
                    
                    print(f"{current_time} - IP Address: {ip_address}, IP Score: {ip_score}, Total Points: {total_points}")
                    line_count += 1
            else:
                print(f"{current_time} - {Fore.RED}Request failed: {data.get('msg')}")
                line_count += 1
        elif response.status_code == 403:
            print(f"{current_time} - {Fore.RED}Access denied, check your token and permissions.")
            # Optionally, handle token refresh or notify the user
        else:
            print(f"{current_time} - {Fore.RED}Failed to fetch data, Status Code: {response.status_code}")
            line_count += 1
        
        time.sleep(5)
except KeyboardInterrupt:
    print(f"{Fore.RED}Program terminated by user")
