"""
OMNISCIENCE NETWORK DISCOVERY ENGINE v6.0
FULLY FUNCTIONAL - Real Network Scanning & Reconnaissance
"""

import socket
import struct
import threading
import time
import random
import ipaddress
import subprocess
import platform
import re
from datetime import datetime
from typing import List, Dict, Any

try:
    import netifaces
except ImportError:
    import netifaces2 as netifaces

class NetworkDevice:
    """Represents a discovered network device"""
    def __init__(self, ip: str):
        self.ip = ip
        self.hostname = ""
        self.mac = ""
        self.vendor = ""
        self.os = ""
        self.open_ports = []
        self.services = {}
        self.vulnerabilities = []
        self.last_seen = datetime.now()
        self.response_time = 0
        
    def to_dict(self):
        return {
            'ip': self.ip,
            'hostname': self.hostname,
            'mac': self.mac,
            'vendor': self.vendor,
            'os': self.os,
            'open_ports': self.open_ports,
            'services': self.services,
            'vulnerabilities': self.vulnerabilities,
            'last_seen': str(self.last_seen),
            'response_time': self.response_time
        }

class NetworkDiscovery:
    """Advanced Network Discovery Engine"""
    
    def __init__(self):
        self.devices = {}
        self.scan_threads = []
        self.active = True
        
        # MAC vendor database (partial)
        self.mac_vendors = {
            '00:50:56': 'VMware',
            '00:0C:29': 'VMware',
            '00:05:69': 'VMware',
            '00:1C:14': 'VMware',
            '00:15:5D': 'Microsoft Hyper-V',
            '00:03:FF': 'Microsoft',
            '08:00:27': 'VirtualBox',
            '52:54:00': 'QEMU/KVM',
            '00:16:3E': 'Xen',
            'B8:27:EB': 'Raspberry Pi',
            'DC:A6:32': 'Raspberry Pi',
            '00:1B:44': 'Cisco',
            '00:1C:0E': 'Cisco',
            '00:50:73': 'Cisco',
            '00:0A:95': 'Apple',
            '00:03:93': 'Apple',
            '00:17:F2': 'Apple',
            '00:1F:5B': 'Apple',
            '00:25:00': 'Apple',
            '28:CF:E9': 'Apple',
            '3C:07:54': 'Apple',
            '00:50:F2': 'Microsoft',
            '00:15:5D': 'Microsoft',
            '00:12:5A': 'Microsoft',
            '00:E0:4C': 'Realtek',
            '00:E0:4D': 'Realtek',
            '52:54:00': 'Red Hat',
            '00:1A:4D': 'Dell',
            '00:14:22': 'Dell',
            '00:1E:C9': 'HP',
            '00:23:7D': 'HP',
            '00:30:6E': 'HP',
        }
        
        # Common ports for service detection
        self.common_ports = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            135: 'MSRPC',
            139: 'NetBIOS',
            143: 'IMAP',
            443: 'HTTPS',
            445: 'SMB',
            1433: 'MSSQL',
            1521: 'Oracle',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            5900: 'VNC',
            6379: 'Redis',
            8080: 'HTTP-Proxy',
            8443: 'HTTPS-Alt',
            27017: 'MongoDB',
        }
        
    def get_current_subnet(self) -> str:
        """Get current subnet CIDR"""
        try:
            gws = netifaces.gateways()
            if 'default' in gws and netifaces.AF_INET in gws['default']:
                iface = gws['default'][netifaces.AF_INET][1]
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    ip = addrs[netifaces.AF_INET][0]['addr']
                    netmask = addrs[netifaces.AF_INET][0]['netmask']
                    
                    # Calculate CIDR
                    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                    return str(network)
        except:
            pass
        return "192.168.1.0/24"
    
    def get_gateway_ip(self) -> str:
        """Get default gateway IP"""
        try:
            gws = netifaces.gateways()
            if 'default' in gws and netifaces.AF_INET in gws['default']:
                return gws['default'][netifaces.AF_INET][0]
        except:
            pass
        return ""
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get comprehensive network information"""
        info = {
            'interfaces': [],
            'gateway': self.get_gateway_ip(),
            'subnet': self.get_current_subnet(),
            'dns_servers': [],
            'hostname': socket.gethostname(),
        }
        
        try:
            for iface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(iface)
                iface_info = {'name': iface, 'addresses': []}
                
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        iface_info['addresses'].append({
                            'type': 'IPv4',
                            'address': addr.get('addr'),
                            'netmask': addr.get('netmask')
                        })
                
                if netifaces.AF_INET6 in addrs:
                    for addr in addrs[netifaces.AF_INET6]:
                        iface_info['addresses'].append({
                            'type': 'IPv6',
                            'address': addr.get('addr', '').split('%')[0]
                        })
                
                if iface_info['addresses']:
                    info['interfaces'].append(iface_info)
        except:
            pass
        
        return info
    
    def get_interface_info(self) -> Dict[str, Any]:
        """Get detailed interface information"""
        return self.get_network_info()
    
    def ping_host(self, ip: str, timeout: int = 1) -> bool:
        """Ping a host to check if it's alive"""
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '1', '-w' if platform.system().lower() == 'windows' else '-W', str(timeout * 1000 if platform.system().lower() == 'windows' else timeout), ip]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout + 1)
            return result.returncode == 0
        except:
            return False
    
    def tcp_connect_scan(self, ip: str, port: int, timeout: float = 0.5) -> bool:
        """TCP connect scan for a specific port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def scan_ports(self, ip: str, ports: List[int] = None) -> List[int]:
        """Scan multiple ports on a host"""
        if ports is None:
            ports = list(self.common_ports.keys())
        
        open_ports = []
        for port in ports:
            if self.tcp_connect_scan(ip, port, timeout=0.3):
                open_ports.append(port)
        
        return open_ports
    
    def get_hostname(self, ip: str) -> str:
        """Resolve hostname from IP"""
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except:
            return ""
    
    def get_mac_address(self, ip: str) -> str:
        """Get MAC address using ARP (Windows)"""
        try:
            if platform.system().lower() == 'windows':
                result = subprocess.run(['arp', '-a', ip], capture_output=True, text=True, timeout=2)
                output = result.stdout
                
                # Parse ARP output
                mac_pattern = r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})'
                match = re.search(mac_pattern, output)
                if match:
                    return match.group(0).replace('-', ':').upper()
            else:
                # Linux/Unix
                result = subprocess.run(['arp', '-n', ip], capture_output=True, text=True, timeout=2)
                output = result.stdout
                mac_pattern = r'([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}'
                match = re.search(mac_pattern, output)
                if match:
                    return match.group(0).upper()
        except:
            pass
        return ""
    
    def get_vendor_from_mac(self, mac: str) -> str:
        """Get vendor from MAC address"""
        if not mac:
            return ""
        
        # Get OUI (first 3 octets)
        oui = ':'.join(mac.split(':')[:3])
        return self.mac_vendors.get(oui, "Unknown")
    
    def detect_os(self, ip: str, open_ports: List[int]) -> str:
        """Detect OS based on open ports and behavior"""
        os_hints = []
        
        # Windows indicators
        if 135 in open_ports or 139 in open_ports or 445 in open_ports:
            os_hints.append("Windows")
        
        if 3389 in open_ports:
            os_hints.append("Windows (RDP)")
        
        # Linux indicators
        if 22 in open_ports:
            os_hints.append("Linux/Unix")
        
        # Database servers
        if 3306 in open_ports:
            os_hints.append("MySQL Server")
        
        if 5432 in open_ports:
            os_hints.append("PostgreSQL Server")
        
        if 1433 in open_ports:
            os_hints.append("Windows (MSSQL)")
        
        # Web servers
        if 80 in open_ports or 443 in open_ports:
            os_hints.append("Web Server")
        
        return " / ".join(os_hints) if os_hints else "Unknown"
    
    def scan_device(self, ip: str) -> NetworkDevice:
        """Comprehensive scan of a single device"""
        device = NetworkDevice(ip)
        
        # Get hostname
        device.hostname = self.get_hostname(ip)
        
        # Scan ports
        device.open_ports = self.scan_ports(ip)
        
        # Get MAC and vendor
        device.mac = self.get_mac_address(ip)
        device.vendor = self.get_vendor_from_mac(device.mac)
        
        # Detect OS
        device.os = self.detect_os(ip, device.open_ports)
        
        # Map services
        for port in device.open_ports:
            service = self.common_ports.get(port, f"Unknown-{port}")
            device.services[port] = service
        
        return device
    
    def icmp_sweep(self, network: str) -> List[str]:
        """ICMP ping sweep of network"""
        alive_hosts = []
        
        try:
            net = ipaddress.IPv4Network(network, strict=False)
            threads = []
            results = []
            
            def ping_worker(ip_str):
                if self.ping_host(ip_str, timeout=1):
                    results.append(ip_str)
            
            # Limit to first 254 hosts for speed
            hosts = list(net.hosts())[:254]
            
            for ip in hosts:
                ip_str = str(ip)
                t = threading.Thread(target=ping_worker, args=(ip_str,))
                t.start()
                threads.append(t)
                
                # Limit concurrent threads
                if len(threads) >= 50:
                    for thread in threads:
                        thread.join(timeout=2)
                    threads = []
            
            # Wait for remaining threads
            for thread in threads:
                thread.join(timeout=2)
            
            alive_hosts = results
        except Exception as e:
            print(f"ICMP sweep error: {e}")
        
        return alive_hosts
    
    def arp_scan(self, network: str) -> List[str]:
        """ARP scan for local network"""
        alive_hosts = []
        
        try:
            # Use system ARP command
            if platform.system().lower() == 'windows':
                result = subprocess.run(['arp', '-a'], capture_output=True, text=True, timeout=5)
                output = result.stdout
                
                # Parse ARP table
                ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
                ips = re.findall(ip_pattern, output)
                
                # Filter by network
                net = ipaddress.IPv4Network(network, strict=False)
                for ip in ips:
                    try:
                        if ipaddress.IPv4Address(ip) in net:
                            alive_hosts.append(ip)
                    except:
                        pass
            else:
                # Linux arp-scan or arp command
                result = subprocess.run(['arp', '-n'], capture_output=True, text=True, timeout=5)
                output = result.stdout
                
                ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
                ips = re.findall(ip_pattern, output)
                
                net = ipaddress.IPv4Network(network, strict=False)
                for ip in ips:
                    try:
                        if ipaddress.IPv4Address(ip) in net:
                            alive_hosts.append(ip)
                    except:
                        pass
        except Exception as e:
            print(f"ARP scan error: {e}")
        
        return list(set(alive_hosts))
    
    def netbios_scan(self, ip: str) -> Dict[str, Any]:
        """NetBIOS enumeration"""
        info = {'ip': ip, 'netbios_name': '', 'workgroup': '', 'services': []}
        
        try:
            # Try NetBIOS name query (port 137)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            
            # NetBIOS name query packet
            query = b'\x82\x28\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00'
            query += b'\x20' + b'CKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' + b'\x00'
            query += b'\x00\x21\x00\x01'
            
            sock.sendto(query, (ip, 137))
            data, _ = sock.recvfrom(1024)
            sock.close()
            
            # Parse response (simplified)
            if len(data) > 56:
                name = data[56:72].decode('ascii', errors='ignore').strip()
                info['netbios_name'] = name
        except:
            pass
        
        return info
    
    def snmp_query(self, ip: str, community: str = 'public') -> Dict[str, Any]:
        """SNMP query (simplified)"""
        info = {'ip': ip, 'snmp_enabled': False, 'community': community}
        
        try:
            # Check if SNMP port is open
            if self.tcp_connect_scan(ip, 161, timeout=1):
                info['snmp_enabled'] = True
        except:
            pass
        
        return info
    
    def mdns_listen(self, timeout: int = 5) -> List[Dict[str, Any]]:
        """Listen for mDNS broadcasts"""
        devices = []
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', 5353))
            sock.settimeout(timeout)
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    data, addr = sock.recvfrom(1024)
                    devices.append({'ip': addr[0], 'type': 'mDNS'})
                except socket.timeout:
                    break
            
            sock.close()
        except:
            pass
        
        return devices
    
    def ssdp_discover(self, timeout: int = 3) -> List[Dict[str, Any]]:
        """SSDP/UPnP discovery"""
        devices = []
        
        try:
            msg = b'M-SEARCH * HTTP/1.1\\r\\n' \
                  b'HOST: 239.255.255.250:1900\\r\\n' \
                  b'MAN: "ssdp:discover"\\r\\n' \
                  b'MX: 1\\r\\n' \
                  b'ST: ssdp:all\\r\\n\\r\\n'
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sock.sendto(msg, ('239.255.255.250', 1900))
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    data, addr = sock.recvfrom(1024)
                    devices.append({'ip': addr[0], 'type': 'UPnP', 'response': data.decode('utf-8', errors='ignore')[:200]})
                except socket.timeout:
                    break
            
            sock.close()
        except:
            pass
        
        return devices
    
    def http_fingerprint(self, ip: str, port: int = 80) -> Dict[str, Any]:
        """HTTP service fingerprinting"""
        info = {'ip': ip, 'port': port, 'server': '', 'title': ''}
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((ip, port))
            
            request = f"GET / HTTP/1.1\\r\\nHost: {ip}\\r\\nConnection: close\\r\\n\\r\\n"
            sock.send(request.encode())
            
            response = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
                if len(response) > 10000:  # Limit response size
                    break
            
            sock.close()
            
            response_str = response.decode('utf-8', errors='ignore')
            
            # Extract Server header
            server_match = re.search(r'Server: ([^\\r\\n]+)', response_str)
            if server_match:
                info['server'] = server_match.group(1)
            
            # Extract title
            title_match = re.search(r'<title>([^<]+)</title>', response_str, re.IGNORECASE)
            if title_match:
                info['title'] = title_match.group(1).strip()
        except:
            pass
        
        return info
    
    def auto_scan(self) -> List[NetworkDevice]:
        """Automatic comprehensive network scan"""
        print("[*] Starting automatic network discovery...")
        
        # Get current subnet
        subnet = self.get_current_subnet()
        print(f"[*] Scanning subnet: {subnet}")
        
        # Phase 1: Quick host discovery
        print("[*] Phase 1: Host discovery (ICMP + ARP)...")
        alive_hosts = set()
        
        # ICMP sweep
        icmp_hosts = self.icmp_sweep(subnet)
        alive_hosts.update(icmp_hosts)
        print(f"[+] ICMP found {len(icmp_hosts)} hosts")
        
        # ARP scan
        arp_hosts = self.arp_scan(subnet)
        alive_hosts.update(arp_hosts)
        print(f"[+] ARP found {len(arp_hosts)} hosts")
        
        # Phase 2: Detailed scanning
        print(f"[*] Phase 2: Detailed scanning of {len(alive_hosts)} hosts...")
        devices = []
        
        for ip in alive_hosts:
            print(f"[*] Scanning {ip}...")
            device = self.scan_device(ip)
            devices.append(device)
            self.devices[ip] = device
        
        print(f"[+] Scan complete: {len(devices)} devices discovered")
        return devices
    
    def fast_sweep(self) -> List[str]:
        """Fast 10-second network sweep"""
        print("[*] Fast sweep initiated...")
        subnet = self.get_current_subnet()
        
        # Quick ICMP sweep with reduced timeout
        alive_hosts = []
        
        try:
            net = ipaddress.IPv4Network(subnet, strict=False)
            threads = []
            results = []
            
            def quick_ping(ip_str):
                if self.ping_host(ip_str, timeout=0.5):
                    results.append(ip_str)
            
            # Scan first 100 hosts only
            hosts = list(net.hosts())[:100]
            
            for ip in hosts:
                ip_str = str(ip)
                t = threading.Thread(target=quick_ping, args=(ip_str,))
                t.start()
                threads.append(t)
                
                if len(threads) >= 100:
                    for thread in threads:
                        thread.join(timeout=0.5)
                    threads = []
            
            for thread in threads:
                thread.join(timeout=0.5)
            
            alive_hosts = results
        except:
            pass
        
        print(f"[+] Fast sweep complete: {len(alive_hosts)} hosts found")
        return alive_hosts
    
    def full_scan(self, target: str) -> List[NetworkDevice]:
        """Full scan of target (IP or network)"""
        devices = []
        
        try:
            # Check if it's a network or single IP
            if '/' in target:
                # Network scan
                net = ipaddress.IPv4Network(target, strict=False)
                hosts = [str(ip) for ip in list(net.hosts())[:254]]
            else:
                # Single IP
                hosts = [target]
            
            print(f"[*] Scanning {len(hosts)} hosts...")
            
            for ip in hosts:
                if self.ping_host(ip, timeout=1):
                    device = self.scan_device(ip)
                    devices.append(device)
                    self.devices[ip] = device
        except Exception as e:
            print(f"[!] Scan error: {e}")
        
        return devices
    
    def ultramax_global_scan(self):
        """ULTRAMAX global scan simulation"""
        print("[*] ULTRAMAX GLOBAL SCAN ACTIVATED")
        print("[*] Scanning all reachable networks...")
        
        # Get all network interfaces
        all_networks = []
        
        try:
            for iface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr.get('addr')
                        netmask = addr.get('netmask')
                        if ip and netmask and not ip.startswith('127.'):
                            network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                            all_networks.append(str(network))
        except:
            pass
        
        print(f"[*] Found {len(all_networks)} networks to scan")
        
        all_devices = []
        for network in all_networks:
            print(f"[*] Scanning {network}...")
            devices = self.full_scan(network)
            all_devices.extend(devices)
        
        print(f"[+] Global scan complete: {len(all_devices)} total devices")
        return all_devices
    
    def _detect_external_info(self) -> Dict[str, Any]:
        """Detect external IP and info"""
        info = {'external_ip': '', 'isp': '', 'country': ''}
        
        try:
            import urllib.request
            with urllib.request.urlopen('https://api.ipify.org', timeout=3) as response:
                info['external_ip'] = response.read().decode('utf-8')
        except:
            pass
        
        return info
