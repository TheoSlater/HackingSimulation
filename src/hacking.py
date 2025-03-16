import time
import random
from colorama import Fore, Style
import player
from servers import get_current_server, disconnect
from trace_system import trace_system as ts  # Fix import

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

    if server.get("auth_type") == "ssh_key":
        print(f"{Fore.RED}❌ Cannot brute force SSH key authentication!{Style.RESET_ALL}")
        return

    # Start trace timer
    ts.start_trace()

    password = server["password"]
    detection_chance = 0
    guessed_password = ""
    attempts = 0
    security_level = server.get("security", 1)

    print(f"\n[+] Initiating brute-force attack on {server['ip']}...\n")

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

    # Stop trace timer on success
    ts.stop_trace()

def crack_ssh_key(server):
    """Attempt to crack SSH key encryption"""
    if not player.has_tool("ssh_cracker"):
        print(f"{Fore.RED}❌ You need the SSH Cracker tool for this!{Style.RESET_ALL}")
        return False

    # Calculate success chance based on server security
    security_level = server.get("security", 1)
    base_success_rate = 70  # Increased from 40%
    success_rate = max(30, base_success_rate - (security_level * 5))  # Security reduces success rate

    print(f"\n{Fore.CYAN}[*] Attempting to crack SSH key...{Style.RESET_ALL}")
    ts.start_trace()

    steps = [
        ("Analyzing encryption type", 1, 2),
        ("Generating prime factors", 2, 4),
        ("Running dictionary attack", 1, 2),
        ("Attempting private key recovery", 2, 3),
        ("Testing recovered key", 1, 2)
    ]

    for step, min_time, max_time in steps:
        print(f"{Fore.YELLOW}[*] {step}...{Style.RESET_ALL}")
        time.sleep(random.uniform(min_time, max_time))
        if random.random() < 0.2:  # 20% chance of showing additional info
            print(f"{Fore.CYAN}[+] Found potential {random.choice(['RSA modulus', 'prime factor', 'key fragment', 'encryption pattern'])}{Style.RESET_ALL}")
    
    success = random.randint(1, 100) <= success_rate  # Use new success rate
    ts.stop_trace()
    
    if success:
        key_data = server["ssh_key"]
        print(f"\n{Fore.GREEN}[+] Key cracking successful!")
        print(f"[+] Key fingerprint: {key_data['fingerprint']}")
        print(f"[+] Recovered private key:\n{key_data['private_key']}{Style.RESET_ALL}")
        server["root_access"] = True
        player.gain_xp(100)
    else:
        print(f"\n{Fore.RED}[-] Failed to crack SSH key")
        print(f"[-] Encryption too strong or key corrupted{Style.RESET_ALL}")
    
    return success

def exploit_service(server, port):
    """Attempt to exploit a specific service port"""
    if check_root_access(server) or check_firewall(server):
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

    print(f"\n{Fore.CYAN}[*] Attempting to exploit {service['name']} ({service.get('version', 'unknown')}) on port {port}...{Style.RESET_ALL}")
    time.sleep(2)

    for vuln in vulnerabilities:
        print(f"{Fore.YELLOW}[*] Trying exploit for {vuln['cve']}{Style.RESET_ALL}")
        time.sleep(1)

        if random.randint(1, 100) <= 70:  # 70% success rate for known vulnerabilities
            print(f"{Fore.GREEN}[+] Successfully exploited {vuln['cve']}!{Style.RESET_ALL}")
            server["root_access"] = True
            player.gain_xp(50)
            return
        
    print(f"{Fore.RED}[-] Failed to exploit vulnerabilities on port {port}{Style.RESET_ALL}")

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
    exploit_chance = max(5, 50 - server.get("security", 1) * 2) 
    if random.randint(1, 100) <= exploit_chance:
        print(f"[+] Exploit found! Root access granted to {server.get('name', 'Unknown')} ({server.get('ip', 'Unknown IP')})")
        server["root_access"] = True  # Grant root access
        player.gain_xp(30)
    else:
        print("[-] No vulnerabilities found. Try brute-forcing instead.")
