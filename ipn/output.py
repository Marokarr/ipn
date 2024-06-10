import textwrap
import json
from colorama import Fore, Style, init

init(autoreset=True)

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

def format_table(data, theme, col1_width=30, col2_width=60):
    border_char = theme.get('border_char', '+')
    header_border_char = theme.get('header_border_char', '-')
    column_border_char = theme.get('column_border_char', '|')
    
    border_line = f"{border_char}{header_border_char * (col1_width + 2)}{border_char}{header_border_char * (col2_width + 2)}{border_char}\n"
    col_border = column_border_char
    
    header_color = get_color(theme.get("header_color", "cyan"))
    row_color = get_color(theme.get("row_color", "yellow"))
    border_color = get_color(theme.get("border_color", "green"))
    reset_color = Style.RESET_ALL

    table = ""
    table += f"{border_color}{border_line}{reset_color}"
    table += f"{col_border} {header_color}{'Network Info':<{col1_width}}{reset_color} {col_border} {header_color}{'Details':<{col2_width}}{reset_color} {col_border}\n"
    table += f"{border_color}{border_line}{reset_color}"
    
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
            
            table += f"{col_border} {row_color}{col1:<{col1_width}}{reset_color} {col_border} {row_color}{col2:<{col2_width}}{reset_color} {col_border}\n"
        
        table += f"{border_color}{border_line}{reset_color}"
    
    return table

def format_json(data):
    return json.dumps(dict(data), indent=4)
