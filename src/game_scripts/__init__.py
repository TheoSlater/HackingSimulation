# This file is used to define the CustomScript class that all custom scripts should inherit from
# This class provides a set of core commands and utility functions that custom scripts can use
# It also provides a way to print colored messages and wait for a set amount of time
# The example.py file is a sample custom script that demonstrates how to use the CustomScript class
# The script_commands.py file provides functions to create and run custom scripts from the terminal
# DO NOT DELETE OR MODIFY THIS FILE

from colorama import Fore, Style
from servers import get_current_server
import time
from command_funcs import (
    execute_scan_command, 
    execute_connect_command, 
    execute_disconnect_command,
    execute_hack_command
)
from hacking import check_root_access, brute_force_attack, exploit_service, exploit_server, crack_ssh_key
from data.server_data import SERVERS  # Add this import

class CustomScript:
    def __init__(self):
        self.name = "Custom Script"
        self.description = "A custom script"
    
    def run(self, server):
        """Override this method to implement script behavior"""
        pass

    # Core command access
    def scan(self, level):
        """Run scan-analyse command"""
        execute_scan_command(str(level))
        
    def connect(self, target):
        """Connect to a server"""
        execute_connect_command(target)
        
    def disconnect(self):
        """Disconnect from server"""
        execute_disconnect_command()
        
    def hack(self):
        """Attempt to steal money"""
        execute_hack_command()
        
    def brute_force(self):
        """Run brute force attack"""
        server = get_current_server()
        if server:
            brute_force_attack(server)
            
    def exploit(self, port=None):
        """Run exploit attack"""
        server = get_current_server()
        if server:
            if port:
                exploit_service(server, str(port))
            else:
                exploit_server()
                
    def crack_ssh(self):
        """Attempt SSH key crack"""
        server = get_current_server()
        if server:
            crack_ssh_key(server)
            
    def check_root_access(self):
        """Check if we have root access"""
        server = get_current_server()
        if not server:
            print(f"{Fore.RED}Not connected to any server!{Style.RESET_ALL}")
            return False
        if not server.get("root_access", False):
            print(f"{Fore.RED}Root access required!{Style.RESET_ALL}")
            return False
        return True
        
    def print_message(self, message, color=None):
        """Print colored message"""
        if color:
            print(f"{color}{message}{Style.RESET_ALL}")
        else:
            print(message)

    def wait(self, seconds):
        """Safe wrapper for time.sleep"""
        time.sleep(min(seconds, 5))  # Cap at 5 seconds for safety

    def get_server_by_name(self, name):
        """Helper to find server by name"""
        for ip, server in SERVERS.items():
            if server["name"].lower() == name.lower():
                return server
        return None
