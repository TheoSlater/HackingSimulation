from servers import list_servers, connect_to_server, disconnect, get_current_server
from hacking import brute_force_attack, exploit_server
from hacking_tools import list_tools, purchase_tool
import player

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
    "exit": "Quit the game."
}

def execute_command(command):
    parts = command.split(" ", 1)
    cmd = parts[0]

    if cmd == "help":
        print("\nAvailable commands:")
        for cmd, desc in COMMANDS.items():
            print(f"- {cmd}: {desc}")

    elif cmd == "scan-analyse":
        if len(parts) < 2 or not parts[1].isdigit():
            print("Usage: scan-analyse <level> (1 or 2)")
            return
        list_servers(int(parts[1]))

    elif cmd == "connect":
        if len(parts) < 2:
            print("Usage: connect <server_name/ip>")
            return
        connect_to_server(parts[1])

    elif cmd == "disconnect":
        disconnect()

    elif cmd == "sudo":
        if len(parts) < 2:
            print("Usage: sudo <command>")
            return
        if parts[1] == "brute-force":
            brute_force_attack()
        elif parts[1] == "exploit":
            exploit_server()
        else:
            print(f"Unknown sudo command: {parts[1]}")

    elif cmd == "ls":
        server = get_current_server()
        if server:
            if server.get("root_access", False):  # Check if root access is granted
                print("\n📂 Files on the server:")
                for file in server.get("files", {}):
                    print(f"- {file}")
            else:
                print("❌ Access Denied. You need root access to list files.")
        else:
            print("❌ Not connected to a server.")

    elif cmd == "open":
        if len(parts) < 2:
            print("Usage: open <filename>")
            return

        server = get_current_server()
        if server:
            if server.get("root_access", False):  # Check if root access is granted
                filename = parts[1]
                if filename in server.get("files", {}):
                    print(f"\n📄 Contents of {filename}:")
                    print(server["files"][filename])
                else:
                    print(f"❌ File '{filename}' not found on this server.")
            else:
                print("❌ Access Denied. You need root access to open files.")
        else:
            print("❌ Not connected to a server.")

    elif cmd == "tools":
        list_tools()

    elif cmd == "buy":
        if len(parts) < 2:
            print("Usage: buy <tool_name>")
            return
        purchase_tool(parts[1])

    elif cmd == "balance":
        print(f"💰 Balance: ${player.get_balance()}")

    elif cmd == "exit":
        print("Goodbye!")
        exit()

    else:
        print("Unknown command. Type 'help' for a list of commands.")
