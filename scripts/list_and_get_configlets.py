# list_and_get_configlets.py
import os
from dotenv import load_dotenv
from cvprac.cvp_client import CvpClient

# ── Load CVP_URL and CVP_TOKEN from .env ───────────────────────────────────
load_dotenv()
cvp_url = os.getenv("CVP_URL")    # e.g. "10.23.60.97"
token   = os.getenv("CVP_TOKEN")  # your raw JWT

if not cvp_url or not token:
    raise ValueError("CVP_URL or CVP_TOKEN is missing")

# ── Connect via token auth ─────────────────────────────────────────────────
clnt = CvpClient()
clnt.connect(
    nodes=[cvp_url],
    username="",        # not needed with api_token
    password="",
    is_cvaas=False,
    api_token=token
)
api = clnt.api

# ── 1) List all Configlets ────────────────────────────────────────────────
# cvprac’s get_configlets returns a dict with 'data' (a list of configlet dicts) :contentReference[oaicite:0]{index=0}
resp = api.get_configlets(start=0, end=100)
configlets = resp.get("data", [])

print(f"{'Name':<30} {'Key':<40} {'Reconciled':<10}")
print("-" * 85)
for cfg in configlets:
    name      = cfg.get("name", "")
    key       = cfg.get("key", "")
    reconciled = cfg.get("reconciled", False)
    print(f"{name:<30} {key:<40} {str(reconciled):<10}")

# ── 2) Fetch a single Configlet by name ────────────────────────────────────
cfg_name = "MyNewConfiglet"
single = api.get_configlet_by_name(cfg_name)  # :contentReference[oaicite:1]{index=1}
if single:
    print("\nDetails for", cfg_name)
    print(f"Key       : {single.get('key')}")
    print(f"Reconciled: {single.get('reconciled')}")
    print("Config:\n", single.get("config"))
else:
    print(f"\nConfiglet {cfg_name!r} not found.")

