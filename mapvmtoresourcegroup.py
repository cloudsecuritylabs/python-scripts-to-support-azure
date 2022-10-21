"""
A program to get a list of all VMs with the Resource group
"""
import os
import json
import getsubscriptionlist

vm_name_rg = {}

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
        vm_name_rg[item['Name']] = item['ResourceGroup']

    print(vm_name_rg)
    return vm_name_rg


def save_vm_resource_group(subscription_name):
    vm_name_rg = get_vm_extension(subscription_name)
    file_name = subscription_name +"-vm-rg.csv"
    with open(file_name, 'w') as f:
        for key, value in vm_name_rg.items():
            line = f'{key}, {value}'.replace("[", "").replace("]", "").replace("'", "")
            f.write(line + "\n")
