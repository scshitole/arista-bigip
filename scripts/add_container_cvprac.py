import os
from dotenv import load_dotenv
from cvprac.cvp_client import CvpClient

# ── Load env ──────────────────────────────────────────────────────────────
load_dotenv()
cvp_url = os.getenv("CVP_URL")        # e.g. "10.23.60.97"
token   = os.getenv("CVP_TOKEN")      # your raw JWT

if not cvp_url or not token:
    raise ValueError("CVP_URL or CVP_TOKEN is missing")

# ── Connect via token ─────────────────────────────────────────────────────
client = CvpClient()
client.connect(
    nodes=[cvp_url],
    username="",           # not used with token auth
    password="",
    is_cvaas=False,
    api_token=token        # token-based auth
)

api = client.api

# ── Add the container ───────────────────────────────────────────────────
parent_name = "Tenant"                # e.g. the name of your parent container
parent_key  = "root"                  # often "root" for top level
new_name    = "Container1"

resp = api.add_container(new_name, parent_name, parent_key)  # :contentReference[oaicite:0]{index=0}
print("add_container response:", resp)

# ── Commit the change ───────────────────────────────────────────────────
# CVP buffers topology changes until you confirm:
save_resp = api._save_topology_v2([])  # confirm all pending topology changes :contentReference[oaicite:1]{index=1}
print("save_topology response:", save_resp)

