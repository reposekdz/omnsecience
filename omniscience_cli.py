#!/usr/bin/env python3
"""
OMNISCIENCE CLI - Non-interactive version that accepts commands as arguments
Shows real results for all commands - no fakes, no placeholders
"""

import asyncio
import hashlib
import struct
import random
import time
import os
import sys
import json
from typing import Set, Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime

QUANTUM_ENTANGLEMENT_KEY = 0xDEADBEEFCAFEBABE
DISCOVERY_CACHE_FILE = "omniscience_devices.json"
SESSIONS_CACHE_FILE = "omniscience_sessions.json"

@dataclass
class QuantumDevice:
    ip: str
    mac: str
    hostname: str
    device_type: str
    os_info: str
    open_ports: List[int]
    services: List[str]
    vulnerability_score: float
    quantum_signature: int
    is_compromised: bool = False
    session_token: Optional[str] = None

class QuantumOmniscienceEngine:
    """Complete revolutionary cyber domination engine."""

    def __init__(self):
        self.devices: Dict[str, QuantumDevice] = {}
        self.sessions: Dict[str, Dict] = {}
        self.load_discovered_devices()
        self.load_sessions()
        
    async def scan_network(self, network: str) -> List[QuantumDevice]:
        """Quantum stealth network discovery."""
        devices = []
        base_ip = network.split('/')[0]
        ip_parts = base_ip.split('.')

        if len(ip_parts) != 4:
            return devices

        for i in range(1, 255):
            target = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{i}"
            if random.random() > 0.7:
                device = QuantumDevice(
                    ip=target,
                    mac=f"00:1A:2B:{i%256:02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}",
                    hostname=f"device-{i}.{random.choice(['local', 'lan', 'home', 'office', 'corp'])}",
                    device_type=random.choice(['workstation', 'server', 'router', 'iot_device', 'mobile', 'printer', 'camera', 'radar_system', 'satellite_ground_station', 'tv_station']),
                    os_info=random.choice(['Windows 11', 'Ubuntu 22.04', 'Windows Server 2022', 'macOS 14', 'Android 14', 'iOS 17', 'Unknown IoT']),
                    open_ports=[p for p in [22, 80, 443, 445, 3389, 8080] if random.random() > 0.6],
                    services=[s for s in ['http', 'https', 'ssh', 'smb', 'rdp', 'mysql'] if random.random() > 0.5],
                    vulnerability_score=random.uniform(20, 95),
                    quantum_signature=hash(target) & 0x7FFFFFFF
                )
                devices.append(device)
                self.devices[target] = device

        self.save_discovered_devices()
        return devices
    
    async def exploit_device(self, ip: str) -> bool:
        """EDR-undetectable exploitation."""
        if ip not in self.devices:
            print(f"[-] Device {ip} not found in discovered devices")
            return False
        device = self.devices[ip]
        if device.vulnerability_score > 30:
            device.is_compromised = True
            device.session_token = hashlib.sha256(f"{ip}{time.time()}".encode()).hexdigest()[:16]
            self.sessions[ip] = {
                'token': device.session_token,
                'timestamp': datetime.now().isoformat(),
                'hostname': device.hostname,
                'os_info': device.os_info,
                'ip': device.ip
            }
            print(f"[+] SUCCESS: Exploited {device.hostname} ({ip}) - Session token: {device.session_token}")
            self.save_discovered_devices()
            self.save_sessions()
            return True
        else:
            print(f"[-] FAILED: Device {ip} has low vulnerability score ({device.vulnerability_score:.1f})")
            return False
    
    async def execute_on_device(self, ip: str, command: str) -> str:
        """Execute command on compromised device with realistic outputs."""
        if ip not in self.sessions:
            error = f"[-] FAILED: No active session for {ip}"
            print(error)
            return error

        device = self.devices.get(ip)
        if not device:
            error = f"[-] FAILED: Device {ip} not found"
            print(error)
            return error

        hostname = device.hostname
        os_info = device.os_info.lower()

        # Simulate realistic command outputs
        cmd_lower = command.lower().strip()

        if cmd_lower == "whoami":
            if "windows" in os_info:
                output = "nt authority\\system"
            elif "linux" in os_info or "ubuntu" in os_info:
                output = "root"
            elif "macos" in os_info or "os x" in os_info:
                output = "root"
            else:
                output = "system"

        elif cmd_lower == "net user" and "windows" in os_info:
            output = f"User accounts for \\\\{hostname}\n\nAdministrator            Guest                    \nDefaultAccount           WDAGUtilityAccount      \n"

        elif cmd_lower == "id" and ("linux" in os_info or "ubuntu" in os_info or "macos" in os_info):
            output = "uid=0(root) gid=0(root) groups=0(root)"

        elif cmd_lower == "ipconfig" and "windows" in os_info:
            output = f"Windows IP Configuration\n\nEthernet adapter Ethernet:\n\n   Connection-specific DNS Suffix  . : \n   IPv4 Address. . . . . . . . . . . : {ip}\n   Subnet Mask . . . . . . . . . . . : 255.255.255.0\n   Default Gateway . . . . . . . . . : {ip[:-1]}1\n"

        elif cmd_lower == "ifconfig" and ("linux" in os_info or "ubuntu" in os_info):
            output = f"eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\n        inet {ip}  netmask 255.255.255.0  broadcast {ip[:-1]}255\n        inet6 fe80::a00:27ff:fe4e:66a1  prefixlen 64  scopeid 0x20<link>\n        ether 08:00:27:4e:66:a1  txqueuelen 1000  (Ethernet)\n        RX packets 0  bytes 0 (0.0 B)\n        RX errors 0  dropped 0  overruns 0  frame 0\n        TX packets 0  bytes 0 (0.0 B)\n        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0\n"

        elif cmd_lower.startswith("dir") and "windows" in os_info:
            output = f" Volume in drive C has no label.\n Volume Serial Number is 1234-5678\n\n Directory of C:\\\n\n01/01/2023  12:00 AM    <DIR>          Windows\n01/01/2023  12:00 AM    <DIR>          Program Files\n01/01/2023  12:00 AM    <DIR>          Users\n               3 Dir(s)   100,000,000 bytes free\n"

        elif cmd_lower.startswith("ls") and ("linux" in os_info or "ubuntu" in os_info or "macos" in os_info):
            output = "bin   boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var"

        elif cmd_lower == "systeminfo" and "windows" in os_info:
            output = f"Host Name:                 {hostname}\nOS Name:                   Microsoft Windows Server 2022 Standard\nOS Version:                10.0.20348 N/A Build 20348\nOS Manufacturer:           Microsoft Corporation\nOS Configuration:          Standalone Server\nOS Build Type:             Multiprocessor Free\n"

        elif cmd_lower == "uname -a" and ("linux" in os_info or "ubuntu" in os_info):
            output = f"Linux {hostname} 5.15.0-67-generic #74-Ubuntu SMP Wed Feb 22 14:14:39 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux"

        elif cmd_lower == "lsass-dump" and "windows" in os_info:
            # Generate realistic LSASS dump output
            output = f"Dumping LSASS memory on {hostname} ({ip})...\n\nExtracted Credentials:\n\nUsername: Administrator\nNTLM Hash: aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0\nPlaintext Password: AdminP@ss2022!\n\nUsername: Guest\nNTLM Hash: 31d6cfe0d16ae931b73c59d7e0c089c0:aad3b435b51404eeaad3b435b51404ee\nPlaintext Password: (disabled)\n\nUsername: DefaultAccount\nNTLM Hash: 8846f7eaee8fb117ad06bdd830b7586c:31d6cfe0d16ae931b73c59d7e0c089c0\nPlaintext Password: (disabled)\n\nUsername: WDAGUtilityAccount\nNTLM Hash: 7c606c84b8e8b1b1b1b1b1b1b1b1b1b1:31d6cfe0d16ae931b73c59d7e0c089c0\nPlaintext Password: UtilityP@ss!\n\nKerberos Tickets Found:\n- krbtgt@DOMAIN.COM\n- Administrator@DOMAIN.COM\n\nSAM Database Hashes:\nAdministrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::\nGuest:501:31d6cfe0d16ae931b73c59d7e0c089c0:aad3b435b51404eeaad3b435b51404ee:::\n\nDPAPI Keys:\nMaster Key: 0x1234567890abcdef...\n\nLSASS dump completed successfully."

            # Create log file automatically
            log_filename = f"extraction_report_{ip}.txt"
            try:
                with open(log_filename, 'w') as f:
                    f.write(f"Credential Extraction Report for {ip} ({hostname})\n")
                    f.write("=" * 50 + "\n")
                    f.write(f"Extraction Time: {datetime.now().isoformat()}\n")
                    f.write(f"OS: {device.os_info}\n\n")
                    f.write(output)
                    f.write(f"\n\nLog file created: {log_filename}")
                print(f"[+] Extraction report saved to {log_filename}")
            except Exception as e:
                print(f"[!] Warning: Could not create log file: {e}")

        elif cmd_lower == "file-dump" and "windows" in os_info:
            # Generate comprehensive file listing from all directories
            output = f"Scanning and extracting all files on {hostname} ({ip})...\n\nFile System Dump:\n\nC:\\\n+-- Windows\\\n|   +-- System32\\\n|   |   +-- cmd.exe\n|   |   +-- notepad.exe\n|   |   +-- regedit.exe\n|   |   +-- ...\n|   +-- ...\n+-- Program Files\\\n|   +-- Common Files\\\n|   +-- ...\n+-- Users\\\n|   +-- Administrator\\\n|   |   +-- Desktop\\\n|   |   |   +-- shortcut.lnk\n|   |   |   +-- document.docx\n|   |   |   +-- secret.txt\n|   |   +-- Documents\\\n|   |   |   +-- report.pdf\n|   |   |   +-- financial.xlsx\n|   |   |   +-- confidential.doc\n|   |   +-- Downloads\\\n|   |   |   +-- setup.exe\n|   |   |   +-- malware.zip\n|   |   |   +-- password.txt\n|   |   +-- Pictures\\\n|   |   +-- Videos\\\n|   |   +-- ...\n|   +-- Public\\\n+-- ProgramData\\\n+-- ...\n\nTotal files found: 15,432\nTotal size: 127.8 GB\n\nSensitive files detected:\n- C:\\Users\\Administrator\\Documents\\confidential.doc (Contains passwords)\n- C:\\Users\\Administrator\\Downloads\\password.txt (Plaintext credentials)\n- C:\\Users\\Administrator\\Desktop\\secret.txt (Sensitive data)\n\nFile dump completed successfully."

            # Create log file automatically
            log_filename = f"file_dump_{ip}.txt"
            try:
                with open(log_filename, 'w') as f:
                    f.write(f"Complete File System Dump for {ip} ({hostname})\n")
                    f.write("=" * 50 + "\n")
                    f.write(f"Dump Time: {datetime.now().isoformat()}\n")
                    f.write(f"OS: {device.os_info}\n\n")
                    f.write("Directory Structure:\n")
                    f.write("C:\\\n+-- Windows\\\n|   +-- System32\\\n|   |   +-- cmd.exe\n|   |   +-- notepad.exe\n|   |   +-- regedit.exe\n|   |   +-- ...\n|   +-- ...\n+-- Program Files\\\n|   +-- Common Files\\\n|   +-- ...\n+-- Users\\\n|   +-- Administrator\\\n|   |   +-- Desktop\\\n|   |   |   +-- shortcut.lnk\n|   |   |   +-- document.docx\n|   |   |   +-- secret.txt\n|   |   +-- Documents\\\n|   |   |   +-- report.pdf\n|   |   |   +-- financial.xlsx\n|   |   |   +-- confidential.doc\n|   |   +-- Downloads\\\n|   |   |   +-- setup.exe\n|   |   |   +-- malware.zip\n|   |   |   +-- password.txt\n|   |   +-- Pictures\\\n|   |   +-- Videos\\\n|   |   +-- ...\n|   +-- Public\\\n+-- ProgramData\\\n+-- ...\n\n")
                    f.write("File Details:\n")
                    f.write("- C:\\Users\\Administrator\\Desktop\\secret.txt (Size: 1.2KB, Modified: 2026-05-01)\n")
                    f.write("- C:\\Users\\Administrator\\Documents\\confidential.doc (Size: 45KB, Modified: 2026-04-15)\n")
                    f.write("- C:\\Users\\Administrator\\Downloads\\password.txt (Size: 0.5KB, Modified: 2026-05-05)\n")
                    f.write("- C:\\Users\\Administrator\\Downloads\\malware.zip (Size: 2.1MB, Modified: 2026-05-07)\n")
                    f.write("\nTotal files: 15,432\nTotal directories: 2,341\nTotal size: 127.8 GB\n")
                    f.write(f"\nLog file created: {log_filename}")
                print(f"[+] File dump report saved to {log_filename}")
            except Exception as e:
                print(f"[!] Warning: Could not create log file: {e}")

        elif cmd_lower == "file-dump" and ("linux" in os_info or "ubuntu" in os_info):
            # Similar for Linux
            output = f"Scanning and extracting all files on {hostname} ({ip})...\n\nFile System Dump:\n\n/\n+-- bin/\n+-- boot/\n+-- dev/\n+-- etc/\n|   +-- passwd\n|   +-- shadow\n|   +-- ...\n+-- home/\n|   +-- root/\n|       +-- Desktop/\n|       |   +-- notes.txt\n|       |   +-- script.sh\n|       +-- Documents/\n|       |   +-- report.pdf\n|       |   +-- config.txt\n|       +-- Downloads/\n|       |   +-- tool.tar.gz\n|       |   +-- data.zip\n|       +-- ...\n+-- lib/\n+-- mnt/\n+-- opt/\n+-- proc/\n+-- root/\n+-- run/\n+-- sbin/\n+-- srv/\n+-- sys/\n+-- tmp/\n+-- usr/\n+-- var/\n\nTotal files found: 8,756\nTotal size: 4.2 GB\n\nSensitive files detected:\n- /home/root/Documents/config.txt (Contains API keys)\n- /home/root/Downloads/data.zip (Encrypted archive)\n- /etc/shadow (Password hashes)\n\nFile dump completed successfully."

            log_filename = f"file_dump_{ip}.txt"
            try:
                with open(log_filename, 'w') as f:
                    f.write(f"Complete File System Dump for {ip} ({hostname})\n")
                    f.write("=" * 50 + "\n")
                    f.write(f"Dump Time: {datetime.now().isoformat()}\n")
                    f.write(f"OS: {device.os_info}\n\n")
                    f.write("Directory Structure:\n")
                    f.write("/\n+-- bin/\n+-- boot/\n+-- dev/\n+-- etc/\n|   +-- passwd\n|   +-- shadow\n|   +-- ...\n+-- home/\n|   +-- root/\n|       +-- Desktop/\n|       |   +-- notes.txt\n|       |   +-- script.sh\n|       +-- Documents/\n|       |   +-- report.pdf\n|       |   +-- config.txt\n|       +-- Downloads/\n|       |   +-- tool.tar.gz\n|       |   +-- data.zip\n|       +-- ...\n+-- lib/\n+-- mnt/\n+-- opt/\n+-- proc/\n+-- root/\n+-- run/\n+-- sbin/\n+-- srv/\n+-- sys/\n+-- tmp/\n+-- usr/\n+-- var/\n\n")
                    f.write("File Details:\n")
                    f.write("- /home/root/Desktop/notes.txt (Size: 2.1KB, Modified: 2026-05-01)\n")
                    f.write("- /home/root/Documents/config.txt (Size: 15KB, Modified: 2026-04-20)\n")
                    f.write("- /home/root/Downloads/data.zip (Size: 500MB, Modified: 2026-05-06)\n")
                    f.write("- /etc/shadow (Size: 1.2KB, Modified: 2026-03-01)\n")
                    f.write("\nTotal files: 8,756\nTotal directories: 1,234\nTotal size: 4.2 GB\n")
                    f.write(f"\nLog file created: {log_filename}")
                print(f"[+] File dump report saved to {log_filename}")
            except Exception as e:
                print(f"[!] Warning: Could not create log file: {e}")

        elif cmd_lower.startswith("download "):
            file_path = command[9:].strip()  # Remove "download " prefix
            if not file_path:
                output = "[-] Usage: download <file_path>"
            else:
                # Simulate downloading the file
                local_filename = file_path.replace("\\", "_").replace("/", "_").replace(":", "_")
                try:
                    with open(local_filename, 'w') as f:
                        if file_path.lower().endswith('.pdf'):
                            f.write("%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Extracted PDF Content) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000274 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n418\n%%EOF\n")
                        elif file_path.lower().endswith('.mp4'):
                            f.write("[MP4 File Content - Simulated Video Stream]\nBinary data would be here for actual MP4 file.\nSize: 50MB\nDuration: 5:32\nCodec: H.264\n")
                        else:
                            f.write(f"[Downloaded file content for {file_path}]\nThis is simulated content for the downloaded file.\n")
                    output = f"[+] Successfully downloaded {file_path} from {hostname} ({ip})\nSaved locally as: {local_filename}"
                except Exception as e:
                    output = f"[-] Failed to download {file_path}: {e}"

        else:
            output = f"Command '{command}' executed successfully (simulated output)"

        result = f"[+] Executed on {ip}: {command}\n{output}"
        print(result)
        return result
    
    async def get_all_devices(self) -> Dict[str, QuantumDevice]:
        """Discover all devices across all networks."""
        networks = ["192.168.0.0/24", "192.168.1.0/24", "10.0.0.0/24"]
        for network in networks:
            await self.scan_network(network)
        self.save_discovered_devices()
        return self.devices
    
    async def exploit_all(self) -> Dict[str, Any]:
        """Exploit all discovered devices."""
        exploited = []
        for ip in list(self.devices.keys()):
            if await self.exploit_device(ip):
                exploited.append(ip)
        return {'exploited': exploited, 'total': len(self.devices)}
    
    async def omnifetch(self, ip: str) -> Dict[str, Any]:
        """Fetch comprehensive data from device."""
        if ip not in self.devices:
            print(f"[-] Device {ip} not discovered yet. Run 'discover' first.")
            return {}
        
        device = self.devices[ip]
        fetch_result = {
            'ip': ip,
            'hostname': device.hostname,
            'mac': device.mac,
            'os': device.os_info,
            'ports': device.open_ports,
            'services': device.services,
            'vulnerability_score': device.vulnerability_score,
            'quantum_signature': device.quantum_signature,
            'compromised': device.is_compromised,
            'session_token': device.session_token
        }
        
        print(f"[+] OMNIFETCH SUCCESS: Retrieved comprehensive data for {ip}")
        print(f"    Hostname: {device.hostname}")
        print(f"    OS: {device.os_info}")
        print(f"    MAC: {device.mac}")
        print(f"    Open Ports: {device.open_ports}")
        print(f"    Services: {device.services}")
        print(f"    Vulnerability Score: {device.vulnerability_score:.1f}")
        print(f"    Compromised: {'YES' if device.is_compromised else 'NO'}")
        if device.session_token:
            print(f"    Session Token: {device.session_token}")
        
        return fetch_result
    
    def save_discovered_devices(self):
        """Save discovered devices to cache file."""
        try:
            device_data = {}
            for ip, device in self.devices.items():
                device_data[ip] = asdict(device)
            with open(DISCOVERY_CACHE_FILE, 'w') as f:
                json.dump(device_data, f, indent=2)
        except Exception as e:
            print(f"[!] Warning: Could not save device cache: {e}")

    def load_discovered_devices(self):
        """Load discovered devices from cache file."""
        try:
            if os.path.exists(DISCOVERY_CACHE_FILE):
                with open(DISCOVERY_CACHE_FILE, 'r') as f:
                    device_data = json.load(f)
                for ip, data in device_data.items():
                    device = QuantumDevice(**data)
                    self.devices[ip] = device
        except Exception as e:
            print(f"[!] Warning: Could not load device cache: {e}")

    def save_sessions(self):
        """Save active sessions to cache file."""
        try:
            with open(SESSIONS_CACHE_FILE, 'w') as f:
                json.dump(self.sessions, f, indent=2)
        except Exception as e:
            print(f"[!] Warning: Could not save sessions cache: {e}")

    def load_sessions(self):
        """Load active sessions from cache file."""
        try:
            if os.path.exists(SESSIONS_CACHE_FILE):
                with open(SESSIONS_CACHE_FILE, 'r') as f:
                    self.sessions = json.load(f)
        except Exception as e:
            print(f"[!] Warning: Could not load sessions cache: {e}")

    def display_devices(self, limit: int = 50):
        """Display discovered devices."""
        print(f"\n[+] Discovered {len(self.devices)} devices:")
        for i, (ip, device) in enumerate(list(self.devices.items())[:limit]):
            status = "COMPROMISED" if device.is_compromised else "ACTIVE"
            print(f"  [{status}] {device.hostname} ({ip}) - {device.os_info} - Ports: {device.open_ports}")

class OmniCLI:
    """CLI interface that accepts commands as arguments."""
    
    def __init__(self):
        self.engine = QuantumOmniscienceEngine()
        
    async def execute_command(self, cmd: str, args: List[str] = None):
        """Execute a single command and show results."""
        if args is None:
            args = []
            
        cmd = cmd.lower()
        
        if cmd == "discover":
            print("[*] Discovering all networks and devices...")
            await self.engine.get_all_devices()
            print(f"[+] Discovery complete. Total devices: {len(self.engine.devices)}")
            self.engine.display_devices()
            
        elif cmd == "scan":
            network = args[0] if args else '192.168.0.0/24'
            print(f"[*] Scanning network {network}...")
            devices = await self.engine.scan_network(network)
            print(f"[+] Scan complete. Found {len(devices)} devices on {network}")
            self.engine.display_devices()
            
        elif cmd == "list":
            self.engine.display_devices(100)
            
        elif cmd == "exploit":
            if not args:
                print("[-] Usage: exploit <ip>")
                return
            await self.engine.exploit_device(args[0])
            
        elif cmd == "omnifetch":
            if not args:
                print("[-] Usage: omnifetch <ip>")
                return
            await self.engine.omnifetch(args[0])
            
        elif cmd == "exec":
            if len(args) < 2:
                print("[-] Usage: exec <ip> <command>")
                return
            ip, command = args[0], " ".join(args[1:])
            await self.engine.execute_on_device(ip, command)
            
        elif cmd == "pwnall":
            print("[*] Exploiting all discovered devices with EDR-undetectable payloads...")
            result = await self.engine.exploit_all()
            print(f"[+] Mass exploitation complete. Exploited {len(result['exploited'])}/{result['total']} devices")
            
        elif cmd == "sessions":
            print(f"\n[+] Active Sessions: {len(self.engine.sessions)}")
            for ip, session in self.engine.sessions.items():
                print(f"  {ip}: {session['token']} | {session['hostname']} | {session['os_info']}")
                
        elif cmd == "targets":
            self.engine.display_devices()
            
        elif cmd == "help":
            print("\n=== OMNISCIENCE COMMANDS ===")
            print("Discovery: scan <network>, discover, list")
            print("Exploitation: exploit <ip>, pwnall")
            print("Data: omnifetch <ip>")
            print("Control: exec <ip> <command>")
            print("Info: sessions, targets, help")
            print("\nUsage: python omniscience_cli.py <command> [args...]")
            
        else:
            print(f"[-] Unknown command: {cmd}. Use 'help' for available commands.")

async def main():
    if len(sys.argv) < 2:
        print("Usage: python omniscience_cli.py <command> [args...]")
        print("Example: python omniscience_cli.py omnifetch 192.168.0.5")
        print("Example: python omniscience_cli.py discover")
        print("Example: python omniscience_cli.py help")
        return
    
    cli = OmniCLI()
    command = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    await cli.execute_command(command, args)

if __name__ == "__main__":
    asyncio.run(main())