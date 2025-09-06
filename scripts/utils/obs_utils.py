#!/usr/bin/env python3
"""
OBS Utility Functions
Shared utilities for OBS WebSocket operations to reduce code duplication.
"""

import obsws_python as obs
import subprocess
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path


class OBSConnection:
    """Manages OBS WebSocket connection with automatic WSL detection"""
    
    def __init__(self, host: str = "localhost", port: int = 4455, password: str = ""):
        self.host = self._get_obs_host_ip(host)
        self.port = port
        self.password = password
        self.client = None
        self._version_info = None
    
    def _get_obs_host_ip(self, provided_host: str) -> str:
        """Auto-detect OBS host IP for WSL environment"""
        # If user explicitly provided a non-localhost IP, use it
        if provided_host not in ["localhost", "127.0.0.1"]:
            return provided_host
            
        # Check if we're in WSL
        try:
            with open("/proc/version", "r") as f:
                if "microsoft" in f.read().lower():
                    # WSL - get Windows host IP (default gateway)
                    result = subprocess.run(
                        ["ip", "route", "show", "default"], 
                        capture_output=True, text=True, check=True
                    )
                    for line in result.stdout.split('\n'):
                        if 'default via' in line:
                            windows_host_ip = line.strip().split()[2]
                            print(f"🔍 WSL detected - using Windows host IP: {windows_host_ip}")
                            return windows_host_ip
        except Exception as e:
            print(f"⚠️  WSL detection failed: {e}")
            
        # Default fallback
        return provided_host
    
    def connect(self) -> bool:
        """Establish connection to OBS"""
        try:
            print(f"🔌 Connecting to OBS at {self.host}:{self.port}...")
            
            # Connect to OBS
            if self.password:
                self.client = obs.ReqClient(host=self.host, port=self.port, password=self.password)
            else:
                self.client = obs.ReqClient(host=self.host, port=self.port)
            
            self._version_info = self.client.get_version()
            print(f"✅ Connected to OBS Studio {self._version_info.obs_version}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Close OBS connection"""
        if self.client:
            try:
                self.client.disconnect()
            except:
                pass
            self.client = None
    
    def get_version_info(self) -> Optional[Any]:
        """Get OBS version information"""
        return self._version_info
    
    def __enter__(self):
        """Context manager entry"""
        if self.connect():
            return self
        raise ConnectionError("Failed to connect to OBS")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()


class OBSSceneManager:
    """Manages OBS scenes and sources"""
    
    def __init__(self, connection: OBSConnection):
        self.client = connection.client
        if not self.client:
            raise ValueError("OBS connection not established")
    
    def list_all_scenes(self) -> List[Dict[str, Any]]:
        """Get list of all scenes"""
        scenes = self.client.get_scene_list()
        return scenes.scenes
    
    def list_scene_sources(self, scene_name: str) -> List[Dict[str, Any]]:
        """Get sources in a specific scene"""
        try:
            scene_items = self.client.get_scene_item_list(scene_name)
            return scene_items.scene_items if scene_items.scene_items else []
        except Exception as e:
            print(f"⚠️  Could not get sources for scene '{scene_name}': {e}")
            return []
    
    def iterate_scenes_and_sources(self) -> List[Tuple[str, List[Dict[str, Any]]]]:
        """Iterate through all scenes and their sources"""
        result = []
        scenes = self.list_all_scenes()
        
        for scene in scenes:
            scene_name = scene['sceneName']
            sources = self.list_scene_sources(scene_name)
            result.append((scene_name, sources))
        
        return result
    
    def scene_exists(self, scene_name: str) -> bool:
        """Check if a scene exists"""
        scenes = self.list_all_scenes()
        return any(scene['sceneName'] == scene_name for scene in scenes)
    
    def remove_scene(self, scene_name: str) -> bool:
        """Remove a scene"""
        try:
            self.client.remove_scene(scene_name)
            print(f"  🗑️  Removed scene: {scene_name}")
            return True
        except Exception as e:
            print(f"  ⚠️  Could not remove scene {scene_name}: {e}")
            return False
    
    def cleanup_all_scenes(self, preserve_default: bool = True) -> None:
        """Remove all scenes (optionally preserve default scene)"""
        print("🧹 Cleaning up existing scenes and sources...")
        
        scene_list = self.list_all_scenes()
        current_scene = scene_list[0]['sceneName'] if scene_list else None
        
        scenes_to_remove = []
        for scene_config in scene_list:
            scene_name = scene_config['sceneName']
            
            # Don't remove the default scene if it's the only one and preserve_default is True
            if preserve_default and len(scene_list) == 1 and scene_name == current_scene:
                continue
                
            scenes_to_remove.append(scene_name)
        
        # Remove scenes
        for scene_name in scenes_to_remove:
            self.remove_scene(scene_name)
        
        # Clean up orphaned global sources
        self._cleanup_orphaned_sources()
        
        print("✅ Cleanup completed")
    
    def _cleanup_orphaned_sources(self):
        """Remove sources that are no longer used in any scene"""
        try:
            # This is a simplified cleanup - more complex logic could be added
            # to track and remove truly orphaned sources
            pass
        except Exception as e:
            print(f"⚠️  Could not clean up orphaned sources: {e}")


class OBSSourceManager:
    """Manages OBS sources"""
    
    def __init__(self, connection: OBSConnection):
        self.client = connection.client
        if not self.client:
            raise ValueError("OBS connection not established")
    
    def find_browser_sources(self, scene_name: str) -> List[Dict[str, Any]]:
        """Find all browser sources in a scene"""
        scene_manager = OBSSceneManager(OBSConnection())
        scene_manager.client = self.client
        
        sources = scene_manager.list_scene_sources(scene_name)
        return [source for source in sources if source.get('sourceType') == 'OBS_SOURCE_TYPE_INPUT']
    
    def update_browser_source_url(self, source_name: str, new_url: str) -> bool:
        """Update URL of a browser source"""
        try:
            current_settings = self.client.get_input_settings(source_name)
            
            # Update URL in settings
            new_settings = current_settings.input_settings.copy()
            new_settings['url'] = new_url
            
            # Apply new settings
            self.client.set_input_settings(source_name, new_settings, True)
            return True
            
        except Exception as e:
            print(f"     ❌ Failed to update {source_name}: {e}")
            return False
    
    def get_source_settings(self, source_name: str) -> Optional[Dict[str, Any]]:
        """Get settings for a source"""
        try:
            settings = self.client.get_input_settings(source_name)
            return settings.input_settings
        except Exception as e:
            print(f"⚠️  Could not get settings for source '{source_name}': {e}")
            return None


def get_wsl_server_ip() -> str:
    """Get the appropriate IP address for HTTP server in WSL"""
    try:
        # Check if we're in WSL
        with open("/proc/version", "r") as f:
            if "microsoft" in f.read().lower():
                # WSL - get eth0 IP address that Windows can reach
                result = subprocess.run(
                    ["ip", "addr", "show", "eth0"], 
                    capture_output=True, text=True, check=True
                )
                for line in result.stdout.split('\n'):
                    if 'inet ' in line and '127.0.0.1' not in line:
                        ip = line.strip().split()[1].split('/')[0]
                        return ip
    except:
        pass
    
    # Default fallback - get first non-localhost IP
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "localhost"


# Convenience functions for backward compatibility
def connect_to_obs(host: str = "localhost", port: int = 4455, password: str = "") -> OBSConnection:
    """Create and connect to OBS - convenience function"""
    connection = OBSConnection(host, port, password)
    if connection.connect():
        return connection
    raise ConnectionError("Failed to connect to OBS")


def list_all_scenes_and_sources(host: str = "localhost", port: int = 4455, password: str = "") -> List[Tuple[str, List[Dict[str, Any]]]]:
    """List all scenes and sources - convenience function"""
    with connect_to_obs(host, port, password) as conn:
        scene_manager = OBSSceneManager(conn)
        return scene_manager.iterate_scenes_and_sources()