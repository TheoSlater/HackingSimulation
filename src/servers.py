import json
import os
import random
from colorama import Fore, Style
from ssh_generator import generate_ssh_key, generate_key_fingerprint
from data.server_data import SERVERS, current_server

# Paths
data_path = os.path.join(os.path.dirname(__file__), "./data/servers.json")
vuln_path = os.path.join(os.path.dirname(__file__), "./data/vulnerabilities.json")

def load_vulnerabilities():
    """Load vulnerability database"""
    if os.path.exists(vuln_path):
        with open(vuln_path, "r") as f:
            return json.load(f)
    return {}

def generate_random_ports():
    """Generate a random set of open ports"""
    possible_ports = list(load_vulnerabilities().keys())
    num_ports = random.randint(2, 5)  # Each server gets 2-5 random ports
    selected_ports = random.sample(possible_ports, min(num_ports, len(possible_ports)))
    return {port: {} for port in selected_ports}

def assign_random_vulnerabilities(server):
    """Randomly assign vulnerabilities to server ports"""
    vulns_db = load_vulnerabilities()
    # Generate random ports first
    server["ports"] = generate_random_ports()
    
    # For each port in the server
    for port in server["ports"].keys():
        if port in vulns_db:
            # Get available vulnerabilities for this port
            available_vulns = vulns_db[port]["vulnerabilities"]
            # Randomly decide how many vulnerabilities (0-2)
            num_vulns = random.randint(0, 2)
            if num_vulns > 0:
                # Randomly select vulnerabilities
                selected_vulns = random.sample(available_vulns, min(num_vulns, len(available_vulns)))
                # Initialize service info
                server["ports"][port] = {
                    "name": vulns_db[port]["service"],
                    "version": selected_vulns[0]["version"],
                    "vulnerabilities": selected_vulns
                }

# Update current_server handling to use the one from server_data
from data.server_data import current_server as global_current_server

def get_current_server():
    return global_current_server

def list_servers(level):
    """List all servers and their details"""
    print(f"\n{Fore.CYAN}🌐 Available Servers:{Style.RESET_ALL}")
    for ip, server in SERVERS.items():
        status = server.get("status", "online")
        name = server['name']
        status_color = {
            "online": Fore.GREEN,
            "offline": Fore.RED,
            "crashed": Fore.RED,
            "overloaded": Fore.RED
        }.get(status, Fore.YELLOW)
        
        server_str = f"- {name} ({ip})"
        if status != "online":
            server_str = f"- ~~{name} ({ip})~~ [{status_color}{status.upper()}{Style.RESET_ALL}]"

        if level == 1:
            print(server_str)
        else:
            security_level = server.get('security', 1)  # Use get() with default
            security_color = Fore.GREEN if security_level <= 3 else Fore.YELLOW if security_level <= 6 else Fore.RED
            print(f"{server_str} | Security Level: {security_color}{security_level}{Style.RESET_ALL}")

def connect_to_server(identifier):
    """ Connect to a server by name or IP. """
    global global_current_server
    
    # Check if already connected
    if global_current_server:
        print(f"{Fore.RED}❌ Already connected to {global_current_server['name']}. Please disconnect first.{Style.RESET_ALL}")
        return False
        
    for ip, server in SERVERS.items():
        if identifier.lower() == ip.lower() or identifier.lower() == server["name"].lower():
            if server.get("status", "online") != "online":
                print(f"{Fore.RED}❌ Cannot connect: Server is {server['status']}{Style.RESET_ALL}")
                return False
                
            global_current_server = server  # Changed this line to directly assign server instead of current_server["ip"] = ip
            global_current_server["ip"] = ip  # Add IP after assignment
            print(f"{Fore.GREEN}🔗 Connected to {server['name']} ({ip}){Style.RESET_ALL}")
            return True
    
    print(f"{Fore.RED}❌ Server not found.{Style.RESET_ALL}")
    return False

def disconnect():
    """ Disconnect from the current server. """
    global global_current_server
    if global_current_server:
        print(f"{Fore.YELLOW}🔌 Disconnected from {global_current_server['name']}{Style.RESET_ALL}")
        global_current_server = None
    else:
        print(f"{Fore.RED}❌ Not connected to any server.{Style.RESET_ALL}")

def is_connected():
    """ Check if currently connected to a server. """
    return global_current_server is not None

def scan_ports(server):
    """Scan server ports and return open ports with their services"""
    ports = server.get("ports", {})
    if not ports:
        return "No open ports found."
    
    result = "\nOpen ports:\n"
    for port, service in ports.items():
        service_name = service.get('name', 'Unknown')
        service_version = service.get('version', '')
        result += f"PORT {port}/tcp - {service_name} {service_version}\n"
    return result

def enumerate_services(server):
    """Get detailed information about services running on the server"""
    services = []
    for port, service in server.get("ports", {}).items():
        vulns = service.get("vulnerabilities", [])
        if vulns:
            services.append(f"\n[!] Vulnerable service on port {port}:")
            services.append(f"   - Service: {service['name']} {service.get('version', '')}")
            for vuln in vulns:
                services.append(f"   - CVE: {vuln['cve']}")
                services.append(f"   - Description: {vuln['description']}")
    return "\n".join(services) if services else "No vulnerable services found."

def set_server_status(server, status):
    """Change server status and handle disconnection"""
    if server and status in ["online", "offline", "crashed", "overloaded"]:
        server["status"] = status
        if status != "online":
            disconnect()
        return True
    return False