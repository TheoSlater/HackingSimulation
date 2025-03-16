import time
import random
from servers import get_current_server
import player
from colorama import Fore, Style

def execute_hack_command():
    """ Hack a server to steal its money if the player has root access. """
    server = get_current_server()
    if not server:
        print(f"{Fore.RED}❌ Not connected to any server.{Style.RESET_ALL}")
        return
    
    if not server.get("root_access", False):  # Check if root access is granted
        print(f"{Fore.RED}⛔ You must have root access to hack this server!{Style.RESET_ALL}")
        return

    if "money" not in server or server["money"] <= 0:
        print(f"{Fore.YELLOW}💸 This server has no money to steal.{Style.RESET_ALL}")
        return

    security_level = server.get("security", 1)
    hack_chance = 80 - (security_level * 10)  # Higher security = lower chance
    print(f"\n{Fore.BLUE}[+] Attempting to hack {server['name']} bank account...{Style.RESET_ALL}")

    time.sleep(2)

    if random.randint(1, 100) <= hack_chance:
        stolen_amount = server["money"]
        player.add_money(stolen_amount)
        server["money"] = 0  # Set money to 0 after hacking
        print(f"{Fore.GREEN}💰 Success! Stole ${stolen_amount} from {server['name']}.{Style.RESET_ALL}")
        player.gain_xp(50)
    else:
        print(f"{Fore.RED}❌ Hack failed! Server security was too strong.{Style.RESET_ALL}")
