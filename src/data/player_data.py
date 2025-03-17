import json
import os
from typing import List, Dict

SAVE_PATH = os.path.join(os.path.dirname(__file__), "save_data.json")

class PlayerData:
    def __init__(self):
        self.money: int = 500
        self.tools: List[str] = []
        self.xp: int = 0
        self.wanted_level: int = 0
        self.tutorial_complete: bool = False
        self.load_save()  # Load saved data on startup

    def save_game(self) -> None:
        """Save current player state"""
        data = {
            "money": self.money,
            "tools": self.tools,
            "xp": self.xp,
            "wanted_level": self.wanted_level,
            "tutorial_complete": self.tutorial_complete
        }
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
        with open(SAVE_PATH, 'w') as f:
            json.dump(data, f, indent=2)

    def load_save(self) -> None:
        """Load saved player state"""
        if os.path.exists(SAVE_PATH):
            try:
                with open(SAVE_PATH, 'r') as f:
                    data = json.load(f)
                    self.money = data.get("money", 500)
                    self.tools = data.get("tools", [])
                    self.xp = data.get("xp", 0)
                    self.wanted_level = data.get("wanted_level", 0)
                    self.tutorial_complete = data.get("tutorial_complete", False)
            except:
                print("Failed to load save data, using defaults")

# Create global player instance
PLAYER = PlayerData()
