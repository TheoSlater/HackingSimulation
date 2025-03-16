import json
import os

# Define player data file path
data_path = os.path.join(os.path.dirname(__file__), "./data/player.json")

# Default player data
DEFAULT_PLAYER = {
    "money": 500,
    "tools": [],
    "xp": 0,
    "wanted_level": 0
}

def save_player(data):
    """ Save player data to file, creating the file and directory if needed """
    os.makedirs(os.path.dirname(data_path), exist_ok=True)  # Ensure directory exists
    with open(data_path, "w") as f:
        json.dump(data, f, indent=4)

def load_player():
    """ Load player data from file or create a new one if missing """
    if not os.path.exists(data_path):
        save_player(DEFAULT_PLAYER)  # Save default data before returning it
        return DEFAULT_PLAYER
    
    with open(data_path, "r") as f:
        return json.load(f)


# Load player data at startup
player_data = load_player()

def get_balance():
    """ Get current balance """
    return player_data["money"]

def add_money(amount):
    """ Add money to player balance """
    player_data["money"] += amount
    save_player(player_data)

def deduct_money(amount):
    """ Deduct money if sufficient balance is available """
    if player_data["money"] >= amount:
        player_data["money"] -= amount
        save_player(player_data)
        return True
    return False  # Not enough money

def has_tool(tool_name):
    """ Check if player owns a tool """
    return tool_name in player_data["tools"]

def buy_tool(tool_name, cost):
    """ Purchase a tool if player has enough money """
    if has_tool(tool_name):
        print(f"You already own {tool_name}!")
        return
    
    if deduct_money(cost):
        player_data["tools"].append(tool_name)
        save_player(player_data)
        print(f"✅ Purchased {tool_name}!")
    else:
        print("❌ Not enough money!")

def gain_xp(amount):
    """ Increase XP and save progress """
    player_data["xp"] += amount
    save_player(player_data)
    print(f"✨ Gained {amount} XP!")

def increase_wanted_level():
    """Increases wanted level when detected."""
    player_data = load_player()  # Reload fresh data
    player_data["wanted_level"] += 1
    save_player(player_data)
    print(f"🚨 Wanted Level: {player_data['wanted_level']}")

