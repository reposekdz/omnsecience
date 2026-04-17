# Omniscience Framework v5.1

## Project Overview
A modular, agentless offensive security and network reconnaissance platform designed for penetration testing, red teaming, and security research. Operates over standard protocols (SMB, WMI, SSH, SNMP, WinRM, DCOM) without installing software on target machines.

## Tech Stack
- **Language**: Python 3.12
- **Key Libraries**: scapy, impacket, paramiko, colorama, pillow, pymysql, psycopg2
- **UI**: ANSI terminal TUI (OmniShell) via `commandcenter.py`

## Project Structure

### Core Modules
| File | Name | Description |
|------|------|-------------|
| `commandcenter.py` | OmniShell | Main CLI orchestrator — **entry point** |
| `network_discovery.py` | NetworkDiscovery | Multi-vector network enumeration (ARP, ICMP, TCP, NetBIOS, mDNS, SSDP, SNMP, DNS-PTR) |
| `passive_intel.py` | AgentlessIntelligence | Passive sniffing, WMI queries, SMB share enum, SNMP polling |
| `remote_control.py` | AgentlessControl | Full remote control via WMI/DCOM/SMB/WinRM/SSH — no agent needed |
| `advanced_scanner.py` | AdvancedNetworkScanner | Cross-subnet, BGP/AS, VPN, traceroute, WAN/LAN topology |
| `lateral_movement.py` | AdvancedCommandCenter | Lateral movement, pivoting, session management, C2 |
| `exploit_engine.py` | UniversalNetworkAccess | Unauthenticated access, Win7–Win11 vuln checks (EternalBlue, BlueKeep, SMBGhost, PrintNightmare, PetitPotam, Zerologon, NoPac) |

### GUI Modules
| File | Description |
|------|-------------|
| `gui_panel.py` / `gui.py` | Tkinter-based GUI (desktop) |
| `gui_manager.py` | Advanced GUI with extended features |
| `mobile_gui.py` / `kivygui.py` | Kivy-based mobile/touch GUI |

### Support Files
| File | Description |
|------|-------------|
| `main.py` | Thin entry point — loads and runs commandcenter.py |
| `setup_wizard.py` | First-run setup wizard |
| `installer.py` | Dependency installer |
| `cross_platform_builder.py` | PyInstaller build helper |

## Module Loading
All modules are loaded dynamically via `get_module()` with a `_MODULE_MAP` lookup:
```python
_MODULE_MAP = {
    "1": "network_discovery",
    "2": "passive_intel",
    "3": "remote_control",
    "5": "advanced_scanner",
    "6": "lateral_movement",
    "7": "exploit_engine",
}
```
This means old numeric references still work as fallbacks.

## Running the App
The workflow runs `python3 commandcenter.py` as a console TUI.

## Key Features Added
- `get_browser_passwords()` — Real Chrome/Edge/Firefox DPAPI password extraction via WMI/PowerShell
- `get_wifi_passwords()` — Real `netsh wlan show profile key=clear` extraction via WMI
- `lsass_dump()` — Real LSASS dump via comsvcs.dll MiniDump over WMI
- Win10/11 exploit checks: SMBGhost, PrintNightmare, PetitPotam, Zerologon, NoPac, WinRM exec
- All dispatch commands wired: `steal-wifi`, `lsass-dump`, `tokens`, `mysql-root`, `postgres`, `scan-exploit`, `vnc-brute`, `telnet-brute`

## Notes
- No web frontend — purely a terminal application
- Requires SYSTEM or admin credentials for most control/exploitation operations
- MySQL/PostgreSQL access uses `pymysql`/`psycopg2` when installed
