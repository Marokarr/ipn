import os
import platform
import socket
import psutil
import textwrap
import toml
from colorama import Fore, Style, init

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
    dns_dict = {}
    if os_type == "Windows":
        # Windows specific method to get DNS servers
        output = os.popen("ipconfig /all").read()
        current_adapter = None
        for line in output.splitlines():
            if "adapter" in line:
                current_adapter = line.strip(':')
                dns_dict[current_adapter] = []
            elif "DNS Servers" in line:
                dns_dict[current_adapter].append(line.split(":")[-1].strip())
            elif current_adapter and dns_dict[current_adapter] and line.startswith(' '):
                dns_dict[current_adapter].append(line.strip())
    else:
        # Unix-like systems method to get DNS servers
        dns_dict["Global DNS"] = []
        with open("/etc/resolv.conf") as f:
            for line in f:
                if line.startswith("nameserver"):
                    dns_dict["Global DNS"].append(line.split()[1])
    
    for adapter, dns_servers in dns_dict.items():
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
