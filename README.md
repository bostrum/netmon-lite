# netmon-lite
Minimalistic version of netmon that sends email alerts on new network devices in the ARP table.  
Simple way of keeping track of new devices being connected to your network.

# Supported
- OPNSense API
- Cisco SNMP

# Getting started
### Prerequisites:
- [OPNSense API documentation](https://docs.opnsense.org/development/how-tos/api.html)
- [Configure Cisco SNMP](https://www.cisco.com/c/en/us/support/docs/ip/simple-network-management-protocol-snmp/7282-12.html)
### Configuration:
Edit the 'config.yaml' which includes examples and the standard yaml format. Configure alert and the arp integration needed for your infrastructure. If needed you can configure multiple alerts and arp integrations to fetch from different devices or systems.
