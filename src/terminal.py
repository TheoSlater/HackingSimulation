import readline
from commands import execute_command
from colorama import Fore, Style
import servers

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
        return f"{Fore.GREEN}hacker@{server_name}({server_ip}){Style.RESET_ALL}> "
    return f"{Fore.GREEN}hacker@terminal{Style.RESET_ALL}> "

def fake_terminal():
    print(f"{Fore.CYAN}Welcome to HackingSim Terminal{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Type 'help' for available commands{Style.RESET_ALL}")
    
    while True:
        try:
            command = input(get_prompt()).strip().lower()
            
            if command:
                history_completer.add_history(command)

            if command == "exit":
                print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
                break

            execute_command(command)

        except KeyboardInterrupt:
            print("\nExiting...")
            break