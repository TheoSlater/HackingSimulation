from command_funcs.data_commands import execute_exfiltrate_command
from command_funcs.server_commands import execute_crack_ssh_command
import player
from colorama import Fore, Style
from command_funcs import (
    execute_help_command,
    execute_scan_command,
    execute_connect_command,
    execute_disconnect_command,
    execute_brute_force_command,
    execute_exploit_command,
    execute_ls_command,
    execute_open_command,
    execute_tools_command,
    execute_buy_command,
    execute_hack_command,
    execute_firewall_scan,
    execute_firewall_bypass,
    execute_balance_command
)
from command_funcs.credit_card_fraud import steal_card_details

# Command definitions with their usage patterns
COMMANDS = {
    "help": (execute_help_command, None),
    "scan-analyse": (execute_scan_command, "<level>"),
    "connect": (execute_connect_command, "<server_name/ip>"),
    "disconnect": (execute_disconnect_command, None),
    "ls": (execute_ls_command, None),
    "open": (execute_open_command, "<filename>"),
    "tools": (execute_tools_command, None),
    "buy": (execute_buy_command, "<tool_name>"),
    "steal-cc": (steal_card_details, None),
    "firewall-scan": (execute_firewall_scan, None),
    "firewall-bypass": (execute_firewall_bypass, None),
    "balance": (execute_balance_command, None),
    "exfiltrate": (execute_exfiltrate_command, "<filename>"),
}

SUDO_COMMANDS = {
    "brute-force": execute_brute_force_command,
    "exploit": execute_exploit_command,
    "hack": execute_hack_command,
    "crack-ssh": execute_crack_ssh_command
}

SPECIAL_COMMANDS = {
    "exit": lambda: (print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}"), exit())
}

def print_usage(command, usage=None):
    """Print command usage with color formatting"""
    if usage:
        print(f"{Fore.YELLOW}Usage: {command} {usage}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Usage: {command}{Style.RESET_ALL}")

def handle_special_command(cmd):
    """Handle special commands like exit and balance"""
    if cmd in SPECIAL_COMMANDS:
        SPECIAL_COMMANDS[cmd]()
        return True
    return False

def handle_sudo_command(parts):
    """Handle sudo commands with proper error checking"""
    if len(parts) < 2:
        print_usage("sudo", "<command> [port]")
        return True

    command_parts = parts[1].split()
    sudo_cmd = command_parts[0]
    
    if sudo_cmd in SUDO_COMMANDS:
        try:
            # Handle port parameter for exploit command
            if sudo_cmd == "exploit" and len(command_parts) > 1:
                SUDO_COMMANDS[sudo_cmd](command_parts[1])
            else:
                SUDO_COMMANDS[sudo_cmd]()
        except Exception as e:
            print(f"{Fore.RED}Error executing sudo command: {str(e)}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Unknown sudo command: {sudo_cmd}{Style.RESET_ALL}")
    return True

def execute_command(command):
    """Main command execution function"""
    if not command:
        return

    parts = command.split(" ", 1)
    cmd = parts[0].lower()

    # Handle special commands first
    if handle_special_command(cmd):
        return

    # Handle sudo commands
    if cmd == "sudo":
        handle_sudo_command(parts)
        return

    # Handle regular commands
    if cmd not in COMMANDS:
        print(f"{Fore.RED}Unknown command. Type 'help' for a list of commands.{Style.RESET_ALL}")
        return

    func, usage = COMMANDS[cmd]
    
    # Check if command requires arguments
    if usage and len(parts) < 2:
        print_usage(cmd, usage)
        return

    # Execute command with error handling
    try:
        if usage:
            func(parts[1])
        else:
            func()
    except Exception as e:
        print(f"{Fore.RED}Error executing command: {str(e)}{Style.RESET_ALL}")