### Create a script.env

```
# script.env
CVP_UTL=10.23.X.X
CVP_TOKEN=cvpadmin
```
### load in bash

```
# source the file Env
source .env

```
### Run python script list_and_get_configlets.py to list Configuration on CVP

```
python list_and_get_configlets.py
/opt/homebrew/Caskroom/miniconda/base/lib/python3.12/site-packages/urllib3/connectionpool.py:1099: InsecureRequestWarning: Unverified HTTPS request is being made to host '10.23.60.97'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(
/opt/homebrew/Caskroom/miniconda/base/lib/python3.12/site-packages/urllib3/connectionpool.py:1099: InsecureRequestWarning: Unverified HTTPS request is being made to host '10.23.60.97'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(
/opt/homebrew/Caskroom/miniconda/base/lib/python3.12/site-packages/urllib3/connectionpool.py:1099: InsecureRequestWarning: Unverified HTTPS request is being made to host '10.23.60.97'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(
Name                           Key                                      Reconciled
-------------------------------------------------------------------------------------
MyNewConfiglet                 configlet_db6139a3-0b4a-431e-8841-9739e7783d8a False     
SYS_TelemetryBuilderV7         SYS_TelemetryBuilderV7_1749837122461     False     
/opt/homebrew/Caskroom/miniconda/base/lib/python3.12/site-packages/urllib3/connectionpool.py:1099: InsecureRequestWarning: Unverified HTTPS request is being made to host '10.23.60.97'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(

Details for MyNewConfiglet
Key       : configlet_db6139a3-0b4a-431e-8841-9739e7783d8a
Reconciled: False
Config:
 
interface Ethernet1
   description Configured via API
   no shutdown
!


```
