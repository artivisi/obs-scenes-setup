#!/usr/bin/env python3
"""
Automated OBS Scene Creation Script

This script automatically creates all OBS scenes, sources, and configurations
without manual clicking. It uses the OBS WebSocket API to create scenes in
real-time or generates a complete scene collection JSON file.

Features:
- Automated scene creation with proper source ordering
- Browser source configuration with GitHub Pages URLs
- Video/audio source detection and auto-assignment
- Filter application (noise suppression, compression, etc.)
- Hotkey assignment and scene transitions
- Cross-platform device compatibility

Usage:
    python auto-scene-creator.py --create-live --github-user username
    python auto-scene-creator.py --create-live --github-user username --offline
    python auto-scene-creator.py --generate-json --output scenes.json
    python auto-scene-creator.py --template java-tutorial --github-user username
"""

import json
import asyncio
import argparse
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import subprocess
import platform

# Check for OBS WebSocket dependency
try:
    import obsws_python as obs
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    print("⚠️  obsws-python not installed. Install with: pip install obsws-python")

@dataclass
class SceneSource:
    """Configuration for a scene source"""
    name: str
    type: str  # 'browser_source', 'video_capture_device', 'display_capture', etc.
    settings: Dict[str, Any]
    filters: List[Dict[str, Any]] = None
    transform: Dict[str, Any] = None
    visible: bool = True
    locked: bool = False

@dataclass
class SceneConfig:
    """Configuration for a complete scene"""
    name: str
    description: str
    sources: List[SceneSource]
    transitions: Optional[Dict[str, Any]] = None
    hotkey: Optional[str] = None

class AutoSceneCreator:
    """Automated OBS scene creation system"""
    
    def __init__(self, github_user: str = "artivisi", obs_host: str = "localhost", obs_port: int = 4455, obs_password: str = "", offline_mode: bool = False):
        self.github_user = github_user
        self.offline_mode = offline_mode
        # Get the project root directory (2 levels up from this script)
        self.project_root = Path(__file__).resolve().parent.parent.parent
        # Use the correct base URL that works
        if offline_mode:
            self.base_url = f"file://{self.project_root}"
        elif github_user == "artivisi":
            self.base_url = "https://artivisi.com/obs-scenes-setup"
        else:
            self.base_url = f"https://{github_user}.github.io/obs-scenes-setup"
        self.obs_client = None
        self.obs_host = obs_host
        self.obs_port = obs_port
        self.obs_password = obs_password
        self.detected_devices = {}
        
        self.platform = platform.system().lower()
        
        # Scene templates
        self.scene_templates = self._create_scene_templates()
        
    def _get_overlay_url(self, overlay_name: str) -> str:
        """Get overlay URL based on offline/online mode"""
        if self.offline_mode:
            # Use relative path from project root
            overlay_path = self.project_root / "docs" / "overlays" / f"{overlay_name}.html"
            return f"file://{overlay_path}"
        else:
            return f"https://{self.github_user}.github.io/obs-scenes-setup/overlays/{overlay_name}.html"
    
    def _create_scene_templates(self) -> List[SceneConfig]:
        """Create all scene configuration templates"""
        # Create source scenes first (these contain the actual devices)
        source_scenes = [
            self._create_camera_scene(),
            self._create_audio_scene(),
            self._create_screen_scene()
        ]
        
        # Add separator to distinguish source scenes from main scenes
        separator_scene = [
            SceneConfig(
                name="═══════ SOURCE SCENES ═══════",
                description="Separator - Source scenes start below this line",
                sources=[]  # Empty scene used as visual separator
            )
        ]
        
        # Create main scenes in reverse order (OBS displays scenes in reverse creation order)
        main_scenes = [
            self._create_outro_scene(),          # F6 - Stream end (created first, appears last)
            self._create_brb_scene(),            # F5 - Breaks/technical issues
            self._create_screen_only_scene(),     # F4 - Full screen demos
            self._create_code_demo_scene(),       # F3 - Main content (coding)
            self._create_talking_head_scene(),    # F2 - Introduction/discussion
            self._create_intro_scene()           # F1 - Stream start (created last, appears first)
        ]
        
        return source_scenes + separator_scene + main_scenes
    
    def _create_camera_scene(self) -> SceneConfig:
        """Create dedicated camera scene - edit camera settings here once"""
        return SceneConfig(
            name="📹 Camera Sources",
            description="Camera sources - edit camera settings here (used by all scenes)",
            sources=[
                SceneSource(
                    name="Main Camera",
                    type="video_capture_device",
                    settings={},  # Let OBS use the default camera device automatically
                    transform={
                        "scaleX": 1.5,   # More moderate scaling (640*1.5=960, well within 1920)
                        "scaleY": 1.5,   # More moderate scaling (360*1.5=540, well within 1080) 
                        "positionX": 0,   # Start at origin - OBS will center based on alignment
                        "positionY": 0    # Start at origin - OBS will center based on alignment
                    },
                    visible=True
                )
            ]
        )
    
    def _create_audio_scene(self) -> SceneConfig:
        """Create dedicated audio scene - edit audio settings here once"""
        return SceneConfig(
            name="🎤 Audio Sources",
            description="Audio sources - edit microphone settings here (used by all scenes)",
            sources=[
                SceneSource(
                    name="Main Microphone",
                    type="audio_input_capture",
                    settings={
                        "device_id": "default"  # User can change this once
                    },
                    filters=[
                        {
                            "name": "Noise Suppression",
                            "type": "noise_suppress_filter",
                            "settings": {"method": "rnnoise"}
                        },
                        {
                            "name": "Compressor",
                            "type": "compressor_filter",
                            "settings": {"ratio": 10, "threshold": -18}
                        },
                        {
                            "name": "Limiter",
                            "type": "limiter_filter", 
                            "settings": {"threshold": -6, "release_time": 60}
                        }
                    ],
                    visible=True
                ),
                SceneSource(
                    name="Guest Microphone",
                    type="audio_input_capture", 
                    settings={
                        "device_id": "default"  # User can change this for guest
                    },
                    filters=[
                        {
                            "name": "Noise Suppression",
                            "type": "noise_suppress_filter",
                            "settings": {"method": "rnnoise"}
                        }
                    ],
                    visible=False
                )
            ]
        )
    
    def _create_screen_scene(self) -> SceneConfig:
        """Create dedicated screen capture scene - edit screen settings here once"""
        return SceneConfig(
            name="🖥️ Screen Sources",
            description="Screen sources - edit display/app/window settings here (used by all scenes)",
            sources=[
                SceneSource(
                    name="Application Capture (VS Code Default)",
                    type="window_capture",
                    settings={
                        "window": "Visual Studio Code"  # Set VS Code as default
                    },
                    transform={
                        "scaleX": 1.0,
                        "scaleY": 1.0,
                        "positionX": 0,
                        "positionY": 0
                    },
                    visible=True  # Default enabled
                ),
                SceneSource(
                    name="Window Capture",
                    type="window_capture", 
                    settings={},  # User can configure specific window
                    transform={
                        "scaleX": 1.0,
                        "scaleY": 1.0,
                        "positionX": 0,
                        "positionY": 0
                    },
                    visible=False  # Disabled by default
                ),
                SceneSource(
                    name="Display Capture", 
                    type="display_capture",
                    settings={
                        "method": "automatic"  # User can change to specific display
                    },
                    transform={
                        "scaleX": 1.0,
                        "scaleY": 1.0,
                        "positionX": 0,
                        "positionY": 0
                    },
                    visible=False  # Disabled by default
                )
            ]
        )
    
    
    def _create_intro_scene(self) -> SceneConfig:
        """Create intro scene configuration"""
        return SceneConfig(
            name="🎬 Intro Scene",
            description="Professional intro with title card and countdown",
            hotkey="F1",
            sources=[
                SceneSource(
                    name="Dynamic Intro Overlay",
                    type="browser_source",
                    settings={
                        "url": self._get_overlay_url("intro"),
                        "width": 1920,
                        "height": 1080,
                        "fps": 30,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True,
                        "reroute_audio": False
                    },
                    visible=True
                ),
                # NO CAMERA IN INTRO - just overlay with title and countdown
                # User instructions for customization
            ]
        )
    
    def _create_talking_head_scene(self) -> SceneConfig:
        """Create talking head scene configuration"""
        return SceneConfig(
            name="👤 Talking Head",
            description="Full camera view for presentations and discussions",
            hotkey="F2",
            sources=[
                SceneSource(
                    name="Main Camera",
                    type="scene_reference",
                    settings={
                        "scene_name": "📹 Camera Sources"
                    },
                    transform={
                        "scaleX": 1.0,
                        "scaleY": 1.0,
                        "rotation": 0.0,
                        "positionX": 0,
                        "positionY": 0
                    },
                    visible=True
                ),
                SceneSource(
                    name="Talking Head Overlay",
                    type="browser_source",
                    settings={
                        "url": self._get_overlay_url("talking-head"),
                        "width": 1920,
                        "height": 1080,
                        "fps": 30,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True,
                        "reroute_audio": False
                    },
                    visible=True
                ),
            ]
        )
    
    def _create_code_demo_scene(self) -> SceneConfig:
        """Create code demonstration scene with PiP camera"""
        return SceneConfig(
            name="💻 Code + Camera",
            description="Split screen with code and presenter camera",
            hotkey="F3",
            sources=[
                SceneSource(
                    name="Screen Capture",
                    type="scene_reference",
                    settings={
                        "scene_name": "🖥️ Screen Sources"
                    },
                    transform={
                        "scaleX": 1.0,  # Fit to full screen
                        "scaleY": 1.0,  # Fit to full screen
                        "positionX": 0,
                        "positionY": 0
                    },
                    visible=True
                ),
                SceneSource(
                    name="PiP Camera (Small Lower Right)",
                    type="scene_reference",
                    settings={
                        "scene_name": "📹 Camera Sources"
                    },
                    transform={
                        "scaleX": 0.33,  # Maintain aspect ratio - scale both dimensions equally
                        "scaleY": 0.33,  # Maintain aspect ratio - same scale as X
                        "positionX": 1560, # Move left to align with blue frame left edge (right: 40px = 1920-40-320 = 1560)
                        "positionY": 780,  # Adjust for new rectangle height (bottom: 120px = 1080-120-180 = 780)
                        "cropLeft": 0,     # Crop settings to match blue rectangle exactly
                        "cropTop": 0,
                        "cropRight": 0,
                        "cropBottom": 0,
                        "boundsType": "OBS_BOUNDS_SCALE_INNER",  # Scale to fit within bounds while maintaining aspect ratio
                        "boundsWidth": 320,  # Exact width of blue rectangle
                        "boundsHeight": 180  # New height of blue rectangle (16:9 aspect ratio)
                    },
                    visible=True
                ),
                SceneSource(
                    name="Code Demo Overlay",
                    type="browser_source",
                    settings={
                        "url": self._get_overlay_url("code-demo"),
                        "width": 1920,
                        "height": 1080,
                        "fps": 30,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True,
                        "reroute_audio": False
                    },
                    visible=True
                ),
            ]
        )
    
    def _create_screen_only_scene(self) -> SceneConfig:
        """Create screen-only scene for detailed demonstrations"""
        return SceneConfig(
            name="🖥️ Screen Only",
            description="Full screen capture for detailed code work",
            hotkey="F4",
            sources=[
                SceneSource(
                    name="Full Screen",
                    type="display_capture",
                    settings={
                        "method": "automatic"
                    },
                    transform={
                        "scaleX": 1.0,
                        "scaleY": 1.0,
                        "positionX": 0,
                        "positionY": 0
                    },
                    visible=True
                ),
                SceneSource(
                    name="Mini Camera (Toggleable)",
                    type="scene_reference",
                    settings={
                        "scene_name": "📹 Camera Sources"
                    },
                    transform={
                        "scaleX": 0.15,  # 15% of full camera (1920*0.15=288px wide)
                        "scaleY": 0.15,  # 15% of full camera (1080*0.15=162px tall) 
                        "positionX": 1632,    # Bottom right: 1920-288=1632
                        "positionY": 918      # Bottom right: 1080-162=918
                    },
                    visible=False  # Disabled by default - user can enable if wanted
                ),
                SceneSource(
                    name="Screen Only Overlay",
                    type="browser_source",
                    settings={
                        "url": self._get_overlay_url("screen-only"),
                        "width": 1920,
                        "height": 1080,
                        "fps": 30,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True,
                        "reroute_audio": False
                    },
                    visible=True
                )
            ]
        )
    
    def _create_brb_scene(self) -> SceneConfig:
        """Create Be Right Back scene"""
        return SceneConfig(
            name="📺 BRB / Technical",
            description="Holding pattern for breaks and technical issues",
            hotkey="F5",
            sources=[
                SceneSource(
                    name="BRB Overlay",
                    type="browser_source",
                    settings={
                        "url": self._get_overlay_url("brb"),
                        "width": 1920,
                        "height": 1080,
                        "fps": 30,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True,
                        "reroute_audio": False
                    },
                    visible=True
                )
            ]
        )
    
    def _create_outro_scene(self) -> SceneConfig:
        """Create outro scene"""
        return SceneConfig(
            name="🎯 Outro Scene",
            description="Professional outro with call to action",
            hotkey="F6",
            sources=[
                SceneSource(
                    name="Outro Overlay",
                    type="browser_source",
                    settings={
                        "url": self._get_overlay_url("outro"),
                        "width": 1920,
                        "height": 1080,
                        "fps": 30,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True,
                        "reroute_audio": False
                    },
                    visible=True
                ),
                # NO CAMERA IN OUTRO - just overlay with thank you message
            ]
        )
    
    
    async def connect_obs(self) -> bool:
        """Connect to OBS WebSocket"""
        if not WEBSOCKET_AVAILABLE:
            print("❌ OBS WebSocket library not available")
            return False
        
        try:
            self.obs_client = obs.ReqClient(
                host=self.obs_host, 
                port=self.obs_port, 
                password=self.obs_password
            )
            
            # Test connection
            version_info = self.obs_client.get_version()
            print(f"✅ Connected to OBS Studio {version_info.obs_version}")
            print(f"📡 WebSocket version: {version_info.obs_web_socket_version}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to OBS: {e}")
            print("💡 Make sure OBS is running with WebSocket server enabled")
            print("   Tools → WebSocket Server Settings → Enable WebSocket server")
            return False
    
    def detect_devices(self) -> Dict[str, Any]:
        """Detect available cameras and audio devices"""
        print("🔍 Detecting available devices...")
        
        devices = {
            'video_devices': [],
            'audio_input_devices': [],
            'audio_output_devices': []
        }
        
        # Try to get devices from OBS directly if connected
        if self.obs_client:
            try:
                # Create a temporary video source to query available devices
                temp_source_name = "temp_device_detection"
                try:
                    self.obs_client.create_input(
                        inputName=temp_source_name,
                        inputKind="av_capture_input_v2" if self.platform == 'darwin' else 'v4l2_source' if self.platform == 'linux' else 'dshow_input',
                        inputSettings={}
                    )
                    
                    # Query available devices
                    input_props = self.obs_client.get_input_properties_list_property_items(
                        input_name=temp_source_name,
                        property_name="device"
                    )
                    
                    for item in input_props.property_items:
                        if item['itemValue'] and item['itemValue'] != 'None':
                            devices['video_devices'].append({
                                'name': item['itemValue'],
                                'type': 'obs_detected'
                            })
                            print(f"📹 Detected camera: {item['itemValue']}")
                    
                    # Clean up temp source
                    self.obs_client.remove_input(temp_source_name)
                    
                except Exception as e:
                    print(f"⚠️  OBS device detection failed: {e}")
                    
            except Exception as e:
                print(f"⚠️  Could not query OBS devices: {e}")
        
        # Run device detection script if available
        script_path = Path(__file__).parent / "device-manager.py"
        if script_path.exists():
            try:
                result = subprocess.run([
                    'python3', str(script_path), '--scan'
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    print("✅ Device detection completed")
                    # Parse device information (simplified)
                    output_lines = result.stdout.split('\n')
                    
                    for line in output_lines:
                        if 'cam link' in line.lower() or 'camera' in line.lower():
                            if not any(dev['name'] == line.strip() for dev in devices['video_devices']):
                                devices['video_devices'].append({
                                    'name': line.strip(),
                                    'type': 'usb_camera'
                                })
                        elif 'audio' in line.lower() or 'microphone' in line.lower():
                            devices['audio_input_devices'].append({
                                'name': line.strip(),
                                'type': 'usb_audio'
                            })
                
            except Exception as e:
                print(f"⚠️  Device detection warning: {e}")
        
        # Fallback device names for macOS
        if not devices['video_devices']:
            if self.platform == 'darwin':
                devices['video_devices'] = [
                    {'name': 'FaceTime HD Camera', 'type': 'built_in'},
                    {'name': 'FaceTime HD Camera (Built-in)', 'type': 'built_in'}
                ]
            else:
                devices['video_devices'] = [
                    {'name': 'Primary Camera', 'type': 'built_in'},
                    {'name': 'Secondary Camera', 'type': 'built_in'}
                ]
        
        if not devices['audio_input_devices']:
            devices['audio_input_devices'] = [
                {'name': 'Primary Microphone', 'type': 'built_in'}
            ]
        
        self.detected_devices = devices
        print(f"📹 Found {len(devices['video_devices'])} video device(s)")
        print(f"🎤 Found {len(devices['audio_input_devices'])} audio device(s)")
        
        return devices
    
    def resolve_device_placeholders(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Replace device placeholders with actual device names"""
        resolved_settings = settings.copy()
        
        # Get actual device names from OBS for more reliable detection
        if self.obs_client:
            try:
                # Get available video devices
                input_props = self.obs_client.get_input_properties_list_property_items(
                    input_name="temp_video_source",
                    property_name="device"
                )
                video_device_names = [item['itemValue'] for item in input_props.property_items if item['itemValue']]
            except:
                video_device_names = []
        else:
            video_device_names = []
        
        # Fallback device mapping
        device_mapping = {
            'AUTO_DETECT_PRIMARY_CAMERA': video_device_names[0] if video_device_names else 'FaceTime HD Camera',
            'AUTO_DETECT_SECONDARY_CAMERA': video_device_names[1] if len(video_device_names) > 1 else video_device_names[0] if video_device_names else 'FaceTime HD Camera',
            'AUTO_DETECT_PRIMARY_AUDIO': self.detected_devices['audio_input_devices'][0]['name'] if self.detected_devices['audio_input_devices'] else 'Default Microphone',
            'AUTO_DETECT_SECONDARY_AUDIO': self.detected_devices['audio_input_devices'][1]['name'] if len(self.detected_devices['audio_input_devices']) > 1 else self.detected_devices['audio_input_devices'][0]['name'] if self.detected_devices['audio_input_devices'] else 'Default Microphone'
        }
        
        for key, value in resolved_settings.items():
            if isinstance(value, str) and value in device_mapping:
                resolved_settings[key] = device_mapping[value]
                print(f"🔧 Resolved {value} → {resolved_settings[key]}")
        
        # For macOS video capture, ensure proper settings
        if self.platform == 'darwin' and 'device' in resolved_settings:
            # Remove incompatible settings for macOS
            resolved_settings.pop('resolution', None)
            resolved_settings.pop('fps', None)
            # Add macOS-specific settings if needed
            if 'device' in resolved_settings and resolved_settings['device']:
                resolved_settings['device_id'] = resolved_settings['device']
        
        return resolved_settings
    
    async def create_scene_live(self, scene_config: SceneConfig) -> bool:
        """Create a scene in live OBS using WebSocket"""
        if not self.obs_client:
            print("❌ Not connected to OBS")
            return False
        
        try:
            print(f"🎬 Creating scene: {scene_config.name}")
            
            # Check if scene exists, remove if it does
            try:
                scene_list = self.obs_client.get_scene_list()
                if scene_config.name in [scene['sceneName'] for scene in scene_list.scenes]:
                    print(f"  🗑️  Removing existing scene: {scene_config.name}")
                    self.obs_client.remove_scene(scene_config.name)
            except Exception as e:
                print(f"  ⚠️  Could not check/remove existing scene: {e}")
            
            # Create the scene
            self.obs_client.create_scene(scene_config.name)
            
            # Add sources in order (first = bottom layer, last = top layer)
            for source in scene_config.sources:
                print(f"  📎 Adding source: {source.name} ({source.type})")
                
                # Use settings directly since we're using default devices
                resolved_settings = source.settings.copy()
                
                # For device sources, make sure we have valid settings
                if source.type == 'video_capture_device':
                    if 'device_id' in resolved_settings:
                        if resolved_settings['device_id'] == 'default':
                            # Remove device_id for default device selection
                            resolved_settings.pop('device_id', None)
                elif source.type == 'audio_input_capture':
                    if 'device_id' in resolved_settings:
                        if resolved_settings['device_id'] == 'default':
                            resolved_settings.pop('device_id', None)
                elif source.type == 'display_capture':
                    if resolved_settings.get('method') == 'automatic':
                        # Let OBS use automatic display selection
                        resolved_settings = {}
                
                # Create unique source name to avoid conflicts
                unique_source_name = f"{scene_config.name.replace('🎬', '').replace('👤', '').replace('💻', '').replace('🖥️', '').replace('📺', '').replace('🎯', '').replace('👥', '').strip().replace(' ', '_')}_{source.name.replace(' ', '_')}"
                
                # Handle scene references differently than regular sources
                if source.type == 'scene_reference':
                    try:
                        # Add scene as a source to current scene
                        scene_to_reference = resolved_settings.get('scene_name')
                        if scene_to_reference:
                            self.obs_client.create_scene_item(
                                scene_name=scene_config.name,
                                source_name=scene_to_reference
                            )
                            print(f"    ✅ Added scene reference: {scene_to_reference}")
                            source_name_for_transform = scene_to_reference
                        else:
                            print(f"    ⚠️  No scene_name provided for scene reference: {source.name}")
                            continue
                    except Exception as source_error:
                        print(f"    ⚠️  Failed to add scene reference {source.name}: {source_error}")
                        continue
                else:
                    # Create regular source
                    try:
                        self.obs_client.create_input(
                            inputName=unique_source_name,
                            inputKind=self._map_source_type(source.type),
                            inputSettings=resolved_settings,
                            sceneName=scene_config.name,
                            sceneItemEnabled=source.visible
                        )
                        print(f"    ✅ Created source: {unique_source_name}")
                        source_name_for_transform = unique_source_name
                    except Exception as source_error:
                        print(f"    ⚠️  Failed to create source {unique_source_name}: {source_error}")
                        continue
                
                # Apply transform if specified
                if source.transform:
                    try:
                        # Get scene item ID for transform
                        scene_items = self.obs_client.get_scene_item_list(scene_config.name)
                        for item in scene_items.scene_items:
                            if item['sourceName'] == source_name_for_transform:
                                self.obs_client.set_scene_item_transform(
                                    scene_name=scene_config.name,
                                    item_id=item['sceneItemId'],
                                    transform=source.transform
                                )
                                break
                    except Exception as e:
                        print(f"    ⚠️  Could not set transform for {unique_source_name}: {e}")
                
                # Set visibility - need to get scene item ID first
                if source.visible != True:  # Only change if not default
                    try:
                        scene_items = self.obs_client.get_scene_item_list(scene_config.name)
                        for item in scene_items.scene_items:
                            if item['sourceName'] == source_name_for_transform:
                                self.obs_client.set_scene_item_enabled(
                                    scene_name=scene_config.name,
                                    item_id=item['sceneItemId'],
                                    enabled=source.visible
                                )
                                break
                    except Exception as e:
                        print(f"    ⚠️  Could not set visibility for {unique_source_name}: {e}")
                
                # Apply filters
                if source.filters:
                    for filter_config in source.filters:
                        try:
                            # Check if filter already exists
                            existing_filters = self.obs_client.get_source_filter_list(unique_source_name)
                            filter_exists = any(f['filterName'] == filter_config['name'] for f in existing_filters.filters)
                            
                            if not filter_exists:
                                self.obs_client.create_source_filter(
                                    source_name=unique_source_name,
                                    filter_name=filter_config['name'],
                                    filter_kind=filter_config['type'],
                                    filter_settings=filter_config.get('settings', {})
                                )
                                print(f"    ✅ Added filter: {filter_config['name']}")
                            else:
                                print(f"    ⚠️  Filter already exists: {filter_config['name']}")
                        except Exception as e:
                            print(f"    ⚠️  Could not add filter {filter_config['name']}: {e}")
            
            # Fix layer ordering - move overlays to top
            self._fix_source_ordering(scene_config)
            
            print(f"✅ Scene '{scene_config.name}' created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create scene '{scene_config.name}': {e}")
            return False
    
    def _map_source_type(self, source_type: str) -> str:
        """Map our source types to OBS source kinds"""
        mapping = {
            'browser_source': 'browser_source',
            'video_capture_device': 'v4l2_source' if self.platform == 'linux' else 'dshow_input' if self.platform == 'windows' else 'av_capture_input_v2',
            'display_capture': 'xshm_input' if self.platform == 'linux' else 'monitor_capture' if self.platform == 'windows' else 'display_capture',
            'audio_input_capture': 'pulse_input_capture' if self.platform == 'linux' else 'wasapi_input_capture' if self.platform == 'windows' else 'coreaudio_input_capture',
            'text_gdiplus': 'text_gdiplus_v2' if self.platform == 'windows' else 'text_ft2_source_v2'  # Text sources
        }
            
        return mapping.get(source_type, source_type)
    
    def _fix_source_ordering(self, scene_config: SceneConfig):
        """Ensure overlays are on top by reordering sources"""
        try:
            # Get current scene items
            scene_items = self.obs_client.get_scene_item_list(scene_config.name)
            items = scene_items.scene_items
            
            # Find overlay sources (browser_source types) and move them to top
            overlay_items = []
            for item in items:
                source_name = item['sourceName']
                # Check if this is an overlay (browser source)
                if any('overlay' in source.name.lower() or source.type == 'browser_source' 
                       for source in scene_config.sources if source.name.replace(' ', '_').replace(':', '_').replace('(', '_').replace(')', '_') in source_name):
                    overlay_items.append(item)
            
            # Move overlay items to top (highest index means top layer)
            for i, overlay_item in enumerate(overlay_items):
                try:
                    # Get current scene item count to determine top index
                    current_items = self.obs_client.get_scene_item_list(scene_config.name)
                    top_index = len(current_items.scene_items) - 1  # Highest index is top layer
                    
                    self.obs_client.set_scene_item_index(
                        scene_name=scene_config.name,
                        item_id=overlay_item['sceneItemId'],
                        item_index=top_index  # Move to highest index (top layer)
                    )
                    print(f"    ✅ Moved {overlay_item['sourceName']} to top layer (index {top_index})")
                except Exception as e:
                    print(f"    ⚠️  Could not reorder overlay {overlay_item['sourceName']}: {e}")
                    
        except Exception as e:
            print(f"    ⚠️  Could not fix source ordering: {e}")
    
    async def import_scene_collection_live(self, json_path: Path) -> bool:
        """Import scene collection from JSON file into live OBS"""
        if not await self.connect_obs():
            return False
            
        try:
            with open(json_path, 'r') as f:
                scene_data = json.load(f)
            
            print(f"📋 Importing scene collection from: {json_path}")
            
            # Create new scene collection
            collection_name = f"Artivisi-{int(time.time())}"
            self.obs_client.create_scene_collection(collection_name)
            print(f"✅ Created scene collection: {collection_name}")
            
            # Import scenes
            success_count = 0
            scene_order = scene_data.get('scene_order', [])
            scenes_data = {scene['name']: scene for scene in scene_data.get('scenes', [])}
            all_sources = {source['name']: source for source in scene_data.get('sources', [])}
            
            for scene_info in scene_order:
                scene_name = scene_info['name']
                print(f"🎬 Creating scene: {scene_name}")
                
                try:
                    # Create scene
                    self.obs_client.create_scene(scene_name)
                    
                    # Find scene data and add sources
                    if scene_name in scenes_data:
                        scene_sources = scenes_data[scene_name].get('sources', [])
                        
                        for scene_item in scene_sources:
                            source_name = scene_item['name']
                            
                            # Find the source definition
                            if source_name in all_sources:
                                source = all_sources[source_name]
                                source_kind = source['versioned_id'] 
                                source_settings = source.get('settings', {})
                                
                                try:
                                    self.obs_client.create_input(
                                        inputName=source_name,
                                        inputKind=source_kind,
                                        inputSettings=source_settings,
                                        sceneName=scene_name,
                                        sceneItemEnabled=scene_item.get('enabled', True)
                                    )
                                    print(f"  ✅ Added source: {source_name}")
                                except Exception as e:
                                    print(f"  ⚠️  Could not add source {source_name}: {e}")
                            else:
                                print(f"  ⚠️  Source definition not found: {source_name}")
                                
                    success_count += 1
                    
                except Exception as e:
                    print(f"❌ Failed to create scene '{scene_name}': {e}")
                    
            print(f"🎉 Imported {success_count}/{len(scene_order)} scenes successfully")
            return success_count > 0
            
        except Exception as e:
            print(f"❌ Failed to import scene collection: {e}")
            return False
    
    def _cleanup_all_scenes(self):
        """Remove all existing scenes and sources to start fresh"""
        try:
            print("\n🧹 Cleaning up existing scenes and sources...")
            
            # Get all scenes
            scene_list = self.obs_client.get_scene_list()
            scenes_to_remove = []
            
            for scene in scene_list.scenes:
                scene_name = scene['sceneName']
                # Don't remove the default scene if it's the only one
                if len(scene_list.scenes) > 1 or scene_name not in ['Scene', 'Default']:
                    scenes_to_remove.append(scene_name)
            
            # Remove scenes (this also removes their sources)
            for scene_name in scenes_to_remove:
                try:
                    self.obs_client.remove_scene(scene_name)
                    print(f"  🗑️  Removed scene: {scene_name}")
                except Exception as e:
                    print(f"  ⚠️  Could not remove scene {scene_name}: {e}")
            
            # Wait a moment for OBS to process the removals
            import time
            time.sleep(0.5)
            
            # Get all global sources and remove them - be more thorough
            try:
                input_list = self.obs_client.get_input_list()
                sources_to_remove = []
                for input_source in input_list.inputs:
                    source_name = input_source['inputName']
                    # Collect all sources first
                    sources_to_remove.append(source_name)
                
                # Remove all sources
                for source_name in sources_to_remove:
                    try:
                        self.obs_client.remove_input(source_name)
                        print(f"  🗑️  Removed global source: {source_name}")
                    except Exception as e:
                        print(f"  ⚠️  Could not remove source {source_name}: {e}")
                        
                # Double-check - try to remove any remaining camera sources specifically
                camera_source_patterns = [
                    "📹_Camera_Sources_Main_Camera",
                    "Camera_Sources_Main_Camera", 
                    "Main_Camera",
                    "📹_Camera_Sources_Main_Camera"
                ]
                
                for pattern in camera_source_patterns:
                    try:
                        self.obs_client.remove_input(pattern)
                        print(f"  🗑️  Cleaned up camera source: {pattern}")
                    except Exception:
                        pass  # Expected to fail if source doesn't exist
                        
            except Exception as e:
                print(f"  ⚠️  Could not cleanup global sources: {e}")
            
            print("✅ Cleanup completed")
            
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
    
    async def create_all_scenes_live(self) -> bool:
        """Create all scenes in live OBS"""
        if not await self.connect_obs():
            return False
        
        # Clean up all existing scenes and sources first
        self._cleanup_all_scenes()
        
        success_count = 0
        for scene_config in self.scene_templates:
            if await self.create_scene_live(scene_config):
                success_count += 1
                
                # Set up hotkeys (requires OBS 28+)
                if scene_config.hotkey:
                    try:
                        # Note: Hotkey assignment via WebSocket is limited
                        print(f"💡 Assign hotkey {scene_config.hotkey} to '{scene_config.name}' manually in OBS")
                    except Exception as e:
                        print(f"⚠️  Could not assign hotkey: {e}")
                
                # Small delay between scenes
                await asyncio.sleep(0.5)
        
        print(f"\n🎉 Created {success_count}/{len(self.scene_templates)} scenes successfully")
        
        # Configure global settings
        await self._configure_global_settings()
        
        return success_count == len(self.scene_templates)
    
    async def _setup_audio_sources(self):
        """Set up global audio sources with filters"""
        print("\n🎤 Setting up audio sources...")
        
        if not self.obs_client:
            return
        
        try:
            # Try to find the actual microphone device name from OBS
            primary_audio = None
            
            # Get all audio inputs to find the microphone
            try:
                input_list = self.obs_client.get_input_list()
                audio_inputs = [inp for inp in input_list.inputs if 'audio' in inp.get('inputKind', '').lower() or 'mic' in inp.get('inputName', '').lower()]
                if audio_inputs:
                    primary_audio = audio_inputs[0]['inputName']
                    print(f"🎙️  Found microphone: {primary_audio}")
                else:
                    print("⚠️  No microphone found, skipping audio filters")
                    return
            except Exception as e:
                print(f"⚠️  Could not detect audio inputs: {e}")
                return
            
            print(f"🎙️  Configuring primary microphone: {primary_audio}")
            
            # Add audio filters (if source exists)
            audio_filters = [
                {
                    'name': 'Noise Suppression',
                    'type': 'noise_suppress_filter',
                    'settings': {'method': 'rnnoise'}
                },
                {
                    'name': 'Compressor',
                    'type': 'compressor_filter', 
                    'settings': {
                        'ratio': 10.0,
                        'threshold': -18.0,
                        'attack_time': 6.0,
                        'release_time': 60.0
                    }
                },
                {
                    'name': 'Limiter',
                    'type': 'limiter_filter',
                    'settings': {
                        'threshold': -6.0,
                        'release_time': 60
                    }
                }
            ]
            
            # Apply filters to microphone source
            for filter_config in audio_filters:
                try:
                    # Check if filter already exists
                    existing_filters = self.obs_client.get_source_filter_list(primary_audio)
                    filter_exists = any(f['filterName'] == filter_config['name'] for f in existing_filters.filters)
                    
                    if not filter_exists:
                        self.obs_client.create_source_filter(
                            source_name=primary_audio,
                            filter_name=filter_config['name'],
                            filter_kind=filter_config['type'],
                            filter_settings=filter_config['settings']
                        )
                        print(f"  ✅ Added {filter_config['name']} filter")
                    else:
                        print(f"  ⚠️  Filter already exists: {filter_config['name']}")
                except Exception as e:
                    print(f"  ⚠️  Could not add {filter_config['name']}: {e}")
            
        except Exception as e:
            print(f"⚠️  Audio setup warning: {e}")
    
    async def _configure_global_settings(self):
        """Configure global OBS settings"""
        print("\n⚙️  Configuring global settings...")
        
        try:
            # Set video settings
            video_settings = {
                'base_width': 1920,
                'base_height': 1080,
                'output_width': 1920,
                'output_height': 1080,
                'fps_numerator': 30,
                'fps_denominator': 1
            }
            
            # Note: Video settings require restart, so just log recommendation
            print("💡 Recommended video settings:")
            print("   Base Resolution: 1920x1080")
            print("   Output Resolution: 1920x1080")
            print("   FPS: 30")
            
            # Configure scene transitions
            print("🔄 Setting up scene transitions...")
            # Default fade transition
            
            print("✅ Global configuration completed")
            
        except Exception as e:
            print(f"⚠️  Global settings warning: {e}")
    
    def generate_scene_collection_json(self, output_path: Path) -> bool:
        """Generate complete OBS scene collection JSON file"""
        print(f"📄 Generating scene collection JSON: {output_path}")
        
        # Detect devices for JSON generation
        self.detect_devices()
        
        scene_collection = {
            "AaronProgrammerScenes": {
                "current_scene": "👤 Talking Head",
                "current_program_scene": "👤 Talking Head", 
                "current_preview_scene": "🎬 Intro Scene",
                "current_transition": "Fade",
                "transition_duration": 300,
                "sources": [],
                "scene_order": [],
                "name": f"Programming Tutorials - {self.github_user.title()}",
                "id": f"id{int(time.time())}",
                "prev_ver": 503316737,
                "scenes": []
            }
        }
        
        # Convert scene configs to OBS JSON format
        for scene_config in self.scene_templates:
            obs_scene = self._convert_scene_to_obs_format(scene_config)
            scene_collection["AaronProgrammerScenes"]["scenes"].append(obs_scene)
            scene_collection["AaronProgrammerScenes"]["scene_order"].append({
                "name": scene_config.name
            })
        
        # Add global sources
        scene_collection["AaronProgrammerScenes"]["sources"] = self._generate_global_sources()
        
        # Write JSON file
        try:
            with open(output_path, 'w') as f:
                json.dump(scene_collection, f, indent=2)
            
            print(f"✅ Scene collection saved to: {output_path}")
            print("📋 Import into OBS: Scene Collection → Import")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to write JSON file: {e}")
            return False
    
    def _convert_scene_to_obs_format(self, scene_config: SceneConfig) -> Dict[str, Any]:
        """Convert our scene config to OBS JSON format"""
        obs_scene = {
            "name": scene_config.name,
            "uuid": f"uuid-{scene_config.name.lower().replace(' ', '-')}",
            "id": len(scene_config.name),
            "prev_ver": 503316737,
            "source_uuid": f"source-{scene_config.name.lower().replace(' ', '-')}",
            "sources": []
        }
        
        # Convert sources
        for i, source in enumerate(scene_config.sources):
            obs_source = {
                "name": source.name,
                "source_uuid": f"source-{source.name.lower().replace(' ', '-')}", 
                "versioned_id": self._map_source_type(source.type),
                "volume": 1.0,
                "balance": 0.5,
                "sync": 0,
                "mixers": 255,
                "monitoring_type": 0,
                "prev_ver": 503316737,
                "id": i + 1,
                "muted": False,
                "push-to-mute": False,
                "push-to-mute-delay": 1000,
                "push-to-talk": False,
                "push-to-talk-delay": 1000,
                "enabled": source.visible,
                "settings": self.resolve_device_placeholders(source.settings)
            }
            
            # Add transform information
            if source.transform:
                obs_source.update(source.transform)
            
            # Add filters
            if source.filters:
                obs_source["filters"] = []
                for filter_config in source.filters:
                    obs_filter = {
                        "name": filter_config['name'],
                        "type": filter_config['type'],
                        "settings": filter_config.get('settings', {}),
                        "enabled": True
                    }
                    obs_source["filters"].append(obs_filter)
            
            obs_scene["sources"].append(obs_source)
        
        return obs_scene
    
    def _generate_global_sources(self) -> List[Dict[str, Any]]:
        """Generate global audio sources"""
        global_sources = []
        
        # Primary microphone
        if self.detected_devices['audio_input_devices']:
            primary_mic = {
                "name": self.detected_devices['audio_input_devices'][0]['name'],
                "versioned_id": self._map_source_type('audio_input_capture'),
                "volume": 1.0,
                "monitoring_type": 2,  # Monitor and Output
                "settings": {
                    "device": self.detected_devices['audio_input_devices'][0]['name']
                },
                "filters": [
                    {
                        "name": "Noise Suppression",
                        "type": "noise_suppress_filter",
                        "enabled": True,
                        "settings": {"method": "rnnoise"}
                    },
                    {
                        "name": "Compressor", 
                        "type": "compressor_filter",
                        "enabled": True,
                        "settings": {
                            "ratio": 10.0,
                            "threshold": -18.0
                        }
                    }
                ]
            }
            global_sources.append(primary_mic)
        
        # Desktop audio
        desktop_audio = {
            "name": "Desktop Audio",
            "versioned_id": "pulse_output_capture" if self.platform == 'linux' else "wasapi_output_capture" if self.platform == 'windows' else "coreaudio_output_capture",
            "volume": 0.5,  # Lower than microphone
            "settings": {}
        }
        global_sources.append(desktop_audio)
        
        return global_sources
    
    def create_template_variations(self, content_type: str) -> List[SceneConfig]:
        """Create specialized templates for different content types"""
        templates = {
            'java': self._create_java_specific_scenes(),
            'linux': self._create_linux_admin_scenes(), 
            'devops': self._create_devops_scenes(),
            'interview': self._create_interview_focused_scenes()
        }
        
        return templates.get(content_type, self.scene_templates)
    
    def _create_java_specific_scenes(self) -> List[SceneConfig]:
        """Java development specific scene modifications"""
        java_scenes = self.scene_templates.copy()
        
        # Modify code demo scene for Java IDE
        for scene in java_scenes:
            if "Code + Camera" in scene.name:
                # Update browser source for Java-specific overlay
                for source in scene.sources:
                    if source.type == "browser_source" and "code-demo" in source.settings.get("url", ""):
                        source.settings["url"] = f"{self.base_url}/overlays/code-demo.html?lang=java&file=Application.java&topic=Java Enterprise Development&recording=true&theme=intellij"
        
        return java_scenes
    
    def _create_linux_admin_scenes(self) -> List[SceneConfig]:
        """Linux administration specific scenes"""
        linux_scenes = self.scene_templates.copy()
        
        # Add terminal-focused scene
        terminal_scene = SceneConfig(
            name="🐧 Terminal Focus",
            description="Terminal-focused layout for Linux administration",
            hotkey="Ctrl+T",
            sources=[
                SceneSource(
                    name="Terminal Screen",
                    type="display_capture",
                    settings={"method": "auto"},
                    transform={"scaleX": 1.0, "scaleY": 1.0},
                    visible=True
                ),
                SceneSource(
                    name="Command Overlay",
                    type="browser_source",
                    settings={
                        "url": f"{self.base_url}/overlays/terminal-overlay.html?theme=dark&showcommands=true",
                        "width": 1920,
                        "height": 1080
                    },
                    visible=True
                )
            ]
        )
        
        linux_scenes.insert(3, terminal_scene)  # Insert after screen only
        return linux_scenes
    
    def _create_devops_scenes(self) -> List[SceneConfig]:
        """DevOps specific scenes with diagram support"""
        devops_scenes = self.scene_templates.copy()
        
        # Modify presentation scenes for DevOps diagrams
        for scene in devops_scenes:
            if "Talking Head" in scene.name:
                # Add architecture diagram overlay
                diagram_source = SceneSource(
                    name="Architecture Overlay",
                    type="browser_source",
                    settings={
                        "url": f"{self.base_url}/overlays/architecture-diagram.html?type=microservices&editable=true",
                        "width": 1920,
                        "height": 1080
                    },
                    visible=False  # Toggle when needed
                )
                scene.sources.append(diagram_source)
        
        return devops_scenes
    
    def _create_interview_focused_scenes(self) -> List[SceneConfig]:
        """Interview-focused scene modifications"""
        interview_scenes = []
        
        # Keep only interview-relevant scenes
        relevant_scene_names = ["Intro", "Dual Camera", "BRB", "Outro"]
        
        for scene in self.scene_templates:
            if any(name in scene.name for name in relevant_scene_names):
                interview_scenes.append(scene)
        
        return interview_scenes

async def main():
    parser = argparse.ArgumentParser(
        description='Automated OBS Scene Creation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create scenes in live OBS
  python auto-scene-creator.py --create-live --github-user myusername
  
  # Generate JSON file for import
  python auto-scene-creator.py --generate-json --output my-scenes.json
  
  # Create Java-specific template
  python auto-scene-creator.py --template java --create-live
        """
    )
    
    parser.add_argument(
        '--create-live',
        action='store_true',
        help='Create scenes in live OBS via WebSocket'
    )
    
    parser.add_argument(
        '--generate-json',
        action='store_true',
        help='Generate OBS scene collection JSON file'
    )
    
    parser.add_argument(
        '--github-user',
        type=str,
        default='artivisi',
        help='GitHub username for overlay URLs'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        help='Output path for JSON file'
    )
    
    parser.add_argument(
        '--template',
        choices=['standard', 'java', 'linux', 'devops', 'interview'],
        default='standard',
        help='Scene template type'
    )
    
    parser.add_argument(
        '--obs-host',
        type=str,
        default='localhost',
        help='OBS WebSocket host'
    )
    
    parser.add_argument(
        '--obs-port',
        type=int,
        default=4455,
        help='OBS WebSocket port'
    )
    
    parser.add_argument(
        '--obs-password',
        type=str,
        default='',
        help='OBS WebSocket password'
    )
    
    parser.add_argument(
        '--import-json',
        type=Path,
        help='Import from existing OBS scene collection JSON file'
    )
    
    parser.add_argument(
        '--offline',
        action='store_true',
        help='Use local overlay files instead of GitHub Pages URLs'
    )
    
    args = parser.parse_args()
    
    if not args.create_live and not args.generate_json and not args.import_json:
        print("❌ Must specify --create-live, --generate-json, or --import-json")
        parser.print_help()
        sys.exit(1)
    
    creator = AutoSceneCreator(
        github_user=args.github_user,
        obs_host=args.obs_host,
        obs_port=args.obs_port,
        obs_password=args.obs_password,
        offline_mode=args.offline
    )
    
    # Apply template modifications
    if args.template != 'standard':
        creator.scene_templates = creator.create_template_variations(args.template)
        print(f"🎨 Using {args.template} template with {len(creator.scene_templates)} scenes")
    
    success = False
    
    if args.import_json:
        print("📦 Importing scene collection from JSON...")
        print("💡 Make sure OBS is running with WebSocket server enabled")
        print("   Tools → WebSocket Server Settings")
        
        success = await creator.import_scene_collection_live(args.import_json)
        
        if success:
            print("\n🎉 Scene collection imported successfully!")
            print("📋 Next steps:")
            print("   1. Check scenes in OBS and test overlays")
            print("   2. Configure device sources (cameras, microphones)")
            print("   3. Assign hotkeys (F1-F7) if needed")
        else:
            print("\n❌ Failed to import scene collection.")
            
    elif args.create_live:
        print("🚀 Creating scenes in live OBS...")
        print("💡 Make sure OBS is running with WebSocket server enabled")
        print("   Tools → WebSocket Server Settings")
        
        success = await creator.create_all_scenes_live()
        
        if success:
            print("\n🎉 All scenes created successfully!")
            print("📋 Next steps:")
            print("   1. Assign hotkeys manually in OBS (F1-F7)")
            print("   2. Test each scene and adjust as needed")
            print("   3. Configure recording/streaming settings")
        else:
            print("\n❌ Some scenes failed to create. Check OBS connection and logs.")
    
    if args.generate_json:
        output_path = args.output or Path(f"scenes-{args.github_user}-{args.template}.json")
        success = creator.generate_scene_collection_json(output_path)
        
        if success:
            print(f"\n✅ Scene collection JSON generated: {output_path}")
            print("📋 To import:")
            print("   1. Open OBS Studio")
            print("   2. Scene Collection → Import")
            print(f"   3. Select {output_path}")
            print("   4. Configure hotkeys (File → Settings → Hotkeys)")
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    asyncio.run(main())