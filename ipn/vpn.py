import platform
import os

def get_vpn_status():
    os_type = platform.system()
    if os_type == "Windows":
        return get_windows_vpn_status()
    else:
        return get_unix_vpn_status()

def get_windows_vpn_status():
    output = os.popen('rasdial').read()
    if "No connections" in output:
        return "No VPN connections"
    else:
        return output.strip()

def get_unix_vpn_status():
    output = os.popen('ip a | grep tun').read()
    if output:
        return "VPN is connected"
    else:
        return "No VPN connections"
