#!/usr/bin/env python3

import sys
import ipaddress

def print_usage():
    print("Usage: {} IP MASK_PREFIX\nFor example: {} 192.168.45.30 21".format(sys.argv[0], sys.argv[0]))

def get_ip_class(ip):
    oc = int(ip.exploded.split(".")[0])
    if oc < 128:
        return "A"
    elif oc < 192:
        return "B"
    elif oc < 224:
        return "C"
    elif oc < 240:
        return "D"
    else:
        return "E"
            

def to_num(ip_str):
    """ converts ip 3-dot string representation to numerical representation"""
    n = 0
    for part in ip_str.split("."):
        n *= 256
        n += int(part)
    return n

def to_str(ip_num):
    """ converts ip represented by uint32 to 3-dot string representation"""
    res = ""

    for i in range(4):
        res = "." + str(ip_num % 256) + res
        ip_num //= 256

    # remove the first dot
    return res[1:]


def mask_prefix_to_num(prefix):
    """ converts subnet mask prefix representation to numerical one
    for example: 
        to_str(mask_prefix_to_num(21)) == "255.255.255.0"
    """
    res = 0
    for i in range(32 - prefix, 32):
       res += 2 ** i 
    return res


if len(sys.argv) != 3:
    print_usage()
    exit(1)


_, ip_str, mask = sys.argv

try:
    ip = ipaddress.IPv4Address(ip_str)
    mask = int(mask)
except ipaddress.AddressValueError:
    print("IP invalid!")
    exit(1)


""" Example of desired output:

    $> ./ip_info 192.168.45.30 21

    192.168.45.30 is valid class C IPv4 address

    Netmask:    255.255.248.0 = 21 
    Network:    192.168.40.0/21
    Broadcast:  192.168.47.255
    Host-range: 192.168.40.1 - 192.168.47.254

    #Hosts/net: 2046
"""

ip_str = ip.exploded

print("{} is valid class {} IPv4 address\n".format(ip_str, get_ip_class(ip)))

num_mask = mask_prefix_to_num(mask)
num_ip = to_num(ip_str)

print("Netmask:\t{} = {}".format(to_str(num_mask), mask))
print("Network:\t{}/{}".format(to_str(num_ip & num_mask), mask))

MAX_UINT = 2**32 - 1
broadcast = num_ip | (MAX_UINT & ~num_mask)
print("Broadcast:\t{}".format(to_str(broadcast)))

host_low = (num_ip & num_mask) + 1 
host_high = broadcast - 1

print("Host-range:\t{} - {}\n".format(to_str(host_low), to_str(host_high)))
print("#Hosts/net:\t{}".format(host_high - host_low + 1))
