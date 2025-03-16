from servers import get_current_server
from colorama import Fore, Style
from data_exfiltration import list_sensitive_data, steal_data

def execute_exfiltrate_command(args=None):
    """List or steal sensitive data from server"""
    server = get_current_server()
    if not server:
        print(f"{Fore.RED}❌ Not connected to any server!{Style.RESET_ALL}")
        return

    if not server.get("root_access", False):
        print(f"{Fore.RED}❌ Root access required to access sensitive data!{Style.RESET_ALL}")
        return

    if not args:
        print(f"{Fore.YELLOW}Usage: exfiltrate list | exfiltrate <filename>{Style.RESET_ALL}")
        return

    if args.lower() == "list":
        sensitive_data = server.get("sensitive_data", {})
        if not sensitive_data:
            print(f"{Fore.YELLOW}No sensitive data found on this server.{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}📁 Available Sensitive Data:{Style.RESET_ALL}")
        for fname, data in sensitive_data.items():
            print(f"- {fname}")
            print(f"  Description: {data['description']}")
            print(f"  Estimated Value: ${data['value']}")
    else:
        steal_data(server, args)
