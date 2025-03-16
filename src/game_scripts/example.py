from game_scripts import CustomScript, Fore

class ExampleVirus(CustomScript):
    def __init__(self):
        super().__init__()
        self.name = "Simple Server Hack"
        self.description = "Basic server hack example"
    
    def run(self, server):
        self.print_message("[*] Starting server hack...", Fore.CYAN)
        self.connect("BetaCorp")
        
        for i in range(5):
            self.print_message(f"[*] Hack iteration {i+1}", Fore.CYAN)
            
            self.exploit()
            self.wait(1)
            
            if not self.check_root_access():
                self.brute_force()
                self.wait(1)
                if not self.check_root_access():
                    self.crack_ssh()
                    self.wait(1)
            
            if self.check_root_access():
                self.hack()
            else:
                self.print_message("[-] Failed to gain access!", Fore.RED)
            
            self.wait(1)
            
        return True