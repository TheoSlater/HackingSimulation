import time
import random
from servers import get_current_server, disconnect
import player

def brute_force_attack():
    """Simulates a brute-force attack with increased detection risks, affected by tools."""
    server = get_current_server()
    if not server:
        print("❌ You're not connected to any server!")
        return

    if server.get("root_access", False):  
        print(f"🔓 You already have root access to {server['name']}!")
        return

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

def exploit_server():
    """Exploit attempt with a lowered success chance unless 'auto_exploit' tool is owned."""
    server = get_current_server()
    if not server:
        print("❌ You're not connected to any server!")
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
