import time
from colorama import Fore, Style
import random
import player

def list_sensitive_data(server):
    """List available sensitive data on the server"""
    sensitive_data = server.get("sensitive_data", {})
    if not sensitive_data:
        print(f"{Fore.YELLOW}No sensitive data found on this server.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}📁 Available Sensitive Data:{Style.RESET_ALL}")
    for filename, data in sensitive_data.items():
        print(f"- {filename} ({data['description']}) - Estimated value: ${data['value']}")

def steal_data(server, filename):
    """Attempt to steal sensitive data"""
    if not server.get("root_access", False):
        print(f"{Fore.RED}❌ Root access required to steal data!{Style.RESET_ALL}")
        return

    sensitive_data = server.get("sensitive_data", {})
    if filename not in sensitive_data:
        print(f"{Fore.RED}❌ File not found: {filename}{Style.RESET_ALL}")
        return

    data = sensitive_data[filename]
    print(f"\n{Fore.CYAN}[*] Attempting to exfiltrate {filename}...{Style.RESET_ALL}")
    
    # Simulate data transfer
    chunks = random.randint(3, 8)
    for i in range(chunks):
        time.sleep(random.uniform(1, 3))
        print(f"{Fore.CYAN}[*] Transferring chunk {i+1}/{chunks}...{Style.RESET_ALL}")

    # Award money and remove the data
    reward = data["value"]
    player.add_money(reward)
    del server["sensitive_data"][filename]
    
    print(f"{Fore.GREEN}✅ Successfully exfiltrated {filename}!")
    print(f"💰 Sold on dark web for ${reward}!{Style.RESET_ALL}")
    player.gain_xp(30)
