import argparse
import logging
from ipn.config import ensure_config_exists, read_config
from ipn.dns import get_dns_info
from ipn.firewall import get_firewall_status
from ipn.network import get_network_info, get_bandwidth_usage
from ipn.output import format_table, format_json
from ipn.vpn import get_vpn_status
from ipn.public_ip import get_public_ip
from ipn.logging_config import setup_logging

def main():
    setup_logging()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Display network information, including DNS servers, firewall status, VPN status, and public IP.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-f', '--firewall', action='store_true', help='Display firewall status')
    parser.add_argument('-v', '--vpn', action='store_true', help='Display VPN status')
    parser.add_argument('-a', '--all', action='store_true', help='Display all information')
    parser.add_argument('-p', '--public-ip', action='store_true', help='Display public IP address')
    parser.add_argument('-j', '--json', action='store_true', help='Output in JSON format')
    parser.add_argument('-b', '--bandwidth', action='store_true', help='Display bandwidth usage')
    args = parser.parse_args()

    try:
        ensure_config_exists()
        config = read_config()
        theme = config["theme"]
    except Exception as e:
        logging.error(f"Error reading configuration: {e}")
        return

    network_info = []

    try:
        if args.all or (not args.firewall and not args.vpn and not args.public_ip and not args.bandwidth):
            network_info = get_network_info()
            dns_info = get_dns_info()
            for adapter, dns_servers in dns_info.items():
                if dns_servers:
                    network_info.append((f"DNS Servers ({adapter})", ", ".join(dns_servers)))
    except Exception as e:
        logging.error(f"Error getting network info: {e}")

    try:
        if args.firewall or args.all:
            firewall_status = get_firewall_status()
            network_info.append(("Firewall Status", firewall_status))
    except Exception as e:
        logging.error(f"Error getting firewall status: {e}")

    try:
        if args.vpn or args.all:
            vpn_status = get_vpn_status()
            network_info.append(("VPN Status", vpn_status))
    except Exception as e:
        logging.error(f"Error getting VPN status: {e}")

    try:
        if args.public_ip or args.all:
            public_ip = get_public_ip()
            network_info.append(("Public IP", public_ip))
    except Exception as e:
        logging.error(f"Error getting public IP: {e}")

    try:
        if args.bandwidth or args.all:
            bandwidth_info = get_bandwidth_usage()
            for iface, stats in bandwidth_info.items():
                network_info.append((f"Bandwidth ({iface})", f"Sent: {stats['bytes_sent']} bytes, Received: {stats['bytes_recv']} bytes"))
    except Exception as e:
        logging.error(f"Error getting bandwidth usage: {e}")

    if not network_info:
        parser.print_help()
    else:
        if args.json:
            try:
                print(format_json(network_info))
            except Exception as e:
                logging.error(f"Error formatting JSON output: {e}")
        else:
            try:
                print(format_table(network_info, theme))
            except Exception as e:
                logging.error(f"Error formatting table output: {e}")

if __name__ == "__main__":
    main()
