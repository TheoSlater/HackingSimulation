from data.player_data import PLAYER
from colorama import Fore, Style

def get_balance():
    return PLAYER.money

def add_money(amount):
    PLAYER.money += amount
    PLAYER.save_game()  # Save after each change

def deduct_money(amount):
    if PLAYER.money >= amount:
        PLAYER.money -= amount
        PLAYER.save_game()  # Save after each change
        return True
    return False

def has_tool(tool_name):
    return tool_name in PLAYER.tools

def buy_tool(tool_name, cost):
    if has_tool(tool_name):
        print(f"{Fore.RED}❌ You already own {tool_name}!{Style.RESET_ALL}")
        return False
    
    if deduct_money(cost):
        PLAYER.tools.append(tool_name)
        PLAYER.save_game()  # Save after purchase
        print(f"{Fore.GREEN}✅ Purchased {tool_name}!{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}❌ Not enough money!{Style.RESET_ALL}")
        return False

def gain_xp(amount):
    PLAYER.xp += amount
    PLAYER.save_game()  # Save after each change
    print(f"{Fore.CYAN}✨ Gained {amount} XP!{Style.RESET_ALL}")

def increase_wanted_level():
    PLAYER.wanted_level += 1
    PLAYER.save_game()  # Save after each change
    print(f"{Fore.RED}🚨 Wanted Level increased to {PLAYER.wanted_level}!{Style.RESET_ALL}")

def get_wanted_level():
    return PLAYER.wanted_level

# Add direct access to PLAYER object
__all__ = ['PLAYER']

