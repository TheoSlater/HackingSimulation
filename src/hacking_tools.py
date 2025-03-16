import player

TOOLS = {
    "faster_bruteforce": {"cost": 500, "effect": "Brute-force is 50% faster"},
    "stealth_mode": {"cost": 1000, "effect": "Reduces detection chance"},
    "auto_exploit": {"cost": 1500, "effect": "Instantly exploits vulnerable servers"},
    "cc_scraper": {"cost": 2000, "effect": "Steal credit card details"},
    "firewall_buster": {"cost": 2500, "effect": "Helps bypass server firewalls"},
    "ssh_cracker": {"cost": 3000, "effect": "Required to crack SSH key authentication"}
}

def list_tools():
    print("\n🛠 Available Hacking Tools:")
    for tool, details in TOOLS.items():
        print(f"- {tool}: ${details['cost']} ({details['effect']})")

def purchase_tool(tool_name):
    if tool_name not in TOOLS:
        print("❌ Invalid tool.")
        return

    player.buy_tool(tool_name, TOOLS[tool_name]["cost"])
