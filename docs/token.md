### Create a script.env

```
# script.env
CVP_HOST=cvp.example.com
CVP_USER=cvpadmin
CVP_PASS=MyP@ssw0rd
CVP_PORT=443   # optional, defaults to 443

```
### load in bash

```
# at top of your bash script (or interactive shell)
set -o allexport
source ./script.env
set +o allexport

```
### cURL example

```
#!/usr/bin/env bash
set -euo pipefail

# load env-file
set -o allexport; source ./script.env; set +o allexport

BASE_URL="https://${CVP_HOST}:${CVP_PORT}/cvpservice"
AUTH_PAYLOAD=$(jq -n --arg u "$CVP_USER" --arg p "$CVP_PASS" '{userId:$u, password:$p}')

# authenticate
curl -k -s -X POST "$BASE_URL/login/authenticate.do" \
     -H "Content-Type: application/json" \
     -d "$AUTH_PAYLOAD" \
     -c cvp.cookie

# subsequent call using saved cookie
curl -k -s -X GET "$BASE_URL/inventory/devices" \
     -b cvp.cookie | jq .

```
