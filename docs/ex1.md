
```
#!/usr/bin/env bash
set -euo pipefail

set -o allexport; source ./script.env; set +o allexport
BASE_URL="https://${CVP_HOST}/cvpservice"

# 1) Authenticate, save cookie
curl -k -s -X POST "${BASE_URL}/login/authenticate.do" \
     -H "Content-Type: application/json" \
     -d "{\"userId\":\"${CVP_USER}\",\"password\":\"${CVP_PASS}\"}" \
     -c cvp.cookie >/dev/null

# 2) Use that cookie on your GET
curl -k -s -X GET "${BASE_URL}/inventory/devices" \
     -b cvp.cookie \
  | jq .

```
