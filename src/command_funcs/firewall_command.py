from servers import get_current_server
from colorama import Fore, Style
import player
import random
import time

def execute_firewall_scan():
    """Scan the current server's firewall"""
    server = get_current_server()
    if not server:
        print(f"{Fore.RED}❌ Not connected to any server.{Style.RESET_ALL}")
        return

    firewall = server.get("firewall", {})
    if not firewall.get("enabled", False):
        print(f"{Fore.GREEN}✓ No firewall detected on this server.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}🔍 Scanning firewall...{Style.RESET_ALL}")
    time.sleep(1)
    
    strength = firewall.get("strength", 1)
    attempts = firewall.get("attempts", 0)
    
    strength_color = Fore.GREEN if strength <= 3 else Fore.YELLOW if strength <= 6 else Fore.RED
    print(f"Firewall Strength: {strength_color}{strength}/10{Style.RESET_ALL}")
    print(f"Failed Attempts: {attempts}")

def execute_firewall_bypass():
    """Attempt to bypass the server's firewall"""
    server = get_current_server()
    if not server:
        print(f"{Fore.RED}❌ Not connected to any server.{Style.RESET_ALL}")
        return

    firewall = server.get("firewall", {})
    if not firewall.get("enabled", False):
        print(f"{Fore.GREEN}✓ No firewall detected on this server.{Style.RESET_ALL}")
        return

    has_buster = player.has_tool("firewall_buster")
    strength = firewall.get("strength", 1)
    base_chance = max(10, 70 - (strength * 10))
    
    if has_buster:
        base_chance += 30
        print(f"{Fore.CYAN}[+] Firewall Buster tool activated{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}🔓 Attempting firewall bypass...{Style.RESET_ALL}")
    time.sleep(2)

    if random.randint(1, 100) <= base_chance:
        print(f"{Fore.GREEN}✓ Firewall successfully bypassed!{Style.RESET_ALL}")
        server["firewall"]["enabled"] = False
        player.gain_xp(25)
    else:
        print(f"{Fore.RED}❌ Bypass attempt failed!{Style.RESET_ALL}")
        server["firewall"]["attempts"] = server["firewall"].get("attempts", 0) + 1
