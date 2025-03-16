import readline
from command_executor import execute_command_with_output
from colorama import Fore, Style
import player
import servers
from malware import update_all_servers_malware
import time
from tutorial import run_tutorial
from commands import COMMANDS, SUDO_COMMANDS, SPECIAL_COMMANDS

history = []

# Configure readline
readline.parse_and_bind('tab: complete')
readline.set_history_length(1000)

# Add custom history handling
class HistoryCompleter:
    def __init__(self):
        self.history = []
    
    def add_history(self, command):
        if command and command.strip():
            self.history.append(command.strip())
            readline.add_history(command)

history_completer = HistoryCompleter()

def get_prompt():
    """Get the terminal prompt based on current server connection"""
    if servers.current_server:
        server_name = servers.current_server['name']
        server_ip = servers.current_server['ip']
        return f"{Fore.GREEN}hacker@{server_name}{Style.RESET_ALL}> "
    return f"{Fore.GREEN}hacker@terminal{Style.RESET_ALL}> "

def fake_terminal():
    print(f"{Fore.CYAN}Welcome to HackingSim Terminal{Style.RESET_ALL}")
    
    # Check if tutorial needs to be run
    if not player.player_data.get("tutorial_complete", False):
        run_tutorial()
    
    print(f"{Fore.YELLOW}Type 'help' for available commands{Style.RESET_ALL}")
    
    last_malware_check = time.time()
    
    while True:
        try:
            # Check malware income every minute
            if time.time() - last_malware_check >= 60:
                update_all_servers_malware(servers.servers)
                last_malware_check = time.time()

            command = input(get_prompt()).strip().lower()
            
            if command:
                history_completer.add_history(command)
                execute_command_with_output(command, COMMANDS, SUDO_COMMANDS, SPECIAL_COMMANDS)

        except KeyboardInterrupt:
            print("\nExiting...")
            break