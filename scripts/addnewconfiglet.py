# add_configlet_cvprac.py
import os
from dotenv import load_dotenv
from cvprac.cvp_client import CvpClient

# ── Load CVP_URL and CVP_TOKEN from .env ────────────────────────────────────
load_dotenv()
cvp_url = os.getenv("CVP_URL")    # e.g. "10.23.60.97"
token   = os.getenv("CVP_TOKEN")  # your raw JWT

if not cvp_url or not token:
    raise ValueError("CVP_URL or CVP_TOKEN is missing")

# ── Connect to CVP via token auth ───────────────────────────────────────────
client = CvpClient()
client.connect(
    nodes=[cvp_url],
    username="",
    password="",
    is_cvaas=False,
    api_token=token
)
api = client.api

# ── Define your new Configlet ──────────────────────────────────────────────
configlet_name = "MyNewConfiglet"
configlet_body = """
interface Ethernet1
   description Configured via API
   no shutdown
!
"""

# ── Add the Configlet ───────────────────────────────────────────────────────
configlet_key = api.add_configlet(configlet_name, configlet_body)  # :contentReference[oaicite:0]{index=0}
print("Created configlet key:", configlet_key)

# ── Commit the change ───────────────────────────────────────────────────────
# CVP buffers Configlet changes as “temp actions”—you must save them
save_resp = api._save_topology_v2([])  # :contentReference[oaicite:1]{index=1}
print("Save topology response:", save_resp)

