#!/bin/bash

set -e

# Create bridge if not exists
BRIDGE=br-data
if ! brctl show | grep -q "$BRIDGE"; then
    echo "Creating bridge $BRIDGE..."
    sudo brctl addbr $BRIDGE
    sudo ip link set $BRIDGE up
fi

# Define veth pairs
declare -A LINKS=(
  [leaf1]=eth0
  [leaf2]=eth1
)

for NODE in "${!LINKS[@]}"; do
  HOST_IF="veth-${NODE}"
  PEER_IF="vpeer-${NODE}"
  HOST_PORT="${LINKS[$NODE]}"

  echo "Rebuilding veth pair for $NODE..."

  # Clean old interfaces
  sudo ip link del $HOST_IF 2>/dev/null || true
  sudo ip link del $PEER_IF 2>/dev/null || true

  # Create veth pair
  sudo ip link add $HOST_IF type veth peer name $PEER_IF

  # Attach host end to bridge and bring up
  sudo brctl addif $BRIDGE $HOST_IF
  sudo ip link set $HOST_IF up

  # Get container PID
  PID=$(docker inspect -f '{{.State.Pid}}' clab-spineleaf-$NODE)

  # Set up network namespace
  sudo mkdir -p /var/run/netns
  sudo ln -sfT /proc/$PID/ns/net /var/run/netns/$NODE

  # Move veth into container
  sudo ip link set $PEER_IF netns $NODE
  sudo ip netns exec $NODE ip link set $PEER_IF name Ethernet2
  sudo ip netns exec $NODE ip link set Ethernet2 up

  echo "$NODE: veth pair attached and up"
done
