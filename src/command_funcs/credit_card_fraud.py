import random
import time
import player
from servers import get_current_server, disconnect

def steal_card_details():
    """Attempts to steal credit card details from a hacked server."""
    server = get_current_server()
    if not server:
        print("❌ You're not connected to any server!")
        return
    
    if not server.get("root_access", False):
        print("❌ You need root access to steal credit card details!")
        return

    print("\n💳 Initiating credit card data theft...\n")
    time.sleep(2)
    
    success_rate = 60  # Harder base success rate
    detection_chance = 25  # Higher base detection risk

    if player.has_tool("cc_scraper"):
        success_rate += 10
    
    if player.has_tool("stealth_mode"):
        detection_chance -= 10

    if random.randint(1, 100) <= success_rate:
        stolen_cards = random.randint(1, 3)  # Reduced stolen cards
        money_earned = sum(random.randint(10, 100) for _ in range(stolen_cards))  # Lower payout

        player.add_money(money_earned)
        print(f"✅ Successfully stole {stolen_cards} credit card(s)!")
        print(f"💰 Sold for ${money_earned}!")

        if random.randint(1, 100) <= detection_chance:
            print("\n🚨 ALERT! Fraud detected! Your wanted level has increased!\n")
            increase_wanted_level()
            disconnect()  # Auto disconnects you if caught
            print("🔌 You were forcibly disconnected from the server!")
    else:
        print("❌ Failed to steal any card details. Try again later!")

def increase_wanted_level():
    player_data = player.load_player()
    player_data["wanted_level"] = player_data.get("wanted_level", 0) + 1
    player.save_player(player_data)

    if player_data["wanted_level"] >= 5:
        print("🚔 The authorities are closing in! Be careful!")

def get_wanted_level():
    return player.load_player().get("wanted_level", 0)
