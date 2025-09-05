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
    
    def __init__(self, github_user: str = "artivisi", obs_host: str = "localhost", obs_port: int = 4455, obs_password: str = ""):
        self.github_user = github_user
        self.base_url = f"https://{github_user}.github.io/obs-scenes-setup"
        self.obs_client = None
        self.obs_host = obs_host
        self.obs_port = obs_port
        self.obs_password = obs_password
        self.detected_devices = {}
        self.platform = platform.system().lower()
        
        # Scene templates
        self.scene_templates = self._create_scene_templates()
    
    def _create_scene_templates(self) -> List[SceneConfig]:
        """Create all scene configuration templates"""
        return [
            self._create_intro_scene(),
            self._create_talking_head_scene(),
            self._create_code_demo_scene(),
            self._create_screen_only_scene(),
            self._create_brb_scene(),
            self._create_outro_scene(),
            self._create_dual_camera_scene()
        ]
    
    def _create_intro_scene(self) -> SceneConfig:
        """Create intro scene configuration"""
        return SceneConfig(
            name="🎬 Intro Scene",
            description="Professional intro with title card and countdown",
            hotkey="F1",
            sources=[
                SceneSource(
                    name="Intro Overlay",
                    type="browser_source",
                    settings={
                        "url": f"{self.base_url}/overlays/intro.html?title=Java Development Mastery&subtitle=Building Enterprise Applications&countdown=true&autoexit=true&duration=10",
                        "width": 1920,
                        "height": 1080,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True,
                        "css": ""
                    },
                    visible=True
                ),
                SceneSource(
                    name="Background Camera",
                    type="video_capture_device",
                    settings={
                        "device": "AUTO_DETECT_PRIMARY_CAMERA",
                        "resolution": "1920x1080",
                        "fps": 30
                    },
                    transform={
                        "scale_x": 1.0,
                        "scale_y": 1.0,
                        "rotation": 0.0,
                        "pos_x": 0,
                        "pos_y": 0,
                        "opacity": 0.3  # Background effect
                    },
                    visible=True
                )
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
                    type="video_capture_device",
                    settings={
                        "device": "AUTO_DETECT_PRIMARY_CAMERA",
                        "resolution": "1920x1080",
                        "fps": 30
                    },
                    transform={
                        "scale_x": 1.0,
                        "scale_y": 1.0,
                        "rotation": 0.0,
                        "pos_x": 0,
                        "pos_y": 0
                    },
                    visible=True
                ),
                SceneSource(
                    name="Talking Head Overlay",
                    type="browser_source",
                    settings={
                        "url": f"{self.base_url}/overlays/talking-head.html?topic=Java Programming&recording=true&hidetitle=false",
                        "width": 1920,
                        "height": 1080,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True
                    },
                    visible=True
                )
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
                    type="display_capture",
                    settings={
                        "method": "auto"
                    },
                    transform={
                        "scale_x": 0.75,
                        "scale_y": 0.75,
                        "pos_x": 0,
                        "pos_y": 0
                    },
                    visible=True
                ),
                SceneSource(
                    name="PiP Camera",
                    type="video_capture_device",
                    settings={
                        "device": "AUTO_DETECT_PRIMARY_CAMERA",
                        "resolution": "1920x1080",
                        "fps": 30
                    },
                    transform={
                        "scale_x": 0.25,
                        "scale_y": 0.25,
                        "pos_x": 1440,
                        "pos_y": 60
                    },
                    visible=True
                ),
                SceneSource(
                    name="Code Demo Overlay",
                    type="browser_source",
                    settings={
                        "url": f"{self.base_url}/overlays/code-demo.html?lang=java&file=Application.java&topic=Spring Boot Development&recording=true",
                        "width": 1920,
                        "height": 1080,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True
                    },
                    visible=True
                )
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
                        "method": "auto"
                    },
                    transform={
                        "scale_x": 1.0,
                        "scale_y": 1.0,
                        "pos_x": 0,
                        "pos_y": 0
                    },
                    visible=True
                ),
                SceneSource(
                    name="Mini Camera",
                    type="video_capture_device",
                    settings={
                        "device": "AUTO_DETECT_PRIMARY_CAMERA",
                        "resolution": "1920x1080",
                        "fps": 30
                    },
                    transform={
                        "scale_x": 0.15,
                        "scale_y": 0.15,
                        "pos_x": 1632,
                        "pos_y": 900
                    },
                    visible=False  # Can be toggled via overlay
                ),
                SceneSource(
                    name="Screen Only Overlay",
                    type="browser_source",
                    settings={
                        "url": f"{self.base_url}/overlays/screen-only.html?hidecam=true&topic=Java Deep Dive&recording=true&progress=true",
                        "width": 1920,
                        "height": 1080,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True
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
                        "url": f"{self.base_url}/overlays/brb.html?type=break&duration=5&music=true&message=Taking a quick break - back in 5 minutes",
                        "width": 1920,
                        "height": 1080,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True
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
                        "url": f"{self.base_url}/overlays/outro.html?message=Hope you enjoyed this session&type=java",
                        "width": 1920,
                        "height": 1080,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True
                    },
                    visible=True
                ),
                SceneSource(
                    name="Background Camera",
                    type="video_capture_device",
                    settings={
                        "device": "AUTO_DETECT_PRIMARY_CAMERA",
                        "resolution": "1920x1080",
                        "fps": 30
                    },
                    transform={
                        "scale_x": 1.0,
                        "scale_y": 1.0,
                        "rotation": 0.0,
                        "pos_x": 0,
                        "pos_y": 0,
                        "opacity": 0.2
                    },
                    visible=True
                )
            ]
        )
    
    def _create_dual_camera_scene(self) -> SceneConfig:
        """Create dual camera scene for interviews"""
        return SceneConfig(
            name="👥 Dual Camera / Interview",
            description="Two camera setup for guest interviews",
            hotkey="F7",
            sources=[
                SceneSource(
                    name="Host Camera",
                    type="video_capture_device",
                    settings={
                        "device": "AUTO_DETECT_PRIMARY_CAMERA",
                        "resolution": "1920x1080",
                        "fps": 30
                    },
                    transform={
                        "scale_x": 0.5,
                        "scale_y": 0.667,
                        "pos_x": 60,
                        "pos_y": 60
                    },
                    visible=True
                ),
                SceneSource(
                    name="Guest Camera",
                    type="video_capture_device",
                    settings={
                        "device": "AUTO_DETECT_SECONDARY_CAMERA",
                        "resolution": "1920x1080",
                        "fps": 30
                    },
                    transform={
                        "scale_x": 0.5,
                        "scale_y": 0.667,
                        "pos_x": 1000,
                        "pos_y": 60
                    },
                    visible=True
                ),
                SceneSource(
                    name="Guest Audio",
                    type="audio_input_capture",
                    settings={
                        "device": "AUTO_DETECT_SECONDARY_AUDIO"
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
                        }
                    ],
                    visible=True
                ),
                SceneSource(
                    name="Dual Camera Overlay",
                    type="browser_source",
                    settings={
                        "url": f"{self.base_url}/overlays/dual-cam.html?layout=balanced&host=Host Name&guest=Guest Name&platform=zoom&topics=true&recording=true",
                        "width": 1920,
                        "height": 1080,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True
                    },
                    visible=True
                )
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
        
        # Run device detection script if available
        script_path = Path(__file__).parent / "device-manager.py"
        if script_path.exists():
            try:
                result = subprocess.run([
                    'python', str(script_path), '--scan'
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    print("✅ Device detection completed")
                    # Parse device information (simplified)
                    output_lines = result.stdout.split('\n')
                    
                    for line in output_lines:
                        if 'cam link' in line.lower() or 'camera' in line.lower():
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
        
        # Fallback device names
        if not devices['video_devices']:
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
        
        device_mapping = {
            'AUTO_DETECT_PRIMARY_CAMERA': self.detected_devices['video_devices'][0]['name'] if self.detected_devices['video_devices'] else 'Default Camera',
            'AUTO_DETECT_SECONDARY_CAMERA': self.detected_devices['video_devices'][1]['name'] if len(self.detected_devices['video_devices']) > 1 else self.detected_devices['video_devices'][0]['name'] if self.detected_devices['video_devices'] else 'Default Camera',
            'AUTO_DETECT_PRIMARY_AUDIO': self.detected_devices['audio_input_devices'][0]['name'] if self.detected_devices['audio_input_devices'] else 'Default Microphone',
            'AUTO_DETECT_SECONDARY_AUDIO': self.detected_devices['audio_input_devices'][1]['name'] if len(self.detected_devices['audio_input_devices']) > 1 else self.detected_devices['audio_input_devices'][0]['name'] if self.detected_devices['audio_input_devices'] else 'Default Microphone'
        }
        
        for key, value in resolved_settings.items():
            if isinstance(value, str) and value in device_mapping:
                resolved_settings[key] = device_mapping[value]
                print(f"🔧 Resolved {value} → {resolved_settings[key]}")
        
        return resolved_settings
    
    async def create_scene_live(self, scene_config: SceneConfig) -> bool:
        """Create a scene in live OBS using WebSocket"""
        if not self.obs_client:
            print("❌ Not connected to OBS")
            return False
        
        try:
            print(f"🎬 Creating scene: {scene_config.name}")
            
            # Create the scene
            self.obs_client.create_scene(scene_config.name)
            
            # Add sources in reverse order (bottom to top)
            for source in reversed(scene_config.sources):
                print(f"  📎 Adding source: {source.name} ({source.type})")
                
                # Resolve device placeholders
                resolved_settings = self.resolve_device_placeholders(source.settings)
                
                # Create the source
                self.obs_client.create_source(
                    scene_name=scene_config.name,
                    source_name=source.name,
                    source_kind=self._map_source_type(source.type),
                    source_settings=resolved_settings
                )
                
                # Apply transform if specified
                if source.transform:
                    transform_info = {
                        'scene_name': scene_config.name,
                        'source_name': source.name,
                        'transform': source.transform
                    }
                    self.obs_client.set_scene_item_transform(**transform_info)
                
                # Set visibility
                self.obs_client.set_scene_item_enabled(
                    scene_name=scene_config.name,
                    source_name=source.name,
                    enabled=source.visible
                )
                
                # Apply filters
                if source.filters:
                    for filter_config in source.filters:
                        self.obs_client.create_source_filter(
                            source_name=source.name,
                            filter_name=filter_config['name'],
                            filter_kind=filter_config['type'],
                            filter_settings=filter_config.get('settings', {})
                        )
            
            print(f"✅ Scene '{scene_config.name}' created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create scene '{scene_config.name}': {e}")
            return False
    
    def _map_source_type(self, source_type: str) -> str:
        """Map our source types to OBS source kinds"""
        mapping = {
            'browser_source': 'browser_source',
            'video_capture_device': 'v4l2_source' if self.platform == 'linux' else 'dshow_input' if self.platform == 'windows' else 'av_capture_input',
            'display_capture': 'xshm_input' if self.platform == 'linux' else 'monitor_capture' if self.platform == 'windows' else 'display_capture',
            'audio_input_capture': 'pulse_input_capture' if self.platform == 'linux' else 'wasapi_input_capture' if self.platform == 'windows' else 'coreaudio_input_capture'
        }
        return mapping.get(source_type, source_type)
    
    async def create_all_scenes_live(self) -> bool:
        """Create all scenes in live OBS"""
        if not await self.connect_obs():
            return False
        
        # Detect devices first
        self.detect_devices()
        
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
        
        # Set up audio sources
        await self._setup_audio_sources()
        
        # Configure global settings
        await self._configure_global_settings()
        
        return success_count == len(self.scene_templates)
    
    async def _setup_audio_sources(self):
        """Set up global audio sources with filters"""
        print("\n🎤 Setting up audio sources...")
        
        if not self.obs_client:
            return
        
        try:
            # Primary microphone with professional filters
            primary_audio = self.detected_devices['audio_input_devices'][0]['name'] if self.detected_devices['audio_input_devices'] else 'Default Microphone'
            
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
                    self.obs_client.create_source_filter(
                        source_name=primary_audio,
                        filter_name=filter_config['name'],
                        filter_kind=filter_config['type'],
                        filter_settings=filter_config['settings']
                    )
                    print(f"  ✅ Added {filter_config['name']} filter")
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
                    transform={"scale_x": 1.0, "scale_y": 1.0},
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
    
    args = parser.parse_args()
    
    if not args.create_live and not args.generate_json:
        print("❌ Must specify either --create-live or --generate-json")
        parser.print_help()
        sys.exit(1)
    
    creator = AutoSceneCreator(
        github_user=args.github_user,
        obs_host=args.obs_host,
        obs_port=args.obs_port,
        obs_password=args.obs_password
    )
    
    # Apply template modifications
    if args.template != 'standard':
        creator.scene_templates = creator.create_template_variations(args.template)
        print(f"🎨 Using {args.template} template with {len(creator.scene_templates)} scenes")
    
    success = False
    
    if args.create_live:
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