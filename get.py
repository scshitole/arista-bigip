import os
import requests
from dotenv import load_dotenv
from pprint import pprint
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

token = os.getenv("CVP_TOKEN")
cvp_url = os.getenv("CVP_URL")

if not token or not cvp_url:
    raise ValueError("CVP_TOKEN or CVP_URL environment variable is missing.")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

url = f"https://{cvp_url}/cvpservice/inventory/devices"
response = requests.get(url, headers=headers, verify=False)

devices = response.json()

print(f"{'Hostname':<20} {'IP Address':<15} {'Serial Number':<15}")
print("=" * 50)
for device in devices:
    print(f"{device.get('hostname', ''):<20} {device.get('ipAddress', ''):<15} {device.get('serialNumber', ''):<15}")
