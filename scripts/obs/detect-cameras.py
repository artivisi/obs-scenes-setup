#!/usr/bin/env python3
"""
OBS Camera Detection and Configuration Script

Detects available cameras and provides OBS WebSocket commands to add them
to your scenes automatically.
"""

import subprocess
import platform
import json
import sys
from pathlib import Path

# Check for OBS WebSocket dependency
try:
    import obsws_python as obs
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    print("⚠️  obsws-python not installed. Install with: pip install --break-system-packages obsws-python")

def detect_cameras():
    """Detect available cameras on the system"""
    cameras = []
    system = platform.system().lower()
    
    print("🔍 Detecting cameras...")
    
    if system == "linux":
        try:
            # List video devices in /dev
            result = subprocess.run(
                ["ls", "/dev/video*"], 
                capture_output=True, text=True, check=False
            )
            
            if result.returncode == 0:
                devices = result.stdout.strip().split('\n')
                for device in devices:
                    if device:
                        # Get device info
                        try:
                            info_result = subprocess.run(
                                ["v4l2-ctl", "--device", device, "--info"],
                                capture_output=True, text=True, check=False
                            )
                            
                            device_name = device
                            if "Card type" in info_result.stdout:
                                for line in info_result.stdout.split('\n'):
                                    if "Card type" in line:
                                        device_name = line.split(':')[1].strip()
                                        break
                            
                            cameras.append({
                                'device_path': device,
                                'name': device_name,
                                'obs_kind': 'v4l2_source'
                            })
                            print(f"📹 Found: {device_name} ({device})")
                        except:
                            cameras.append({
                                'device_path': device,
                                'name': f"Camera {device}",
                                'obs_kind': 'v4l2_source'
                            })
                            print(f"📹 Found: Camera {device}")
                            
        except Exception as e:
            print(f"⚠️  Error detecting Linux cameras: {e}")
            
    elif system == "windows":
        try:
            # Use PowerShell to detect cameras
            result = subprocess.run([
                "powershell", "-Command",
                "Get-CimInstance -ClassName Win32_PnPEntity | Where-Object {$_.PNPClass -eq 'Camera' -or $_.Name -like '*camera*' -or $_.Name -like '*webcam*'} | Select-Object Name, DeviceID"
            ], capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines[2:]:  # Skip headers
                    if line.strip():
                        parts = line.split()
                        if len(parts) > 0:
                            camera_name = ' '.join(parts[:-1]) if len(parts) > 1 else parts[0]
                            cameras.append({
                                'device_path': camera_name,
                                'name': camera_name,
                                'obs_kind': 'dshow_input'
                            })
                            print(f"📹 Found: {camera_name}")
                            
        except Exception as e:
            print(f"⚠️  Error detecting Windows cameras: {e}")
            
    elif system == "darwin":  # macOS
        try:
            # Use system_profiler to detect cameras
            result = subprocess.run([
                "system_profiler", "SPCameraDataType", "-json"
            ], capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for camera_type in data.get('SPCameraDataType', []):
                    for camera in camera_type.get('_items', []):
                        camera_name = camera.get('_name', 'Unknown Camera')
                        cameras.append({
                            'device_path': camera_name,
                            'name': camera_name,
                            'obs_kind': 'av_capture_input'
                        })
                        print(f"📹 Found: {camera_name}")
                        
        except Exception as e:
            print(f"⚠️  Error detecting macOS cameras: {e}")
    
    if not cameras:
        print("❌ No cameras detected")
        # Add common fallback options
        if system == "linux":
            cameras.append({
                'device_path': '/dev/video0',
                'name': 'Default Camera',
                'obs_kind': 'v4l2_source'
            })
        elif system == "windows":
            cameras.append({
                'device_path': 'Default',
                'name': 'Default Camera',
                'obs_kind': 'dshow_input'
            })
        elif system == "darwin":
            cameras.append({
                'device_path': 'Default',
                'name': 'Default Camera', 
                'obs_kind': 'av_capture_input'
            })
    
    return cameras

def add_cameras_to_obs(cameras, obs_host="localhost", obs_port=4455, obs_password=""):
    """Add detected cameras to OBS scenes"""
    if not WEBSOCKET_AVAILABLE:
        print("❌ Cannot connect to OBS - obsws-python not available")
        return False
        
    try:
        print(f"🔌 Connecting to OBS at {obs_host}:{obs_port}")
        client = obs.ReqClient(host=obs_host, port=obs_port, password=obs_password)
        
        # Test connection
        version_info = client.get_version()
        print(f"✅ Connected to OBS Studio {version_info.obs_version}")
        
        # Get scenes that need cameras
        scene_list = client.get_scene_list()
        camera_scenes = []
        
        for scene in scene_list.scenes:
            scene_name = scene['sceneName']
            # Check for scene keywords (handle emoji names)
            scene_lower = scene_name.lower()
            if any(keyword in scene_lower for keyword in ['intro', 'talking', 'code', 'outro', 'dual', 'camera']):
                camera_scenes.append(scene_name)
                print(f"  📋 Found camera scene: {scene_name}")
        
        print(f"📋 Found {len(camera_scenes)} scenes that need cameras")
        
        # Add primary camera to scenes
        primary_camera = cameras[0] if cameras else None
        if primary_camera:
            for scene_name in camera_scenes:
                try:
                    print(f"📷 Adding {primary_camera['name']} to {scene_name}")
                    
                    settings = {}
                    if primary_camera['obs_kind'] == 'v4l2_source':
                        settings['device_id'] = primary_camera['device_path']
                    elif primary_camera['obs_kind'] == 'dshow_input':
                        settings['video_device_id'] = primary_camera['device_path']
                    elif primary_camera['obs_kind'] == 'av_capture_input':
                        settings['device'] = primary_camera['device_path']
                    
                    client.create_input(
                        inputName="Main Camera",
                        inputKind=primary_camera['obs_kind'],
                        inputSettings=settings,
                        sceneName=scene_name,
                        sceneItemEnabled=True
                    )
                    print(f"  ✅ Added to {scene_name}")
                    
                except Exception as e:
                    print(f"  ⚠️  Could not add to {scene_name}: {e}")
        
        # Add secondary camera to dual camera scene if available
        if len(cameras) > 1:
            secondary_camera = cameras[1]
            try:
                print(f"📷 Adding {secondary_camera['name']} to Dual Camera scene")
                
                settings = {}
                if secondary_camera['obs_kind'] == 'v4l2_source':
                    settings['device_id'] = secondary_camera['device_path']
                elif secondary_camera['obs_kind'] == 'dshow_input':
                    settings['video_device_id'] = secondary_camera['device_path']
                elif secondary_camera['obs_kind'] == 'av_capture_input':
                    settings['device'] = secondary_camera['device_path']
                
                client.create_input(
                    inputName="Secondary Camera",
                    inputKind=secondary_camera['obs_kind'],
                    inputSettings=settings,
                    sceneName="👥 Dual Camera / Interview",
                    sceneItemEnabled=True
                )
                print(f"  ✅ Added secondary camera")
                
            except Exception as e:
                print(f"  ⚠️  Could not add secondary camera: {e}")
        
        print("🎉 Camera setup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to OBS: {e}")
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Detect and configure cameras for OBS')
    parser.add_argument('--detect-only', action='store_true', help='Only detect cameras, don\'t add to OBS')
    parser.add_argument('--obs-host', default='localhost', help='OBS WebSocket host')
    parser.add_argument('--obs-port', type=int, default=4455, help='OBS WebSocket port')
    parser.add_argument('--obs-password', default='', help='OBS WebSocket password')
    
    args = parser.parse_args()
    
    # Detect cameras
    cameras = detect_cameras()
    
    if not cameras:
        print("❌ No cameras found")
        return 1
    
    print(f"\n📋 Summary: Found {len(cameras)} camera(s)")
    for i, camera in enumerate(cameras):
        print(f"  {i+1}. {camera['name']} ({camera['obs_kind']})")
    
    if args.detect_only:
        print("\n💡 Use --obs-host and --obs-password to add these cameras to OBS automatically")
        return 0
    
    # Add to OBS
    if WEBSOCKET_AVAILABLE:
        success = add_cameras_to_obs(
            cameras, 
            args.obs_host, 
            args.obs_port, 
            args.obs_password
        )
        return 0 if success else 1
    else:
        print("\n❌ Cannot add to OBS - install obsws-python first")
        print("   pip install --break-system-packages obsws-python")
        return 1

if __name__ == "__main__":
    sys.exit(main())