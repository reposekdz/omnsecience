# OMNISCIENCE FRAMEWORK v4.0 - OFFICIAL DOCUMENTATION

Welcome to the **Omniscience Documentation**. This guide provides a comprehensive breakdown of the framework's architecture, capabilities, and every command available in the Master Shell (`4.py`).

## 1. System Architecture

The Omniscience framework is designed as a modular, agentless offensive security platform.

- **1.py (NetworkDiscovery)**: The tactical eyes. Handles multi-vector discovery (ARP, ICMP, SNMP, mDNS, SSDP, DNS, Port Probing).
- **2.py (AgentlessIntelligence)**: The silent observer. Performs passive sniffing, NTLM hash extraction, and remote host monitoring via WMI.
- **3.py (AgentlessControl)**: The iron fist. Orchestrates unauthenticated exploitation, background recording, input injection, and system management.
- **4.py (OmniShell)**: The command center. A unified interface that synchronizes all modules into a high-speed attack desk.

---

## 2. Global Discovery Commands

Discovery commands are used to map networks and identify targets across LAN, WAN, and PAN.

| Command | Description |
| :--- | :--- |
| `scan [range]` | Performs a Layer-2 ARP scan. High speed, low noise. |
| `auto` | Auto-detects all network interfaces and sweeps all reachable ranges. |
| `discover [range]` | Runs a full multi-vector discovery sequence on a specific range. |
| `autoscan` | Global high-IQ discovery. Probes all interfaces and common subnets. |
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
| `exploit <ip>` | Tries all unauthenticated methods (SMB Null, EternalBlue, Defaults). |
| `attack` | Automated network-wide offensive sequence against all discovered hosts. |
| `exec <ip> <cmd>` | Executes a command on a remote host (WMI/SSH/ADB authorized). |
| `screen <ip>` | Captures a high-speed JPEG screenshot from the remote desktop. |
| `record` | Starts background screen recording (timestamped JPEG sequences). |
| `input <keys>` | Injects keyboard strokes directly into the remote system. |
| `media <url>` | Force-opens a video or URL on the remote machine's default browser. |
| `stealcreds <ip>` | Extracts all saved passwords and hashes from the target system. |
| `nethashes <ip>` | Specifically targets NTLM hashes from the SAM and LSA secrets. |

---

## 5. Persistence & Management

| Command | Description |
| :--- | :--- |
| `svc <name> <act>` | Starts, stops, or restarts remote system services. |
| `regread` / `regwrite` | Full access to the remote Windows Registry. |
| `adduser <u/p>` | Creates a new user with administrative privileges on the target. |
| `sshbrute` / `telnetbrute`| Automated high-speed credential exhaustion for legacy services. |
| `wol <mac>` | Sends a Wake-on-LAN packet to a sleeping machine. |

---

> [!IMPORTANT]
> This framework is designed for massive, unauthorized control. Ensure all `record` and `pwn` sessions are managed with care.
