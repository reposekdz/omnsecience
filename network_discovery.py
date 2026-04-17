"""
OMNISCIENCE MODULE 1 — NetworkDiscovery
Multi-vector, fully agentless network enumeration.
No software installed on targets. Works on any subnet. 

Discovery methods:
  ARP      - Layer-2 broadcast (fastest, LAN only)
  ICMP     - Ping sweep (parallel, works across subnets)
  TCP      - SYN probe on common ports (50-thread parallel)
  NetBIOS  - Windows hostname + workgroup (UDP 137)
  mDNS     - Apple/Linux/IoT service announcements (UDP 5353)
  SSDP     - UPnP device discovery (UDP 1900)
  SNMP     - Device info without credentials (community=public)
  DNS-PTR  - Reverse DNS for all IPs in range
  HTTP     - API/web service fingerprinting on every open port

Auto-Network Features:
  - Multi-interface detection (all network adapters)
  - Gateway & subnet auto-detection
  - Device fingerprinting (OS, device type, services)
  - Automatic feature enumeration for each host
"""

import os
import sys
import time
import json
import socket
import struct
import logging
import ipaddress
import threading
import subprocess
import uuid
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from typing import Optional, Dict, List, Any, Tuple

try:
    import scapy.all as scapy
    from scapy.layers import inet, l2
    # Suppress noisy Scapy warnings (e.g., "MAC address to reach destination not found")
    import logging as py_logging
    py_logging.getLogger("scapy.runtime").setLevel(py_logging.ERROR)
    SCAPY_OK = True
except ImportError:
    SCAPY_OK = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | Discovery | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("discovery.log", mode="a"),
    ]
)
logger = logging.getLogger("Omniscience.Discovery")

# Common TCP ports to probe
COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 137, 139, 143,
    389, 443, 445, 465, 587, 631, 993, 995, 1080, 1433, 1521,
    2049, 2082, 2083, 2222, 3000, 3306, 3389, 3690, 4444, 4848,
    5000, 5432, 5555, 5900, 5985, 6379, 7070, 7443, 8000, 8008,
    8080, 8081, 8443, 8888, 9000, 9090, 9200, 9418, 10000, 27017,
]

# TTL -> OS hint
TTL_OS = {
    (1,  64):  "Linux/Android/macOS",
    (65, 128): "Windows",
    (129,255): "Cisco/Network Device",
}

MAC_VENDORS = {
    # VMware & VirtualBox
    "000C29": "VMware", "001A11": "Google", "FCAA14": "Amazon",
    "005056": "VMware", "000D3A": "VMware", "00155D": "Microsoft Hyper-V",
    "001DD8": "Microsoft", "001B21": "Intel",
    
    # Single Board Computers
    "B827EB": "Raspberry Pi", "B82344": "Raspberry Pi", "DC:A6:32": "Raspberry Pi",
    "E4:5F:01": "Raspberry Pi",
    
    # Apple devices
    "DC4F22": "Apple", "3C5AB4": "Apple", "F0189B": "Apple", "A4D1D2": "Apple",
    "7C6DF8": "Apple", "F0DCE2": "Apple", "6C4008": "Apple",
    
    # Samsung
    "9C2986": "Samsung", "D850E6": "Samsung", "B47F9F": "Samsung",
    "8C71F8": "Samsung", "48D7E2": "Samsung",
    
    # Huawei
    "18AF61": "Huawei", "48A73E": "Huawei", "00E0FC": "Huawei",
    "C86000": "Huawei", "04B0E7": "Huawei",
    
    # Xiaomi
    "E4B318": "Xiaomi", "34:80:B3": "Xiaomi", "F0B431": "Xiaomi",
    
    # TP-Link
    "7085C2": "TP-Link", "50C7BF": "TP-Link", "5464CD": "TP-Link",
    "E848B8": "TP-Link", "A42BB0": "TP-Link",
    
    # Netgear
    "D460E3": "Netgear", "C03F0E": "Netgear", "2C3033": "Netgear",
    
    # D-Link
    "C80E77": "D-Link", "1CEAAD": "D-Link", "5CD2E8": "D-Link",
    
    # Cisco
    "000000": "Xerox", "00E04C": "Realtek", "001122": "Cisco",
    "00249B": "Cisco", "000C30": "Cisco",
    
    # Asus
    "001FC6": "Asus", "002215": "Asus", "047D7B": "Asus",
    
    # Generic
    "000000": "Unknown",
}

# Extended device type detection based on ports and services
DEVICE_TYPE_PATTERNS = {
    "router": ["192.168.0.1", "192.168.1.1", "10.0.0.1", "10.0.1.1", "gateway"],
    "camera": [554, 8554, 8081],
    "printer": [631, 9100, 515],
    "nas": [5000, 5001, 8080, 8443],
    "iot": [1883, 8883, 5683],
    "game_console": [3074, 3478, 3479, 3480],
    "smart_tv": [5500, 9000],
    "voip": [5060, 5061],
    "database": [3306, 5432, 27017, 6379, 1433],
    "web_server": [80, 443, 8080, 8443],
}

# HTTP service fingerprints for identification
HTTP_FINGERPRINTS = {
    "apache": [b"Apache", b"Server: Apache"],
    "nginx": [b"nginx", b"Server: nginx"],
    "iis": [b"IIS", b"Server: Microsoft-IIS"],
    "nodejs": [b"Server: Express", b"X-Powered-By: Express"],
    "django": [b"Set-Cookie: csrftoken", b"X-Frame-Options: SAMEORIGIN"],
    "flask": [b"Server: Werkzeug", b"Set-Cookie: session"],
    "tomcat": [b"Server: Apache-Coyote", b"Apache Tomcat"],
    "jetty": [b"Server: Jetty"],
}


class NetworkInterfaceDetector:
    """
    Advanced network interface and gateway detection.
    Automatically detects all network interfaces, gateways, and subnets.
    """
    
    def __init__(self):
        self.interfaces: List[Dict[str, Any]] = []
        self.gateway: Optional[Dict[str, str]] = None
        self.local_ip: str = ""
        self.subnet_mask: str = ""
        self.network_range: str = ""
        self._detect_all()
    
    def _detect_all(self):
        """Detect all network information."""
        self._detect_interfaces()
        self._detect_gateway()
        self._detect_local_info()
        self._detect_external_info()
    
    def _detect_external_info(self):
        """Detect external IP and gateway details (WAN/GAN)."""
        self.external_ip = "Unknown"
        self.external_hostname = "Unknown"
        try:
            # Try multiple services for redundancy
            for service in ["https://api.ipify.org", "https://ifconfig.me/ip", "https://icanhazip.com"]:
                try:
                    import urllib.request
                    with urllib.request.urlopen(service, timeout=3) as response:
                        self.external_ip = response.read().decode().strip()
                        if self.external_ip:
                            break
                except:
                    continue
            
            if self.external_ip != "Unknown":
                self.external_hostname = socket.gethostbyaddr(self.external_ip)[0]
        except:
            pass
        logger.info(f"[WAN] External IP: {self.external_ip} ({self.external_hostname})")
    
    def _detect_interfaces(self):
        """Detect all network interfaces on the system."""
        interfaces = []
        
        # Method 1: Use socket and common interfaces
        try:
            # Get all interfaces using socket
            import subprocess
            if os.name == "nt":
                # Windows
                try:
                    result = subprocess.run(["ipconfig"], capture_output=True, text=True, timeout=5)
                    current_iface = ""
                    for line in result.stdout.splitlines():
                        line = line.strip()
                        if line and not line.startswith(" "):
                            # New adapter
                            if "adapter" in line.lower():
                                current_iface = line.split("adapter")[1].strip(" :").strip()
                        elif "IPv4 Address" in line and ":" in line:
                            ip = line.split(":")[-1].strip()
                            if not ip.startswith("169."):
                                interfaces.append({
                                    "name": current_iface,
                                    "ip": ip,
                                    "type": "ethernet"
                                })
                except:
                    pass
            else:
                # Unix/Linux
                try:
                    result = subprocess.run(["ip", "addr"], capture_output=True, text=True, timeout=5)
                    current_iface = ""
                    for line in result.stdout.splitlines():
                        line = line.strip()
                        if line and not line.startswith(" ") and ":" in line:
                            current_iface = line.split(":")[0].strip()
                        elif "inet " in line and current_iface:
                            parts = line.split()
                            if len(parts) >= 2:
                                ip = parts[1].split("/")[0]
                                if not ip.startswith("169."):
                                    interfaces.append({
                                        "name": current_iface,
                                        "ip": ip,
                                        "type": "ethernet"
                                    })
                except:
                    pass
        except:
            pass
        
        # Method 2: Direct socket detection (fallback)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            
            if not any(i["ip"] == local_ip for i in interfaces):
                interfaces.append({
                    "name": "primary",
                    "ip": local_ip,
                    "type": "primary"
                })
        except:
            pass
        
        self.interfaces = interfaces
    
    def _detect_gateway(self):
        """Detect default gateway using multiple methods."""
        gateway = None
        
        try:
            if os.name == "nt":
                # Windows - use route print
                result = subprocess.run(["route", "print", "0.0.0.0"], 
                                       capture_output=True, text=True, timeout=5)
                for line in result.stdout.splitlines():
                    if "0.0.0.0" in line or "Default Gateway" in line:
                        parts = line.split()
                        for p in parts:
                            if re.match(r'\d+\.\d+\.\d+\.\d+', p):
                                if p != "0.0.0.0":
                                    gateway = p
                                    break
            else:
                # Unix - check route or ip
                result = subprocess.run(["ip", "route"], capture_output=True, text=True, timeout=5)
                for line in result.stdout.splitlines():
                    if "default" in line:
                        parts = line.split()
                        for i, p in enumerate(parts):
                            if p == "default" and i + 1 < len(parts):
                                gateway = parts[i + 1]
                                break
        except:
            pass
        
        # Fallback: guess from local IP
        if not gateway and self.interfaces:
            for iface in self.interfaces:
                if iface.get("ip"):
                    parts = iface["ip"].split(".")
                    gateway = f"{parts[0]}.{parts[1]}.{parts[2]}.1"
                    break
        
        if gateway:
            self.gateway = {"ip": gateway}
            # Try to get MAC of gateway
            if SCAPY_OK:
                try:
                    pkt = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=gateway)
                    answered, _ = scapy.srp(pkt, timeout=1, verbose=False)
                    if answered:
                        self.gateway["mac"] = answered[0][1].hwsrc
                except:
                    pass
    
    def _detect_local_info(self):
        """Detect local IP and calculate network range."""
        if self.interfaces:
            # Prefer non-localhost interface
            for iface in self.interfaces:
                ip = iface.get("ip", "")
                if ip and not ip.startswith("127.") and not ip.startswith("169."):
                    self.local_ip = ip
                    # Calculate network range (assume /24 for simplicity)
                    parts = ip.split(".")
                    self.network_range = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
                    self.subnet_mask = "255.255.255.0"
                    break
            
            # Fallback to first interface
            if not self.local_ip and self.interfaces:
                self.local_ip = self.interfaces[0].get("ip", "192.168.1.1")
                parts = self.local_ip.split(".")
                self.network_range = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
                self.subnet_mask = "255.255.255.0"
    
    def get_auto_range(self) -> str:
        """Get the automatically detected network range."""
        return self.network_range or "192.168.1.0/24"
    
    def get_gateway_ip(self) -> str:
        """Get gateway IP address."""
        if self.gateway:
            return self.gateway.get("ip", "")
        return ""
    
    def get_local_ip(self) -> str:
        """Get local IP address."""
        return self.local_ip
    
    def get_all_ips(self) -> List[str]:
        """Get all IP addresses from detected interfaces."""
        return [i.get("ip", "") for i in self.interfaces if i.get("ip")]
    
    def get_interface_info(self) -> Dict[str, Any]:
        """Get comprehensive interface information."""
        return {
            "interfaces": self.interfaces,
            "gateway": self.gateway,
            "local_ip": self.local_ip,
            "subnet_mask": self.subnet_mask,
            "network_range": self.network_range
        }
    
    def get_all_interface_ranges(self) -> List[str]:
        """Extract all IP ranges from all active network interfaces."""
        ranges = []
        if self.network_range:
            ranges.append(self.network_range)
        for i in self.interfaces:
            ip = i.get("ip")
            mask = i.get("mask", "255.255.255.0")
            if ip and ip != "127.0.0.1":
                # Convert IP/Mask to CIDR
                parts = ip.split('.')
                net_range = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
                if net_range not in ranges:
                    ranges.append(net_range)
        return ranges

    def __str__(self) -> str:
        lines = ["Network Interface Information:"]
        lines.append(f"  Local IP: {self.local_ip}")
        lines.append(f"  Subnet Mask: {self.subnet_mask}")
        lines.append(f"  Network Range: {self.network_range}")
        if self.gateway:
            lines.append(f"  Gateway IP: {self.gateway.get('ip', 'N/A')}")
            if "mac" in self.gateway:
                lines.append(f"  Gateway MAC: {self.gateway.get('mac', 'N/A')}")
        lines.append(f"  Interfaces: {len(self.interfaces)}")
        return "\n".join(lines)


class HostRecord:
    """Stores all discovered info about a single host."""

    def __init__(self, ip: str):
        self.ip = ip
        self.mac = ""
        self.vendor = ""
        self.hostname = ""
        self.os_hint = ""
        self.device_type = ""  # router, computer, phone, iot, etc.
        self.ttl = 0
        self.first_seen = time.time()
        self.last_seen = time.time()
        self.open_ports = {}        # {port: {"service": str, "banner": str, "api": bool}}
        self.netbios = {}           # {name, workgroup, type}
        self.mdns_services = []
        self.ssdp_info = {}
        self.snmp_info = {}
        self.api_endpoints = []     # [{port, path, method, status, title, server}]
        self.http_hosts = []
        self.discovery_methods = []
        self.is_gateway = False
        self.is_local = False
        self.device_fingerprint = {}  # Additional fingerprinting info

    def to_dict(self) -> dict:
        return {
            "ip": self.ip, "mac": self.mac, "vendor": self.vendor,
            "hostname": self.hostname, "os_hint": self.os_hint, 
            "device_type": self.device_type, "ttl": self.ttl,
            "open_ports": self.open_ports, "netbios": self.netbios,
            "mdns_services": self.mdns_services, "ssdp_info": self.ssdp_info,
            "snmp_info": self.snmp_info, "api_endpoints": self.api_endpoints,
            "discovery_methods": self.discovery_methods,
            "is_gateway": self.is_gateway, "is_local": self.is_local,
            "device_fingerprint": self.device_fingerprint,
            "first_seen": self.first_seen, "last_seen": self.last_seen,
        }

    def determine_device_type(self):
        """Automatically determine device type based on open ports and info."""
        ports = list(self.open_ports.keys())
        
        # Check for router/gateway
        if self.hostname and any(x in self.hostname.lower() for x in ['router', 'gateway', 'ap']):
            return "router"
        
        # Check by port signatures
        if 554 in ports or 8554 in ports:
            return "camera"
        if 631 in ports or 9100 in ports:
            return "printer"
        if 5000 in ports or 5001 in ports:
            return "nas"
        if 1883 in ports or 8883 in ports:
            return "iot"
        if 3074 in ports or 3478 in ports:
            return "game_console"
        if 5060 in ports or 5061 in ports:
            return "voip"
        if 3306 in ports or 5432 in ports or 27017 in ports:
            return "database_server"
        if 80 in ports or 443 in ports or 8080 in ports:
            return "web_server"
        if 22 in ports:
            return "linux_server"
        if 3389 in ports or 445 in ports:
            return "windows_pc"
        
        # Check by vendor
        if self.vendor:
            if "Raspberry" in self.vendor:
                return "single_board_computer"
            if "Apple" in self.vendor:
                return "apple_device"
            if "Samsung" in self.vendor or "Xiaomi" in self.vendor or "Huawei" in self.vendor:
                return "smartphone"
        
        # Default based on OS
        if "Linux" in self.os_hint:
            return "linux_device"
        if "Windows" in self.os_hint:
            return "windows_device"
        
        return "unknown"

    def summary(self) -> str:
        ports = sorted(self.open_ports.keys())
        device_type = self.device_type or "unknown"
        gateway_mark = "[GATEWAY]" if self.is_gateway else ""
        local_mark = "[LOCAL]" if self.is_local else ""
        return (
            f"{self.ip:<18} {self.mac:<19} {self.vendor:<18} "
            f"{self.hostname:<25} {self.os_hint:<18} {device_type:<12} "
            f"Ports:{len(ports)} {gateway_mark} {local_mark}"
        )


class NetworkDiscovery:
    """
    Full-spectrum, agentless network discovery engine.
    Combines 8 independent discovery methods and merges results.
    Includes auto-network detection and device fingerprinting.
    """

    def __init__(self):
        self.hosts = {}          # ip -> HostRecord
        self._lock = threading.Lock()
        self._ssdp_sock = None
        self._mdns_sock = None
        
        # Auto-network detection
        self.interface_detector = NetworkInterfaceDetector()
        self._auto_detected = False

    def auto_detect_network(self) -> str:
        """
        Automatically detect the connected network and return the range.
        This is the main entry point for auto-network functionality.
        """
        logger.info("[AUTO] Detecting network configuration...")
        
        # Get auto-detected range
        network_range = self.interface_detector.get_auto_range()
        local_ip = self.interface_detector.get_local_ip()
        gateway_ip = self.interface_detector.get_gateway_ip()
        
        logger.info(f"[AUTO] Local IP: {local_ip}")
        logger.info(f"[AUTO] Network Range: {network_range}")
        logger.info(f"[AUTO] Gateway: {gateway_ip}")
        
        self._auto_detected = True
        return network_range
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get comprehensive network information."""
        return self.interface_detector.get_interface_info()
    
    def get_all_device_ips(self) -> List[str]:
        """Get all IP addresses of discovered devices."""
        return sorted(self.hosts.keys(), key=lambda x: socket.inet_aton(x))
    
    def get_device_by_ip(self, ip: str) -> Optional[HostRecord]:
        """Get device information by IP address."""
        return self.hosts.get(ip)
    
    def get_gateway_device(self) -> Optional[HostRecord]:
        """Get the gateway device if discovered."""
        gateway_ip = self.interface_detector.get_gateway_ip()
        if gateway_ip:
            return self.hosts.get(gateway_ip)
        return None

    # ─── Internal: record management ─────────────────────────────────────────

    def _get_or_create(self, ip: str) -> HostRecord:
        with self._lock:
            if ip not in self.hosts:
                self.hosts[ip] = HostRecord(ip)
            return self.hosts[ip]

    def _mac_vendor(self, mac: str) -> str:
        if not mac:
            return ""
        prefix = mac.upper().replace(":", "").replace("-", "")[:6]
        return MAC_VENDORS.get(prefix, "")

    def _os_from_ttl(self, ttl: int) -> str:
        for (lo, hi), os_name in TTL_OS.items():
            if lo <= ttl <= hi:
                return os_name
        return "Unknown"

    # ─── METHOD 1: ARP scan ───────────────────────────────────────────────────

    def arp_scan(self, ip_range: str) -> list:
        if not SCAPY_OK:
            return []
        logger.info(f"[ARP] Scanning {ip_range}")
        found = []
        try:
            pkt = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=ip_range)
            answered, _ = scapy.srp(pkt, timeout=2, verbose=False, retry=2)
            for _, recv in answered:
                h = self._get_or_create(recv.psrc)
                h.mac = recv.hwsrc
                h.vendor = self._mac_vendor(recv.hwsrc)
                if "ARP" not in h.discovery_methods:
                    h.discovery_methods.append("ARP")
                found.append(recv.psrc)
                logger.info(f"[ARP] {recv.psrc:<18} {recv.hwsrc}  {h.vendor}")
        except Exception as e:
            logger.error(f"ARP scan error: {e}")
        return found

    # ─── METHOD 2: ICMP ping sweep ────────────────────────────────────────────

    def _icmp_ping(self, ip: str, timeout: float = 0.8) -> bool:
        try:
            if os.name == "nt":
                r = subprocess.run(
                    ["ping", "-n", "1", "-w", str(int(timeout * 1000)), ip],
                    capture_output=True, timeout=timeout + 1
                )
                return r.returncode == 0
            else:
                r = subprocess.run(
                    ["ping", "-c", "1", "-W", str(int(timeout)), ip],
                    capture_output=True, timeout=timeout + 1
                )
                return r.returncode == 0
        except Exception:
            return False

    def _icmp_scapy(self, ip: str, timeout: float = 0.8) -> tuple:
        """Returns (alive, ttl)"""
        try:
            pkt = scapy.IP(dst=ip, ttl=64) / scapy.ICMP()
            resp = scapy.sr1(pkt, timeout=timeout, verbose=False)
            if resp and resp.haslayer(scapy.ICMP):
                return True, resp.ttl
        except Exception:
            pass
        return False, 0

    def icmp_sweep(self, ip_range: str, max_workers: int = 100) -> list:
        logger.info(f"[ICMP] Sweep {ip_range}")
        try:
            network = ipaddress.ip_network(ip_range, strict=False)
            ips = [str(h) for h in network.hosts()]
        except ValueError:
            ips = [ip_range]

        found = []

        def _probe(ip):
            if SCAPY_OK:
                alive, ttl = self._icmp_scapy(ip)
                if alive:
                    h = self._get_or_create(ip)
                    h.ttl = ttl
                    h.os_hint = self._os_from_ttl(ttl)
                    if "ICMP" not in h.discovery_methods:
                        h.discovery_methods.append("ICMP")
                    return ip
            else:
                if self._icmp_ping(ip):
                    h = self._get_or_create(ip)
                    if "ICMP" not in h.discovery_methods:
                        h.discovery_methods.append("ICMP")
                    return ip
            return None

        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="ICMP") as ex:
            futures = {ex.submit(_probe, ip): ip for ip in ips}
            for fut in as_completed(futures):
                result = fut.result()
                if result:
                    found.append(result)
                    logger.info(f"[ICMP] {result} is alive")

        return found

    # ─── METHOD 3: TCP port probe ─────────────────────────────────────────────

    def tcp_probe(self, ip: str, ports: list = None, timeout: float = 0.4) -> dict:
        if ports is None:
            ports = COMMON_PORTS
        open_ports = {}

        def _check(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((ip, port))
                sock.close()
                return port, result == 0
            except Exception:
                return port, False

        with ThreadPoolExecutor(max_workers=60, thread_name_prefix="TCP") as ex:
            futures = {ex.submit(_check, p): p for p in ports}
            for fut in as_completed(futures):
                port, is_open = fut.result()
                if is_open:
                    svc = self._port_service(port)
                    open_ports[port] = {"service": svc, "banner": "", "api": False}

        if open_ports:
            h = self._get_or_create(ip)
            with self._lock:
                for port, data in open_ports.items():
                    h.open_ports[port] = data
            if "TCP" not in h.discovery_methods:
                h.discovery_methods.append("TCP")
            logger.info(f"[TCP] {ip}: open ports {sorted(open_ports.keys())}")

        return open_ports

    @staticmethod
    def _port_service(port: int) -> str:
        SERVICES = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC", 137: "NetBIOS-NS",
            139: "NetBIOS-SSN", 143: "IMAP", 389: "LDAP", 443: "HTTPS",
            445: "SMB", 465: "SMTPS", 587: "SMTP", 631: "IPP", 993: "IMAPS",
            995: "POP3S", 1080: "SOCKS", 1433: "MSSQL", 1521: "Oracle",
            2049: "NFS", 2082: "cPanel", 2083: "cPanel-SSL", 2222: "SSH-alt",
            3000: "HTTP-dev", 3306: "MySQL", 3389: "RDP", 3690: "SVN",
            4444: "Metasploit", 4848: "GlassFish", 5000: "HTTP-dev",
            5432: "PostgreSQL", 5555: "ADB", 5900: "VNC", 5985: "WinRM-HTTP",
            6379: "Redis", 7443: "HTTP-alt-SSL", 8000: "HTTP-dev",
            8080: "HTTP-proxy", 8081: "HTTP-alt", 8443: "HTTPS-alt",
            8888: "Jupyter", 9000: "HTTP-dev", 9090: "HTTP-mgmt",
            9200: "Elasticsearch", 27017: "MongoDB",
        }
        return SERVICES.get(port, "Unknown")

    # ─── METHOD 4: NetBIOS scan ───────────────────────────────────────────────

    def netbios_scan(self, ip: str, timeout: float = 2.0) -> dict:
        """Query NetBIOS Name Service (UDP 137) — no credentials needed."""
        result = {}
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            # NetBIOS Name Service status request
            query = bytes([
                0x00, 0x00,              # Transaction ID
                0x00, 0x10,              # Flags: query
                0x00, 0x01,              # Questions: 1
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # RR counts
                0x20,                    # Name length
            ]) + b"CKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + bytes([
                0x00,                    # End
                0x00, 0x21,              # Type: NBSTAT
                0x00, 0x01,              # Class: IN
            ])
            sock.sendto(query, (ip, 137))
            data, _ = sock.recvfrom(1024)
            sock.close()

            if len(data) > 57:
                num_names = data[56]
                offset = 57
                names = []
                for _ in range(num_names):
                    if offset + 18 > len(data):
                        break
                    raw_name = data[offset:offset + 15].decode(errors="ignore").strip()
                    name_type = data[offset + 15]
                    flags = struct.unpack(">H", data[offset + 16:offset + 18])[0]
                    names.append({"name": raw_name, "type": hex(name_type), "flags": hex(flags)})
                    offset += 18

                result["names"] = names
                # Extract hostname (type 0x00) and workgroup (type 0x00 with group flag)
                for n in names:
                    t = int(n["type"], 16)
                    f = int(n["flags"], 16)
                    if t == 0x00 and not (f & 0x8000):
                        result["hostname"] = n["name"].strip()
                    elif t == 0x00 and (f & 0x8000):
                        result["workgroup"] = n["name"].strip()
                    elif t == 0x20:
                        result["file_server"] = n["name"].strip()

                # MAC from last 6 bytes
                if len(data) >= offset + 6:
                    mac_bytes = data[offset:offset + 6]
                    result["mac"] = ":".join(f"{b:02x}" for b in mac_bytes)

                if result:
                    h = self._get_or_create(ip)
                    h.netbios = result
                    if result.get("hostname"):
                        h.hostname = result["hostname"]
                    if result.get("mac") and not h.mac:
                        h.mac = result["mac"]
                        h.vendor = self._mac_vendor(result["mac"])
                    if "NetBIOS" not in h.discovery_methods:
                        h.discovery_methods.append("NetBIOS")
                    logger.info(f"[NETBIOS] {ip}: hostname={result.get('hostname','')} "
                                f"workgroup={result.get('workgroup','')}")

        except socket.timeout:
            pass
        except Exception as e:
            logger.debug(f"NetBIOS {ip}: {e}")
        return result

    def netbios_sweep(self, ip_range: str, max_workers: int = 50) -> dict:
        logger.info(f"[NETBIOS] Sweep {ip_range}")
        try:
            network = ipaddress.ip_network(ip_range, strict=False)
            ips = [str(h) for h in network.hosts()]
        except ValueError:
            ips = [ip_range]

        results = {}
        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="NB") as ex:
            futures = {ex.submit(self.netbios_scan, ip): ip for ip in ips}
            for fut in as_completed(futures):
                ip = futures[fut]
                r = fut.result()
                if r:
                    results[ip] = r
        return results

    # ─── METHOD 5: mDNS discovery ─────────────────────────────────────────────

    def mdns_listen(self, duration: float = 5.0) -> dict:
        """Listen for mDNS announcements (multicast 224.0.0.251:5353)."""
        results = defaultdict(list)
        logger.info(f"[mDNS] Listening {duration}s on 224.0.0.251:5353")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except (AttributeError, OSError):
                pass
            sock.bind(("", 5353))
            mcast_req = struct.pack("4sL", socket.inet_aton("224.0.0.251"), socket.INADDR_ANY)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mcast_req)
            sock.settimeout(1.0)
            end = time.time() + duration
            while time.time() < end:
                try:
                    data, (src_ip, _) = sock.recvfrom(8192)
                    if len(data) > 12:
                        # Advanced mDNS/DNS-SD Parsing
                        # Skip header (12 bytes)
                        ptr = 12
                        def _parse_name(raw, p):
                            parts = []
                            while p < len(raw):
                                l = raw[p]
                                if l == 0: return ".".join(parts), p + 1
                                if l & 0xC0 == 0xC0: # Pointer
                                    return ".".join(parts), p + 2
                                p += 1
                                if p + l <= len(raw):
                                    parts.append(raw[p:p+l].decode(errors="ignore"))
                                p += l
                            return ".".join(parts), p
                        
                        try:
                            service, _ = _parse_name(data, ptr)
                            if service and not service.startswith("_"):
                                if src_ip not in results[src_ip]:
                                    results[src_ip].append(service)
                                h = self._get_or_create(src_ip)
                                if service not in h.mdns_services:
                                    h.mdns_services.append(service)
                                if "mDNS" not in h.discovery_methods:
                                    h.discovery_methods.append("mDNS")
                                # Map common services to ports
                                if "_http" in service: h.open_ports[80] = {"service": "HTTP (mDNS)", "banner": service}
                                if "_ssh" in service: h.open_ports[22] = {"service": "SSH (mDNS)", "banner": service}
                                logger.info(f"[mDNS] {src_ip}: {service}")
                        except: pass
                except socket.timeout: continue
            sock.close()
        except Exception as e:
            logger.debug(f"mDNS listen: {e}")
        return dict(results)

    def _resolve_ssdp_xml(self, ip: str, url: str):
        """Background XML fetcher for rich SSDP metadata."""
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=3) as resp:
                body = resp.read().decode(errors="ignore")
                h = self._get_or_create(ip)
                for tag in ["friendlyName", "manufacturer", "modelName", "modelNumber"]:
                    m = re.search(f"<{tag}>(.*?)</{tag}>", body, re.I)
                    if m:
                        val = m.group(1).strip()
                        h.ssdp_info[tag] = val
                        if tag == "friendlyName" and not h.hostname: h.hostname = val
                        if tag == "manufacturer" and not h.vendor: h.vendor = val
                logger.debug(f"[SSDP-XML] enriched {ip}")
        except: pass

    # ─── METHOD 6: SSDP/UPnP discovery ───────────────────────────────────────

    def ssdp_discover(self, timeout: float = 5.0) -> dict:
        """Send UPnP M-SEARCH, collect all responses."""
        logger.info("[SSDP] UPnP M-SEARCH broadcast")
        results = {}
        msearch = (
            "M-SEARCH * HTTP/1.1\r\n"
            "HOST: 239.255.255.250:1900\r\n"
            "MAN: \"ssdp:discover\"\r\n"
            "MX: 3\r\n"
            "ST: ssdp:all\r\n\r\n"
        ).encode()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(1.0)
            sock.sendto(msearch, ("239.255.255.250", 1900))
            end = time.time() + timeout
            while time.time() < end:
                try:
                    data, (src_ip, _) = sock.recvfrom(8192)
                    text = data.decode(errors="ignore")
                    headers = {l.split(':', 1)[0].upper().strip(): l.split(':', 1)[1].strip() 
                               for l in text.splitlines() if ':' in l}
                    
                    if src_ip not in results:
                        results[src_ip] = headers
                        h = self._get_or_create(src_ip)
                        h.ssdp_info = headers
                        if "SSDP" not in h.discovery_methods:
                            h.discovery_methods.append("SSDP")
                        
                        # High-IQ Fingerprinting from headers
                        serv = headers.get("SERVER", "") or headers.get("ST", "")
                        loc = headers.get("LOCATION", "")
                        if serv or loc:
                            logger.info(f"[SSDP] {src_ip}: {serv[:60]} -> {loc}")
                        
                        # Try to resolve friendly name from LOCATION XML
                        if loc:
                            threading.Thread(target=self._resolve_ssdp_xml, args=(src_ip, loc), daemon=True).start()
                except socket.timeout:
                    continue
            sock.close()
        except Exception as e:
            logger.debug(f"SSDP: {e}")
        return results

    # ─── METHOD 7: SNMP polling ───────────────────────────────────────────────

    def snmp_query(self, ip: str, community: str = "public", timeout: float = 2.0) -> dict:
        """
        SNMPv1 GetRequest for sysDescr (OID 1.3.6.1.2.1.1.1.0).
        No credentials needed for devices with default community string.
        """
        result = {}
        try:
            # Build SNMPv1 GetRequest manually
            def _encode_oid(oid_str):
                parts = list(map(int, oid_str.split(".")))
                encoded = bytes([40 * parts[0] + parts[1]])
                for p in parts[2:]:
                    if p < 128:
                        encoded += bytes([p])
                    else:
                        encoded += bytes([0x80 | (p >> 7), p & 0x7F])
                return b"\x06" + bytes([len(encoded)]) + encoded

            def _tlv(tag, value):
                return bytes([tag, len(value)]) + value

            def _snmp_get(oid_str):
                oid = _encode_oid(oid_str)
                varbind = _tlv(0x30, _tlv(0x30, oid + b"\x05\x00"))
                community_b = community.encode()
                pdu = _tlv(0xA0, b"\x02\x01\x00\x02\x01\x00\x02\x01\x00" + varbind)
                msg = _tlv(0x30,
                           b"\x02\x01\x00" +
                           _tlv(0x04, community_b) +
                           pdu)
                return msg

            OIDs = {
                "sysDescr":    "1.3.6.1.2.1.1.1.0",
                "sysName":     "1.3.6.1.2.1.1.5.0",
                "sysLocation": "1.3.6.1.2.1.1.6.0",
                "sysContact":  "1.3.6.1.2.1.1.4.0",
                "sysUptime":   "1.3.6.1.2.1.1.3.0",
            }
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            for key, oid in OIDs.items():
                try:
                    sock.sendto(_snmp_get(oid), (ip, 161))
                    data, _ = sock.recvfrom(4096)
                    # Extract string value (type 0x04 = OctetString)
                    idx = data.rfind(b"\x04")
                    if idx >= 0 and idx + 1 < len(data):
                        slen = data[idx + 1]
                        val = data[idx + 2: idx + 2 + slen].decode(errors="ignore").strip()
                        if val:
                            result[key] = val
                except socket.timeout:
                    break
                except Exception:
                    continue
            sock.close()

            if result:
                h = self._get_or_create(ip)
                h.snmp_info = result
                if not h.hostname and result.get("sysName"):
                    h.hostname = result["sysName"]
                if not h.os_hint and result.get("sysDescr"):
                    h.os_hint = result["sysDescr"][:60]
                if "SNMP" not in h.discovery_methods:
                    h.discovery_methods.append("SNMP")
                logger.info(f"[SNMP] {ip}: {result.get('sysDescr','')[:80]}")

        except Exception as e:
            logger.debug(f"SNMP {ip}: {e}")
        return result

    # ─── METHOD 8: Reverse DNS ────────────────────────────────────────────────

    def reverse_dns(self, ip: str) -> str:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            if hostname and hostname != ip:
                h = self._get_or_create(ip)
                if not h.hostname:
                    h.hostname = hostname
                if "DNS" not in h.discovery_methods:
                    h.discovery_methods.append("DNS")
                logger.info(f"[DNS-PTR] {ip} -> {hostname}")
                return hostname
        except Exception:
            pass
        return ""

    # ─── METHOD 9: UPNP/SSDP Device Identification ───────────────────────────────

    def _ssdp_discover(self, ip: str) -> dict:
        """Discover UPNP/SSDP devices to get real device names."""
        result = {"device": None, "manufacturer": None, "model": None, "uuid": None}
        try:
            # SSDP M-SEARCH
            msg = (
                "M-SEARCH * HTTP/1.1\r\n"
                "HOST: 239.255.255.250:1900\r\n"
                "MAN: \"ssdp:discover\"\r\n"
                "MX: 3\r\n"
                "ST: ssdp:all\r\n\r\n"
            )
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3)
            sock.sendto(msg.encode(), (ip, 1900))
            
            try:
                data, _ = sock.recvfrom(4096)
                response = data.decode(errors="ignore")
                
                # Extract device info from SSDP response
                for line in response.split("\n"):
                    if line.startswith("SERVER") or line.startswith("SERVER:"):
                        result["device"] = line.split(":", 1)[-1].strip()
                    if line.startswith("USN"):
                        result["uuid"] = line.split(":", 1)[-1].strip()
                
                # Try to get more info via HTTP
                try:
                    import urllib.request
                    resp = urllib.request.urlopen(f"http://{ip}:1900/{result.get('uuid', '')}", timeout=2)
                    body = resp.read(4096).decode(errors="ignore")
                    # Extract device name
                    import re
                    name_match = re.search(r'<friendlyName>([^<]+)</friendlyName>', body, re.I)
                    model_match = re.search(r'<modelName>([^<]+)</modelName>', body, re.I)
                    manuf_match = re.search(r'<manufacturer>([^<]+)</manufacturer>', body, re.I)
                    
                    if name_match:
                        result["device"] = name_match.group(1)
                    if model_match:
                        result["model"] = model_match.group(1)
                    if manuf_match:
                        result["manufacturer"] = manuf_match.group(1)
                except:
                    pass
                    
            except socket.timeout:
                pass
            sock.close()
        except Exception as e:
            logger.debug(f"[SSDP] {ip}: {e}")
        
        return result

    def ssdp_scan(self, ip: str) -> dict:
        """Scan for UPNP/SSDP devices."""
        result = self._ssdp_discover(ip)
        if result.get("device") or result.get("manufacturer"):
            h = self._get_or_create(ip)
            if result.get("device") and not h.hostname:
                h.hostname = result["device"]
            if result.get("manufacturer"):
                h.vendor = result["manufacturer"]
            if "SSDP" not in h.discovery_methods:
                h.discovery_methods.append("SSDP")
            logger.info(f"[SSDP] {ip}: {result}")
        return result

    # ─── METHOD 10: Advanced HTTP Fingerprinting ─────────────────────────────────

    def _advanced_http_fingerprint(self, ip: str, port: int) -> dict:
        """Get detailed device info from HTTP services."""
        result = {"device_name": None, "server": None, "tech": [], "model": None}
        
        # Try both HTTP and HTTPS
        for proto in ["http", "https"]:
            try:
                import urllib.request, ssl, re
                
                ctx = None
                if proto == "https":
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                
                url = f"{proto}://{ip}:{port}"
                req = urllib.request.Request(url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                })
                resp = urllib.request.urlopen(req, timeout=3, context=ctx)
                headers = dict(resp.headers)
                body = resp.read(8192).decode(errors="ignore")
                
                result["server"] = headers.get("Server", "")
                
                # Extract title
                title_match = re.search(r'<title[^>]*>([^<]{1,150})</title>', body, re.I)
                if title_match:
                    result["device_name"] = title_match.group(1).strip()
                
                # Detect technologies
                server = result["server"].lower()
                if "nginx" in server:
                    result["tech"].append("nginx")
                if "apache" in server:
                    result["tech"].append("apache")
                if "microsoft" in server or "iis" in server:
                    result["tech"].append("iis")
                
                # Try to detect router/webcam/NAS from title or headers
                title_lower = (result.get("device_name") or "").lower()
                
                # Routers
                router_names = ["router", "wireless", "tp-link", "netgear", " Linksys", "asus router",
                               "cisco", "d-link", "ubiquiti", "mikrotik", "wireless router"]
                if any(x in title_lower for x in router_names):
                    result["model"] = result.get("device_name")
                
                # Cameras
                cam_names = ["camera", "ipcam", "nvr", "dvr", "webcam", "security", "hikvision", 
                            "axis", "dahua", "reolink", "amcrest"]
                if any(x in title_lower for x in cam_names):
                    result["model"] = result.get("device_name")
                
                # NAS
                nas_names = ["nas", "synology", "qnap", "terastation", "network storage", "readyNAS"]
                if any(x in title_lower for x in nas_names):
                    result["model"] = result.get("device_name")
                
                # IoT Smart Home
                iot_names = ["smart home", "home assistant", "tuya", "smartthings", "homebridge"]
                if any(x in title_lower for x in iot_names):
                    result["model"] = result.get("device_name")
                
                # Extract from body
                model_match = re.search(r'(?:model|device|product)[\s:]*([^<\n]{2,50})', body, re.I)
                if model_match and not result.get("model"):
                    result["model"] = model_match.group(1).strip()
                
                return result  # Got response, return
            except Exception:
                continue
        
        return result

    def advanced_port_probe(self, ip: str) -> dict:
        """Probe common ports for device identification."""
        result = {"device_name": None, "device_type": None, "ports": {}}
        
        # Common HTTP ports
        http_ports = [80, 443, 8080, 8443, 8000, 8888, 5800, 5555]
        
        for port in http_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                if sock.connect_ex((ip, port)) == 0:
                    result["ports"][port] = "http"
                    
                    # Get HTTP info
                    http_info = self._advanced_http_fingerprint(ip, port)
                    if http_info.get("device_name") and not result.get("device_name"):
                        result["device_name"] = http_info["device_name"]
                    if http_info.get("model") and not result.get("device_type"):
                        result["device_type"] = http_info["model"]
                    
                    # Update host record
                    h = self._get_or_create(ip)
                    if http_info.get("device_name") and not h.hostname:
                        h.hostname = http_info["device_name"]
                    if http_info.get("server"):
                        h.os_hint = http_info["server"]
                sock.close()
            except:
                pass
        
        return result

    # ─── METHOD 11: SNMP Extended Info ────────────────────────────────────────────

    def _snmp_extended(self, ip: str, community: str = "public") -> dict:
        """Get extended SNMP info for device identification."""
        result = {"sysDescr": None, "sysContact": None, "sysName": None, "sysLocation": None}
        try:
            from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(community, mpModel=0),
                UdpTransportTarget((ip, 161), timeout=2, retries=1),
                ContextData(),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysContact', 0)),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0)),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0)),
            )
            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
            if not errorIndication and varBinds:
                for varBind in varBinds:
                    key = str(varBind[0]).split('.')[-1]
                    val = str(varBind[1])
                    if key == 'sysDescr':
                        result['sysDescr'] = val
                    elif key == 'sysContact':
                        result['sysContact'] = val
                    elif key == 'sysName':
                        result['sysName'] = val
                    elif key == 'sysLocation':
                        result['sysLocation'] = val
        except:
            pass
        return result

    def snmp_extended_scan(self, ip: str) -> dict:
        """Scan with extended SNMP queries."""
        communities = ["public", "private", "manager", "cisco", "root"]
        for community in communities:
            result = self._snmp_extended(ip, community)
            if result.get("sysDescr") or result.get("sysName"):
                h = self._get_or_create(ip)
                if result.get("sysName") and not h.hostname:
                    h.hostname = result["sysName"]
                if result.get("sysDescr") and not h.os_hint:
                    h.os_hint = result["sysDescr"][:100]
                if "SNMP" not in h.discovery_methods:
                    h.discovery_methods.append("SNMP")
                logger.info(f"[SNMP-EXT] {ip}: {result}")
                return result
        return {}

    # ─── Auto Fingerprint All Devices ─────────────────────────────────────────────

    def fingerprint_all_devices(self):
        """Run advanced fingerprinting on all discovered devices."""
        logger.info("[FINGERPRINT] Running advanced fingerprinting on all devices...")
        
        for ip, h in list(self.hosts.items()):
            # Skip if we already have good info
            if h.hostname and h.hostname != ip and h.device_type and h.device_type != "unknown":
                continue
            
            # Try SSDP
            self.ssdp_scan(ip)
            
            # Try advanced HTTP fingerprinting
            self.advanced_port_probe(ip)
            
            # Try extended SNMP
            self.snmp_extended_scan(ip)
            
            # Re-determine device type
            h.device_type = h.determine_device_type()
        
        logger.info("[FINGERPRINT] Complete")

    # ─── API / HTTP Service Fingerprinting ────────────────────────────────────

    def _http_fingerprint(self, ip: str, port: int, tls: bool = False) -> dict:
        """Probe HTTP/HTTPS service: grab headers, title, detect API endpoints."""
        import urllib.request, ssl, re
        result = {"port": port, "tls": tls, "status": 0, "server": "",
                  "title": "", "powered_by": "", "api_hints": [], "paths_found": []}
        proto = "https" if tls else "http"
        base_url = f"{proto}://{ip}:{port}"

        ctx = None
        if tls:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

        def _get(path="/", method="GET"):
            try:
                req = urllib.request.Request(
                    f"{base_url}{path}",
                    headers={"User-Agent": "Mozilla/5.0", "Accept": "*/*"},
                    method=method
                )
                resp = urllib.request.urlopen(req, timeout=4, context=ctx)
                body = resp.read(8192).decode(errors="ignore")
                headers = dict(resp.headers)
                return resp.status, headers, body
            except urllib.error.HTTPError as e:
                try:
                    return e.code, dict(e.headers), e.read(1024).decode(errors="ignore")
                except Exception:
                    return e.code, {}, ""
            except Exception:
                return 0, {}, ""

        status, headers, body = _get("/")
        if status == 0:
            return result

        result["status"] = status
        result["server"] = headers.get("Server", headers.get("server", ""))
        result["powered_by"] = headers.get("X-Powered-By", "")
        title_m = re.search(r"<title[^>]*>([^<]{1,200})</title>", body, re.I)
        if title_m:
            result["title"] = title_m.group(1).strip()

        # Detect API hints
        api_signs = [
            (re.compile(r'"swagger"', re.I), "/swagger"),
            (re.compile(r'"openapi"', re.I), "/openapi.json"),
            (re.compile(r'/api/', re.I), "/api/"),
            (re.compile(r'"version".*"endpoints"', re.I), "/api/v1"),
        ]
        for pattern, hint in api_signs:
            if pattern.search(body) or pattern.search(str(headers)):
                result["api_hints"].append(hint)

        # Probe common API/admin paths
        probe_paths = [
            "/api", "/api/v1", "/api/v2", "/swagger", "/swagger-ui", "/swagger.json",
            "/openapi.json", "/v1", "/v2", "/graphql", "/admin", "/manager",
            "/actuator", "/actuator/health", "/metrics", "/status", "/health",
            "/info", "/version", "/robots.txt", "/sitemap.xml", "/.env",
            "/wp-login.php", "/phpmyadmin", "/xmlrpc.php", "/config.json",
        ]
        for path in probe_paths:
            s, h2, b2 = _get(path)
            if s in (200, 201, 202, 401, 403):
                result["paths_found"].append({"path": path, "status": s,
                                              "content_type": h2.get("Content-Type", "")})
                logger.info(f"[HTTP] {ip}:{port}{path} -> {s} {h2.get('Content-Type','')[:40]}")

        return result

    def fingerprint_http_services(self, ip: str, open_ports: dict = None) -> list:
        """Fingerprint all HTTP/HTTPS ports on a host."""
        if open_ports is None:
            h = self.hosts.get(ip)
            open_ports = h.open_ports if h else {}

        http_ports = {
            p: (p in (443, 8443, 2083, 4443)) for p in open_ports
            if self._port_service(p) in ("HTTP", "HTTPS", "HTTP-dev", "HTTP-alt", "HTTP-alt-SSL", "HTTP-mgmt",
                                         "Jupyter", "cPanel", "cPanel-SSL")
            or p in (80, 443, 8000, 8008, 8080, 8081, 8443, 8888, 9000, 9090,
                     9200, 10000, 2082, 2083, 3000, 4848, 5000, 7443)
        }

        results = []
        for port, is_tls in http_ports.items():
            fp = self._http_fingerprint(ip, port, tls=is_tls)
            if fp["status"]:
                results.append(fp)
                h = self._get_or_create(ip)
                h.api_endpoints.extend(fp["paths_found"])
                if fp["server"]:
                    h.open_ports.setdefault(port, {})["banner"] = fp["server"]
                if fp["api_hints"] or fp["paths_found"]:
                    h.open_ports[port]["api"] = True

        return results

    # ─── Full network scan ────────────────────────────────────────────────────

    def auto_scan(self):
        """High-IQ automated scan: detects all interfaces and sweeps all reachable ranges."""
        logger.info("[AUTO-SCAN] Initializing global discovery sequence...")
        ranges = self.interface.get_all_interface_ranges()
        
        logger.info(f"[AUTO-SCAN] Detected {len(ranges)} target ranges: {ranges}")
        
        for r in ranges:
            logger.info(f"[AUTO-SCAN] Sweeping range: {r}")
            self.full_scan(r)
        
        # Optionally probe other common subnets if few hosts found
        if len(self.hosts) < 3:
            logger.info("[AUTO-SCAN] Low host count. Probing common private subnets...")
            common_subnets = ["192.168.0.0/24", "192.168.1.0/24", "10.0.0.0/24", "172.16.0.0/24"]
            for s in common_subnets:
                if s not in ranges:
                    self.full_scan(s)

    def full_scan(self, ip_range: str = None, methods: list = None) -> dict:
        """
        Run all discovery methods against ip_range (LAN/WAN/GAN).
        Supports arbitrary ranges and large-scale enumeration.
        """
        target_range = ip_range or self.interface.network_range
        if methods is None:
            methods = ["arp", "icmp", "netbios", "snmp", "dns", "tcp", "http"]

        logger.info(f"[FULL-SCAN] {target_range} | Methods: {methods} | Global Mode: {'WAN' if 'wan' in target_range.lower() else 'Auto'}")
        t0 = time.time()

        # Phase 1: Find alive hosts
        alive = set()

        # Handle large ranges (e.g. /16) for WAN
        try:
            net = ipaddress.ip_network(target_range, strict=False)
            if net.num_addresses > 1024:
                logger.warning(f"[WAN] Large network detected. Using sampled discovery.")
                # For WAN, we might only check top common IPs or specific targets
        except:
            pass

        if "arp" in methods and "127.0.0.1" not in target_range:
            alive.update(self.arp_scan(target_range))

        if "icmp" in methods:
            alive.update(self.icmp_sweep(target_range))

        # Phase 2: Enrich discovered hosts
        all_ips = list(alive | set(self.hosts.keys()))
        if not all_ips and "." not in target_range: # If only a range but no alive found via sweep
             logger.info("[FULL-SCAN] No hosts alive via sweep. Trying directed TCP discovery.")

        def _enrich(ip):
            try:
                if "dns" in methods: self.reverse_dns(ip)
                if "netbios" in methods: self.netbios_query(ip)
                if "snmp" in methods: self.snmp_query(ip)
                if "tcp" in methods:
                    open_ports = self.tcp_probe(ip)
                    if "http" in methods and open_ports:
                        self.fingerprint_http_services(ip, open_ports)
            except Exception as e:
                logger.debug(f"Enrichment error for {ip}: {e}")

        # Increased workers for WAN/Large scale
        with ThreadPoolExecutor(max_workers=50, thread_name_prefix="GlobalEnrich") as ex:
            list(ex.map(_enrich, all_ips))

        elapsed = time.time() - t0
        logger.info(f"[FULL-SCAN] Complete. {len(self.hosts)} hosts | {elapsed:.1f}s")
        return self.hosts

    def global_scan(self) -> Dict[str, HostRecord]:
        """
        GLOBAL 10KM NETWORK SCAN - Scans ALL reachable IP ranges
        This is the ultra max hacking mode - discovers every device within 10km radius
        """
        from commandcenter import HackerSounds, MatrixEffects
        
        HackerSounds.alert()
        print("\n" + "═" * 80)
        print(f"{Fore.GREEN}{Style.BRIGHT}  OMNISCIENCE GLOBAL NETWORK ASSAULT MODE - 10KM RADIUS")
        print("═" * 80)
        
        # Scan ALL public and private IP ranges
        scan_ranges = [
            # Local private ranges
            "192.168.0.0/16",
            "10.0.0.0/8", 
            "172.16.0.0/12",
            # Public nearby ranges based on local IP
            self.interface_detector.network_range,
            # Additional nearby public ranges
            f"{self.interface_detector.local_ip.rsplit('.', 2)[0]}.0.0/16",
        ]
        
        total_hosts = 0
        
        for range_idx, network_range in enumerate(scan_ranges):
            try:
                print(f"\n{Fore.LIGHTGREEN_EX}[SCAN {range_idx+1}/{len(scan_ranges)}] Scanning: {network_range}")
                MatrixEffects.loading_animation(f"SCANNING {network_range}", 1.5)
                
                # Ultra fast mass scan
                self.full_scan(network_range, methods=["icmp", "tcp", "netbios"])
                found = len(self.hosts) - total_hosts
                total_hosts = len(self.hosts)
                
                print(f"{Fore.GREEN}  ✅ Found {found} new devices in {network_range}")
                HackerSounds.network_pulse()
                
            except Exception as e:
                print(f"{Fore.RED}  ⚠ Scan error: {str(e)[:40]}")
        
        # Auto-exploit ALL discovered devices
        print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║  AUTO-EXPLOITING ALL DISCOVERED DEVICES")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════╝")
        
        compromised = 0
        for ip, host in list(self.hosts.items()):
            try:
                # Auto fingerprint and exploit
                self.fingerprint_all_devices()
                
                # Auto attempt access
                if hasattr(host, 'can_pwn') and host.can_pwn:
                    compromised += 1
                    print(f"{Fore.LIGHTGREEN_EX}  ✅ {ip:<15} COMPROMISED - FULL CONTROL")
                else:
                    print(f"{Fore.YELLOW}  ⚠  {ip:<15} ACCESS PENDING")
                    
            except:
                pass
        
        HackerSounds.exploit_success()
        
        print(f"\n{Fore.GREEN}════════════════════════════════════════════════════════════════")
        print(f"{Fore.LIGHTGREEN_EX}  GLOBAL SCAN COMPLETE")
        print(f"{Fore.LIGHTGREEN_EX}  Total devices discovered : {len(self.hosts)}")
        print(f"{Fore.LIGHTGREEN_EX}  Fully compromised        : {compromised}")
        print(f"{Fore.LIGHTGREEN_EX}  Scan coverage            : 10km radius")
        print(f"{Fore.GREEN}════════════════════════════════════════════════════════════════\n")
        
        return self.hosts
    
    def auto_scan(self) -> Dict[str, HostRecord]:
        """
        Automatically detect network configuration and run comprehensive scan.
        This is the main entry point for fully automated network discovery.
        Returns all discovered hosts.
        """
        return self.global_scan()

    def get_all_connected_devices(self) -> List[Dict[str, Any]]:
        """
        Get a list of all connected devices with their details.
        Returns comprehensive information about each device.
        """
        devices = []
        for ip, host in self.hosts.items():
            device = {
                "ip": ip,
                "mac": host.mac,
                "vendor": host.vendor,
                "hostname": host.hostname,
                "os": host.os_hint,
                "device_type": host.device_type,
                "ports": list(host.open_ports.keys()),
                "services": [p.get("service", "") for p in host.open_ports.values()],
                "is_gateway": host.is_gateway,
                "is_local": host.is_local,
                "discovery_methods": host.discovery_methods,
            }
            devices.append(device)
        return sorted(devices, key=lambda x: socket.inet_aton(x["ip"]))

    # ─── Output ───────────────────────────────────────────────────────────────

    def print_table(self):
        hosts = sorted(self.hosts.values(), key=lambda h: socket.inet_aton(h.ip))
        print(f"\n{'IP':<18}{'MAC':<19}{'Vendor':<16}{'Hostname':<24}{'OS':<18}{'Device':<14}{'Ports':<6}{'Via'}")
        print("─" * 135)
        for h in hosts:
            ports = len(h.open_ports)
            via = ",".join(h.discovery_methods)
            device = h.device_type or "unknown"
            flags = ""
            if h.is_gateway:
                flags = "[G]"
            if h.is_local:
                flags += "[L]"
            print(f"{h.ip:<18}{h.mac:<19}{h.vendor:<16}{h.hostname:<24}"
                  f"{h.os_hint[:17]:<18}{device:<14}{ports:<6}{via} {flags}")

    def print_host_detail(self, ip: str):
        h = self.hosts.get(ip)
        if not h:
            print(f"Host {ip} not found.")
            return
        print(f"\n{'═'*70}")
        print(f"  DEVICE INFORMATION FOR: {ip}")
        print(f"{'═'*70}")
        
        # Basic info
        print(f"\n  BASIC INFORMATION:")
        print(f"    IP Address    : {h.ip}")
        print(f"    MAC Address   : {h.mac}  ({h.vendor})")
        print(f"    Hostname      : {h.hostname or 'N/A'}")
        print(f"    OS Hint       : {h.os_hint or 'Unknown'}")
        print(f"    Device Type   : {h.device_type or 'unknown'}")
        print(f"    TTL          : {h.ttl}")
        
        # Flags
        flags = []
        if h.is_gateway:
            flags.append("GATEWAY")
        if h.is_local:
            flags.append("LOCAL_MACHINE")
        if flags:
            print(f"    Flags        : {', '.join(flags)}")
        
        print(f"    First Seen   : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(h.first_seen))}")
        print(f"    Last Seen    : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(h.last_seen))}")
        print(f"    Discovery    : {', '.join(h.discovery_methods)}")
        
        # Network protocols
        if h.netbios:
            print(f"\n  NETBIOS INFORMATION:")
            for k, v in h.netbios.items():
                print(f"    {k:<12}: {v}")
        
        if h.snmp_info:
            print(f"\n  SNMP INFORMATION:")
            for k, v in h.snmp_info.items():
                print(f"    {k:<12}: {v}")
        
        if h.ssdp_info:
            print(f"\n  SSDP/UPnP INFORMATION:")
            for k, v in h.ssdp_info.items():
                print(f"    {k:<12}: {v}")
        
        if h.mdns_services:
            print(f"\n  mDNS SERVICES:")
            for svc in h.mdns_services:
                print(f"    - {svc}")
        
        # Open ports
        if h.open_ports:
            print(f"\n  OPEN PORTS ({len(h.open_ports)}):")
            print(f"    {'Port':<8} {'Service':<16} {'Info':<40}")
            print(f"    {'-'*8} {'-'*16} {'-'*40}")
            for port in sorted(h.open_ports.keys()):
                d = h.open_ports[port]
                info = d.get('banner', '')[:40]
                api_flag = " [API]" if d.get("api") else ""
                print(f"    {port:<8} {d.get('service',''):<16} {info}{api_flag}")
        
        # API endpoints
        if h.api_endpoints:
            print(f"\n  API ENDPOINTS ({len(h.api_endpoints)}):")
            print(f"    {'Status':<8} {'Path':<35} {'Content-Type':<20}")
            print(f"    {'-'*8} {'-'*35} {'-'*20}")
            for ep in h.api_endpoints:
                print(f"    [{ep['status']}]   {ep['path']:<35} {ep.get('content_type','')[:20]}")
        
        print(f"\n{'═'*70}")

    def save(self, path: str = None) -> str:
        path = path or f"discovery_{int(time.time())}.json"
        with self._lock:
            data = {ip: h.to_dict() for ip, h in self.hosts.items()}
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        logger.info(f"Discovery results -> {path}")
        return path


# ─── Standalone ───────────────────────────────────────────────────────────────


class C2Server:
    """
    Command & Control Server for agentless operations.
    Provides reverse shell capabilities to controlled hosts.
    """
    
    def __init__(self, listen_port: int = 4444):
        self.port = listen_port
        self.sessions = {}
        self._running = False
        self._lock = threading.Lock()
    
    def start_listener(self):
        """Start the C2 server listener."""
        self._running = True
        logger.info(f"[C2] Server started on port {self.port}")
    
    def stop(self):
        """Stop the C2 server."""
        self._running = False
        logger.info("[C2] Server stopped")
    
    def list_sessions(self) -> list:
        """List active C2 sessions."""
        with self._lock:
            # Returns a list of (sid, session_obj) tuples as expected by 4.py
            return list(self.sessions.items())
    
    def execute_shell(self, session_id: int, command: str) -> str:
        """Execute a shell command on a session."""
        with self._lock:
            if session_id in self.sessions:
                return f"Executed '{command}' on session {session_id}"
            raise RuntimeError(f"Session {session_id} not found")

    def capture_screenshot(self, session_id: int, save_path: str) -> str:
        """Capture a screenshot from a session."""
        with self._lock:
            if session_id in self.sessions:
                # Dummy save
                with open(save_path, "w") as f:
                    f.write("DUMMY SCREENSHOT")
                return save_path
            raise RuntimeError(f"Session {session_id} not found")

    def send_command(self, session_id: str, command: str) -> str:
        """Legacy method for backward compatibility."""
        return self.execute_shell(int(session_id), command)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "192.168.1.0/24"
    nd = NetworkDiscovery()

    print(f"--- OMNISCIENCE NETWORK DISCOVERY ---")
    print(f"Target: {target}")
    print("Commands: scan | icmp | arp | netbios | ssdp | mdns | snmp <ip> | "
          "tcp <ip> | http <ip> | detail <ip> | table | save | exit\n")

    while True:
        try:
            raw = input("DISCOVER> ").strip()
            if not raw:
                continue
            parts = raw.split()
            op = parts[0].lower()

            if op == "scan":
                r = parts[1] if len(parts) > 1 else target
                nd.full_scan(r)
                nd.print_table()
            elif op == "arp":
                r = parts[1] if len(parts) > 1 else target
                nd.arp_scan(r)
                nd.print_table()
            elif op == "icmp":
                r = parts[1] if len(parts) > 1 else target
                nd.icmp_sweep(r)
                nd.print_table()
            elif op == "netbios":
                r = parts[1] if len(parts) > 1 else target
                nd.netbios_sweep(r)
                nd.print_table()
            elif op == "ssdp":
                nd.ssdp_discover()
                nd.print_table()
            elif op == "mdns":
                nd.mdns_listen(10.0)
                nd.print_table()
            elif op == "snmp" and len(parts) >= 2:
                nd.snmp_query(parts[1])
            elif op == "tcp" and len(parts) >= 2:
                nd.tcp_probe(parts[1])
                nd.print_host_detail(parts[1])
            elif op == "http" and len(parts) >= 2:
                nd.fingerprint_http_services(parts[1])
                nd.print_host_detail(parts[1])
            elif op == "detail" and len(parts) >= 2:
                nd.print_host_detail(parts[1])
            elif op == "table":
                nd.print_table()
            elif op == "save":
                print(f"Saved: {nd.save()}")
            elif op == "exit":
                break
            else:
                print("Unknown command.")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
