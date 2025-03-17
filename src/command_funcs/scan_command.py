from servers import list_servers, get_current_server, scan_ports, enumerate_services
from colorama import Fore, Style
import time

def execute_scan_command(level):
    """
    Scan network or current server
    Level 1: Basic network scan
    Level 2: Detailed network scan
    Level 3: Port scan current server
    Level 4: Service enumeration
    """
    if not level.isdigit() or int(level) not in [1, 2, 3, 4]:
        print("Usage: scan-analyse <level> (1-4)")
        print("1: Basic network scan")
        print("2: Detailed network scan")
        print("3: Port scan current server")
        print("4: Service enumeration")
        return

    level = int(level)
    if level in [3, 4]:
        server = get_current_server()
        if not server:
            print(f"{Fore.RED}Not connected to any server.{Style.RESET_ALL}")
            return
        
        if server.get("status", "online") != "online":
            print(f"{Fore.RED}❌ Server is {server['status'].upper()}{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}[*] Scanning {server['ip']}...{Style.RESET_ALL}")
        time.sleep(1)
        
        if level == 3:
            result = scan_ports(server)
        else:
            result = enumerate_services(server)
        print(result)
    else:
        list_servers(level)