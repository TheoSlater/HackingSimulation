COMMANDS = {
    "help": "Show available commands.",
    "scan-analyse <level>": "Scan network/server (1=basic net, 2=detailed net, 3=ports, 4=service enum)",
    "connect <server_name/ip>": "Connect to a server.",
    "disconnect": "Disconnect from the current server.",
    "sudo brute-force": "Attempt to hack the current server.",
    "sudo exploit <port>": "Try to exploit vulnerabilities on a specific port",
    "sudo exploit": "Try to find a backdoor exploit.",
    "sudo crack-ssh": "Attempt to crack SSH key authentication",
    "exfiltrate list": "View available sensitive data files",
    "exfiltrate <filename>": "Steal specific sensitive data file",
    "ls": "List files on the hacked server.",
    "open <filename>": "View the contents of a file.",
    "tools": "View available hacking tools.",
    "buy <tool_name>": "Buy a hacking tool.",
    "balance": "Check money balance.",
    "hack": "Attempt to hack the current server for money.",
    "firewall-scan": "Scan the current server's firewall",
    "firewall-bypass": "Attempt to bypass the server's firewall",
    "exit": "Quit the game.",
    "malware": "List available malware types",
    "malware-status": "Check deployed malware status",
    "malware-deploy <type>": "Deploy malware to current server",
    "steal-cc": "Steal and sell credit card data from the server",
    "touch <filename>": "Create a new custom script/virus",
    "run <filename>": "Run a custom script on the current server",
}

def execute_help_command():
    print("\nAvailable commands:")
    for cmd, desc in COMMANDS.items():
        print(f"- {cmd}: {desc}")