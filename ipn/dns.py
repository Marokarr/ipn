import platform
import os

def get_windows_dns():
    import winreg
    dns_servers = {}
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces') as interfaces_key:
            for i in range(winreg.QueryInfoKey(interfaces_key)[0]):
                interface_key_name = winreg.EnumKey(interfaces_key, i)
                with winreg.OpenKey(interfaces_key, interface_key_name) as interface_key:
                    try:
                        name_server = winreg.QueryValueEx(interface_key, 'NameServer')[0]
                        if name_server:
                            dns_servers[interface_key_name] = name_server.split(',')
                    except FileNotFoundError:
                        pass
    except Exception as e:
        print(f"Failed to retrieve DNS settings from registry: {e}")
    return dns_servers

def get_unix_dns():
    dns_servers = {}
    try:
        with open("/etc/resolv.conf") as f:
            dns_servers["Global DNS"] = []
            for line in f:
                if line.startswith("nameserver"):
                    dns_servers["Global DNS"].append(line.split()[1])
    except Exception as e:
        print(f"Failed to read /etc/resolv.conf: {e}")
    return dns_servers

def get_dns_info():
    os_type = platform.system()
    if os_type == "Windows":
        return get_windows_dns()
    else:
        return get_unix_dns()
