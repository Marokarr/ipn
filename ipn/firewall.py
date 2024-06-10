import platform
import os

def get_firewall_status():
    os_type = platform.system()
    if os_type == "Windows":
        return get_windows_firewall_status()
    else:
        return get_unix_firewall_status()

def get_windows_firewall_status():
    output = os.popen('netsh advfirewall show allprofiles').read()
    return output.strip()

def get_unix_firewall_status():
    if os.path.exists('/usr/sbin/ufw'):
        output = os.popen('sudo ufw status').read()
        return output.strip()
    elif os.path.exists('/sbin/iptables'):
        output = os.popen('sudo iptables -L').read()
        return output.strip()
    else:
        return "Firewall status not available"
