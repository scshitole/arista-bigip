
```
#!/usr/bin/env bash
set -euo pipefail

set -o allexport; source ./script.env; set +o allexport
BASE_URL="https://${CVP_HOST}/cvpservice"

# 1) Authenticate, save cookie
curl -k -v \
     -X POST "https://${CVP_HOST}/cvpservice/login/authenticate.do" \
     -H "Content-Type: application/json" \
     -d "{\"userId\":\"${CVP_USER}\",\"password\":\"${CVP_PASS}\"}" \
     -c cvp.cookie


# 2) Use that cookie on your GET
curl -k -s \
     -X GET "https://${CVP_HOST}/cvpservice/inventory/containers" \
     -b cvp.cookie \
  | jq .


[
  {
    "Key": "root",
    "Name": "Tenant",
    "CreatedBy": "cvp system",
    "CreatedOn": 1749837122336,
    "Mode": "expand"
  },
  {
    "Key": "undefined_container",
    "Name": "Undefined",
    "CreatedBy": "cvp system",
    "CreatedOn": 1749837122380,
    "Mode": "expand"
  }
]

```
