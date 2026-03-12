# OMNISCIENCE FRAMEWORK v5.0 - COMPREHENSIVE DOCUMENTATION

**DISCLAIMER: This documentation is for educational and security research purposes only. Unauthorized access to computer systems is illegal.**

---

## TABLE OF CONTENTS
1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Module Breakdown](#3-module-breakdown)
4. [Capabilities Analysis](#4-capabilities-analysis)
5. [Where It Can Be Applied](#5-where-it-can-be-applied)
6. [Assessment: Good vs Bad](#6-assessment-good-vs-bad)
7. [Technical Requirements](#7-technical-requirements)
8. [Legal and Ethical Considerations](#8-legal-and-ethical-considerations)
9. [Complete Feature List](#9-complete-feature-list)

---

## 1. PROJECT OVERVIEW

The **Omniscience Framework** is a sophisticated, modular network reconnaissance and remote access platform designed for offensive security operations. It operates as an **agentless** system, meaning no software needs to be installed on target machines.

### Key Details
- **Version**: 5.0
- **Language**: Python 3
- **Architecture**: Modular (7 core modules + 1 orchestrator)
- **Total Lines of Code**: ~8,000+ lines across 7 Python files
- **Platform Support**: Windows, Linux, macOS (controller), targets Windows/Linux

### Core Philosophy
The framework is designed to provide "complete network visibility and control" through:
- Multi-vector network discovery
- Passive intelligence gathering
- Remote control without agents
- Automated exploitation
- Lateral movement
- Command & Control (C2) capabilities

---

## 2. SYSTEM ARCHITECTURE

### File Structure
```
heavy/
├── 1.py              # NetworkDiscovery (1,746 lines)
│                      Multi-vector network enumeration
├── 2.py              # AgentlessIntelligence (873 lines)
│                      Passive sniffing & WMI queries
├── 3.py              # AgentlessControl (2,099 lines)
│                      Remote control & exploitation
├── 4.py              # OmniShell (759 lines)
│                      Main orchestrator & UI
├── 5.py              # AdvancedNetworkScanner (785 lines)
│                      Cross-network discovery
├── 6.py              # AdvancedCommandCenter (~700 lines)
│                      Lateral movement & C2
├── 7.py              # UniversalNetworkAccess (~750 lines)
│                      Unauthenticated access
├── DOCUMENTATION.md  # Official framework guide
├── README.md         # This file
└── *.log            # Various log files
```

### Dependencies
- **scapy.all** - Packet crafting, ARP scanning, sniffing
- **impacket** - SMB/WMI/DCOM remote protocols
- **paramiko** - SSH client functionality
- **nmap** (optional) - Network scanning
- **pysnmp** (optional) - SNMP queries

---

## 3. MODULE BREAKDOWN

### MODULE 1: NetworkDiscovery (1.py)
**Purpose**: Multi-vector, fully agentless network enumeration

**Discovery Methods** (9 total):
| Method | Protocol | Layer | Description |
|--------|----------|-------|-------------|
| ARP | Broadcast | L2 | Fastest, LAN only |
| ICMP | Ping | L3 | Works across subnets |
| TCP | SYN | L4 | 50-thread parallel probing |
| NetBIOS | UDP 137 | L7 | Windows hostname/workgroup |
| mDNS | UDP 5353 | L7 | Apple/Linux/IoT services |
| SSDP | UDP 1900 | L7 | UPnP device discovery |
| SNMP | UDP 161 | L7 | Device info (community=public) |
| DNS-PTR | TCP/UDP 53 | L7 | Reverse DNS lookup |
| HTTP | TCP 80/443 | L7 | API fingerprinting |

**Auto-Detection Features**:
- Multi-interface detection
- Gateway & subnet auto-detection
- External IP detection
- Device fingerprinting (OS, type, services)

**Device Type Detection**:
- Routers (192.168.0.1, 10.0.0.1 patterns)
- Cameras (RTSP ports 554, 8554)
- Printers (IPP port 631)
- NAS (ports 5000, 5001, 8080)
- IoT (MQTT ports 1883, 8883)
- Game consoles (ports 3074, 3478)
- Smart TVs (ports 5500, 9000)
- VoIP (SIP ports 5060, 5061)
- Databases (MySQL, PostgreSQL, MongoDB, Redis)
- Web Servers

**MAC Vendor Database**: VMware, VirtualBox, Hyper-V, Raspberry Pi, Apple, Samsung, Huawei, Xiaomi, TP-Link, Netgear, D-Link, Cisco, Asus, Intel

---

### MODULE 2: AgentlessIntelligence (2.py)
**Purpose**: Passive intelligence gathering WITHOUT sending traffic to targets

**Capabilities**:
| Capability | Description |
|------------|-------------|
| **Packet Sniffing** | HTTP credentials, cookies, DNS, FTP, Telnet, SMTP |
| **Credential Capture** | Basic Auth, POST data, NTLM hashes |
| **WMI Queries** | Remote Windows query without agents |
| **SMB Enumeration** | Share/file enumeration (null sessions) |
| **SNMP Polling** | Real-time interface stats |
| **Continuous Monitoring** | Per-host activity stream |

**Data Captured**:
- HTTP cookies and Basic Auth credentials
- FTP usernames and passwords
- Telnet session data
- SMTP commands and credentials
- DNS queries and responses
- NTLMSSP challenge/response data
- Windows process lists
- Logged-in users
- Installed software
- Services and scheduled tasks
- Event logs (Security, System, Application)
- Shared folders and files
- Disk information

---

### MODULE 3: AgentlessControl (3.py)
**Purpose**: Full remote control WITHOUT installing agents

**Windows Capabilities** (via WMI/DCOM/SMB/WinRM):
- Execute any shell command
- Capture live screenshots (JPEG compression)
- Kill/start processes remotely
- Start/stop/install/delete services
- Read/write/delete registry keys
- Upload/download files via SMB
- Wake-on-LAN
- Remote shutdown/reboot/logoff
- Enumerate/manage local users/groups

**Advanced Windows Features**:
- Pass-the-Hash authentication (NTLM)
- Token stealing and impersonation
- Cached credential harvesting
- LSASS dump for password hashes
- Service account enumeration
- RDP hijacking
- PowerShell Empire-style payloads
- Reverse TCP shells (Windows/Linux)
- Port forwarding/tunneling
- Lateral movement automation
- Browser password extraction (Chrome, Firefox, Edge)
- WiFi password extraction
- Clipboard access
- System information gathering
- RDP enable/disable
- Firewall management
- Webcam capture
- Scheduled task creation

**Linux Capabilities** (via SSH):
- Interactive shell
- Command execution with output
- File upload/download (SFTP)
- Process management
- System info gathering
- Reverse shell creation
- SSH backdoor installation
- Cron persistence

**Exploitation Methods**:
- SSH brute-force (default credentials)
- Telnet brute-force
- RDP brute-force
- VNC brute-force
- FTP anonymous access
- SMB null sessions
- MS17-010 (EternalBlue) detection
- BlueKeep (CVE-2019-0708) detection
- MySQL root access
- PostgreSQL access
- MSSQL access

**Default Credentials Database**:
```
SSH: root, admin, pi, ubuntu with passwords: "", root, toor, pass, admin, raspberry
Windows: Administrator with passwords: "", administrator, password, 123456
Router: admin with common router defaults
```

---

### MODULE 4: OmniShell (4.py)
**Purpose**: Main orchestrator with advanced terminal UI

**UI Features**:
- ANSI color codes (16 foreground + 16 background)
- Gradient text effects
- Typewriter animation
- Loading bars
- Rainbow text
- Box drawing
- Tree-style help menus

**Integrated Modules**:
- NetworkDiscovery
- AgentlessIntelligence
- AgentlessControl
- C2Server
- AdvancedNetworkScanner
- AdvancedCommandCenter
- UniversalNetworkAccess
- MITMEngine

**MITM Capabilities**:
- ARP scan
- ARP spoofing (man-in-the-middle)
- IP forwarding
- Traffic interception
- Target/gateway poisoning

---

### MODULE 5: AdvancedNetworkScanner (5.py)
**Purpose**: Multi-dimensional network discovery across network types

**Network Types Supported**:
- LAN (Local Area Network)
- WAN (Wide Area Network)
- GAN (Global Area Network)
- MAN (Metropolitan Area Network)
- PAN (Personal Area Network)
- VPN networks
- Cloud providers

**Advanced Features**:
- Cross-subnet discovery
- Traceroute with service fingerprinting
- Network topology mapping
- Public IP range scanning
- BGP/AS enumeration
- VPN tunnel detection
- Multi-homed device detection
- NAT traversal identification
- ISP fingerprinting and geolocation

**Cloud Provider Ranges**:
- AWS: 3.0.0.0/8, 4.0.0.0/9, 15.0.0.0/9, 16.0.0.0/9, 18.0.0.0/8
- Azure: 13.64.0.0/11, 20.0.0.0/8, 40.0.0.0/8, 52.0.0.0/8
- GCP: 34.64.0.0/10, 35.192.0.0/11, 104.16.0.0/12
- DigitalOcean, Linode, Oracle, Alibaba, IBM

**VPN Detection Ports**: 500, 4500, 1701, 443, 8443, 1194, 1723, 8080

---

### MODULE 6: AdvancedCommandCenter (6.py)
**Purpose**: Command execution, lateral movement, and distributed control

**Capabilities**:
- Multi-host parallel execution
- Lateral movement automation
- Network pivoting through compromised hosts
- Advanced persistence mechanisms
- Real-time device monitoring dashboard
- Cross-network exploitation chains
- Distributed task execution
- Automated privilege escalation
- Session management across network boundaries
- Credential harvesting from sessions
- Interactive session shells

**Payload Generation**:
- Windows reverse shell (PowerShell)
- Linux reverse shell (bash)
- Staged payloads
- Persistence mechanisms

---

### MODULE 7: UniversalNetworkAccess (7.py)
**Purpose**: Universal, unauthenticated network access

**⚠️ WARNING**: This module explicitly attempts unauthorized access

**Features**:
- Ultra-comprehensive device discovery
- Automatic unauthenticated access attempts
- Default credential testing
- Known exploit targeting
- Network-wide autonomous exploitation
- SMB null session access
- SSH default credentials
- FTP anonymous access

**Vulnerability Database**:
- SMB: MS17-010 (EternalBlue), SMB signing not required
- RDP: CVE-2019-0708 (BlueKeep)
- SSH: Default credentials
- FTP: Anonymous access

---

## 4. CAPABILITIES ANALYSIS

### Network Discovery
| Capability | Implemented | Method |
|------------|-------------|--------|
| ARP Scanning | ✅ | scapy |
| ICMP Ping | ✅ | subprocess/scapy |
| TCP Port Scan | ✅ | socket |
| Service Detection | ✅ | banner grabbing |
| OS Fingerprinting | ✅ | TTL analysis |
| Device Type Detection | ✅ | port signatures + MAC |
| Cross-subnet | ✅ | source routing |
| Cloud Scanning | ✅ | IP ranges |
| Traceroute | ✅ | ICMP/UDP |
| Geolocation | ✅ | ip-api.com |

### Intelligence Gathering
| Capability | Implemented | Method |
|------------|-------------|--------|
| Packet Sniffing | ✅ | scapy |
| Credential Capture | ✅ | regex parsing |
| NTLM Hash Extraction | ✅ | traffic analysis |
| WMI Queries | ✅ | impacket |
| SMB Enumeration | ✅ | impacket |
| SNMP Polling | ✅ | socket |
| DNS Capture | ✅ | packet analysis |

### Remote Control
| Capability | Implemented | Method |
|------------|-------------|--------|
| Command Execution | ✅ | WMI/SSH |
| Screenshot Capture | ✅ | PowerShell |
| Process Management | ✅ | WMI |
| Service Management | ✅ | SCM |
| Registry Access | ✅ | winreg/SMB |
| File Operations | ✅ | SMB |
| Key Injection | ✅ | SendKeys |
| Clipboard Access | ✅ | PowerShell |
| User Management | ✅ | WMI |
| Firewall Control | ✅ | PowerShell |

### Exploitation
| Capability | Implemented | Status |
|------------|------------|--------|
| EternalBlue | ⚠️ | Detection only |
| BlueKeep | ⚠️ | Detection only |
| Default Credentials | ✅ | Built-in lists |
| Brute Force | ✅ | SSH/FTP/Telnet/RDP/VNC |
| Lateral Movement | ✅ | Automated |
| Null Sessions | ✅ | SMB |
| Password Harvesting | ✅ | Browser/WiFi |

---

## 5. WHERE IT CAN BE APPLIED

### ✅ LEGITIMATE APPLICATIONS

#### 1. Authorized Penetration Testing
- **Scope**: Networks you own or have written authorization for
- **Use Case**: Red team operations, security assessments
- **Benefit**: Comprehensive testing without agents

#### 2. Vulnerability Assessment
- **Scope**: Your own infrastructure
- **Use Case**: Identify weak configurations, default credentials
- **Benefit**: Automated scanning and reporting

#### 3. Red Team Operations
- **Scope**: Authorized engagement
- **Use Case**: Simulate advanced persistent threats
- **Benefit**: Realistic attack simulation

#### 4. Security Research
- **Scope**: Lab environments, research networks
- **Use Case**: Study attack vectors, develop defenses
- **Benefit**: Understanding attacker techniques

#### 5. Incident Response
- **Scope**: Networks under your jurisdiction
- **Use Case**: Investigate breaches, identify compromised systems
- **Benefit**: Deep visibility into network traffic

#### 6. Network Management (Limited)
- **Scope**: Networks you administer
- **Use Case**: Device discovery, inventory
- **Caution**: Some features exceed legitimate need

---

## 6. ASSESSMENT: GOOD VS BAD

### ✅ GOOD ASPECTS

| Aspect | Analysis |
|--------|----------|
| **Modular Design** | Well-organized, maintainable code |
| **Agentless** | No deployment needed on targets |
| **Multi-vector** | Comprehensive coverage of discovery methods |
| **Educational** | Demonstrates real attack techniques |
| **Automation** | Efficient for repetitive security tasks |
| **Documentation** | Includes usage guides |

### ⚠️ CONCERNING ASPECTS

| Aspect | Risk Level | Issue |
|--------|------------|-------|
| **Credential Capture** | 🔴 HIGH | Actively harvests credentials from network traffic |
| **Unauthenticated Access** | 🔴 HIGH | Attempts access without credentials |
| **Exploit Database** | 🔴 HIGH | References known vulnerabilities |
| **Lateral Movement** | 🔴 HIGH | Automated spread between systems |
| **MITM Capability** | 🔴 HIGH | ARP spoofing for traffic interception |
| **Remote Control** | 🔴 HIGH | Full control without agent |
| **Default Creds** | 🟡 MEDIUM | Built-in default password lists |
| **Data Exfiltration** | 🔴 HIGH | File download/upload capabilities |

### 🔴 HIGH-RISK FUNCTIONALITY

1. **Passive Credential Harvesting**
   - Captures credentials from HTTP, FTP, SMTP, Telnet
   - NTLM hash extraction from traffic
   - No target notification

2. **Unauthenticated Exploitation**
   - Null session access to SMB
   - Default credential attacks
   - Exploit framework integration

3. **Remote Control Without Agents**
   - WMI remote execution
   - SMB file operations
   - Registry manipulation

4. **Man-in-the-Middle**
   - ARP spoofing
   - Traffic interception
   - Session hijacking

5. **Automated Lateral Movement**
   - Credential harvesting
   - Pivot chain management
   - Network-wide exploitation

---

## 7. TECHNICAL REQUIREMENTS

### Python Dependencies
```python
scapy          # Packet crafting
impacket        # SMB/WMI protocols
paramiko        # SSH client
nmap            # Optional
pysnmp          # Optional
```

### System Requirements
- **OS**: Linux (primary), Windows (limited)
- **Privileges**: Root/Administrator (for raw sockets, ARP spoofing)
- **Network**: Multi-homed support

### Target Requirements
- **Windows**: WMI enabled, RPC ports open (135, 445)
- **Linux**: SSH daemon running
- **Network**: IP connectivity

---

## 8. LEGAL AND ETHICAL CONSIDERATIONS

### ⚖️ LEGAL STATUS

**This tool CAN be used illegally if**:
- Accessing systems without authorization
- Intercepting communications without consent
- Stealing credentials from others
- Disabling or damaging systems
- Exfiltrating data without permission
- Using for unauthorized surveillance

**This tool CAN be used legally if**:
- You own the target systems
- You have written authorization from the owner
- You're conducting authorized security testing
- You're in a bug bounty program with explicit scope

### 🔐 ETHICAL GUIDELINES

1. **Authorization First**
   - Never use on systems you don't own
   - Get written permission for testing
   - Stay within scope

2. **Data Handling**
   - Don't exfiltrate sensitive data
   - Report vulnerabilities found
   - Destroy harvested data after testing

3. **Impact Assessment**
   - Understand what features will break
   - Avoid destructive operations
   - Restore any changes made

4. **Professional Use**
   - Only for legitimate security work
   - Follow professional ethics codes (OSCP, CEH, etc.)
   - Document your activities

---

## 9. COMPLETE FEATURE LIST

### Network Discovery (1.py)
- [x] ARP scan
- [x] ICMP ping sweep
- [x] TCP port probe (50+ ports)
- [x] NetBIOS enumeration
- [x] mDNS discovery
- [x] SSDP/UPnP discovery
- [x] SNMP polling
- [x] Reverse DNS
- [x] HTTP fingerprinting
- [x] API endpoint detection
- [x] Device type classification
- [x] MAC vendor lookup
- [x] OS detection via TTL
- [x] Auto-network detection
- [x] Gateway identification
- [x] Multi-interface support

### Intelligence Gathering (2.py)
- [x] HTTP packet sniffing
- [x] Credential extraction (Basic Auth)
- [x] Cookie capture
- [x] FTP credential capture
- [x] Telnet session capture
- [x] SMTP command capture
- [x] DNS query logging
- [x] NTLM hash capture
- [x] WMI process listing
- [x] WMI user enumeration
- [x] WMI software listing
- [x] WMI service listing
- [x] WMI event log reading
- [x] WMI scheduled tasks
- [x] SMB share enumeration
- [x] SMB null session
- [x] Continuous monitoring

### Remote Control (3.py)
- [x] WMI command execution
- [x] Remote screenshot
- [x] Process listing
- [x] Process killing
- [x] Service control
- [x] Registry read/write
- [x] File upload/download
- [x] User enumeration
- [x] User creation
- [x] Remote shutdown/reboot
- [x] Wake-on-LAN
- [x] SSH command execution
- [x] SSH brute force
- [x] ADB Android control
- [x] Browser password extraction
- [x] WiFi password extraction
- [x] Clipboard access
- [x] System info gathering
- [x] RDP enable/disable
- [x] Firewall management
- [x] Persistence mechanisms
- [x] Scheduled task creation
- [x] Key injection
- [x] Mouse injection

### Exploitation (3.py)
- [x] SMB vulnerability check
- [x] MS17-010 detection
- [x] SSH brute force
- [x] Telnet brute force
- [x] RDP brute force
- [x] VNC brute force
- [x] FTP anonymous access
- [x] MySQL access
- [x] PostgreSQL access
- [x] MSSQL access
- [x] Network-wide attack automation

### Advanced Scanner (5.py)
- [x] Cross-subnet scanning
- [x] Traceroute
- [x] Service fingerprinting per hop
- [x] VPN detection
- [x] Cloud provider scanning
- [x] ASN lookup
- [x] Geolocation
- [x] NAT detection
- [x] Network topology mapping

### Command Center (6.py)
- [x] Session management
- [x] Multi-host execution
- [x] Lateral movement
- [x] Pivot chains
- [x] Payload generation
- [x] Credential harvesting
- [x] Interactive shells
- [x] Real-time dashboard

### Universal Access (7.py)
- [x] All-vector discovery
- [x] Auto-exploitation
- [x] Null session access
- [x] Default credential testing
- [x] Vulnerability scanning

---

## SUMMARY

The **Omniscience Framework** is a powerful network penetration testing toolkit with capabilities spanning:

- ✅ Network discovery (9 methods)
- ✅ Passive intelligence gathering
- ✅ Active reconnaissance
- ✅ Remote control (Windows/Linux)
- ✅ Exploitation and lateral movement
- ✅ Cloud and VPN detection
- ✅ Automated attack chains

### Where it can be applied:
- ✅ Authorized penetration testing
- ✅ Vulnerability assessment
- ✅ Red team operations
- ✅ Security research
- ❌ Unauthorized access
- ❌ Illegal surveillance
- ❌ Data theft

### Assessment:
This is a **professional-grade offensive security tool** that demonstrates real attack techniques. While valuable for legitimate security work, it contains dangerous capabilities that could be misused. **Always ensure proper written authorization** before using any of its capabilities on systems you don't own.

---

*Documentation generated from complete analysis of Omniscience Framework v5.0*
*Total code analyzed: ~8,000+ lines across 7 Python modules*
