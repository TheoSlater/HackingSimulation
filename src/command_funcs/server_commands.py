import player
from servers import get_current_server
from colorama import Fore, Style
from hacking import check_firewall, brute_force_attack, exploit_service, exploit_server, crack_ssh_key
from tutorial import tutorial_active

def execute_brute_force_command():
    server = get_current_server()
    if not server:
        print(f"{Fore.RED}❌ Not connected to any server!{Style.RESET_ALL}")
        return

    brute_force_attack(server)

def execute_exploit_command(port=None):
    server = get_current_server()
    if not server:
        print(f"{Fore.RED}❌ Not connected to any server!{Style.RESET_ALL}")
        return

    if tutorial_active:
        # Always succeed during tutorial
        print(f"{Fore.GREEN}[+] Successfully exploited server!{Style.RESET_ALL}")
        server["root_access"] = True
        player.gain_xp(50)
        return

    # Normal exploit logic
    if port:
        exploit_service(server, str(port))
    else:
        exploit_server()

def execute_crack_ssh_command():
    server = get_current_server()
    if not server:
        print(f"{Fore.RED}❌ Not connected to any server!{Style.RESET_ALL}")
        return

    if check_firewall(server):
        return

    if server.get("auth_type") != "ssh_key":
        print(f"{Fore.RED}❌ This server doesn't use SSH key authentication!{Style.RESET_ALL}")
        return

    crack_ssh_key(server)