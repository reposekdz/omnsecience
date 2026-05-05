# OMNISCIENCE FRAMEWORK v7.1.002 ULTRAMAX PRO - OFFICIAL DOCUMENTATION

Welcome to the **Omniscience Documentation**. This guide provides a comprehensive breakdown of the framework's architecture, capabilities, and every command available in the Master Shell (`4.py`).

## 1. System Architecture

The Omniscience framework is designed as a modular, agentless offensive security platform.

- **Module 1 (NetworkDiscovery)**: Advanced reconnaissance. Multi-vector discovery (ARP, ICMP, SNMP, mDNS, SSDP, DNS-PTR).
- **Module 2 (PassiveIntel)**: Passive NTLM extraction, traffic analysis, and WMI monitoring.
- **Module 3 (AgentlessControl)**: Full RCE via WMI/WinRM/SSH. No target software required.
- **Module 4 (OmniShell)**: The Command Center. Real-time orchestration.
- **Module 5 (AdvancedScanner)**: Cross-subnet and BGP/ASN topology mapping.
- **Module 6 (LateralMovement)**: Pivoting, Credential Relaying (NTLM/SMB).
- **Module 7 (ExploitEngine)**: Real-time CVE execution (EternalBlue, SMBGhost, etc.).

---

## 2. Global Discovery Commands

Discovery commands are used to map networks and identify targets across LAN, WAN, and PAN.

| Command | Description |
| :--- | :--- |
| `scan [range]` | Performs a Layer-2 ARP scan. High speed, low noise. |
| `auto` | Auto-detects all network interfaces and sweeps all reachable ranges. |
| `discover [range]` | Runs a full multi-vector discovery sequence on a specific range. |
| `globalscan` | Global high-IQ discovery. Probes all interfaces, VPNs, and common subnets. |
| `network` | Shows detailed configuration for your local interfaces and gateway. |
| `arp [range]` | Standalone ARP scan. |
| `icmp [range]` | ICMP Ping sweep for Layer-3 discovery. |
| `snmp <ip>` | Non-blocking SNMP query for system metadata (sysDescr, sysName). |
| `mdns` / `ssdp` | Passive and active listener for multicast broadcast services (IoT/AV). |
| `http <ip>` | Fingerprints web services, titles, and potential API endpoints. |

---

## 3. Passive Intelligence Commands

These commands gather data without sending packets to the target (MITM) or by querying remote management logs.

| Command | Description |
| :--- | :--- |
| `sniff [iface]` | Starts the NTLM hash extractor and general packet sniffer. |
| `stopsniff` | Ceases all background sniffing operations. |
| `creds` | Lists all captured credentials (NTLM, HTTP, Telnet, etc.). |
| `dnslog` | Displays a live log of DNS queries captured on the network. |
| `wmi-log <ip> <u> <p>` | Streams remote Windows Security/System event logs live. |
| `monitor <ip> <u> <p>` | Continuously polls for process and network changes on a remote host. |
| `intercepts` | Lists all active Man-in-the-Middle (ARP Spoofing) sessions. |

---

## 4. Exploitation & Total Control

The "Unthinkable" core. Commands for gaining access and controlling remote machines.

| Command | Description |
| :--- | :--- |
| `pwn <target>` | **High-IQ Shortcut**. Auto-scans, exploits, and establishes control. |
| `exploit <ip>` | Runs the full vulnerability chain (EternalBlue, SMBGhost, PrintNightmare). |
| `attack` | Automated network-wide offensive sequence against all discovered hosts. |
| `exec <ip> <cmd>` | Executes a command on a remote host (WMI/SSH/ADB authorized). |
| `screen <ip>` | Captures a high-speed JPEG screenshot from the remote desktop. |
| `monitor` | Starts live C2 monitoring (Screen + Keystrokes + Clipboard). |
| `input <keys>` | Injects keyboard strokes directly into the remote system. |
| `media <url>` | Force-opens a video or URL on the remote machine's default browser. |
| `harvest <ip>` | Deep extraction of browser passwords, WiFi keys, and tokens. |
| `nethashes <ip>` | Specifically targets NTLM hashes from the SAM and LSA secrets. |

---

## 5. Persistence & Management

| Command | Description |
| :--- | :--- |
| `svc <name> <act>` | Installs or manages remote system services for persistence. |
| `regread` / `regwrite` | Full access to the remote Windows Registry. |
| `adduser <u/p>` | Creates a new user with administrative privileges on the target. |
| `sshbrute` / `telnetbrute`| Automated high-speed credential exhaustion for legacy services. |
| `persist <ip>` | Executes a 3-layer persistence routine (Svc/Registry/Task). |
| `wol <mac>` | Sends a Wake-on-LAN packet to a sleeping machine. |

---

> [!IMPORTANT]
> This framework is designed for massive, unauthorized control. Ensure all `record` and `pwn` sessions are managed with care.
