#!/usr/bin/env python3
"""
apply_configlet_cvprac_onprem.py
Applies "MyNewConfiglet" to Spine & Leaf containers on on-prem CVP
using the proper cvprac workflow with temp actions and save topology.
"""
import os
import urllib3
import json
from dotenv import load_dotenv
from cvprac.cvp_client import CvpClient

# Suppress TLS warnings (lab only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load .env
load_dotenv()
CVP_URL     = os.getenv("CVP_URL")      # e.g. "cvp.example.net"
CVP_TOKEN   = os.getenv("CVP_TOKEN")    # your raw JWT for on-prem CVP
CFG_NAME    = "MyNewConfiglet"          # the configlet you created

if not CVP_URL or not CVP_TOKEN:
    raise RuntimeError("CVP_URL and CVP_TOKEN must be set in .env")

try:
    # 1) Connect to CVP via cvprac
    client = CvpClient()
    client.connect(
        [CVP_URL],
        "", "",                # no user/pass when using token auth
        api_token=CVP_TOKEN
    )
    api = client.api
    print("Successfully connected to CVP")

    # 2) Fetch all containers, find Spine & Leaf objects
    print("Fetching containers...")
    all_containers = api.get_containers(start=0, end=100).get("data", [])
    
    if not all_containers:
        raise RuntimeError("No containers found in CVP")
    
    print(f"Found {len(all_containers)} containers")
    for c in all_containers:
        print(f"  - {c.get('Name', c.get('name', 'Unknown'))}")

    def find_container(name):
        for c in all_containers:
            container_name = c.get("Name") or c.get("name")
            if container_name == name:
                return c
        raise RuntimeError(f"Container {name!r} not found in CVP")

    spine = find_container("Spine")
    leaf  = find_container("Leaf")
    
    print("Found containers:")
    print(f"  Spine: {spine.get('Key', spine.get('key', 'N/A'))}")
    print(f"  Leaf : {leaf.get('Key', leaf.get('key', 'N/A'))}")

    # 3) Fetch all configlets, find your MyNewConfiglet key
    print("Fetching configlets...")
    all_cfgs = api.get_configlets(start=0, end=100).get("data", [])
    
    if not all_cfgs:
        raise RuntimeError("No configlets found in CVP")
    
    print(f"Found {len(all_cfgs)} configlets")
    for cfg in all_cfgs:
        print(f"  - {cfg.get('name', 'Unknown')}")
    
    configlet_info = next((c for c in all_cfgs if c["name"] == CFG_NAME), None)
    if not configlet_info:
        raise RuntimeError(f"Configlet {CFG_NAME!r} not found in CVP")
    
    cfg_key = configlet_info["key"]
    print(f"Configlet key: {cfg_key}")

    # 4) Check if configlets are already applied
    def check_configlet_applied(container_info, configlet_key):
        cont_key = container_info.get("Key") or container_info.get("key")
        cont_name = container_info.get("Name") or container_info.get("name")
        
        try:
            existing_configlets = api.get_configlets_by_container_id(cont_key)
            existing_configlet_list = existing_configlets.get("data", [])
            existing_configlet_keys = [cfg["configletKey"] for cfg in existing_configlet_list]
            
            return configlet_key in existing_configlet_keys
            
        except Exception as e:
            print(f"  Warning: Could not check existing configlets for {cont_name}: {e}")
            return False

    # Check current state
    spine_has_configlet = check_configlet_applied(spine, cfg_key)
    leaf_has_configlet = check_configlet_applied(leaf, cfg_key)
    
    print(f"Current state:")
    print(f"  Spine has configlet: {spine_has_configlet}")
    print(f"  Leaf has configlet: {leaf_has_configlet}")
    
    if spine_has_configlet and leaf_has_configlet:
        print("Both containers already have the configlet applied!")
    else:
        print("\nApplying configlet using proper CVP workflow...")
        
        # 5) Create temp actions for containers that need the configlet
        temp_actions = []
        
        if not spine_has_configlet:
            spine_action = {
                "info": f"Configlet Assign: to Container {spine.get('Name', spine.get('name'))}",
                "infoPreview": f"<b>Configlet Assign:</b> to Container {spine.get('Name', spine.get('name'))}",
                "action": "associate",
                "nodeType": "configlet",
                "nodeId": cfg_key,
                "toId": spine.get('Key', spine.get('key')),
                "toIdType": "container",
                "nodeName": CFG_NAME,
                "toName": spine.get('Name', spine.get('name')),
                "childTasks": [],
                "parentTask": "",
                "ignoreNodeId": "",
                "ignoreNodeName": ""
            }
            temp_actions.append(spine_action)
            print(f"  Added temp action for Spine")
        
        if not leaf_has_configlet:
            leaf_action = {
                "info": f"Configlet Assign: to Container {leaf.get('Name', leaf.get('name'))}",
                "infoPreview": f"<b>Configlet Assign:</b> to Container {leaf.get('Name', leaf.get('name'))}",
                "action": "associate",
                "nodeType": "configlet", 
                "nodeId": cfg_key,
                "toId": leaf.get('Key', leaf.get('key')),
                "toIdType": "container",
                "nodeName": CFG_NAME,
                "toName": leaf.get('Name', leaf.get('name')),
                "childTasks": [],
                "parentTask": "",
                "ignoreNodeId": "",
                "ignoreNodeName": ""
            }
            temp_actions.append(leaf_action)
            print(f"  Added temp action for Leaf")
        
        if temp_actions:
            # 6) Add temp actions
            print("Adding temp actions...")
            temp_action_data = {"data": temp_actions}
            
            try:
                add_temp_result = api.add_temp_action(temp_action_data)
                print(f"Temp actions added successfully: {add_temp_result}")
            except Exception as e:
                print(f"Failed to add temp actions: {e}")
                # Try direct API call
                try:
                    print("Trying direct API call for temp actions...")
                    add_temp_result = client.post('/cvpservice/provisioning/addTempAction.do', 
                                                data=temp_action_data)
                    print(f"Direct temp action result: {add_temp_result}")
                except Exception as e2:
                    print(f"Direct API call also failed: {e2}")
                    raise
            
            # 7) Save topology to commit the temp actions
            print("Saving topology to commit changes...")
            try:
                # Try different save methods
                if hasattr(api, 'save_topology_v2'):
                    save_result = api.save_topology_v2([])
                    print(f"Save topology v2 result: {save_result}")
                elif hasattr(api, 'save_topology_v1'):
                    save_result = api.save_topology_v1([])
                    print(f"Save topology v1 result: {save_result}")
                elif hasattr(api, 'save_topology'):
                    save_result = api.save_topology([])
                    print(f"Save topology result: {save_result}")
                else:
                    # Use direct API call
                    print("Using direct saveTopology API call...")
                    save_data = {"data": []}  # Empty data to commit existing temp actions
                    save_result = client.post('/cvpservice/provisioning/saveTopology.do', 
                                            data=save_data)
                    print(f"Direct save result: {save_result}")
                    
            except Exception as e:
                print(f"Save topology failed: {e}")
                print("Changes may not be committed. Check CVP GUI for pending actions.")
        else:
            print("No temp actions needed - configlets already applied.")

    # 8) Verify final state
    print("\n=== Verification ===")
    for container_name, container in [("Spine", spine), ("Leaf", leaf)]:
        cont_key = container.get("Key") or container.get("key")
        print(f"\n{container_name} Container:")
        
        try:
            configlets = api.get_configlets_by_container_id(cont_key)
            configlet_list = configlets.get("data", [])
            
            if configlet_list:
                print(f"  Applied configlets ({len(configlet_list)}):")
                for cfg in configlet_list:
                    name = cfg.get('configletName', 'Unknown')
                    key = cfg.get('configletKey', 'Unknown')
                    print(f"    - {name}")
                    if name == CFG_NAME:
                        print("      ✓ MyNewConfiglet successfully applied!")
            else:
                print("  No configlets applied")
                
        except Exception as e:
            print(f"  Error checking configlets: {e}")
    
    # 9) Check for any pending tasks
    print("\n=== Checking for pending tasks ===")
    try:
        pending_tasks = api.get_tasks_by_status("Pending")
        
        if isinstance(pending_tasks, dict) and "data" in pending_tasks:
            tasks_data = pending_tasks["data"]
        elif isinstance(pending_tasks, list):
            tasks_data = pending_tasks
        else:
            tasks_data = []
        
        if tasks_data:
            print(f"Found {len(tasks_data)} pending tasks:")
            for task in tasks_data:
                print(f"  - {task.get('description', task.get('info', 'No description'))}")
            print("You may need to execute these tasks in the CVP GUI")
        else:
            print("No pending tasks found")
            
    except Exception as e:
        print(f"Error checking pending tasks: {e}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    print("Script completed")
