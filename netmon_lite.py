import json
from datetime import datetime
import yaml
import requests
from tabulate import tabulate
from send_mail import send_mail

# current date and time for logging findings
time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
new_devices = []
history = []

# config variables
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# history file with known devices
with open("arp-table.json", "r") as f:
    data = json.load(f)
history = [d['MACAddr'] for d in data['history']]

for arp in config["arp"]:
    if arp == "opnsense":
        # calls opnsense api for arp table
        ipv4 = config["arp"][arp]["ip"]
        url = "https://{0}/api/diagnostics/interface/getArp".format(ipv4)
        r = requests.get(url, verify = False, auth = (config["arp"][arp]["api"], config["arp"][arp]["secret"]), timeout=10)
        response = json.loads(r.text)
        
        # reading through response for unknown mac addresses
        for line in response:
            if line["mac"] not in history:
                # adding new devices to json
                new_item = {"Time" : time, "MACAddr" : line["mac"], "IPv4" : line['ip'], "Int" : line['intf'], "Manu" : line['manufacturer']}
                new_devices.append(new_item)
    if arp == "cisco":
        # coming soon

if new_devices != []:
    print("Found new network devices! ({0})".format(len(new_devices)))

    # alerting using all configured channels
    for alert in config["alert"]:
        if alert == "gmail":
            send_mail(
                config["alert"][alert]["smtp"],config["alert"][alert]["port"],
                config["alert"][alert]["from"]["usr"],config["alert"][alert]["from"]["pwd"],
                config["alert"][alert]["to"],
                "WARNING: New network device found!",new_devices
            )
    
    # exporting to history file for next run
    data["history"].extend(new_devices)
    with open("arp-table.json", "w") as f:
        json.dump(data, f, indent=4)
    print("New devices saved to history file")
else:
    print("No new network devices")