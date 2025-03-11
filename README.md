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
Create a new file named 'config.yaml', example can be found below. Configure your alert and the arp integration needed for your infrastructure. If needed you can configure multiple alerts and arp integrations to fetch from different devices or systems.
````
alert:
  gmail:
    smtp: smtp.gmail.com
    port: 587
    from:
      usr: "yoursender@gmail.com"
      pwd: "password"
    to: ["receiver@domain.com"]
arp:
  opnsense:
    ip: 192.168.1.1
    api: ""
    secret: ""
  cisco:
    ip: 192.168.1.1
    snmp: public
    oid: "1.3.6.1.2.1.3.1"
````
