from colorama import Fore, Back, Style, init
init(autoreset=True)
"""
OMNISCIENCE MODULE 5 — AdvancedNetworkScanner
Multi-dimensional network discovery across LAN, WAN, GAN, MAN, and PAN.
Cross-subnet enumeration, traceroute intelligence, network topology mapping,
BGP/AS enumeration, VPN detection, and internet-wide scanning capabilities.

Advanced Features:
  - Cross-subnet discovery through multiple vectors
  - Traceroute with service fingerprinting at each hop
  - Network topology reconstruction via multiple methods
  - Public IP range scanning (cloud providers, datacenters)
  - BGP autonomous system enumeration
  - VPN tunnel detection and analysis
  - Multi-homed device detection
  - NAT traversal identification
  - ISP fingerprinting and geolocation
  - Network path analysis and latency mapping
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
import urllib.request
import urllib.parse
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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | AdvScanner | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("advscan.log", mode="a"),
    ]
)
logger = logging.getLogger("Omniscience.AdvScanner")

# Geographic IP ranges for major cloud providers and datacenters
CLOUD_RANGES = {
    "aws": ["3.0.0.0/8", "4.0.0.0/9", "15.0.0.0/9", "16.0.0.0/9", "18.0.0.0/8"],
    "azure": ["13.64.0.0/11", "20.0.0.0/8", "40.0.0.0/8", "52.0.0.0/8"],
    "gcp": ["34.64.0.0/10", "35.192.0.0/11", "104.16.0.0/12", "108.177.0.0/14"],
    "digitalocean": ["64.0.0.0/8", "104.0.0.0/9", "108.0.0.0/9"],
    "linode": ["50.0.0.0/8", "172.0.0.0/8", "192.0.0.0/8"],
    "oracle": ["140.0.0.0/8", "143.0.0.0/8", "129.0.0.0/8"],
    "alibaba": ["42.0.0.0/8", "47.0.0.0/8", "106.0.0.0/8"],
    "ibm": ["169.0.0.0/9", "172.0.0.0/9", "32.0.0.0/9"],
}

# Common VPN detection ports
VPN_PORTS = [500, 4500, 1701, 443, 8443, 1194, 1723, 8080]

# Traceroute timeouts per hop
TRACEROUTE_TIMEOUT = 3


class TracerouteHop:
    """Represents a single traceroute hop."""
    def __init__(self, hop_num: int, ip: str = None, hostname: str = None, 
                 rtt: float = None, asn: str = None, location: str = None):
        self.hop_num = hop_num
        self.ip = ip
        self.hostname = hostname
        self.rtt = rtt
        self.asn = asn
        self.location = location
        self.services = []  # Detected services at this hop
        self.is_private = False
        self.is_router = False
        self.is_firewall = False
        self.is_load_balancer = False
        
    def to_dict(self) -> dict:
        return {
            "hop": self.hop_num,
            "ip": self.ip,
            "hostname": self.hostname,
            "rtt_ms": self.rtt,
            "asn": self.asn,
            "location": self.location,
            "services": self.services,
            "is_private": self.is_private,
            "is_router": self.is_router,
            "is_firewall": self.is_firewall,
            "is_lb": self.is_load_balancer,
        }


class NetworkDevice:
    """Extended network device with cross-network information."""
    def __init__(self, ip: str):
        self.ip = ip
        self.mac = ""
        self.hostname = ""
        self.reverse_dns = ""
        self.asn = ""
        self.isp = ""
        self.location = {"city": "", "country": "", "lat": 0.0, "lon": 0.0}
        self.netmask = ""
        self.broadcast = ""
        self.network_type = "unknown"  # lan, wan, gan, man, vpn
        self.first_hop = 0
        self.last_hop = 0
        self.traceroute_path = []
        self.open_ports = {}
        self.services = []
        self.device_type = "unknown"
        self.is_honeypot = False
        self.is_vpn_gateway = False
        self.is_nat_device = False
        self.is_proxy = False
        self.tags = []
        self.last_seen = time.time()
        
    def to_dict(self) -> dict:
        return {
            "ip": self.ip,
            "mac": self.mac,
            "hostname": self.hostname,
            "reverse_dns": self.reverse_dns,
            "asn": self.asn,
            "isp": self.isp,
            "location": self.location,
            "network_type": self.network_type,
            "traceroute_path": [h.to_dict() for h in self.traceroute_path],
            "open_ports": self.open_ports,
            "services": self.services,
            "device_type": self.device_type,
            "is_honeypot": self.is_honeypot,
            "is_vpn_gateway": self.is_vpn_gateway,
            "is_nat": self.is_nat_device,
            "is_proxy": self.is_proxy,
            "tags": self.tags,
        }


class AdvancedNetworkScanner:
    """
    Advanced multi-dimensional network scanner.
    Discovers devices across LAN, WAN, GAN, MAN, PAN and VPN networks.
    """
    
    def __init__(self):
        self.hosts: Dict[str, NetworkDevice] = {}
        self._lock = threading.Lock()
        self._scanning = False
        self._cancel_event = threading.Event()
        
        # Local network detection
        self.local_ip = self._get_local_ip()
        self.gateway = self._detect_gateway()
        self.network_range = self._detect_network_range()
        
    def _get_local_ip(self) -> str:
        """Get local IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def _detect_gateway(self) -> str:
        """Detect gateway IP."""
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
            else:
                result = subprocess.run(["ip", "route"], capture_output=True, text=True, timeout=5)
                for line in result.stdout.splitlines():
                    if "default" in line:
                        parts = line.split()
                        for i, p in enumerate(parts):
                            if p == "default" and i + 1 < len(parts):
                                return parts[i + 1]
        except:
            pass
        
        # Fallback
        parts = self.local_ip.split(".")
        return f"{parts[0]}.{parts[1]}.{parts[2]}.1"
    
    def _detect_network_range(self) -> str:
        """Detect local network range."""
        parts = self.local_ip.split(".")
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
        return "192.168.1.0/24"
    
    def _is_private_ip(self, ip: str) -> bool:
        """Check if IP is private."""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return (ipaddress.ip_address(ip_obj) in ipaddress.ip_network("10.0.0.0/8") or
                    ipaddress.ip_address(ip_obj) in ipaddress.ip_network("172.16.0.0/12") or
                    ipaddress.ip_address(ip_obj) in ipaddress.ip_network("192.168.0.0/16") or
                    ipaddress.ip_address(ip_obj) in ipaddress.ip_network("127.0.0.0/8"))
        except:
            return False
    
    def _get_asn_info(self, ip: str) -> Dict[str, str]:
        """Get ASN information for an IP using Team Cymru DNS-based lookup."""
        result = {"asn": "", "isp": "", "org": ""}
        if self._is_private_ip(ip):
            return result
            
        import socket
        try:
            # Use high-performance socket-based WHOIS for BGP intelligence
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect(("whois.cymru.com", 43))
            s.send(f" -v {ip}\n".encode())
            response = b""
            while True:
                data = s.recv(4096)
                if not data: break
                response += data
            s.close()
            
            # Parse structured WHOIS response for AS and ISP data
            lines = response.decode().splitlines()
            for line in lines:
                if "|" in line and ip in line:
                    parts = line.split("|")
                    if len(parts) >= 3:
                        result["asn"] = f"AS{parts[0].strip()}"
                        result["isp"] = parts[2].strip()
                        result["org"] = parts[2].strip()
                    break
        except Exception as e:
            logger.debug(f"ASN lookup failed for {ip}: {e}")
        
        return result
    
    def _geo_locate_ip(self, ip: str) -> Dict[str, Any]:
        """Get geolocation info for an IP."""
        location = {"city": "Unknown", "country": "Unknown", "lat": 0.0, "lon": 0.0}
        
        if self._is_private_ip(ip):
            return location
        
        try:
            # Use ip-api.com (free tier)
            url = f"http://ip-api.com/json/{ip}?fields=status,country,city,lat,lon,isp,org,as"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                if data.get("status") == "success":
                    location = {
                        "city": data.get("city", "Unknown"),
                        "country": data.get("country", "Unknown"),
                        "lat": data.get("lat", 0.0),
                        "lon": data.get("lon", 0.0),
                        "isp": data.get("isp", ""),
                        "org": data.get("org", ""),
                        "as": data.get("as", ""),
                    }
        except Exception as e:
            logger.debug(f"Geo lookup {ip}: {e}")
        
        return location
    
    def traceroute(self, target: str, max_hops: int = 30) -> List[TracerouteHop]:
        """Perform traceroute with service detection."""
        logger.info(f"[TRACEROUTE] Tracing path to {target}")
        hops = []
        
        if not SCAPY_OK:
            # Fallback to system traceroute
            try:
                result = subprocess.run(
                    ["tracert", "-d", "-w", "1000", "-h", str(max_hops), target],
                    capture_output=True, text=True, timeout=60
                )
                for line in result.stdout.splitlines():
                    match = re.match(r'\s*(\d+)\s+(\S+)\s+(\S+)', line)
                    if match:
                        hop_num = int(match.group(1))
                        ip = match.group(2) if match.group(2) != "*" else None
                        rtt_str = match.group(3).replace("ms", "").strip()
                        try:
                            rtt = float(rtt_str) if rtt_str != "*" else None
                        except:
                            rtt = None
                        hop = TracerouteHop(hop_num, ip, rtt=rtt)
                        if ip:
                            hop.is_private = self._is_private_ip(ip)
                            # Try to get hostname
                            try:
                                hop.hostname = socket.gethostbyaddr(ip)[0]
                            except:
                                pass
                        hops.append(hop)
            except Exception as e:
                logger.error(f"Traceroute failed: {e}")
            return hops
        
        # Scapy-based traceroute
        for ttl in range(1, max_hops + 1):
            if self._cancel_event.is_set():
                break
                
            pkt = scapy.IP(dst=target, ttl=ttl) / scapy.ICMP()
            try:
                reply = scapy.sr1(pkt, timeout=TRACEROUTE_TIMEOUT, verbose=False)
                
                if reply:
                    hop = TracerouteHop(ttl, ip=reply.src, rtt=reply.time * 1000)
                    hop.is_private = self._is_private_ip(reply.src)
                    
                    # Try hostname resolution
                    try:
                        hop.hostname = socket.gethostbyaddr(reply.src)[0]
                    except:
                        pass
                    
                    # Get ASN info for public IPs
                    if not hop.is_private:
                        asn_info = self._get_asn_info(reply.src)
                        hop.asn = asn_info.get("asn", "")
                    
                    # Check if this looks like a router/firewall
                    if hop.rtt and hop.rtt > 0:
                        hop.is_router = True
                    
                    hops.append(hop)
                    
                    # Check if we reached the target
                    if reply.src == target:
                        logger.info(f"[TRACEROUTE] Reached target at hop {ttl}")
                        break
                        
            except Exception as e:
                logger.debug(f"Hop {ttl}: {e}")
                hops.append(TracerouteHop(ttl))
        
        logger.info(f"[TRACEROUTE] Complete: {len(hops)} hops")
        return hops
    
    def traceroute_with_services(self, target: str, max_hops: int = 30) -> List[TracerouteHop]:
        """Traceroute with service detection at each hop."""
        hops = self.traceroute(target, max_hops)
        
        # For each hop, try to detect services
        for hop in hops:
            if hop.ip and not hop.is_private:
                # Quick port scan to detect services
                services = self._quick_service_scan(hop.ip)
                hop.services = services
                
                # Identify device type based on services
                if 22 in services:
                    hop.is_router = True
                if 80 in services or 443 in services:
                    hop.is_load_balancer = True
                if 500 in services or 4500 in services:
                    hop.is_firewall = True
        
        return hops
    
    def _quick_service_scan(self, ip: str) -> List[int]:
        """Quick scan for common services."""
        common = [22, 23, 80, 443, 445, 3389, 500, 4500, 1701, 1194, 1723]
        open_ports = []
        
        for port in common:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                sock.close()
                if result == 0:
                    open_ports.append(port)
            except:
                pass
        
        return open_ports
    
    def scan_cross_subnet(self, source_ip: str, target_subnet: str) -> List[str]:
        """Scan devices in a different subnet from source IP."""
        logger.info(f"[CROSS-SUBNET] Scanning {target_subnet} from {source_ip}")
        found = []
        
        try:
            network = ipaddress.ip_network(target_subnet, strict=False)
            ips = [str(h) for h in network.hosts()][:256]  # Limit to 256 for performance
            
            def check_host(ip):
                # Try to reach via specific source
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.bind((source_ip, 0))
                    sock.connect((ip, 445))  # Try SMB port
                    sock.close()
                    return ip
                except:
                    pass
                # Try ICMP
                try:
                    pkt = scapy.IP(src=source_ip, dst=ip) / scapy.ICMP()
                    reply = scapy.sr1(pkt, timeout=1, verbose=False)
                    if reply:
                        return ip
                except:
                    pass
                return None
            
            with ThreadPoolExecutor(max_workers=50) as ex:
                futures = {ex.submit(check_host, ip): ip for ip in ips}
                for fut in as_completed(futures):
                    result = fut.result()
                    if result:
                        found.append(result)
                        logger.info(f"[CROSS-SUBNET] Found: {result}")
                        
        except Exception as e:
            logger.error(f"Cross-subnet scan error: {e}")
        
        return found
    
    def discover_vpn_networks(self, target_ip: str = None) -> List[Dict[str, Any]]:
        """Detect VPN connections and gateways."""
        logger.info("[VPN] Scanning for VPN networks")
        vpn_info = []
        
        if not target_ip:
            target_ip = self.gateway
        
        # Check common VPN ports
        vpn_ports = {
            500: "IPSec",
            4500: "IPSec NAT-T",
            1701: "L2TP",
            1723: "PPTP",
            1194: "OpenVPN",
            443: "OpenVPN/SSL-VPN",
            8443: "OpenVPN",
            8080: "HTTP-VPN",
        }
        
        for port, vpn_type in vpn_ports.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target_ip, port))
                sock.close()
                if result == 0:
                    vpn_info.append({
                        "ip": target_ip,
                        "port": port,
                        "type": vpn_type,
                        "detected_at": time.time()
                    })
                    logger.info(f"[VPN] {target_ip}:{port} - {vpn_type}")
            except:
                pass
        
        return vpn_info
    
    def scan_public_ranges(self, provider: str = "aws", max_hosts: int = 100) -> List[NetworkDevice]:
        """Scan public IP ranges (cloud providers)."""
        logger.info(f"[PUBLIC-SCAN] Scanning {provider} ranges")
        found = []
        
        ranges = CLOUD_RANGES.get(provider.lower(), [])
        if not ranges:
            logger.warning(f"Unknown provider: {provider}")
            return found
        
        for cidr in ranges[:2]:  # Limit to first 2 ranges
            try:
                network = ipaddress.ip_network(cidr, strict=False)
                ips = [str(h) for h in network.hosts()][:max_hosts]
                
                def check_public(ip):
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        # Try common web ports
                        for port in [80, 443, 22, 3389]:
                            result = sock.connect_ex((ip, port))
                            sock.close()
                            if result == 0:
                                device = NetworkDevice(ip)
                                device.network_type = "cloud"
                                device.services = [port]
                                location = self._geo_locate_ip(ip)
                                device.location = location
                                device.isp = location.get("isp", provider)
                                return device
                    except:
                        pass
                    return None
                
                with ThreadPoolExecutor(max_workers=30) as ex:
                    futures = {ex.submit(check_public, ip): ip for ip in ips}
                    for fut in as_completed(futures):
                        device = fut.result()
                        if device:
                            found.append(device)
                            self.hosts[device.ip] = device
                            logger.info(f"[PUBLIC-SCAN] Found: {device.ip} ({device.services})")
                            
            except Exception as e:
                logger.error(f"Range scan error: {e}")
        
        return found
    
    def detect_nat_device(self, ip: str) -> bool:
        """Detect if an IP is behind NAT."""
        try:
            # Check for port reuse patterns
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, 80))
            sock.close()
            
            # Check TTL patterns - NAT devices often have different TTL behavior
            pkt = scapy.IP(dst=ip, ttl=64) / scapy.ICMP()
            reply = scapy.sr1(pkt, timeout=2, verbose=False)
            
            if reply and reply.ttl:
                # Low TTL (like 64) suggests direct, higher might suggest NAT
                if reply.ttl < 64:
                    return True
        except:
            pass
        
        return False
    
    def discover_all_network_types(self, target: str = None) -> Dict[str, List[NetworkDevice]]:
        """Discover devices across all network types."""
        logger.info("[DISCOVERY] Starting multi-network discovery")
        results = {
            "lan": [],
            "wan": [],
            "gan": [],  # Global Area Network
            "man": [],  # Metropolitan Area Network
            "vpn": [],
            "cloud": [],
        }
        
        # 1. LAN Discovery
        logger.info("[DISCOVERY] Scanning LAN")
        lan_ips = self._scan_network_range(self.network_range)
        for ip in lan_ips:
            device = NetworkDevice(ip)
            device.network_type = "lan"
            device.traceroute_path = self.traceroute_with_services(ip, max_hops=10)
            if device.traceroute_path:
                device.first_hop = len(device.traceroute_path)
            results["lan"].append(device)
            self.hosts[ip] = device
        
        # 2. WAN Discovery via gateway
        logger.info("[DISCOVERY] Scanning WAN (via gateway)")
        if self.gateway:
            wan_device = NetworkDevice(self.gateway)
            wan_device.network_type = "wan"
            wan_device.is_nat_device = self.detect_nat_device(self.gateway)
            wan_device.traceroute_path = self.traceroute_with_services("8.8.8.8", max_hops=15)
            results["wan"].append(wan_device)
            self.hosts[self.gateway] = wan_device
        
        # 3. VPN Detection
        logger.info("[DISCOVERY] Detecting VPN")
        vpn_info = self.discover_vpn_networks()
        for v in vpn_info:
            device = NetworkDevice(v["ip"])
            device.network_type = "vpn"
            device.is_vpn_gateway = True
            device.services = [v["port"]]
            results["vpn"].append(device)
            self.hosts[v["ip"]] = device
        
        # 4. Cloud/Public scan
        logger.info("[DISCOVERY] Scanning cloud ranges")
        for provider in CLOUD_RANGES.keys():
            cloud_devices = self.scan_public_ranges(provider, max_hosts=50)
            results["cloud"].extend(cloud_devices)
        
        # 5. GAN/MAN via traceroute to distant targets
        logger.info("[DISCOVERY] Discovering GAN/MAN via traceroute")
        distant_targets = [
            "1.1.1.1",  # Cloudflare
            "8.8.8.8",  # Google DNS
            "208.67.222.222",  # OpenDNS
        ]
        
        for target in distant_targets:
            path = self.traceroute_with_services(target, max_hops=20)
            for hop in path:
                if hop.ip and not self._is_private_ip(hop.ip) and hop.ip not in self.hosts:
                    device = NetworkDevice(hop.ip)
                    device.network_type = "gan"
                    device.first_hop = hop.hop_num
                    device.location = self._geo_locate_ip(hop.ip)
                    device.asn = hop.asn
                    device.isp = device.location.get("isp", "")
                    device.services = hop.services
                    results["gan"].append(device)
                    self.hosts[hop.ip] = device
        
        logger.info(f"[DISCOVERY] Complete: {len(self.hosts)} total devices")
        return results
    
    def _scan_network_range(self, cidr: str, max_workers: int = 50) -> List[str]:
        """Scan a network range for active hosts."""
        found = []
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            ips = [str(h) for h in network.hosts()]
        except ValueError:
            return [cidr]
        
        def check_host(ip):
            try:
                if SCAPY_OK:
                    pkt = scapy.IP(dst=ip) / scapy.ICMP()
                    reply = scapy.sr1(pkt, timeout=1, verbose=False)
                    if reply:
                        return ip
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, 445))
                    sock.close()
                    if result == 0:
                        return ip
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(check_host, ip): ip for ip in ips}
            for fut in as_completed(futures):
                result = fut.result()
                if result:
                    found.append(result)
        
        return found
    
    def get_device_by_ip(self, ip: str) -> Optional[NetworkDevice]:
        """Get device by IP."""
        return self.hosts.get(ip)
    
    def get_all_devices(self) -> List[NetworkDevice]:
        """Get all discovered devices."""
        return list(self.hosts.values())
    
    def get_devices_by_type(self, network_type: str) -> List[NetworkDevice]:
        """Get devices by network type."""
        return [d for d in self.hosts.values() if d.network_type == network_type]
    
    def get_topology_map(self) -> Dict[str, Any]:
        """Get network topology map."""
        topology = {
            "local_ip": self.local_ip,
            "gateway": self.gateway,
            "network_range": self.network_range,
            "devices": [],
            "connections": [],
        }
        
        # Build topology from traceroute paths
        for ip, device in self.hosts.items():
            device_info = device.to_dict()
            topology["devices"].append(device_info)
            
            # Build connections based on traceroute
            if device.traceroute_path:
                for hop in device.traceroute_path:
                    if hop.ip:
                        topology["connections"].append({
                            "from": self.local_ip,
                            "to": hop.ip,
                            "hop": hop.hop_num,
                            "rtt": hop.rtt,
                        })
        
        return topology
    
    def print_discovery_summary(self):
        """Print discovery summary."""
        print("\n" + "=" * 80)
        print(" ADVANCED NETWORK DISCOVERY SUMMARY")
        print("=" * 80)
        print(f"\nLocal IP     : {self.local_ip}")
        print(f"Gateway      : {self.gateway}")
        print(f"Network      : {self.network_range}")
        
        # Count by type
        type_counts = defaultdict(int)
        for device in self.hosts.values():
            type_counts[device.network_type] += 1
        
        print("\nDevices by Network Type:")
        for ntype, count in sorted(type_counts.items()):
            print(f"  {ntype.upper():<10} : {count}")
        
        # Show some sample devices
        print("\nSample Discoveries:")
        for ip, device in list(self.hosts.items())[:10]:
            location = f"{device.location.get('city', 'Unknown')}, {device.location.get('country', 'Unknown')}"
            print(f"  {ip:<18} {device.network_type:<8} {location}")
        
        print("\n" + "=" * 80)


# ─── Standalone ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    scanner = AdvancedNetworkScanner()
    print("OMNISCIENCE ADVANCED NETWORK SCANNER")
    print("Commands: discover, traceroute <ip>, vpn, cloud <provider>, topology, exit")
    
    while True:
        try:
            raw = input("ADVSCAN> ").strip()
            if not raw:
                continue
            parts = raw.split()
            op = parts[0].lower()
            
            if op in ("discover", "scan"):
                results = scanner.discover_all_network_types()
                scanner.print_discovery_summary()
                
            elif op == "traceroute" and len(parts) >= 2:
                path = scanner.traceroute_with_services(parts[1])
                print(f"\nTraceroute to {parts[1]}:")
                for hop in path:
                    if hop.ip:
                        print(f"  {hop.hop_num:<2}. {hop.ip:<18} {hop.rtt:>6.1f}ms {hop.hostname or ''}")
                    else:
                        print(f"  {hop.hop_num:<2}. *")
            
            elif op == "vpn":
                vpn_info = scanner.discover_vpn_networks()
                print(f"\nVPN Networks Found: {len(vpn_info)}")
                for v in vpn_info:
                    print(f"  {v['ip']}:{v['port']} - {v['type']}")
            
            elif op == "cloud" and len(parts) >= 2:
                provider = parts[1]
                devices = scanner.scan_public_ranges(provider, max_hosts=20)
                print(f"\n{provider.upper()} Devices Found: {len(devices)}")
                for d in devices:
                    print(f"  {d.ip} - {d.location.get('city', 'Unknown')}")
            
            elif op == "topology":
                topo = scanner.get_topology_map()
                print(f"\nNetwork Topology:")
                print(json.dumps(topo, indent=2, default=str))
            
            elif op in ("exit", "quit"):
                break
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")