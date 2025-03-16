import json
import os

# Path to the JSON file
data_path = os.path.join(os.path.dirname(__file__), "./data/servers.json")

def load_servers():
    """ Load servers from servers.json """
    if os.path.exists(data_path):
        with open(data_path, "r") as f:
            return json.load(f)
    else:
        print("❌ Error: servers.json not found.")
        return {}

# Load servers at startup
servers = load_servers()
current_server = None

def list_servers(level):
    """ List available servers. Level 1 shows names, Level 2 shows IPs and security. """
    print("\n🌐 Available Servers:")
    for ip, server in servers.items():
        if level == 1:
            print(f"- {server['name']}")
        else:
            print(f"- {server['name']} ({ip}) | Security Level: {server['security']}")

def connect_to_server(identifier):
    """ Connect to a server by name or IP. """
    global current_server
    for ip, server in servers.items():
        if identifier in (ip, server["name"]):
            current_server = server.copy()  # Copy server data to avoid modifying original
            current_server["ip"] = ip  # Store the IP inside the server data
            print(f"🔗 Connected to {server['name']} ({ip})")
            return
    print("❌ Server not found.")


def disconnect():
    """ Disconnect from the current server. """
    global current_server
    if current_server:
        print(f"🔌 Disconnected from {current_server['name']}")
        current_server = None
    else:
        print("❌ Not connected to any server.")

def get_current_server():
    """ Get the currently connected server. """
    return current_server
