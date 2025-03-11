import asyncio
from pysnmp.hlapi.asyncio import *
from pysnmp.hlapi.v3arch.asyncio import UdpTransportTarget
import re

# convert mac address to valid format for comparison in arp-table.json
def format_mac(mac):
    if not mac:
        return mac
    else:
        # remove '0x' prefix if present
        if mac.startswith("0x"):
            mac = mac[2:]

        # split non special char mac and add colon
        if len(mac) == 12:
            mac = [mac[i:i+2] for i in range(0, len(mac), 2)]
            mac = ":".join(mac).lower()

        return mac

# extract info from snmp
def extract_info(oid, value):

    vlan_match = re.search(r"\.2\.(\d+)\.1\.", oid)
    vlan = vlan_match.group(1) if vlan_match else None

    ipv4_octets = oid.split(".")[-4:]
    ipv4 = ".".join(ipv4_octets) if len(ipv4_octets) == 4 else None

    mac = value.strip() if value else None

    return vlan, ipv4, mac

# convert oid string to tuple for comparison
def oid_to_tuple(oid):
    return tuple(map(int, oid.strip('.').split('.')))

# check if oid is within the specified range
def is_oid_in_range(current_oid, start_oid, stop_oid):
    current_oid_tuple = oid_to_tuple(current_oid)
    start_oid_tuple = oid_to_tuple(start_oid)
    stop_oid_tuple = oid_to_tuple(stop_oid)

    # esnure current oid starts with start oid prefix
    if not current_oid_tuple[:len(start_oid_tuple)] == start_oid_tuple:
        return False

    # check so current oid is less or equal to stop oid
    return current_oid_tuple <= stop_oid_tuple

# snmp walk between start and stop OID
async def snmp_walk(host, port, community, start_oid, stop_oid):
    snmp_engine = SnmpEngine()
    snmp_community = CommunityData(community)
    snmp_transport = await UdpTransportTarget.create((host, port))
    snmp_context = ContextData()
    next_oid = start_oid
    results = []

    while True:
        errorIndication, errorStatus, errorIndex, varBinds = await next_cmd(
            snmp_engine,
            snmp_community,
            snmp_transport,
            snmp_context,
            ObjectType(ObjectIdentity(next_oid))
        )

        if errorIndication:
            print(f"Error: {errorIndication}")
            break
        elif errorStatus:
            print(f"Error: {errorStatus.prettyPrint()}")
            break
        else:
            for varBind in varBinds:
                oid, value = varBind
                current_oid = str(oid)

                if not is_oid_in_range(current_oid, start_oid, stop_oid):
                    return results
                
                vlan,ipv4,mac = extract_info(current_oid, value.prettyPrint())
                results.append({"vlan": vlan, "ip": ipv4, "mac": format_mac(mac)})

                next_oid = oid

    return results

# function called from main netmon-lite
def get(host, port, community, start_oid, stop_oid):
    results = asyncio.run(snmp_walk(host, port, community, start_oid, stop_oid))
    return results
