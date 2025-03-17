import time
from colorama import Fore, Style
import player
from command_executor import execute_command_with_output

tutorial_active = False

def run_tutorial():
    """Run the interactive tutorial"""
    from commands import COMMANDS, SUDO_COMMANDS, SPECIAL_COMMANDS 
    global tutorial_active
    tutorial_active = True
    print(f"\n{Fore.CYAN}=== Welcome to HackingSim Tutorial ==={Style.RESET_ALL}")
    print("This tutorial will guide you through hacking your first server.")
    input("Press Enter to continue...")

    steps = [
        ("First, let's scan the network to find available servers.", "scan-analyse 1"),
        ("Now let's get more details about these servers.", "scan-analyse 2"),
        ("Let's connect to AlphaNet.", "connect alphanet"),
        ("Check if there's a firewall.", "firewall-scan"),
        ("Let's try to bypass it.", "firewall-bypass"),
        ("Now let's see what ports are open.", "scan-analyse 3"),
        ("Check for vulnerabilities on these ports.", "scan-analyse 4"),
        ("Let's try to exploit one of the open ports.", "sudo exploit 80"),
        ("Now that we have access, let's steal some money.", "hack"),
        ("Now, lets look for sensitive data.", "exfiltrate list"),
        ("Finally, let's steal some sensitivesdv data.", "exfiltrate customer_records.csv")
    ]

    for instruction, command in steps:
        print(f"\n{Fore.YELLOW}[Tutorial] {instruction}")
        print(f"{Fore.GREEN}[Tutorial] {command}{Style.RESET_ALL}")
        user_input = input("> ").strip().lower()
        
        # Execute the actual command using new executor
        execute_command_with_output(user_input, COMMANDS, SUDO_COMMANDS, SPECIAL_COMMANDS)
        
        time.sleep(1)

    tutorial_active = False
    print(f"\n{Fore.CYAN}=== Tutorial Complete! ==={Style.RESET_ALL}")
    print("You now know the basics of hacking servers!")
    print("Type 'help' anytime to see all available commands.")
    
    # Mark tutorial as complete and save state
    player.PLAYER.tutorial_complete = True
    player.PLAYER.save_game()  # Add this line to save the state

