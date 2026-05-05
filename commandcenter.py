import asyncio
import sys
import os
import socket
import time
from colorama import Fore, Style, init
from typing import Dict, Any, List
from datetime import datetime

# Dynamic loading of real logic modules
try:
    from advanced_scanner import AdvancedNetworkScanner
    from lateral_movement import AdvancedCommandCenter
    from exploit_engine import UniversalNetworkAccess
    from remote_control import AgentlessControl
    from passive_intel import AgentlessIntelligence
except ImportError:
    pass

# Initialize Colorama
init(autoreset=True)

class AMMOEngine:
    """Asynchronous Multi-threaded Modular Orchestrator (AMMO v2)"""
    def __init__(self):
        self.tasks = []
        self.concurrency_limit = 2000
        self.semaphore = asyncio.Semaphore(self.concurrency_limit)

    async def execute_task(self, coro):
        async with self.semaphore:
            return await coro

class HackerSounds:
    @staticmethod
    def alert(): print(f"{Fore.RED}[!] SOUND: ALERT")
    @staticmethod
    def network_pulse(): print(f"{Fore.CYAN}[*] SOUND: NETWORK PULSE")
    @staticmethod
    def exploit_success(): print(f"{Fore.GREEN}[+] SOUND: EXPLOIT SUCCESS")
    @staticmethod
    def connection_established(): print(f"{Fore.BLUE}[*] SOUND: CONNECTION ESTABLISHED")

class MatrixEffects:
    @staticmethod
    def digital_rain():
        print(f"{Fore.GREEN}[*] VISUAL: DIGITAL RAIN")

class OmniShell:
    def __init__(self):
        self.version = "7.1.002"
        self.ammo = AMMOEngine()
        self.targets = []
        
        # Initialize Functional Engines
        try:
            self.scanner = AdvancedNetworkScanner()
            self.lateral = AdvancedCommandCenter()
            self.exploiter = UniversalNetworkAccess()
            self.control = AgentlessControl()
            self.intel = AgentlessIntelligence()
            
            # Wire modules together for autonomous chains
            self.lateral.set_modules(discovery=self.scanner, intel=self.intel, control=self.control)
        except NameError:
            print(f"{Fore.RED}[!] Warning: Logic modules failed to load. Run install.py.")

    def display_banner(self):
        """Advanced High-Technology Banner with live stats."""
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        print(f"{Fore.LIGHTBLACK_EX}{Style.BRIGHT}╔{'═'*98}╗")
        print(f"{Fore.CYAN}{Style.BRIGHT}  ║  ██████╗ ███╗   ███╗███╗   ██╗██╗███████╗ ██████╗██╗███████╗███╗   ██╗ ██████╗███████╗  ║")
        print(f"{Fore.CYAN}{Style.BRIGHT}  ║  ██╔═══██╗████╗ ████║████╗  ██║██║██╔════╝██╔════╝██║██╔════╝████╗  ██║██╔════╝██╔════╝  ║")
        print(f"{Fore.CYAN}{Style.BRIGHT}  ║  ██║   ██║██╔████╔██║██╔██╗ ██║██║███████╗██║     ██║█████╗  ██╔██╗ ██║██║     █████╗    ║")
        print(f"{Fore.CYAN}{Style.BRIGHT}  ║  ██║   ██║██║╚██╔╝██║██║╚██╗██║██║╚════██║██║     ██║██╔══╝  ██║╚██╗██║██║     ██╔══╝    ║")
        print(f"{Fore.CYAN}{Style.BRIGHT}  ║  ╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║███████╗╚██████╗██║███████╗██║ ╚████║╚██████╗███████╗  ║")
        print(f"{Fore.CYAN}{Style.BRIGHT}  ║   ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝ ╚═════╝╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝  ║")
        print(f"{Fore.LIGHTBLACK_EX}╠{'═'*98}╣")
        print(f"{Fore.LIGHTBLACK_EX}║   {Fore.LIGHTGREEN_EX}▸ SYSTEM: {sys.platform.upper()} {Fore.LIGHTGREEN_EX}▸ HOST: {hostname} {Fore.LIGHTGREEN_EX}▸ IP: {local_ip}{' '*(68-len(hostname)-len(local_ip))}║")
        print(f"{Fore.LIGHTBLACK_EX}║   {Fore.MAGENTA}▸ VERSION: {self.version} {Fore.MAGENTA}▸ ENGINE: AMMO v2 {Fore.MAGENTA}▸ CONCURRENCY: {self.ammo.concurrency_limit}{' '*34}║")
        print(f"{Fore.LIGHTBLACK_EX}╚{'═'*98}╝")
        print(f"{Fore.YELLOW}[i] Terminal Ready. Type 'help' for available commands.\n")

    async def handle_command(self, cmd_input: str):
        parts = cmd_input.split()
        if not parts: return
        
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ["exit", "quit"]:
            print(f"{Fore.YELLOW}Shutting down AMMO engine...")
            sys.exit(0)
        
        elif cmd == "globalscan":
            if hasattr(self, 'exploiter'):
                print(f"{Fore.GREEN}[*] Initiating ULTRAMAX Global Network Discovery...")
                # UniversalNetworkAccess provides the most comprehensive discovery
                loop = asyncio.get_event_loop()
                self.targets = await loop.run_in_executor(None, self.exploiter.ultramax_global_scan)
                print(f"{Fore.GREEN}[+] Scan Complete. {len(self.targets)} active targets identified.")
            else:
                print(f"{Fore.RED}[!] Module Error: Exploit engine not initialized.")

        elif cmd == "pwn":
            if not args:
                print(f"{Fore.RED}[!] Usage: pwn <target_ip>")
                return
            if hasattr(self, 'exploiter'):
                print(f"{Fore.RED}[!] Launching Autonomous Exploitation Chain on {args[0]}...")
                loop = asyncio.get_event_loop()
                res = await loop.run_in_executor(None, self.exploiter.pwn_target, args[0])
                if res.get("success"):
                    print(f"{Fore.GREEN}[+] Target Compromised via {res.get('method')}!")
                else:
                    print(f"{Fore.YELLOW}[-] Exploitation failed or target patched.")
            else:
                print(f"{Fore.RED}[!] Module Error: Exploit engine not initialized.")

        elif cmd == "harvest":
            if not args:
                print(f"{Fore.RED}[!] Usage: harvest <ip> <user> <pass>")
                return
            if hasattr(self, 'control'):
                user = args[1] if len(args) > 1 else "Administrator"
                pwd = args[2] if len(args) > 2 else ""
                print(f"{Fore.MAGENTA}[*] Harvesting credentials and vault tokens from {args[0]}...")
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, self.control.extract_all_data, args[0], user, pwd)
                print(f"{Fore.GREEN}[+] Harvest complete. Stored in local DB.")
            else:
                print(f"{Fore.RED}[!] Module Error: Control engine not initialized.")

        elif cmd == "targets":
            self.list_targets()

        elif cmd == "help":
            self.show_help()
            
        else:
            print(f"{Fore.RED}[?] Unknown command: {cmd}")

    async def run_module(self, mod_id: str, function: str, args: list):
        """Legacy module runner simulation."""
        try:
            # Dynamic loading simulation as per replit.md
            print(f"{Fore.BLUE}[M] Loading {module_name}...")
            await asyncio.sleep(0.5) # Simulate async load
            print(f"{Fore.GREEN}[+] Executing {function} with args {args}")
        except Exception as e:
            print(f"{Fore.RED}[!] Module Error: {str(e)}")

    def list_targets(self):
        if not self.targets:
            print(f"{Fore.YELLOW}[!] No targets discovered yet. Run 'globalscan'.")
        else:
            print(f"\n{Fore.CYAN}DISCOVERED TARGETS:")
            print(f"{Fore.CYAN}{'='*60}")
            for idx, t in enumerate(self.targets):
                ip = getattr(t, 'ip', str(t))
                os_type = getattr(t, 'os', 'Unknown OS')
                status = "COMPROMISED" if getattr(t, 'is_compromised', False) else "ACTIVE"
                print(f"  [{idx}] {ip:<15} | {os_type:<15} | {status}")

    def show_help(self):
        print(f"\n{Fore.WHITE}Available Commands:")
        print("  globalscan         - Scan all reachable networks")
        print("  pwn <ip>           - Autonomous exploitation")
        print("  harvest <ip>       - Extract browser/system credentials")
        print("  targets            - List discovered hosts")
        print("  exit               - Close shell\n")

async def main_loop():
    shell = OmniShell()
    shell.display_banner()
    while True:
        try:
            cmd = input(f"{Fore.CYAN}omniscence> {Style.RESET_ALL}")
            await shell.handle_command(cmd)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

if __name__ == "__main__":
    asyncio.run(main_loop())