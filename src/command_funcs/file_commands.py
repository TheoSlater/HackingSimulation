from servers import get_current_server

def execute_ls_command():
    server = get_current_server()
    if server:
        if server.get("root_access", False):
            print("\n📂 Files on the server:")
            for file in server.get("files", {}):
                print(f"- {file}")
        else:
            print("❌ Access Denied. You need root access to list files.")
    else:
        print("❌ Not connected to a server.")

def execute_open_command(filename):
    if not filename:
        print("Usage: open <filename>")
        return

    server = get_current_server()
    if server:
        if server.get("root_access", False):
            if filename in server.get("files", {}):
                print(f"\n📄 Contents of {filename}:")
                print(server["files"][filename])
            else:
                print(f"❌ File '{filename}' not found on this server.")
        else:
            print("❌ Access Denied. You need root access to open files.")
    else:
        print("❌ Not connected to a server.")