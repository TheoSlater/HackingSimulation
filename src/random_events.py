import random
from colorama import Fore, Style
import player
from servers import disconnect

class RandomEvent:
    EVENTS = {
        "investigation": {
            "chance": 15,
            "message": "🚔 Server is under federal investigation! Extra security measures detected.",
            "effect": lambda server: {"security": server.get("security", 1) + 2}
        },
        "honeypot": {
            "chance": 10,
            "message": "🍯 Warning: Honeypot detected! This might be a trap.",
            "effect": lambda server: {"detection_multiplier": 2}
        },
        "maintenance": {
            "chance": 20,
            "message": "🔧 System maintenance in progress. Security temporarily reduced.",
            "effect": lambda server: {"security": max(1, server.get("security", 1) - 1)}
        },
        "alert": {
            "chance": 25,
            "message": "⚠️ Security alert active! Random security scans in progress.",
            "effect": lambda server: {"random_disconnects": True}
        }
    }

    @staticmethod
    def check_for_event(server):
        """Check if a random event should occur"""
        for event_name, event in RandomEvent.EVENTS.items():
            if random.randint(1, 100) <= event["chance"]:
                return RandomEvent.trigger_event(server, event_name, event)
        return None

    @staticmethod
    def trigger_event(server, event_name, event):
        """Trigger a random event"""
        print(f"\n{Fore.YELLOW}{event['message']}{Style.RESET_ALL}")
        
        # Apply event effects
        effects = event["effect"](server)
        for key, value in effects.items():
            server[key] = value

        if event_name == "honeypot" and random.randint(1, 100) <= 30:
            print(f"{Fore.RED}🚨 Honeypot triggered! Money lost evading detection!{Style.RESET_ALL}")
            loss = int(player.get_balance() * 0.2)  # Lose 20% of money
            player.deduct_money(loss)
            disconnect()
            return False

        return True
