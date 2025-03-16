import os
import importlib.util
import shutil
from colorama import Fore, Style
import subprocess
import sys
import platform
from servers import get_current_server

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "game_scripts")

def execute_touch_command(filename):
    """Create a new script file from template"""
    if not filename.endswith('.py'):
        filename += '.py'
        
    filepath = os.path.join(SCRIPTS_DIR, filename)
    template_path = os.path.join(SCRIPTS_DIR, "example.py")
    
    if os.path.exists(filepath):
        print(f"{Fore.RED}Script {filename} already exists!{Style.RESET_ALL}")
        return
        
    try:
        shutil.copy2(template_path, filepath)
        print(f"{Fore.GREEN}Created new script: {filename}")
        print(f"Edit the file at: {filepath}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error creating script: {str(e)}{Style.RESET_ALL}")

def execute_run_script_command(filename):
    """Run a custom script in a new terminal window"""
    if not filename.endswith('.py'):
        filename += '.py'
        
    filepath = os.path.join(SCRIPTS_DIR, filename)
    src_dir = os.path.dirname(os.path.dirname(__file__))  # Get src directory
    
    if not os.path.exists(filepath):
        print(f"{Fore.RED}Script not found: {filename}{Style.RESET_ALL}")
        return

    # Create a runner script that will execute in the new window
    runner_path = os.path.join(SCRIPTS_DIR, "_runner.py")
    with open(runner_path, 'w') as f:
        f.write(f"""
import sys
import os
# Add src directory to Python path
sys.path.insert(0, '{src_dir}')

import time
from colorama import init, Fore, Style
init()  # Initialize colorama for the new window

print(f"{{Fore.CYAN}}Running {filename}...{{Style.RESET_ALL}}\\n")

try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("script", "{filepath}")
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
    print(f"{{Fore.RED}}Error: {{str(e)}}{{Style.RESET_ALL}}")

print("\\nPress Enter to close this window...")
input()
""")

    # Launch new terminal based on OS
    if platform.system() == "Windows":
        subprocess.Popen(["start", "cmd", "/k", "python", runner_path], shell=True)
    elif platform.system() == "Darwin":  # macOS
        applescript = f'''
        tell application "Terminal"
            do script "python3 '{runner_path}'"
        end tell
        '''
        subprocess.run(["osascript", "-e", applescript])
    else:  # Linux
        subprocess.Popen(["x-terminal-emulator", "-e", f"python3 {runner_path}"])

    print(f"{Fore.GREEN}Script launched in new window!{Style.RESET_ALL}")
