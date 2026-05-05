"""
OMNISCIENCE MODULE 1 — NetworkDiscovery
Real network discovery engine with ARP, ICMP, NetBIOS, mDNS, SSDP.
No mocks, real functional scanning for Windows.

DISCLAIMER: Authorized security testing only.
"""

import os
import socket
import subprocess
import threading
import time
import ipaddress
from datetime import datetime
import logging
try:
    import netifaces
except ImportError:
    import netifaces2 as netifaces
from scapy.all import ARP, Ether, srp, sr1, IP, ICMP, UDP, DNS, DNSQR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Omniscience.Discovery")

class NetworkDiscovery:
    def __init__(self):
        self.hosts = []
        self.interfaces = []
        self._lock = threading.Lock()
        self.get_interfaces()
    
    def get_interfaces(self):
        """Get network interfaces with real IPs"""
        self.interfaces = []
        try:
            for interface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr['addr']
                        if ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.'):
                            netmask = addr.get('netmask', '255.255.255.0')
                            network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                            self.interfaces.append({
                                'name': interface,
                                'ip': ip, 
                                'network': str(network)
                            })
        except:
            pass
    
    def get_current_subnet(self):
        """Get primary subnet"""
        if self.interfaces:
            return self.interfaces[0]['network']
        return '192.168.1.0/24'
    
    def arp_scan(self, network):
        """Real ARP scan using scapy"""
        logger.info(f"ARP scanning {network}")
        self.hosts = []
        
        try:
            # Scapy ARP scan
            answered, _ = srp(
                Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network),
                timeout=2, verbose=0
            )
            
            for sent, received in answered:
                host = {
                    'ip': received.psrc,
                    'mac': received.hwsrc,
                    'hostname': '',
                    'os_hint': 'Unknown',
                    'device_type': 'Unknown',
                    'timestamp': datetime.now()
                }
                self.hosts.append(host)
                logger.info(f"Found: {host['ip']} ({host['mac']})")
            
            # Fallback Windows arp -a
            try:
                result = subprocess.run(['arp', '-a'], capture_output=True, text=True, timeout=5)
                for line in result.stdout.splitlines():
                    if network.split('/')[0] in line:
                        logger.info(f"ARP: {line}")
            except:
                pass
                
        except Exception as e:
            logger.error(f"ARP scan failed: {e}")
        
        return self.hosts
    
    def icmp_sweep(self, network):
        """ICMP ping sweep"""
        logger.info(f"ICMP sweep {network}")
        hosts = []
        network_obj = ipaddress.IPv4Network(network)
        
        def ping_host(ip):
            try:
                # Scapy ping
                resp = sr1(IP(dst=str(ip))/ICMP(), timeout=1, verbose=0)
                if resp:
                    hosts.append({'ip': str(ip), 'alive': True})
            except:
                pass
        
        threads = []
        for ip in network_obj.hosts():
            t = threading.Thread(target=ping_host, args=(ip,))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join(timeout=3)
        
        alive_hosts = [h for h in hosts if h.get('alive')]
        self.hosts = alive_hosts
        return alive_hosts
    
    def netbios_scan(self, ip):
        """NetBIOS name resolution"""
        logger.info(f"NetBIOS scan {ip}")
        try:
            result = subprocess.run(['nbtstat', '-A', ip], capture_output=True, text=True, timeout=5)
            names = []
            for line in result.stdout.splitlines():
                if '<00>' in line or '<20>' in line:
                    names.append(line.strip())
            return {'ip': ip, 'netbios_names': names}
        except:
            return {'ip': ip, 'error': 'nbtstat failed'}
    
    def mdns_listen(self, timeout=10):
        """mDNS discovery"""
        logger.info("Real mDNS discovery using scapy multicast")
        devices = []
        try:
            # mDNS query for all services on 224.0.0.251
            pkt = IP(dst="224.0.0.251")/UDP(sport=5353, dport=5353)/DNS(rd=1, qd=DNSQR(qname="_services._dns-sd._udp.local"))
            ans, _ = srp(Ether(dst="01:00:5e:00:00:fb")/pkt, timeout=timeout, verbose=0)
            for _, r in ans:
                if r.haslayer(IP) and r[IP].src not in [d['ip'] for d in devices]:
                    devices.append({'ip': r[IP].src, 'type': 'mDNS'})
        except Exception as e:
            logger.error(f"mDNS failed: {e}")
        return devices
    
    def ssdp_discover(self, timeout=5):
        """SSDP/UPnP discovery"""
        logger.info("Real SSDP/UPnP discovery using M-SEARCH")
        devices = []
        ssdp_request = (
            'M-SEARCH * HTTP/1.1\r\n'
            'HOST: 239.255.255.250:1900\r\n'
            'MAN: "ssdp:discover"\r\n'
            'MX: 2\r\n'
            'ST: ssdp:all\r\n'
            '\r\n'
        )
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sock.sendto(ssdp_request.encode(), ("239.255.255.250", 1900))
            while True:
                try:
                    data, addr = sock.recvfrom(1024)
                    if addr[0] not in [d['ip'] for d in devices]:
                        devices.append({'ip': addr[0], 'type': 'SSDP'})
                except socket.timeout:
                    break
            sock.close()
        except Exception as e:
            logger.error(f"SSDP failed: {e}")
        return devices
    
    def auto_scan(self):
        """Full auto discovery"""
        logger.info("FULL AUTO SCAN STARTED")
        subnet = self.get_current_subnet()
        
        # Multi-threaded discovery
        threads = []
        t1 = threading.Thread(target=self.arp_scan, args=(subnet,))
        t2 = threading.Thread(target=self.icmp_sweep, args=(subnet,))
        threads.extend([t1, t2])
        
        t1.start()
        t2.start()
        
        for t in threads:
            t.join()
        
        # Dedupe hosts
        seen_ips = set()
        unique_hosts = []
        for host in self.hosts:
            ip = host['ip']
            if ip not in seen_ips:
                seen_ips.add(ip)
                unique_hosts.append(host)
        
        self.hosts = unique_hosts
        logger.info(f"AUTO SCAN COMPLETE: {len(self.hosts)} unique hosts")
        return self.hosts
    
    def get_network_info(self):
        """Get network configuration"""
        return {
            'interfaces': self.interfaces,
            'hosts': self.hosts,
            'gateway': self.get_gateway_ip()
        }
    
    def get_gateway_ip(self):
        """Find gateway IP"""
        try:
            gws = netifaces.gateways()
            return gws['default'][netifaces.AF_INET][0]
        except:
            return 'Unknown'
    
    def get_interface_info(self):
        """Detailed interface info"""
        return self.interfaces
