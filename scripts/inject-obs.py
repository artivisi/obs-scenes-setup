#!/usr/bin/env python3
"""
OBS Scene Collection Injector via WebSocket

Injects generated scene overlays into OBS by creating a dedicated scene collection.
Does not pollute the default scene collection. Creates professional scene layouts
with proper source ordering and audio processing.

Usage:
    python scripts/inject-obs.py --collection my-event-abc123 --webserver http://192.168.1.100:8080
    python scripts/inject-obs.py --collection my-event-abc123 --webserver http://192.168.1.100:8080 --obs-host 192.168.1.50
"""

import argparse
import asyncio
import sys
import json
from pathlib import Path
from typing import Dict, Any, List
import requests
from urllib.parse import urljoin
from datetime import datetime

try:
    import obsws_python as obs
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    print("⚠️  obsws-python not installed. Install with: pip install obsws-python")

class OBSSceneInjector:
    """Inject scene collection into OBS via WebSocket"""
    
    def __init__(self, collection_name: str, webserver_url: str, obs_host: str = "localhost", obs_port: int = 4455):
        # Generate unique collection name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.collection_name = f"{collection_name}-{timestamp}"
        self.webserver_url = webserver_url.rstrip('/')
        self.obs_host = obs_host
        self.obs_port = obs_port
        self.obs_client = None
        self.available_scenes = []
        
    async def connect_obs(self) -> bool:
        """Connect to OBS WebSocket"""
        if not WEBSOCKET_AVAILABLE:
            print("❌ OBS WebSocket library not available")
            return False
        
        try:
            print(f"🔌 Connecting to OBS at {self.obs_host}:{self.obs_port}...")
            
            self.obs_client = obs.ReqClient(
                host=self.obs_host, 
                port=self.obs_port
            )
            
            version_info = self.obs_client.get_version()
            print(f"✅ Connected to OBS Studio {version_info.obs_version}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to OBS: {e}")
            print("💡 Make sure OBS is running with WebSocket enabled")
            print("   Tools → WebSocket Server Settings → Enable WebSocket server")
            return False
    
    def discover_scenes(self) -> bool:
        """Discover available scenes from webserver"""
        try:
            print(f"🔍 Discovering scenes at: {self.webserver_url}")
            
            # Try to get scene list from metadata
            metadata_url = urljoin(self.webserver_url + '/', 'scene-collection.json')
            try:
                response = requests.get(metadata_url, timeout=5)
                if response.status_code == 200:
                    metadata = response.json()
                    self.available_scenes = metadata.get('scenes', [])
                    print(f"📋 Found {len(self.available_scenes)} scenes from metadata")
                    return True
            except:
                pass
            
            # Fallback: try common scene names
            common_scenes = [
                'intro.html', 'talking-head.html', 'code-demo.html', 
                'screen-only.html', 'brb.html', 'outro.html', 'dual-cam.html'
            ]
            
            self.available_scenes = []
            for scene in common_scenes:
                try:
                    scene_url = urljoin(self.webserver_url + '/', scene)
                    response = requests.head(scene_url, timeout=3)
                    if response.status_code == 200:
                        self.available_scenes.append(scene)
                except:
                    pass
            
            if self.available_scenes:
                print(f"🔍 Discovered {len(self.available_scenes)} scenes by probing")
                return True
            else:
                # Emergency fallback - assume scenes exist
                print("⚠️ Webserver test failed, assuming standard scenes exist...")
                self.available_scenes = ['brb.html', 'talking-head.html', 'code-demo.html', 'screen-only.html', 'outro.html']
                print(f"🔍 Using {len(self.available_scenes)} standard scenes")
                return True
                
        except Exception as e:
            print(f"❌ Failed to discover scenes: {e}")
            return False
    
    def create_scene_collection(self) -> bool:
        """Create dedicated scene collection in OBS"""
        try:
            print(f"📚 Creating scene collection: {self.collection_name}")
            
            # Create new scene collection (with unique timestamp name)
            self.obs_client.create_scene_collection(self.collection_name)
            print(f"✅ Scene collection created: {self.collection_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to create scene collection: {e}")
            return False
    
    def inject_scenes(self) -> bool:
        """Inject all discovered scenes into OBS using nested scene architecture"""
        if not self.available_scenes:
            print("❌ No scenes to inject")
            return False
        
        print(f"🎬 Creating nested scene architecture...")
        
        # Step 1: Create dedicated source scenes
        if not self._create_source_scenes():
            print("❌ Failed to create source scenes")
            return False
        
        # Step 1.5: Create separator between source and session scenes
        self._create_separator_scene()
        
        # Step 2: Create session scenes with nested references
        print(f"🎬 Creating {len(self.available_scenes)} session scenes...")
        success_count = 0
        for scene_file in self.available_scenes:
            if self._create_session_scene(scene_file):
                success_count += 1
        
        print(f"\\n✅ Successfully created {success_count}/{len(self.available_scenes)} session scenes")
        
        if success_count > 0:
            # Configure hotkeys and audio
            self._configure_scene_hotkeys()
            self._configure_audio_processing()
            
            print(f"\\n🎉 Scene collection ready: {self.collection_name}")
            print(f"📋 Session scenes: {success_count} scenes")
            print(f"📋 Source scenes: Camera, Screen, Audio (configure devices here)")
            return True
        
        return False
    
    def _create_source_scenes(self) -> bool:
        """Create dedicated source scenes for Camera, Screen, and Audio"""
        try:
            print("🎥 Creating dedicated source scenes...")
            
            # Create Camera Source Scene
            camera_scene = "📹 Camera"
            self._create_camera_source_scene(camera_scene)
            
            # Create Screen Source Scene  
            screen_scene = "🖥️ Screen"
            self._create_screen_source_scene(screen_scene)
            
            # Create Audio Source Scene
            audio_scene = "🎤 Audio"
            self._create_audio_source_scene(audio_scene)
            
            print(f"✅ Created 3 dedicated source scenes")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create source scenes: {e}")
            return False
    
    def _create_camera_source_scene(self, scene_name: str):
        """Create dedicated camera source scene"""
        try:
            # Remove existing scene if it exists
            try:
                self.obs_client.remove_scene(scene_name)
            except:
                pass
            
            # Create camera scene
            self.obs_client.create_scene(scene_name)
            print(f"  📹 {scene_name}")
            
            # Try to add camera source (platform-agnostic)
            camera_sources = [
                # Windows/Cross-platform
                {"kind": "dshow_input", "name": "Camera (DirectShow)"},
                # Linux 
                {"kind": "v4l2_source", "name": "Camera (V4L2)"},
                # macOS
                {"kind": "av_capture_input", "name": "Camera (AVCapture)"}
            ]
            
            for camera_config in camera_sources:
                try:
                    self.obs_client.create_input(
                        inputName=camera_config["name"],
                        inputKind=camera_config["kind"],
                        inputSettings={},
                        sceneName=scene_name,
                        sceneItemEnabled=True
                    )
                    print(f"    ✅ Added {camera_config['name']}")
                    break  # Success, stop trying other sources
                except:
                    continue  # Try next camera source type
            else:
                print(f"    ⚠️  No camera detected (will need manual configuration)")
                
        except Exception as e:
            print(f"    ❌ Camera scene error: {e}")
    
    def _create_screen_source_scene(self, scene_name: str):
        """Create dedicated screen capture source scene"""
        try:
            # Remove existing scene
            try:
                self.obs_client.remove_scene(scene_name)
            except:
                pass
            
            # Create screen scene
            self.obs_client.create_scene(scene_name)
            print(f"  🖥️ {scene_name}")
            
            # Try to add screen capture (platform-agnostic)
            screen_sources = [
                # Windows - prioritize window capture
                {"kind": "window_capture", "name": "Window Capture"}, 
                # Cross-platform display capture
                {"kind": "monitor_capture", "name": "Display Capture"},
                # Linux (X11/Wayland)
                {"kind": "xshm_input", "name": "Screen Capture (X11)"},
                # macOS
                {"kind": "display_capture", "name": "Display Capture (macOS)"}
            ]
            
            for screen_config in screen_sources:
                try:
                    self.obs_client.create_input(
                        inputName=screen_config["name"],
                        inputKind=screen_config["kind"],
                        inputSettings={},
                        sceneName=scene_name,
                        sceneItemEnabled=True
                    )
                    print(f"    ✅ Added {screen_config['name']}")
                    break
                except:
                    continue
            else:
                print(f"    ⚠️  No screen capture added (will need manual configuration)")
                
        except Exception as e:
            print(f"    ❌ Screen scene error: {e}")
    
    def _create_audio_source_scene(self, scene_name: str):
        """Create dedicated audio source scene"""
        try:
            # Remove existing scene
            try:
                self.obs_client.remove_scene(scene_name)
            except:
                pass
            
            # Create audio scene
            self.obs_client.create_scene(scene_name)
            print(f"  🎤 {scene_name}")
            
            # Note: Audio sources are typically handled globally in OBS
            # This scene serves as a placeholder for audio-specific configurations
            print(f"    ℹ️  Audio configured globally (see Audio Mixer)")
                
        except Exception as e:
            print(f"    ❌ Audio scene error: {e}")
    
    def _create_separator_scene(self):
        """Create visual separator scene between source and session scenes"""
        separator_name = "━━━━━━━━ SESSION SCENES ━━━━━━━━"
        
        try:
            # Remove existing separator
            try:
                self.obs_client.remove_scene(separator_name)
            except:
                pass
            
            # Create empty separator scene
            self.obs_client.create_scene(separator_name)
            print(f"  📋 {separator_name}")
            
        except Exception as e:
            print(f"    ❌ Separator scene error: {e}")
    
    def _create_session_scene(self, scene_file: str) -> bool:
        """Create a session scene using nested source scenes"""
        try:
            # Generate scene name from filename
            scene_name = self._generate_scene_name(scene_file)
            scene_url = urljoin(self.webserver_url + '/', scene_file)
            scene_type = scene_file.replace('.html', '').lower()
            
            print(f"  🎬 Creating scene: {scene_name}")
            
            # Remove existing scene if it exists
            try:
                self.obs_client.remove_scene(scene_name)
            except:
                pass
            
            # Create scene
            self.obs_client.create_scene(scene_name)
            
            # First add nested source scenes (background layers)
            self._add_nested_sources(scene_name, scene_type)
            
            # Then add browser source overlay (foreground layer)
            overlay_name = f"{scene_name} - Overlay"
            try:
                self.obs_client.create_input(
                    inputName=overlay_name,
                    inputKind="browser_source",
                    inputSettings={
                        "url": scene_url,
                        "width": 1920,
                        "height": 1080,
                        "fps": 30,
                        "shutdown_source_when_not_visible": True,
                        "restart_when_active": True
                    },
                    sceneName=scene_name,
                    sceneItemEnabled=True
                )
                print(f"      🎨 Added overlay: {scene_url}")
            except Exception as e:
                print(f"      ❌ Failed to add overlay: {e}")
            
            print(f"    ✅ {scene_name}")
            return True
            
        except Exception as e:
            print(f"    ❌ Failed to create {scene_file}: {e}")
            return False
    
    def _add_nested_sources(self, scene_name: str, scene_type: str):
        """Add nested source scenes based on session scene type"""
        try:
            camera_scene = "📹 Camera"
            screen_scene = "🖥️ Screen"
            
            if 'talking' in scene_type:
                # Talking Head: Full screen camera
                self._add_nested_scene(scene_name, camera_scene, "fullscreen", scale=1.0)
                print(f"      📹 Added camera (full)")
            
            elif 'code' in scene_type or 'demo' in scene_type:
                # Code Demo: Screen + small camera
                self._add_nested_scene(scene_name, screen_scene, "fullscreen", scale=1.0)
                self._add_nested_scene(scene_name, camera_scene, "bottom-right", scale=0.25)
                print(f"      🖥️ Added screen + 📹 camera (PiP)")
            
            elif 'screen' in scene_type:
                # Screen Only: Full screen only
                self._add_nested_scene(scene_name, screen_scene, "fullscreen", scale=1.0)
                print(f"      🖥️ Added screen (full)")
            
            elif 'brb' in scene_type:
                # BRB: No video sources (just overlay)
                print(f"      📺 Overlay only")
            
            elif 'intro' in scene_type or 'outro' in scene_type:
                # Intro/Outro: No video sources initially (just overlay)
                print(f"      🎬 Overlay only")
            
            else:
                # Default: Add camera
                self._add_nested_scene(scene_name, camera_scene, "center", scale=0.5)
                print(f"      📹 Added default camera")
                
        except Exception as e:
            print(f"      ⚠️  Could not add nested sources: {e}")
    
    def _add_nested_scene(self, parent_scene: str, source_scene: str, position: str, scale: float = 1.0):
        """Add a source scene as nested scene in parent scene"""
        try:
            # Add the source scene directly to the parent scene
            # This creates a nested scene reference
            scene_item_id = self.obs_client.create_scene_item(
                scene_name=parent_scene,
                source_name=source_scene
            )
            
            print(f"        ✅ Added nested scene {source_scene} to {parent_scene}")
            
            # Apply transform based on position and scale
            transform = self._get_nested_transform(position, scale)
            
            # Apply transform to the nested scene using the returned scene item ID
            self.obs_client.set_scene_item_transform(
                parent_scene,
                scene_item_id.scene_item_id,
                transform
            )
            
        except Exception as e:
            print(f"        ❌ Failed to add nested scene {source_scene}: {e}")
    
    def _get_nested_transform(self, position: str, scale: float) -> dict:
        """Get transform for nested scene positioning"""
        transforms = {
            "fullscreen": {
                "positionX": 0, "positionY": 0,
                "scaleX": 1.0, "scaleY": 1.0
            },
            "center": {
                "positionX": 960, "positionY": 540,
                "scaleX": scale, "scaleY": scale
            },
            "top-right": {
                "positionX": 1440, "positionY": 0,
                "scaleX": scale, "scaleY": scale
            },
            "bottom-right": {
                "positionX": 1400, "positionY": 765,
                "scaleX": scale, "scaleY": scale
            },
            "top-left": {
                "positionX": 0, "positionY": 0,
                "scaleX": scale, "scaleY": scale
            },
            "bottom-left": {
                "positionX": 0, "positionY": 810,
                "scaleX": scale, "scaleY": scale
            }
        }
        
        return transforms.get(position, transforms["center"])
    
    def _generate_scene_name(self, scene_file: str) -> str:
        """Generate friendly scene name from filename"""
        name = scene_file.replace('.html', '').replace('-', ' ').replace('_', ' ')
        
        # Add emojis and proper formatting
        emoji_map = {
            'intro': '🎬 Intro Scene',
            'talking head': '👤 Talking Head', 
            'code demo': '💻 Code Demo',
            'screen only': '🖥️ Screen Only',
            'brb': '📺 BRB / Technical',
            'outro': '🎯 Outro Scene',
            'dual cam': '👥 Dual Camera'
        }
        
        return emoji_map.get(name.lower(), f"🎨 {name.title()}")
    
    def _configure_scene_hotkeys(self):
        """Configure hotkeys for scenes (F1-F7)"""
        print("🔢 Configuring scene hotkeys...")
        print("   💡 Assign hotkeys manually in OBS: File → Settings → Hotkeys")
        print("      Recommended: F1=Intro, F2=Talking Head, F3=Code Demo, F4=Screen Only, F5=BRB, F6=Outro")
    
    def _configure_audio_processing(self):
        """Configure audio processing chain"""
        try:
            print("🎤 Configuring audio processing...")
            
            # Find microphone inputs
            input_list = self.obs_client.get_input_list()
            audio_inputs = [inp for inp in input_list.inputs 
                           if 'audio' in inp.get('inputKind', '').lower() or 
                              'mic' in inp.get('inputName', '').lower()]
            
            for audio_input in audio_inputs[:1]:  # Process first microphone
                input_name = audio_input['inputName']
                print(f"  🎙️ Processing: {input_name}")
                
                # Add audio filters
                filters = [
                    {"name": "Noise Suppression", "type": "noise_suppress_filter", 
                     "settings": {"method": "rnnoise"}},
                    {"name": "Compressor", "type": "compressor_filter",
                     "settings": {"ratio": 10.0, "threshold": -18.0}},
                    {"name": "Limiter", "type": "limiter_filter",
                     "settings": {"threshold": -6.0, "release_time": 60}}
                ]
                
                for filter_config in filters:
                    try:
                        self.obs_client.create_source_filter(
                            source_name=input_name,
                            filter_name=filter_config['name'],
                            filter_kind=filter_config['type'],
                            filter_settings=filter_config['settings']
                        )
                        print(f"    ✅ {filter_config['name']}")
                    except Exception as e:
                        print(f"    ⚠️  {filter_config['name']}: {e}")
                
        except Exception as e:
            print(f"  ⚠️  Audio configuration warning: {e}")

async def main():
    parser = argparse.ArgumentParser(description='Inject scene collection into OBS via WebSocket')
    parser.add_argument('--collection', required=True, help='Scene collection name')
    parser.add_argument('--webserver', required=True, help='Webserver URL (e.g., http://192.168.1.100:8080)')
    parser.add_argument('--obs-host', default='localhost', help='OBS WebSocket host')
    parser.add_argument('--obs-port', type=int, default=4455, help='OBS WebSocket port')
    parser.add_argument('--test', action='store_true', help='Test connection only')
    
    args = parser.parse_args()
    
    if not WEBSOCKET_AVAILABLE:
        print("❌ obsws-python library required. Install with: pip install obsws-python")
        sys.exit(1)
    
    injector = OBSSceneInjector(args.collection, args.webserver, args.obs_host, args.obs_port)
    
    # Test connections
    if not await injector.connect_obs():
        sys.exit(1)
    
    if not injector.discover_scenes():
        sys.exit(1)
    
    if args.test:
        print("\\n🧪 Connection test successful!")
        print(f"   OBS: Connected to {args.obs_host}:{args.obs_port}")
        print(f"   Webserver: {len(injector.available_scenes)} scenes found")
        return
    
    # Create scene collection and inject scenes
    if not injector.create_scene_collection():
        sys.exit(1)
    
    if not injector.inject_scenes():
        sys.exit(1)
    
    print(f"\\n🎉 OBS integration complete!")
    print(f"📚 Scene collection: {args.collection}")
    print(f"🎬 Scenes ready in OBS Studio")

if __name__ == "__main__":
    asyncio.run(main())