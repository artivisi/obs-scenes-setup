#!/usr/bin/env python3
"""
Cross-Platform Device Management for OBS Setup

This script handles device detection, USB hub management, and cross-platform
compatibility for the Artivisi OBS tutorial setup. It automatically detects
cameras, microphones, and other devices across Windows, macOS, and Linux.

Features:
- Auto-detect Cam Link 4K devices (primary and secondary)
- Find USB audio devices (Hollyland Lark M2, etc.)
- Generate platform-specific OBS profiles
- Handle device connection order and USB port consistency
- Provide fallback options for built-in devices

Usage:
    python device-manager.py --scan
    python device-manager.py --generate-profile --platform windows
    python device-manager.py --test-devices
"""

import json
import argparse
import sys
import os
import platform
import subprocess
import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple

@dataclass
class DeviceInfo:
    """Information about a detected device"""
    device_id: str
    name: str
    type: str  # 'video', 'audio_input', 'audio_output'
    platform_path: str
    is_usb: bool
    vendor_id: Optional[str] = None
    product_id: Optional[str] = None
    description: Optional[str] = None

class DeviceManager:
    """Cross-platform device detection and management"""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.devices = {
            'video': [],
            'audio_input': [],
            'audio_output': []
        }
        
    def scan_devices(self) -> Dict[str, List[DeviceInfo]]:
        """Scan for all available devices on the current platform"""
        print(f"🔍 Scanning devices on {self.platform.title()}...")
        
        if self.platform == 'windows':
            return self._scan_windows()
        elif self.platform == 'darwin':  # macOS
            return self._scan_macos()
        elif self.platform == 'linux':
            return self._scan_linux()
        else:
            print(f"❌ Unsupported platform: {self.platform}")
            return self.devices
    
    def _scan_windows(self) -> Dict[str, List[DeviceInfo]]:
        """Scan devices on Windows using PowerShell"""
        try:
            # Video devices
            video_cmd = [
                'powershell', '-Command',
                'Get-WmiObject -Class Win32_PnPEntity | Where-Object {$_.Name -like "*camera*" -or $_.Name -like "*capture*" -or $_.Name -like "*cam link*"} | Select-Object Name, DeviceID, Description'
            ]
            result = subprocess.run(video_cmd, capture_output=True, text=True, check=True)
            self._parse_windows_devices(result.stdout, 'video')
            
            # Audio devices
            audio_cmd = [
                'powershell', '-Command',
                'Get-WmiObject -Class Win32_SoundDevice | Select-Object Name, DeviceID, Description'
            ]
            result = subprocess.run(audio_cmd, capture_output=True, text=True, check=True)
            self._parse_windows_devices(result.stdout, 'audio_input')
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Error scanning Windows devices: {e}")
        
        return self.devices
    
    def _scan_macos(self) -> Dict[str, List[DeviceInfo]]:
        """Scan devices on macOS using system_profiler"""
        try:
            # Video devices
            video_cmd = ['system_profiler', 'SPCameraDataType', '-json']
            result = subprocess.run(video_cmd, capture_output=True, text=True, check=True)
            self._parse_macos_video_devices(result.stdout)
            
            # Audio devices
            audio_cmd = ['system_profiler', 'SPAudioDataType', '-json']
            result = subprocess.run(audio_cmd, capture_output=True, text=True, check=True)
            self._parse_macos_audio_devices(result.stdout)
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Error scanning macOS devices: {e}")
        
        return self.devices
    
    def _scan_linux(self) -> Dict[str, List[DeviceInfo]]:
        """Scan devices on Linux using v4l2 and arecord"""
        try:
            # Video devices
            video_cmd = ['v4l2-ctl', '--list-devices']
            result = subprocess.run(video_cmd, capture_output=True, text=True, check=True)
            self._parse_linux_video_devices(result.stdout)
            
            # Audio devices
            audio_cmd = ['arecord', '-l']
            result = subprocess.run(audio_cmd, capture_output=True, text=True, check=True)
            self._parse_linux_audio_devices(result.stdout)
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Error scanning Linux devices: {e}")
        except FileNotFoundError:
            print("⚠️  v4l2-ctl or arecord not found. Install v4l-utils and alsa-utils.")
        
        return self.devices
    
    def _parse_windows_devices(self, output: str, device_type: str):
        """Parse Windows PowerShell device output"""
        lines = output.strip().split('\n')
        current_device = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('Name'):
                current_device['name'] = line.split(':', 1)[1].strip()
            elif line.startswith('DeviceID'):
                current_device['device_id'] = line.split(':', 1)[1].strip()
            elif line.startswith('Description'):
                current_device['description'] = line.split(':', 1)[1].strip()
                
                # Complete device info
                if 'name' in current_device and 'device_id' in current_device:
                    device = DeviceInfo(
                        device_id=current_device['device_id'],
                        name=current_device['name'],
                        type=device_type,
                        platform_path=current_device['device_id'],
                        is_usb='USB' in current_device.get('description', ''),
                        description=current_device.get('description')
                    )
                    self.devices[device_type].append(device)
                current_device = {}
    
    def _parse_macos_video_devices(self, json_output: str):
        """Parse macOS video device JSON output"""
        try:
            data = json.loads(json_output)
            for camera_info in data.get('SPCameraDataType', []):
                device = DeviceInfo(
                    device_id=camera_info.get('_name', 'Unknown'),
                    name=camera_info.get('_name', 'Unknown Camera'),
                    type='video',
                    platform_path=camera_info.get('_name', ''),
                    is_usb='USB' in camera_info.get('_name', ''),
                    description=camera_info.get('_name')
                )
                self.devices['video'].append(device)
        except json.JSONDecodeError as e:
            print(f"⚠️  Error parsing macOS video devices: {e}")
    
    def _parse_macos_audio_devices(self, json_output: str):
        """Parse macOS audio device JSON output"""
        try:
            data = json.loads(json_output)
            for audio_section in data.get('SPAudioDataType', []):
                for device_name, device_info in audio_section.items():
                    if isinstance(device_info, dict):
                        device = DeviceInfo(
                            device_id=device_name,
                            name=device_name,
                            type='audio_input',
                            platform_path=device_name,
                            is_usb='USB' in device_name,
                            description=device_name
                        )
                        self.devices['audio_input'].append(device)
        except json.JSONDecodeError as e:
            print(f"⚠️  Error parsing macOS audio devices: {e}")
    
    def _parse_linux_video_devices(self, output: str):
        """Parse Linux v4l2-ctl output"""
        lines = output.split('\n')
        current_name = None
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('\t'):
                current_name = line.rstrip(':')
            elif line.startswith('\t/dev/video'):
                device_path = line.strip()
                device = DeviceInfo(
                    device_id=device_path,
                    name=current_name or 'Unknown Camera',
                    type='video',
                    platform_path=device_path,
                    is_usb='usb' in current_name.lower() if current_name else False,
                    description=current_name
                )
                self.devices['video'].append(device)
    
    def _parse_linux_audio_devices(self, output: str):
        """Parse Linux arecord -l output"""
        for line in output.split('\n'):
            if line.startswith('card'):
                match = re.search(r'card (\d+): (.+?) \[(.+?)\]', line)
                if match:
                    card_id, device_name, device_desc = match.groups()
                    device = DeviceInfo(
                        device_id=f"hw:{card_id}",
                        name=device_name,
                        type='audio_input',
                        platform_path=f"hw:{card_id}",
                        is_usb='USB' in device_desc,
                        description=device_desc
                    )
                    self.devices['audio_input'].append(device)
    
    def find_cam_links(self) -> List[DeviceInfo]:
        """Find all Cam Link devices (primary and secondary)"""
        cam_links = []
        
        for device in self.devices['video']:
            name_lower = device.name.lower()
            if 'cam link' in name_lower or 'elgato' in name_lower:
                cam_links.append(device)
        
        return sorted(cam_links, key=lambda x: x.device_id)
    
    def find_usb_audio_devices(self) -> List[DeviceInfo]:
        """Find USB audio devices (like Hollyland Lark M2)"""
        usb_audio = []
        
        for device in self.devices['audio_input']:
            if device.is_usb:
                usb_audio.append(device)
        
        return usb_audio
    
    def generate_obs_profile(self, profile_name: str, output_path: Path) -> bool:
        """Generate OBS profile configuration with detected devices"""
        cam_links = self.find_cam_links()
        usb_audio = self.find_usb_audio_devices()
        
        # Basic profile template
        profile_config = {
            "name": profile_name,
            "platform": self.platform,
            "video_devices": {},
            "audio_devices": {},
            "fallback_devices": {},
            "device_priorities": {}
        }
        
        # Configure primary and secondary cameras
        if len(cam_links) >= 1:
            profile_config["video_devices"]["primary_camera"] = {
                "device_id": cam_links[0].device_id,
                "name": cam_links[0].name,
                "resolution": "1920x1080",
                "framerate": "30"
            }
        
        if len(cam_links) >= 2:
            profile_config["video_devices"]["secondary_camera"] = {
                "device_id": cam_links[1].device_id,
                "name": cam_links[1].name,
                "resolution": "1920x1080",
                "framerate": "30"
            }
        
        # Configure USB audio
        if usb_audio:
            profile_config["audio_devices"]["primary_microphone"] = {
                "device_id": usb_audio[0].device_id,
                "name": usb_audio[0].name,
                "sample_rate": "48000"
            }
        
        # Add fallback devices
        video_devices = [d for d in self.devices['video'] if d not in cam_links]
        if video_devices:
            profile_config["fallback_devices"]["camera"] = {
                "device_id": video_devices[0].device_id,
                "name": video_devices[0].name
            }
        
        audio_devices = [d for d in self.devices['audio_input'] if not d.is_usb]
        if audio_devices:
            profile_config["fallback_devices"]["microphone"] = {
                "device_id": audio_devices[0].device_id,
                "name": audio_devices[0].name
            }
        
        # Write profile
        try:
            with open(output_path, 'w') as f:
                json.dump(profile_config, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"❌ Error writing profile: {e}")
            return False
    
    def print_device_report(self):
        """Print a comprehensive device report"""
        print("\n📱 Device Detection Report")
        print("=" * 50)
        
        # Cam Link devices
        cam_links = self.find_cam_links()
        print(f"\n📹 Cam Link Devices ({len(cam_links)} found):")
        if cam_links:
            for i, device in enumerate(cam_links, 1):
                print(f"  {i}. {device.name}")
                print(f"     ID: {device.device_id}")
                print(f"     Path: {device.platform_path}")
        else:
            print("  ⚠️  No Cam Link devices detected")
            print("     - Check USB connections")
            print("     - Ensure Elgato software is installed")
        
        # USB Audio devices
        usb_audio = self.find_usb_audio_devices()
        print(f"\n🎤 USB Audio Devices ({len(usb_audio)} found):")
        if usb_audio:
            for device in usb_audio:
                print(f"  • {device.name}")
                print(f"    ID: {device.device_id}")
        else:
            print("  ⚠️  No USB audio devices detected")
            print("     - Check Hollyland Lark M2 connection")
            print("     - Verify USB audio drivers")
        
        # All video devices
        print(f"\n📷 All Video Devices ({len(self.devices['video'])} found):")
        for device in self.devices['video']:
            status = "🔗 USB" if device.is_usb else "🖥️ Built-in"
            print(f"  {status} {device.name}")
        
        # All audio input devices
        print(f"\n🎧 All Audio Input Devices ({len(self.devices['audio_input'])} found):")
        for device in self.devices['audio_input']:
            status = "🔗 USB" if device.is_usb else "🖥️ Built-in"
            print(f"  {status} {device.name}")
        
        # Recommendations
        print(f"\n💡 Setup Recommendations:")
        if len(cam_links) == 0:
            print("  ❌ No Cam Link devices found - single camera setup only")
        elif len(cam_links) == 1:
            print("  ✅ Single Cam Link found - solo tutorial setup ready")
            print("  💡 Add second Cam Link for guest interviews")
        else:
            print("  ✅ Multiple Cam Link devices - dual camera setup ready")
        
        if len(usb_audio) == 0:
            print("  ⚠️  No USB audio found - using built-in microphone")
        else:
            print("  ✅ USB audio device found - professional audio ready")
        
        print(f"\n🔧 Platform: {self.platform.title()}")
        print(f"📁 Next Step: Generate OBS profile with detected devices")

def main():
    parser = argparse.ArgumentParser(
        description='Cross-platform device management for OBS setup',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python device-manager.py --scan
  python device-manager.py --generate-profile --platform windows
  python device-manager.py --test-devices --verbose
        """
    )
    
    parser.add_argument(
        '--scan',
        action='store_true',
        help='Scan and report all detected devices'
    )
    
    parser.add_argument(
        '--generate-profile',
        action='store_true',
        help='Generate OBS profile with detected devices'
    )
    
    parser.add_argument(
        '--platform',
        choices=['windows', 'macos', 'linux', 'auto'],
        default='auto',
        help='Target platform (auto-detect if not specified)'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        help='Output path for generated profile'
    )
    
    parser.add_argument(
        '--test-devices',
        action='store_true',
        help='Test device connectivity and functionality'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Initialize device manager
    manager = DeviceManager()
    
    if args.scan or args.generate_profile or args.test_devices:
        # Scan for devices
        devices = manager.scan_devices()
        
        if args.scan:
            manager.print_device_report()
        
        if args.generate_profile:
            # Determine output path
            if args.output:
                output_path = args.output
            else:
                script_dir = Path(__file__).parent
                profiles_dir = script_dir.parent.parent / 'profiles'
                profiles_dir.mkdir(exist_ok=True)
                platform_name = args.platform if args.platform != 'auto' else manager.platform
                output_path = profiles_dir / f'{platform_name}-devices.json'
            
            # Generate profile
            profile_name = f"Artivisi Tutorial Setup - {manager.platform.title()}"
            success = manager.generate_obs_profile(profile_name, output_path)
            
            if success:
                print(f"\n✅ Profile generated: {output_path}")
                print(f"📋 Import this into your OBS scene collection setup")
            else:
                print(f"\n❌ Failed to generate profile")
                sys.exit(1)
        
        if args.test_devices:
            # Basic device testing
            cam_links = manager.find_cam_links()
            usb_audio = manager.find_usb_audio_devices()
            
            print(f"\n🧪 Device Testing Results:")
            print(f"✅ Cam Link devices: {len(cam_links)} detected")
            print(f"✅ USB audio devices: {len(usb_audio)} detected")
            
            if len(cam_links) >= 2 and len(usb_audio) >= 1:
                print(f"🎉 Full dual-camera interview setup ready!")
            elif len(cam_links) >= 1 and len(usb_audio) >= 1:
                print(f"✅ Single-camera tutorial setup ready!")
            else:
                print(f"⚠️  Setup incomplete - check device connections")
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()