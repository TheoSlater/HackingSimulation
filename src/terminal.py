import readline
from command_executor import execute_command_with_output
from colorama import Fore, Style
import player
import servers
from malware import update_all_servers_malware
import time
from tutorial import run_tutorial
from commands import COMMANDS, SUDO_COMMANDS, SPECIAL_COMMANDS
from data.server_data import SERVERS
from data.player_data import PLAYER

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
    
    if not player.PLAYER.tutorial_complete:
        run_tutorial()
    else:
        print(f"{Fore.YELLOW}Type 'help' for available commands{Style.RESET_ALL}")
    
    last_malware_check = time.time()
    last_save = time.time()
    
    while True:
        try:
            current_time = time.time()
            
            # Check malware income every minute
            if current_time - last_malware_check >= 60:
                update_all_servers_malware(SERVERS)
                last_malware_check = current_time

            # Auto-save every 5 minutes
            if current_time - last_save >= 300:
                PLAYER.save_game()
                print(f"{Fore.CYAN}🔄 Game auto-saved{Style.RESET_ALL}")
                last_save = current_time

            command = input(get_prompt()).strip().lower()
            
            if command:
                history_completer.add_history(command)
                execute_command_with_output(command, COMMANDS, SUDO_COMMANDS, SPECIAL_COMMANDS)

        except KeyboardInterrupt:
            print("\nExiting...")
            break