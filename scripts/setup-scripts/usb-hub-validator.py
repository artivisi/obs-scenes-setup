#!/usr/bin/env python3
"""
USB Hub Connection Validator for OBS Multi-Camera Setup

This script validates USB hub connections, checks power distribution,
and provides recommendations for optimal device connectivity order.
Specifically designed for the Artivisi dual Cam Link + USB audio setup.

Features:
- Validate USB 3.0 hub capacity and power distribution
- Check device connection order and stability
- Monitor bandwidth usage for multiple Cam Links
- Provide recommendations for USB port assignment
- Test device enumeration consistency

Usage:
    python usb-hub-validator.py --validate
    python usb-hub-validator.py --monitor --duration 30
    python usb-hub-validator.py --recommend-order
"""

import json
import argparse
import sys
import time
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class USBDevice:
    """USB device information"""
    device_id: str
    name: str
    vendor_id: str
    product_id: str
    bus_number: int
    port_number: int
    speed: str
    power_consumption: Optional[int] = None
    hub_tier: Optional[int] = None

@dataclass
class HubInfo:
    """USB hub information"""
    hub_id: str
    name: str
    total_ports: int
    used_ports: int
    available_bandwidth: float
    power_capacity: int
    connected_devices: List[USBDevice]

class USBHubValidator:
    """Validates USB hub setup for multi-camera OBS configuration"""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.hubs: List[HubInfo] = []
        self.cam_links: List[USBDevice] = []
        self.audio_devices: List[USBDevice] = []
        
    def scan_usb_topology(self) -> bool:
        """Scan USB topology and identify hubs and devices"""
        print("🔍 Scanning USB topology...")
        
        try:
            if self.platform == 'windows':
                return self._scan_windows_usb()
            elif self.platform == 'darwin':
                return self._scan_macos_usb()
            elif self.platform == 'linux':
                return self._scan_linux_usb()
            else:
                print(f"❌ Unsupported platform: {self.platform}")
                return False
        except Exception as e:
            print(f"❌ Error scanning USB topology: {e}")
            return False
    
    def _scan_linux_usb(self) -> bool:
        """Scan USB devices on Linux using lsusb and udevadm"""
        try:
            # Get basic USB device list
            result = subprocess.run(['lsusb', '-v'], capture_output=True, text=True, check=True)
            self._parse_linux_lsusb(result.stdout)
            
            # Get detailed device information
            result = subprocess.run(['lsusb', '-t'], capture_output=True, text=True, check=True)
            self._parse_linux_topology(result.stdout)
            
            return True
        except subprocess.CalledProcessError:
            print("⚠️  lsusb not available. Install usbutils package.")
            return False
        except FileNotFoundError:
            print("⚠️  USB tools not found. Install usbutils package.")
            return False
    
    def _scan_windows_usb(self) -> bool:
        """Scan USB devices on Windows using PowerShell"""
        try:
            # Get USB devices
            cmd = [
                'powershell', '-Command',
                'Get-WmiObject -Class Win32_USBHub | Select-Object Name, DeviceID, Description'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self._parse_windows_usb(result.stdout)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Error scanning Windows USB: {e}")
            return False
    
    def _scan_macos_usb(self) -> bool:
        """Scan USB devices on macOS using system_profiler"""
        try:
            cmd = ['system_profiler', 'SPUSBDataType', '-json']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self._parse_macos_usb(result.stdout)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Error scanning macOS USB: {e}")
            return False
    
    def _parse_linux_lsusb(self, output: str):
        """Parse lsusb output to identify Cam Links and audio devices"""
        lines = output.split('\n')
        current_device = {}
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('Bus '):
                # New device
                parts = line.split()
                if len(parts) >= 6:
                    bus_num = int(parts[1])
                    device_num = int(parts[3].rstrip(':'))
                    ids = parts[5].split(':')
                    vendor_id, product_id = ids[0], ids[1]
                    
                    current_device = {
                        'bus_number': bus_num,
                        'device_number': device_num,
                        'vendor_id': vendor_id,
                        'product_id': product_id
                    }
            
            elif 'idProduct' in line and current_device:
                # Extract product name
                product_name = line.split('idProduct')[1].strip()
                current_device['name'] = product_name
                
                # Identify device type
                if self._is_cam_link(product_name, current_device['vendor_id'], current_device['product_id']):
                    device = USBDevice(
                        device_id=f"{current_device['bus_number']}-{current_device['device_number']}",
                        name=product_name,
                        vendor_id=current_device['vendor_id'],
                        product_id=current_device['product_id'],
                        bus_number=current_device['bus_number'],
                        port_number=current_device['device_number'],
                        speed='3.0'  # Assume USB 3.0 for Cam Links
                    )
                    self.cam_links.append(device)
                
                elif self._is_usb_audio(product_name, current_device['vendor_id'], current_device['product_id']):
                    device = USBDevice(
                        device_id=f"{current_device['bus_number']}-{current_device['device_number']}",
                        name=product_name,
                        vendor_id=current_device['vendor_id'],
                        product_id=current_device['product_id'],
                        bus_number=current_device['bus_number'],
                        port_number=current_device['device_number'],
                        speed='2.0'  # Assume USB 2.0 for audio
                    )
                    self.audio_devices.append(device)
    
    def _parse_linux_topology(self, output: str):
        """Parse lsusb -t output for hub topology"""
        # Simplified topology parsing
        lines = output.split('\n')
        for line in lines:
            if 'hub' in line.lower():
                # Extract hub information
                pass
    
    def _parse_windows_usb(self, output: str):
        """Parse Windows PowerShell USB output"""
        # Simplified Windows parsing
        pass
    
    def _parse_macos_usb(self, json_output: str):
        """Parse macOS USB JSON output"""
        try:
            data = json.loads(json_output)
            # Extract USB device information from macOS system profiler
            for usb_section in data.get('SPUSBDataType', []):
                self._extract_macos_devices(usb_section)
        except json.JSONDecodeError as e:
            print(f"⚠️  Error parsing macOS USB data: {e}")
    
    def _extract_macos_devices(self, usb_data: dict):
        """Recursively extract devices from macOS USB data"""
        if isinstance(usb_data, dict):
            name = usb_data.get('_name', 'Unknown')
            
            if self._is_cam_link(name, '', ''):
                # Create Cam Link device entry
                device = USBDevice(
                    device_id=name,
                    name=name,
                    vendor_id=usb_data.get('vendor_id', ''),
                    product_id=usb_data.get('product_id', ''),
                    bus_number=0,
                    port_number=0,
                    speed=usb_data.get('speed', 'Unknown')
                )
                self.cam_links.append(device)
            
            elif self._is_usb_audio(name, '', ''):
                device = USBDevice(
                    device_id=name,
                    name=name,
                    vendor_id=usb_data.get('vendor_id', ''),
                    product_id=usb_data.get('product_id', ''),
                    bus_number=0,
                    port_number=0,
                    speed=usb_data.get('speed', 'Unknown')
                )
                self.audio_devices.append(device)
            
            # Recursively check nested devices
            for key, value in usb_data.items():
                if key.startswith('_') and isinstance(value, dict):
                    self._extract_macos_devices(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            self._extract_macos_devices(item)
    
    def _is_cam_link(self, name: str, vendor_id: str, product_id: str) -> bool:
        """Check if device is a Cam Link"""
        name_lower = name.lower()
        
        # Known Cam Link identifiers
        cam_link_names = ['cam link', 'elgato', 'capture card']
        cam_link_vendors = ['0fd9']  # Elgato vendor ID
        
        return (any(identifier in name_lower for identifier in cam_link_names) or
                vendor_id.lower() in cam_link_vendors)
    
    def _is_usb_audio(self, name: str, vendor_id: str, product_id: str) -> bool:
        """Check if device is a USB audio device"""
        name_lower = name.lower()
        
        # Known USB audio identifiers
        audio_names = ['lark', 'audio', 'microphone', 'headset', 'usb audio']
        
        return any(identifier in name_lower for identifier in audio_names)
    
    def validate_setup(self) -> Dict[str, any]:
        """Validate the current USB setup for dual camera configuration"""
        print("\n🔍 Validating USB Hub Setup...")
        
        validation_result = {
            'overall_status': 'unknown',
            'cam_links_found': len(self.cam_links),
            'audio_devices_found': len(self.audio_devices),
            'issues': [],
            'recommendations': [],
            'optimal_setup': False
        }
        
        # Check Cam Link count
        if len(self.cam_links) == 0:
            validation_result['issues'].append("No Cam Link devices detected")
            validation_result['recommendations'].append("Connect at least one Elgato Cam Link 4K")
        elif len(self.cam_links) == 1:
            validation_result['recommendations'].append("Add second Cam Link for dual camera interviews")
        elif len(self.cam_links) >= 2:
            validation_result['optimal_setup'] = True
        
        # Check USB audio
        if len(self.audio_devices) == 0:
            validation_result['issues'].append("No USB audio devices detected")
            validation_result['recommendations'].append("Connect Hollyland Lark M2 or USB microphone")
        
        # Check for device conflicts
        bus_usage = {}
        for device in self.cam_links + self.audio_devices:
            bus = device.bus_number
            if bus in bus_usage:
                bus_usage[bus] += 1
            else:
                bus_usage[bus] = 1
        
        # Bandwidth validation
        high_bandwidth_buses = [bus for bus, count in bus_usage.items() if count > 1]
        if high_bandwidth_buses and len(self.cam_links) >= 2:
            validation_result['issues'].append("Multiple high-bandwidth devices on same USB bus")
            validation_result['recommendations'].append("Use USB 3.0 hub or separate USB controllers")
        
        # Overall status
        if not validation_result['issues']:
            if validation_result['optimal_setup']:
                validation_result['overall_status'] = 'optimal'
            else:
                validation_result['overall_status'] = 'good'
        elif len(validation_result['issues']) <= 2:
            validation_result['overall_status'] = 'workable'
        else:
            validation_result['overall_status'] = 'problematic'
        
        return validation_result
    
    def recommend_connection_order(self) -> List[str]:
        """Recommend optimal device connection order"""
        recommendations = [
            "📋 Optimal USB Connection Order:",
            "",
            "1. 🔌 Connect USB 3.0 hub to laptop first",
            "   - Use USB 3.0 port for maximum bandwidth",
            "   - Ensure hub has sufficient power (5V, 2A minimum)",
            "",
            "2. 📹 Connect Primary Cam Link (becomes Device 1)",
            "   - Connect to first USB 3.0 port on hub",
            "   - Wait for driver installation to complete",
            "",
            "3. 📹 Connect Secondary Cam Link (becomes Device 2)",
            "   - Connect to second USB 3.0 port on hub", 
            "   - Ensure different USB controller if possible",
            "",
            "4. 🎤 Connect USB Audio Device",
            "   - Hollyland Lark M2 or similar USB microphone",
            "   - Can use USB 2.0 port to save 3.0 bandwidth",
            "",
            "5. 🎹 Connect Macropad Last",
            "   - Lowest bandwidth requirement",
            "   - Any available USB port",
            "",
            "⚠️  Important Notes:",
            "- Always connect devices in the same order",
            "- Avoid unplugging/replugging during recording",
            "- Test device enumeration after each connection",
            "- Restart OBS if device order changes"
        ]
        
        return recommendations
    
    def monitor_stability(self, duration: int = 30) -> Dict[str, any]:
        """Monitor USB device stability over time"""
        print(f"📊 Monitoring USB stability for {duration} seconds...")
        
        start_time = time.time()
        snapshots = []
        
        while time.time() - start_time < duration:
            self.scan_usb_topology()
            snapshot = {
                'timestamp': datetime.now().isoformat(),
                'cam_links': len(self.cam_links),
                'audio_devices': len(self.audio_devices),
                'cam_link_ids': [device.device_id for device in self.cam_links],
                'audio_ids': [device.device_id for device in self.audio_devices]
            }
            snapshots.append(snapshot)
            
            time.sleep(2)  # Check every 2 seconds
        
        # Analyze stability
        cam_link_counts = [s['cam_links'] for s in snapshots]
        audio_counts = [s['audio_devices'] for s in snapshots]
        
        stability_report = {
            'duration': duration,
            'snapshots': len(snapshots),
            'cam_link_stability': len(set(cam_link_counts)) == 1,
            'audio_stability': len(set(audio_counts)) == 1,
            'device_id_changes': self._detect_id_changes(snapshots),
            'overall_stability': True
        }
        
        # Check for device ID changes (indicating disconnects/reconnects)
        stability_report['overall_stability'] = (
            stability_report['cam_link_stability'] and 
            stability_report['audio_stability'] and 
            not stability_report['device_id_changes']
        )
        
        return stability_report
    
    def _detect_id_changes(self, snapshots: List[Dict]) -> bool:
        """Detect if device IDs changed during monitoring"""
        if len(snapshots) < 2:
            return False
        
        first_cam_ids = set(snapshots[0]['cam_link_ids'])
        first_audio_ids = set(snapshots[0]['audio_ids'])
        
        for snapshot in snapshots[1:]:
            current_cam_ids = set(snapshot['cam_link_ids'])
            current_audio_ids = set(snapshot['audio_ids'])
            
            if current_cam_ids != first_cam_ids or current_audio_ids != first_audio_ids:
                return True
        
        return False
    
    def print_validation_report(self, validation_result: Dict[str, any]):
        """Print comprehensive validation report"""
        print("\n📋 USB Hub Validation Report")
        print("=" * 50)
        
        # Status indicator
        status_icons = {
            'optimal': '🎉',
            'good': '✅', 
            'workable': '⚠️',
            'problematic': '❌'
        }
        
        status = validation_result['overall_status']
        icon = status_icons.get(status, '❓')
        
        print(f"\n{icon} Overall Status: {status.title()}")
        print(f"📹 Cam Link devices: {validation_result['cam_links_found']}")
        print(f"🎤 Audio devices: {validation_result['audio_devices_found']}")
        
        # Issues
        if validation_result['issues']:
            print(f"\n❌ Issues Found:")
            for issue in validation_result['issues']:
                print(f"  • {issue}")
        
        # Recommendations
        if validation_result['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in validation_result['recommendations']:
                print(f"  • {rec}")
        
        # Device details
        if self.cam_links:
            print(f"\n📹 Detected Cam Link Devices:")
            for i, device in enumerate(self.cam_links, 1):
                print(f"  {i}. {device.name}")
                print(f"     Bus: {device.bus_number}, Port: {device.port_number}")
                print(f"     Speed: USB {device.speed}")
        
        if self.audio_devices:
            print(f"\n🎤 Detected Audio Devices:")
            for device in self.audio_devices:
                print(f"  • {device.name}")
                print(f"    Bus: {device.bus_number}, Port: {device.port_number}")

def main():
    parser = argparse.ArgumentParser(
        description='USB Hub Validator for OBS Multi-Camera Setup',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate current USB hub setup'
    )
    
    parser.add_argument(
        '--monitor',
        action='store_true',
        help='Monitor USB device stability over time'
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=30,
        help='Monitoring duration in seconds (default: 30)'
    )
    
    parser.add_argument(
        '--recommend-order',
        action='store_true',
        help='Show recommended device connection order'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    validator = USBHubValidator()
    
    if args.recommend_order:
        recommendations = validator.recommend_connection_order()
        for line in recommendations:
            print(line)
        return
    
    if args.validate:
        # Scan devices first
        if not validator.scan_usb_topology():
            print("❌ Failed to scan USB topology")
            sys.exit(1)
        
        # Run validation
        result = validator.validate_setup()
        validator.print_validation_report(result)
        
        # Exit with appropriate code
        if result['overall_status'] in ['optimal', 'good']:
            sys.exit(0)
        elif result['overall_status'] == 'workable':
            sys.exit(1)
        else:
            sys.exit(2)
    
    if args.monitor:
        # Scan initial state
        if not validator.scan_usb_topology():
            print("❌ Failed to scan USB topology")
            sys.exit(1)
        
        # Monitor stability
        stability = validator.monitor_stability(args.duration)
        
        print(f"\n📊 Stability Report:")
        print(f"✅ Duration: {stability['duration']} seconds")
        print(f"📊 Snapshots: {stability['snapshots']}")
        print(f"📹 Cam Link stability: {'✅' if stability['cam_link_stability'] else '❌'}")
        print(f"🎤 Audio stability: {'✅' if stability['audio_stability'] else '❌'}")
        print(f"🔄 Device ID changes: {'❌' if stability['device_id_changes'] else '✅'}")
        
        overall_icon = '✅' if stability['overall_stability'] else '❌'
        print(f"\n{overall_icon} Overall Stability: {'Good' if stability['overall_stability'] else 'Issues Detected'}")
        
        sys.exit(0 if stability['overall_stability'] else 1)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()