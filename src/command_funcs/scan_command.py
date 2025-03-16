from servers import list_servers

def execute_scan_command(level):
    if not level.isdigit() or int(level) not in [1, 2]:
        print("Usage: scan-analyse <level> (1 or 2)")
        return
    list_servers(int(level))