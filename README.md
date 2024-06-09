# IPN - Network Information Tool

A simple tool to display network information, including DNS servers, on various platforms.

## Features

- Displays operating system information
- Shows hostname and local IP address
- Lists network interfaces and their IP addresses
- Supports theming via a configuration file

## Installation

### Requirements

- Python 3.6 or higher
- `psutil`, `tabulate`, `toml`, and `colorama` libraries

### Install via pip

Download, extract and enter the directoy

```sh
cd ipn
```

To install the `ipn` package, run:

```sh
pip install .
```

This will install the `ipn` command and ensure it is available in your PATH.

## Configuration

The tool supports theming via a configuration file. The configuration file should be located at:

- **Linux/MacOS**: `~/.config/ipn/config.toml`
- **Windows**: `%LOCALAPPDATA%\ipn\config.toml`

### Default Configuration

If the configuration file does not exist, it will be created with the following default settings:

```toml
[theme]
border_char = "+"
header_border_char = "-"
column_border_char = "|"
header_color = "cyan"
row_color = "white"
```

You can modify the configuration file to change the theme.

## Usage

After installing the package, you can run the `ipn` command from any terminal:

```sh
ipn
```

## Troubleshooting

### Command Not Found

If the `ipn` command is not found, ensure the Python scripts directory is in your PATH.

#### Linux/MacOS/WSL

1. **Locate the Scripts Directory**:
   Run the following command to determine where Python user scripts are installed:

   ```sh
   python -m site --user-base
   ```

   Typically, the scripts are located in `~/.local/bin`.

2. **Add to PATH**:
   Add the scripts directory to your PATH by modifying your shell configuration file (`~/.bashrc`, `~/.zshrc`, or similar):
   ```sh
   echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
   ```
   Source the file to apply the changes:
   ```sh
   source ~/.bashrc
   ```

#### Windows

1. **Locate the Scripts Directory**:
   The scripts are typically located in `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python<version>\Scripts`.

2. **Add to PATH**:
   - Open the Start Search, type in "env", and select "Edit the system environment variables".
   - In the System Properties window, click on the "Environment Variables..." button.
   - In the Environment Variables window, find the "Path" variable in the "System variables" section, select it, and click "Edit...".
   - Add the path to the scripts directory, for example:
     ```sh
     C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python<version>\Scripts
     ```
   - Click OK on all windows to save the changes.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
