import threading
import time
from colorama import Fore, Style
from servers import disconnect, get_current_server
import player

class TraceSystem:
    def __init__(self):
        self.trace_timer = None
        self.trace_active = False
        self.trace_time = 0
        self.max_trace_time = 60  # seconds before getting traced

    def start_trace(self):
        """Start the trace countdown"""
        if self.trace_timer:
            return
        
        self.trace_active = True
        self.trace_time = 0
        self.trace_timer = threading.Thread(target=self._trace_countdown)
        self.trace_timer.daemon = True
        self.trace_timer.start()

    def stop_trace(self):
        """Stop the trace countdown"""
        self.trace_active = False
        self.trace_timer = None

    def _trace_countdown(self):
        """Count up until max_trace_time is reached"""
        while self.trace_active and self.trace_time < self.max_trace_time:
            time.sleep(1)
            self.trace_time += 1
            if self.trace_time % 10 == 0:
                remaining = self.max_trace_time - self.trace_time
                print(f"\n{Fore.YELLOW}⚠️ WARNING: {remaining} seconds until trace complete!{Style.RESET_ALL}")
            
        if self.trace_active:
            self._traced()

    def _traced(self):
        """Handle getting traced"""
        server = get_current_server()
        print(f"\n{Fore.RED}🚨 TRACED! Connection detected by {server['name']}!{Style.RESET_ALL}")
        
        # Penalties
        money_loss = int(player.get_balance() * 0.3)
        player.deduct_money(money_loss)
        print(f"{Fore.RED}💸 Lost ${money_loss} in trace evasion!{Style.RESET_ALL}")
        
        if player.has_tool("stealth_mode"):
            print(f"{Fore.RED}🛠️ Stealth mode tool was confiscated!{Style.RESET_ALL}")
            player.PLAYER.tools.remove("stealth_mode")  # Direct modification of tools
        
        disconnect()
        player.increase_wanted_level()

trace_system = TraceSystem()
