import os
import platform
import socket
import psutil
import textwrap
import toml
from colorama import Fore, Style, init

# Add imports for Windows registry access
if platform.system() == "Windows":
    import winreg

init(autoreset=True)

# Determine the config file path based on the OS
def get_config_path():
    if platform.system() == "Windows":
        config_dir = os.path.join(os.getenv("LOCALAPPDATA"), "ipn")
    else:
        config_dir = os.path.join(os.getenv("HOME"), ".config", "ipn")
    config_file = os.path.join(config_dir, "config.toml")
    return config_dir, config_file

# Ensure the config directory and file exist
def ensure_config_exists():
    config_dir, config_file = get_config_path()
    
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    if not os.path.exists(config_file):
        default_config = {
            "theme": {
                "border_char": "+",
                "header_border_char": "-",
                "column_border_char": "|",
                "header_color": "cyan",
                "row_color": "white"
            }
        }
        with open(config_file, 'w') as file:
            toml.dump(default_config, file)

# Read theme configuration
def read_config():
    _, config_file = get_config_path()
    with open(config_file, 'r') as file:
        return toml.load(file)

ensure_config_exists()
config = read_config()
theme = config["theme"]

# Function to get the color from the configuration
def get_color(color_name):
    colors = {
        "black": Fore.BLACK,
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "reset": Fore.RESET
    }
    return colors.get(color_name.lower(), Fore.WHITE)

header_color = get_color(theme["header_color"])
row_color = get_color(theme["row_color"])

def get_windows_dns():
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

    # Get DNS servers
    dns_info = get_dns_info()
    for adapter, dns_servers in dns_info.items():
        if dns_servers:
            network_info.append((f"DNS Servers ({adapter})", ", ".join(dns_servers)))

    return network_info

def format_table(data, col1_width=30, col2_width=60):
    border_line = f"{theme['border_char']}{theme['header_border_char'] * (col1_width + 2)}{theme['border_char']}{theme['header_border_char'] * (col2_width + 2)}{theme['border_char']}\n"
    col_border = theme['column_border_char']
    
    table = ""
    table += border_line
    table += f"{col_border} {header_color}{'Network Info':<{col1_width}}{Style.RESET_ALL} {col_border} {header_color}{'Details':<{col2_width}}{Style.RESET_ALL} {col_border}\n"
    table += border_line
    
    for key, value in data:
        key_wrapped = textwrap.wrap(key, col1_width)
        value_wrapped = textwrap.wrap(value, col2_width)
        
        max_lines = max(len(key_wrapped), len(value_wrapped))
        
        for i in range(max_lines):
            if i < len(key_wrapped):
                col1 = key_wrapped[i]
            else:
                col1 = ""
            
            if i < len(value_wrapped):
                col2 = value_wrapped[i]
            else:
                col2 = ""
            
            table += f"{col_border} {row_color}{col1:<{col1_width}}{Style.RESET_ALL} {col_border} {row_color}{col2:<{col2_width}}{Style.RESET_ALL} {col_border}\n"
        
        table += border_line
    
    return table

def main():
    network_info = get_network_info()
    print(format_table(network_info))

if __name__ == "__main__":
    main()
