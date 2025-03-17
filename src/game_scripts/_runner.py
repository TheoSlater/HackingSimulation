# DO NOT TOUCH THIS FILE
# RUNS SCRIPTS FROM game_scripts DIRECTORY IN A SEPERATE WINDOW
import sys
import os
# Add src directory to Python path
sys.path.insert(0, '/Users/theoslater/Documents/Code/HackingSimulation/src')

import time
from colorama import init, Fore, Style
init()  # Initialize colorama for the new window

print(f"{Fore.CYAN}Running example.py...{Style.RESET_ALL}\n")

try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("script", "/Users/theoslater/Documents/Code/HackingSimulation/src/game_scripts/example.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    for item in dir(module):
        if item != 'CustomScript' and isinstance(getattr(module, item), type):
            if issubclass(getattr(module, item), module.CustomScript):
                script_class = getattr(module, item)
                script = script_class()
                script.run(None)  # Pass None as server for now
                break
except Exception as e:
    print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

print("\nPress Enter to close this window...")
input()
