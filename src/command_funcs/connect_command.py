from servers import connect_to_server, disconnect

def execute_connect_command(server):
    if not server:
        print("Usage: connect <server_name/ip>")
        return
    connect_to_server(server)

def execute_disconnect_command():
    disconnect()