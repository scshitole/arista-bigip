
### Create arista containers
```
containerlab deploy -t spineleaf.yaml
```
### Run this script to create br-data bridge
```
chmod +x restore-veth-links.sh
./restore-veth-links.sh
```

### add ens6 interface to the br-data 

```
sudo brctl addif br-data ens6
sudo ip link set ens6 up
```
### If eth0 or eth1 are not attached to any bridge:

```
sudo brctl addif br-data eth0
sudo brctl addif br-data eth1
sudo ip link set eth0 up
sudo ip link set eth1 up

```

```
brctl show
br-data         8000.a6c4c1482085       no              ens6
                                                        eth0
                                                        eth1
                                                        veth-leaf1
                                                        veth-leaf2

```
###

Absolutely — here’s a **step-by-step working guide** based on everything you’ve done and confirmed to get **Arista cEOS in Containerlab talking to BIG-IP** via `br-data` and enabling SSH access.

---

## ✅ Step-by-Step: Arista cEOS ↔ BIG-IP Lab on Ubuntu Host

---

### 🔧 **1. Physically connect**:

Connect **Ubuntu Host A (`ens6`)** → **BIG-IP interface `1.1`** using a cable or vSwitch.

---

### 🏗️ **2. Create Linux bridge on Host A**

```bash
sudo ip link add br-data type bridge
sudo ip link set ens6 master br-data
sudo ip link set br-data up
sudo ip link set ens6 up
```

> `br-data` now connects containers to BIG-IP via `ens6`

---

### 🐳 **3. Create Docker network mapped to `br-data`**

```bash
docker network create \
  -d bridge \
  --subnet=10.1.10.0/24 \
  --gateway=10.1.10.1 \
  -o com.docker.network.bridge.name=br-data \
  clab-data-net
```

---

### 🧾 **4. Create `ceos1.cfg` startup config**

File: `ceos1.cfg`

```bash
!
hostname ceos1
username admin privilege 15 secret admin
!
interface Ethernet1
   no switchport
   ip address 10.1.10.10/24
   no shutdown
!
interface Management1
   ip address dhcp
!
ip routing
!
```

---

### 📄 **5. Create `ceos-l2test.yaml` Containerlab topology**

```yaml
name: ceos-l2test
topology:
  nodes:
    ceos1:
      kind: ceos
      image: ceos:4.29.0F
      startup-config: ceos1.cfg
```

---

### 🚀 **6. Deploy the lab**

```bash
sudo containerlab deploy -t ceos-l2test.yaml
```

---

### 🔗 **7. Manually connect cEOS to `clab-data-net`**

```bash
docker network connect clab-data-net clab-ceos-l2test-ceos1
```

---

### 🔧 **8. Configure Ethernet1 (if not auto-set)**

```bash
docker exec -it clab-ceos-l2test-ceos1 Cli
enable
configure
interface Ethernet1
  no switchport
  ip address 10.1.10.10/24
  no shutdown
end
```

---

### 🔐 **9. SSH into Arista**

```bash
ssh admin@172.20.20.2
# password: admin
```

If SSH fails, recheck your `ceos1.cfg` includes:

```bash
username admin privilege 15 secret admin
```

---

### 🧪 **10. Test Ping Both Ways**

* From **cEOS → BIG-IP**: ✅ `ping 10.1.10.5`
* From **BIG-IP → cEOS**:

  * May need:

    * ✅ Static ARP entry
    * ✅ Proxy ARP on VLAN
    * ✅ Static route via Host A (`10.1.10.4`)

---

Would you like this turned into a downloadable script or templated multi-node topology next?
