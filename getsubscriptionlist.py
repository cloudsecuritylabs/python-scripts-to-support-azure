"""
A useful Python program to loop over management group structure 
It gets the subscription details.
It can get the subscription id, based on the subscription name and vice versa
Author: Ankan Basu
"""
import os

# Provide full dictionary of enabled subscriptions
def get_enabled_subscriptions():
    subscription_name_id = {}
    subscription_list = os.popen('az account subscription list -o table').readlines()
    for line in subscription_list:
        splitted = line.split()
        sub_name = splitted[1]
        sub_id = splitted[3]
        enabled = splitted [2]
        if enabled == "Enabled":
            subscription_name_id[sub_name] = sub_id
    return subscription_name_id

# get total count of subscriptions under mg
def count_total_subscriptions_mg():
    return len(get_mg_subscriptions())

# get subscription id from subscription name
def get_subscription_id(subscription_name):
    if subscription_name in get_enabled_subscriptions().keys():
        return get_enabled_subscriptions()[subscription_name]

# get subscription name from subscription id
def get_subscription_name(subscription_id):
    for name, id in get_enabled_subscriptions().items():
        if id == subscription_id:
            return name
            break
        elif id != subscription_id:
            continue
        else:
            "Invalid id"



