import time
import random
from servers import get_current_server
import player
from colorama import Fore, Style
from tutorial import tutorial_active

def execute_hack_command():
    """Hack a server to steal its money if the player has root access."""
    server = get_current_server()
    if not server:
        print(f"{Fore.RED}❌ Not connected to any server.{Style.RESET_ALL}")
        return
    
    if not server.get("root_access", False):
        print(f"{Fore.RED}⛔ You must have root access to hack this server!{Style.RESET_ALL}")
        return

    if "money" not in server or server["money"] <= 0:
        print(f"{Fore.YELLOW}💸 This server has no money to steal.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.BLUE}[+] Attempting to hack {server['name']} bank account...{Style.RESET_ALL}")
    time.sleep(2)

    # Calculate amount to steal (between $50-$150)
    max_steal = min(150, server["money"])
    stolen_amount = max_steal if tutorial_active else random.randint(50, max_steal)
    
    # Always succeed during tutorial
    if tutorial_active:
        player.add_money(stolen_amount)
        server["money"] -= stolen_amount
        print(f"{Fore.GREEN}💰 Success! Stole ${stolen_amount} from {server['name']}.{Style.RESET_ALL}")
        if server["money"] > 0:
            print(f"{Fore.CYAN}ℹ️ Server still has ${server['money']} available.{Style.RESET_ALL}")
        player.gain_xp(10)
        return

    # Normal hack logic for non-tutorial
    if random.randint(1, 100) <= 70:  # 70% success rate
        player.add_money(stolen_amount)
        server["money"] -= stolen_amount
        print(f"{Fore.GREEN}💰 Success! Stole ${stolen_amount} from {server['name']}.{Style.RESET_ALL}")
        if server["money"] > 0:
            print(f"{Fore.CYAN}ℹ️ Server still has ${server['money']} available.{Style.RESET_ALL}")
        player.gain_xp(10)
    else:
        print(f"{Fore.RED}❌ Hack failed! Bank transfer was blocked.{Style.RESET_ALL}")
