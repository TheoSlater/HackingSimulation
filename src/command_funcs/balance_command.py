from colorama import Fore, Style
import player

def execute_balance_command():
    """Display player's current balance"""
    print(f"{Fore.GREEN}💰 Balance: ${player.get_balance()}{Style.RESET_ALL}")
