import json
import os
import random
from colorama import Fore, Style
from ssh_generator import generate_ssh_key, generate_key_fingerprint

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

def load_servers():
    """Load servers and randomly assign vulnerabilities"""
    if os.path.exists(data_path):
        with open(data_path, "r") as f:
            servers = json.load(f)
            # Assign random vulnerabilities to each server
            for server in servers.values():
                assign_random_vulnerabilities(server)
                if server.get("auth_type") == "ssh_key":
                    server["ssh_key"] = {
                        "private_key": generate_ssh_key(),
                        "fingerprint": generate_key_fingerprint()
                    }
            return servers
    else:
        print(f"{Fore.RED}❌ Error: servers.json not found.{Style.RESET_ALL}")
        return {}

# Load servers at startup
servers = load_servers()
current_server = None

def list_servers(level):
    print(f"\n{Fore.CYAN}🌐 Available Servers:{Style.RESET_ALL}")
    for ip, server in servers.items():
        if level == 1:
            print(f"- {server['name']} ({ip})") 
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
        if identifier.lower() == ip.lower() or identifier.lower() == server["name"].lower():
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

def scan_ports(server):
    """Scan server ports and return open ports with their services"""
    ports = server.get("ports", {})
    if not ports:
        return "No open ports found."
    
    result = "\nOpen ports:\n"
    for port, service in ports.items():
        result += f"PORT {port}/tcp - {service['name']} {service.get('version', '')}\n"
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