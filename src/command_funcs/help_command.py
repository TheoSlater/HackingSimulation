COMMANDS = {
    "help": "Show available commands.",
    "scan-analyse <level>": "Scan for servers (1 = basic, 2 = detailed).",
    "connect <server_name/ip>": "Connect to a server.",
    "disconnect": "Disconnect from the current server.",
    "sudo brute-force": "Attempt to hack the current server.",
    "sudo exploit": "Try to find a backdoor exploit.",
    "ls": "List files on the hacked server.",
    "open <filename>": "View the contents of a file.",
    "tools": "View available hacking tools.",
    "buy <tool_name>": "Buy a hacking tool.",
    "balance": "Check money balance.",
    "hack": "Attempt to hack the current server for money.",
    "exit": "Quit the game.",
}

def execute_help_command():
    print("\nAvailable commands:")
    for cmd, desc in COMMANDS.items():
        print(f"- {cmd}: {desc}")