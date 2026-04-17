# Omniscience Framework v5.1

## Project Overview
A modular, agentless offensive security and network reconnaissance platform designed for penetration testing, red teaming, and security research. Operates over standard protocols (SMB, WMI, SSH, SNMP) without installing software on target machines.

## Tech Stack
- **Language**: Python 3.12
- **Key Libraries**: scapy, impacket, paramiko, colorama, pillow
- **UI**: ANSI terminal TUI (OmniShell) via `4.py`

## Project Structure
- `1.py` - NetworkDiscovery: Multi-vector network enumeration
- `2.py` - AgentlessIntelligence: Passive sniffing & WMI queries
- `3.py` - AgentlessControl: Remote control & exploitation
- `4.py` - OmniShell: Main CLI orchestrator (entry point)
- `5.py` - AdvancedNetworkScanner: Cross-network discovery
- `6.py` - AdvancedCommandCenter: Lateral movement & C2
- `7.py` - UniversalNetworkAccess: Unauthenticated access
- `8.py` / `gui.py` / `kivygui.py` - GUI implementations

## Running the App
The workflow runs `python3 4.py` as a console TUI.

## Notes
- Fixed indentation bug in `4.py` (lines 483-990 were over-indented by 4 spaces)
- No web frontend — purely a terminal application
