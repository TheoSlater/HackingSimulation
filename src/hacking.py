import time
import random
from colorama import Fore, Style
import player
from servers import get_current_server, disconnect
from tutorial import tutorial_active
import os
from random_events import RandomEvent

def check_firewall(server):
    """Check if server has an active firewall"""
    firewall = server.get("firewall", {})
    if firewall.get("enabled", False):
        print(f"{Fore.RED}❌ Access blocked by firewall. Use 'firewall-scan' and 'firewall-bypass' first.{Style.RESET_ALL}")
        return True
    return False

def check_root_access(server):
    """Check if we already have root access"""
    if server.get("root_access", False):
        print(f"{Fore.YELLOW}⚠️ You already have root access to {server['name']}!{Style.RESET_ALL}")
        return True
    return False

def brute_force_attack(server):
    """Execute brute force attack on server"""
    if check_root_access(server) or check_firewall(server):
        return

    # Check for random events before proceeding
    if RandomEvent.check_for_event(server) is False:
        return

    if server.get("auth_type") == "ssh_key":
        print(f"{Fore.RED}❌ Cannot brute force SSH key authentication!{Style.RESET_ALL}")
        return

    password = server["password"]
    detection_chance = 0
    attempts = 0
    security_level = server.get("security", 1)
    wordlist_path = os.path.join(os.path.dirname(__file__), "./data/wordlist.txt")

    print(f"\n[+] Initiating dictionary attack on {server['ip']}...")
    print("[+] Loading wordlist...")

    try:
        with open(wordlist_path, 'r') as f:
            wordlist = [line.strip() for line in f]
    except:
        print(f"{Fore.RED}❌ Failed to load wordlist!{Style.RESET_ALL}")
        return

    # Try common passwords first
    for attempt in wordlist:
        attempts += 1
        detection_chance += 0.3 * (security_level / 100)
        
        print(f"[*] Attempting: {attempt}", end="\r", flush=True)
        time.sleep(random.uniform(0.01, 0.1))

        if player.has_tool("stealth_mode"):
            detection_chance *= 0.5

        if random.randint(1, 100) < detection_chance:
            print("\n\n[!] ALERT! You have been detected and disconnected!")
            disconnect()
            return

        if attempt == password:
            print(f"\n\n[+] Password found: {password}")
            print(f"[+] Attempts: {attempts}")
            server["root_access"] = True
            player.gain_xp(20)
            return

    # If common passwords fail, try brute force with incremental characters
    print("\n[-] Dictionary attack failed, switching to brute force...")

    guessed_password = ""
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+="
    
    # Faster brute-force if tool is owned
    brute_force_speed = 0.07 if player.has_tool("faster_bruteforce") else 0.15  

    for char in password:
        found = False
        while not found:
            for attempt in random.sample(charset, len(charset)):
                attempts += 1
                # Increased detection risk
                detection_chance += 0.3 * (security_level / 100)
                
                print(f"[*] Trying: {guessed_password + attempt}", end="\r", flush=True)
                time.sleep(random.uniform(0.01, brute_force_speed))

                # Stealth mode reduces detection chance
                if player.has_tool("stealth_mode"):
                    detection_chance *= 0.5  

                if random.randint(1, 100) < detection_chance:
                    print("\n\n[!] ALERT! You have been detected and disconnected!")
                    disconnect()
                    return  

                if attempt == char:
                    guessed_password += char
                    found = True
                    break

    print(f"\n\n[+] Success! Root access gained to {server['ip']}")
    print(f"[+] Password: {password}")
    print(f"[+] Total Attempts: {attempts}\n")
    server["root_access"] = True  # Grant root access
    player.gain_xp(20)

def crack_ssh_key(server):
    """Attempt to crack SSH key encryption"""
    if not player.has_tool("ssh_cracker"):
        print(f"{Fore.RED}❌ You need the SSH Cracker tool for this!{Style.RESET_ALL}")
        return False

    stages = [
        ("Analyzing key type and encryption", 0.95),  # Increased from 0.9
        ("Extracting public parameters", 0.9),  # Increased from 0.8
        ("Calculating prime factors", 0.8),  # Increased from 0.7
        ("Running lattice reduction attack", 0.7),  # Increased from 0.6
        ("Reconstructing private key", 0.6)  # Increased from 0.5
    ]

    total_chance = 1.0
    for stage, chance in stages:
        print(f"\n{Fore.YELLOW}[*] {stage}...{Style.RESET_ALL}")
        time.sleep(random.uniform(2, 4))

        if random.random() > chance:
            print(f"{Fore.RED}[-] Failed: {stage}")
            print("[-] Key complexity too high for current methods{Style.RESET_ALL}")
            return False

        # Show technical details
        if random.random() < 0.3:
            details = [
                "Found weak prime factor",
                "Detected vulnerable key generation",
                "Successfully reduced lattice dimension",
                "Located matching key fragment",
                "Recovered partial key bytes"
            ]
            print(f"{Fore.CYAN}[+] {random.choice(details)}{Style.RESET_ALL}")
            
        total_chance *= chance

    # Final success chance based on security level
    if random.random() < total_chance:
        print(f"\n{Fore.GREEN}[+] Successfully recovered private key!")
        print(f"[+] Key fingerprint: {server['ssh_key']['fingerprint']}")
        print(f"[+] Private key:\n{server['ssh_key']['private_key']}{Style.RESET_ALL}")
        server["root_access"] = True
        player.gain_xp(100)
        return True

    return False

def exploit_service(server, port):
    """Attempt to exploit a specific service port"""
    if check_root_access(server) or check_firewall(server):
        return

    # Check for random events before proceeding
    if RandomEvent.check_for_event(server) is False:
        return

    # Always succeed if tutorial not completed
    if not player.player_data.get("tutorial_complete", False):
        print(f"{Fore.GREEN}[+] Successfully exploited server!{Style.RESET_ALL}")
        server["root_access"] = True
        player.gain_xp(50)
        return

    ports = server.get("ports", {})
    if port not in ports:
        print(f"{Fore.RED}❌ Port {port} is not open on this server.{Style.RESET_ALL}")
        return

    service = ports[port]
    vulnerabilities = service.get("vulnerabilities", [])
    
    if not vulnerabilities:
        print(f"{Fore.YELLOW}No known vulnerabilities for {service['name']} on port {port}{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}[*] Initiating exploit chain on {service['name']} ({service.get('version', 'unknown')}):{Style.RESET_ALL}")
    
    # Try multi-stage exploit chain
    stages = [
        ("Fingerprinting service", 0.95),        # Was 0.9
        ("Checking version compatibility", 0.95), # Was 0.95
        ("Building exploit payload", 0.9),        # Was 0.8 - Significantly increased
        ("Injecting shellcode", 0.85),           # Was 0.7 - Significantly increased
        ("Attempting privilege escalation", 0.8)  # Was 0.6 - Significantly increased
    ]

    current_success = 1.0
    for stage, chance in stages:
        print(f"\n[*] {stage}...")
        time.sleep(random.uniform(1, 2))
        
        # Each stage has a cumulative chance of failure
        stage_roll = random.random()
        if stage_roll > current_success * chance:
            print(f"{Fore.RED}[-] Failed at stage: {stage} (rolled {stage_roll:.2f} vs needed {current_success * chance:.2f}){Style.RESET_ALL}")
            return
            
        current_success *= chance
        print(f"{Fore.GREEN}[+] {stage} successful {current_success:.2f}{Style.RESET_ALL}")

    # If all stages succeed, grant access
    print(f"\n{Fore.GREEN}[+] Exploit chain successful! Root access granted.{Style.RESET_ALL}")
    server["root_access"] = True
    player.gain_xp(50)

def exploit_server():
    """Exploit attempt with a lowered success chance unless 'auto_exploit' tool is owned."""
    server = get_current_server()
    if not server:
        print("❌ You're not connected to any server!")
        return

    if check_firewall(server):
        return
    
    if server.get("root_access", False):  
        print(f"🔓 You already have root access to {server['name']}!")
        return

    print(f"\n[+] Scanning {server.get('ip', 'Unknown IP')} for exploits...")
    time.sleep(2)

    if player.has_tool("auto_exploit"):
        print(f"[+] Auto-exploit activated! Root access granted to {server.get('name', 'Unknown')} ({server.get('ip', 'Unknown IP')})")
        server["root_access"] = True  # Grant root access
        player.gain_xp(50)
        return

    # Lower exploit chance to make it slightly harder
    exploit_chance = max(15, 60 - server.get("security", 1) * 2)  # Increased base chance from 50 to 60, min from 5 to 15
    if random.randint(1, 100) <= exploit_chance:
        print(f"[+] Exploit found! Root access granted to {server.get('name', 'Unknown')} ({server.get('ip', 'Unknown IP')})")
        server["root_access"] = True  # Grant root access
        player.gain_xp(30)
    else:
        print("[-] No vulnerabilities found. Try brute-forcing instead.")
