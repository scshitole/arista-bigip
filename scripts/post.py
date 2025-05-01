import os
import requests
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

token = os.getenv("CVP_TOKEN")
cvp_url = os.getenv("CVP_URL")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

url = f"https://{cvp_url}/cvpservice/configlet/addConfiglet"

payload = {
    "name": "demo-ntp-config",
    "config": "ntp server 192.168.1.10 prefer"
}

response = requests.post(url, json=payload, headers=headers, verify=False)

if response.status_code == 200:
    print("✅ Configlet created successfully!")
    print(response.json())
else:
    print(f"❌ Failed to create configlet: {response.status_code}")
    print(response.text)
