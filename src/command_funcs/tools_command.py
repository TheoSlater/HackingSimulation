from hacking_tools import list_tools, purchase_tool
from player import get_balance

def execute_tools_command():
    """Display available hacking tools"""
    print("\n🛠️  Available Hacking Tools:")
    list_tools()
    print(f"\n💰 Your balance: ${get_balance()}")

def execute_buy_command(tool_name):
    """Purchase a hacking tool"""
    if not tool_name:
        print("Usage: buy <tool_name>")
        return
        
    success = purchase_tool(tool_name)
    if success:
        print(f"✅ Successfully purchased {tool_name}")
        print(f"💰 Remaining balance: ${get_balance()}")
    else:
        print("❌ Failed to purchase tool. Insufficient funds or invalid tool name.")