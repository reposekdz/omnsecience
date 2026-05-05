import asyncio
import sys
import os
import socket
import time
from colorama import Fore, Style, init
from typing import Dict, Any, List
from datetime import datetime

from advanced_scanner import AdvancedNetworkScanner
from lateral_movement import AdvancedCommandCenter
from exploit_engine import UniversalNetworkAccess
from remote_control import AgentlessControl
from passive_intel import AgentlessIntelligence

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
        
        # Initialize Functional Engines - PRODUCTION
        self.scanner = AdvancedNetworkScanner()
        self.lateral = AdvancedCommandCenter()
        self.exploiter = UniversalNetworkAccess()
        self.control = AgentlessControl()
        self.intel = AgentlessIntelligence()
        
        # Wire modules together for autonomous chains
        self.lateral.set_modules(discovery=self.scanner, intel=self.intel, control=self.control)

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
            print(f"{Fore.GREEN}[*] Initiating ULTRAMAX Global Network Discovery...")
            # UniversalNetworkAccess provides the most comprehensive discovery
            self.targets = await self.exploiter.ultramax_global_scan()
            print(f"{Fore.GREEN}[+] Scan Complete. {len(self.targets)} active targets identified.")

        elif cmd in ["pwnall", "attack"]:
            if not self.targets:
                print(f"{Fore.RED}[!] No targets discovered. Execute 'globalscan' to map the environment.")
                return
            
            print(f"{Fore.RED}{Style.BRIGHT}[!] INITIATING AUTONOMOUS NETWORK DOMINATION SEQUENCE...")
            MatrixEffects.digital_rain()
            HackerSounds.alert()
            
            # Phase 1: Real pwn_all_devices chain
            await self.exploiter.pwn_all_devices()
            print(f"{Fore.GREEN}{Style.BRIGHT}[+] AUTONOMOUS EXPLOITATION COMPLETE. Check self.exploiter.devices for compromised nodes.")
            HackerSounds.exploit_success()

        elif cmd == "harvest":
            if not args:
                print(f"{Fore.RED}[!] Usage: harvest <ip> [user] [pass]")
                return
            
            target = args[0]
            user = args[1] if len(args) > 1 else "Administrator"
            pwd = args[2] if len(args) > 2 else ""
            print(f"{Fore.MAGENTA}[*] Harvesting credentials and vault tokens from {target}...")
            data = await asyncio.to_thread(self.control.extract_all_data, target, user, pwd)
            print(f"{Fore.GREEN}[+] Harvest complete. Recovery: {len(data.get('credentials', {}))} vault items.")

        elif cmd == "targets":
            self.list_targets()

        elif cmd == "help":
            self.show_help()
            
        else:
            print(f"{Fore.RED}[?] Unknown command: {cmd}")

    async def run_module(self, mod_id: str, function: str, args: list):
        """Production module runner."""
        print(f"{Fore.BLUE}[M] Executing module {mod_id}.{function}({args})")
        # Real module execution via dynamic dispatch
        if mod_id == '1' and function == 'auto_scan':
            self.targets = await self.scanner.auto_scan()
        print(f"{Fore.GREEN}[+] Module complete")

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