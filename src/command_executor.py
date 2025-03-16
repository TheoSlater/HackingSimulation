from colorama import Fore, Style

def execute_command_with_output(command, commands_dict, sudo_commands_dict, special_commands_dict):
    """Execute a command and return its output"""
    if not command:
        return

    parts = command.split(" ", 1)
    cmd = parts[0].lower()

    # Handle special commands
    if cmd in special_commands_dict:
        special_commands_dict[cmd]()
        return

    # Handle sudo commands
    if cmd == "sudo":
        handle_sudo_command(parts, sudo_commands_dict)
        return

    # Handle regular commands
    if cmd not in commands_dict:
        print(f"{Fore.RED}Unknown command. Type 'help' for a list of commands.{Style.RESET_ALL}")
        return

    func, usage = commands_dict[cmd]
    
    # Check if command requires arguments
    if usage and len(parts) < 2:
        print(f"{Fore.YELLOW}Usage: {cmd} {usage}{Style.RESET_ALL}")
        return

    # Execute command
    try:
        if usage:
            func(parts[1])
        else:
            func()
    except Exception as e:
        print(f"{Fore.RED}Error executing command: {str(e)}{Style.RESET_ALL}")

def handle_sudo_command(parts, sudo_commands):
    """Handle sudo commands with proper error checking"""
    if len(parts) < 2:
        print(f"{Fore.YELLOW}Usage: sudo <command> [port]{Style.RESET_ALL}")
        return

    command_parts = parts[1].split()
    sudo_cmd = command_parts[0]
    
    if sudo_cmd in sudo_commands:
        try:
            # Handle port parameter for exploit command
            if sudo_cmd == "exploit" and len(command_parts) > 1:
                sudo_commands[sudo_cmd](command_parts[1])
            else:
                sudo_commands[sudo_cmd]()
        except Exception as e:
            print(f"{Fore.RED}Error executing sudo command: {str(e)}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Unknown sudo command: {sudo_cmd}{Style.RESET_ALL}")
