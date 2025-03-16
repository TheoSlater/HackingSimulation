import json
import os
from colorama import Fore, Style

# Path to the JSON file
data_path = os.path.join(os.path.dirname(__file__), "./data/servers.json")

def load_servers():
    """ Load servers from servers.json """
    if os.path.exists(data_path):
        with open(data_path, "r") as f:
            return json.load(f)
    else:
        print(f"{Fore.RED}❌ Error: servers.json not found.{Style.RESET_ALL}")
        return {}

# Load servers at startup
servers = load_servers()
current_server = None

def list_servers(level):
    """ List available servers. Level 1 shows names, Level 2 shows IPs and security. """
    print(f"\n{Fore.CYAN}🌐 Available Servers:{Style.RESET_ALL}")
    for ip, server in servers.items():
        if level == 1:
            print(f"- {server['name']}")
        else:
            security_color = Fore.GREEN if server['security'] <= 3 else Fore.YELLOW if server['security'] <= 6 else Fore.RED
            print(f"- {server['name']} ({ip}) | Security Level: {security_color}{server['security']}{Style.RESET_ALL}")

def connect_to_server(identifier):
    """ Connect to a server by name or IP. """
    global current_server
    
    # Check if already connected
    if current_server:
        print(f"{Fore.RED}❌ Already connected to {current_server['name']}. Please disconnect first.{Style.RESET_ALL}")
        return False
        
    for ip, server in servers.items():
        if identifier.lower() in (ip.lower(), server["name"].lower()):
            current_server = server.copy()  # Copy server data to avoid modifying original
            current_server["ip"] = ip  # Store the IP inside the server data
            print(f"{Fore.GREEN}🔗 Connected to {server['name']} ({ip}){Style.RESET_ALL}")
            return True
    print(f"{Fore.RED}❌ Server not found.{Style.RESET_ALL}")
    return False

def disconnect():
    """ Disconnect from the current server. """
    global current_server
    if current_server:
        print(f"{Fore.YELLOW}🔌 Disconnected from {current_server['name']}{Style.RESET_ALL}")
        current_server = None
    else:
        print(f"{Fore.RED}❌ Not connected to any server.{Style.RESET_ALL}")

def get_current_server():
    """ Get the currently connected server. """
    return current_server

def is_connected():
    """ Check if currently connected to a server. """
    return current_server is not None