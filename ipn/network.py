import platform
import socket
import psutil
import os
import logging

def get_network_info():
    network_info = []

    # Get OS type
    os_type = platform.system()
    network_info.append(("Operating System", os_type))

    # Get hostname
    hostname = socket.gethostname()
    network_info.append(("Hostname", hostname))

    # Get local IP address
    local_ip = socket.gethostbyname(hostname)
    network_info.append(("Local IP", local_ip))

    # Get network interfaces and their IP addresses
    for interface_name, addrs in psutil.net_if_addrs().items():
        addresses = []
        for addr in addrs:
            if addr.family == socket.AF_INET or addr.family == socket.AF_INET6:
                addresses.append(addr.address)
        if addresses:
            network_info.append((interface_name, ", ".join(addresses)))

    return network_info

def get_bandwidth_usage():
    io_counters = psutil.net_io_counters(pernic=True)
    bandwidth_info = {}
    for interface, counters in io_counters.items():
        bandwidth_info[interface] = {
            'bytes_sent': counters.bytes_sent,
            'bytes_recv': counters.bytes_recv,
            'packets_sent': counters.packets_sent,
            'packets_recv': counters.packets_recv
        }
    return bandwidth_info