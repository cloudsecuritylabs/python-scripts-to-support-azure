"""
This program gets a list of VM agents within Azure Virtual Machines 
The output is stored in a text file.
Author: Ankan Basu
Required: getsubscriptoinlist.py file
"""

import os
import json
import getsubscriptionlist

vm_agents = {}

def get_vm_extension(subscription_name):
    subscription_id = getsubscriptionlist.get_subscription_id(subscription_name)
    os.system('az account set -s' + subscription_id)
    os.system('az account show')

    query_string = '"[].{ Name:name, \
                                                    OS:storageProfile.osDisk.osType, \
                                                    ProvisioningState: provisioningState, \
                                                    ResourceGroup: resourceGroup, \
                                                    Size: hardwareProfile.vmSize, \
                                                    Identity: identity.type ,\
                                                    Location: location, \
                                                    AutoUpdate: osProfile.windowsConfiguration.enableAutomaticUpdates, \
                                                    VmAgentPlatformUpdate: osProfile.windowsConfiguration.enableVMAgentPlatformUpdates, \
                                                    PatchSettingMode: osProfile.windowsConfiguration.patchSettings.patchMode, \
                                                    ProvisionVmAgent: osProfile.windowsConfiguration.provisionVmAgent, \
                                                    StorageImageRG : storageProfile.imageReference.resourceGroup, \
                                                    Tags : tags,\
                                                    ResourceIds: resources[].id, \
                                                    admin:osProfile.adminUsername}"'
    query = f'az vm list --query {query_string}'

    result = os.popen(query).read()
    jsoned = json.loads(result)

    for item in jsoned:
        agents_per_vm=item["ResourceIds"]
        for k,v in item.items():
            if k=="ResourceIds" and len(v) > 0:
                agent_list = []
                agent_list.append(item["OS"])
                for entry in v:
                    agent_list.append(entry.split("/")[-1])
                vm_agents[item['Name']] = agent_list
            elif k=="ResourceIds" and len(v) == 0:
                agent_list = []
                agent_list.append(item["OS"])
                agent_list.append("Missing all agents")
                vm_agents[item['Name']] = agent_list

    print(len(vm_agents))
    return vm_agents


def save_vm_agents_to_file(subscription_name):
    vm_agents = get_vm_extension(subscription_name)
    file_name = subscription_name +".csv"
    with open(file_name, 'w') as f:
        for key, value in vm_agents.items():
            line = f'{key}, {value}'.replace("[", "").replace("]", "").replace("'", "")
            f.write(line + "\n")




