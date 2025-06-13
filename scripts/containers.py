import os
import requests
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

token   = os.getenv("CVP_TOKEN")
raw_url = os.getenv("CVP_URL")

if not token or not raw_url:
    raise ValueError("CVP_TOKEN or CVP_URL environment variable is missing.")

# strip any “http://” or “https://”
host = raw_url.removeprefix("https://").removeprefix("http://")
base = f"https://{host}"
url  = f"{base}/cvpservice/inventory/containers"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

resp = requests.get(url, headers=headers, verify=False)
resp.raise_for_status()

body = resp.json()

# CVP returns a top‐level list here, so just treat it as such:
if isinstance(body, list):
    containers = body
else:
    # fallback if wrapped in {"data": [...]}
    containers = body.get("data", [])

if not containers:
    print("No containers found.")
    exit(0)

# Print container info using the correct JSON keys
print(f"{'Container Name':<30} {'Key':<40} {'Mode':<10}")
print("=" * 82)
for c in containers:
    name = c.get("Name", "")
    key  = c.get("Key", "")
    mode = c.get("Mode", "")
    print(f"{name:<30} {key:<40} {mode:<10}")

