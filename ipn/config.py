import os
import platform
import toml

def get_config_path():
    if platform.system() == "Windows":
        config_dir = os.path.join(os.getenv("LOCALAPPDATA"), "ipn")
    else:
        config_dir = os.path.join(os.getenv("HOME"), ".config", "ipn")
    config_file = os.path.join(config_dir, "config.toml")
    return config_dir, config_file

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

def read_config():
    _, config_file = get_config_path()
    with open(config_file, 'r') as file:
        return toml.load(file)
