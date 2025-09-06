#!/usr/bin/env python3
"""
Scene Webserver Launcher with Environment Detection

Launches HTTP server for scene overlays with proper networking configuration
for different environments (WSL, macOS, Linux). Handles OBS address and
scene webserver address based on the running environment.

Usage:
    python scripts/serve-scenes.py generated-scenes/my-event-abc123_20240906_143022
    python scripts/serve-scenes.py generated-scenes/my-event-abc123_20240906_143022 --port 8080
"""

import argparse
import subprocess
import socket
import sys
import json
import platform
import os
from pathlib import Path
from typing import Tuple, Dict, Any
import threading
import time

class SceneWebserver:
    """HTTP server launcher with environment-specific networking"""
    
    def __init__(self, scenes_dir: Path, port: int = 8080):
        self.scenes_dir = scenes_dir
        self.port = port
        self.project_root = Path(__file__).parent.parent
        self.metadata = {}
        self.server_process = None
        
        # Environment detection
        self.platform = platform.system().lower()
        self.is_wsl = self._detect_wsl()
        
    def _detect_wsl(self) -> bool:
        """Detect if running in WSL environment"""
        try:
            with open("/proc/version", "r") as f:
                return "microsoft" in f.read().lower()
        except:
            return False
    
    def load_metadata(self) -> bool:
        """Load scene collection metadata"""
        metadata_file = self.scenes_dir / "scene-collection.json"
        if not metadata_file.exists():
            print(f"⚠️  No metadata file found: {metadata_file}")
            return False
            
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            
            print(f"📖 Loaded metadata for: {self.metadata.get('collection_name', 'Unknown')}")
            return True
        except Exception as e:
            print(f"❌ Failed to load metadata: {e}")
            return False
    
    def get_network_addresses(self) -> Tuple[str, str]:
        """Get webserver and OBS addresses based on environment"""
        webserver_ip = self._get_webserver_ip()
        obs_ip = self._get_obs_ip()
        
        print(f"🌐 Network Configuration:")
        print(f"   Environment: {self._get_environment_description()}")
        print(f"   Webserver IP: {webserver_ip}")
        print(f"   OBS IP: {obs_ip}")
        
        return webserver_ip, obs_ip
    
    def _get_environment_description(self) -> str:
        """Get human-readable environment description"""
        if self.is_wsl:
            return "WSL (Windows Subsystem for Linux)"
        elif self.platform == "darwin":
            return "macOS"
        elif self.platform == "linux":
            return "Linux"
        elif self.platform == "windows":
            return "Windows"
        else:
            return f"Unknown ({self.platform})"
    
    def _get_webserver_ip(self) -> str:
        """Get appropriate IP address for HTTP server"""
        if self.is_wsl:
            # WSL - get eth0 IP that Windows can reach
            try:
                result = subprocess.run(
                    ["ip", "addr", "show", "eth0"], 
                    capture_output=True, text=True, check=True
                )
                for line in result.stdout.split('\n'):
                    if 'inet ' in line and '127.0.0.1' not in line:
                        return line.strip().split()[1].split('/')[0]
            except:
                pass
        
        # Default fallback - get first non-localhost IP
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except:
            return "localhost"
    
    def _get_obs_ip(self) -> str:
        """Get OBS WebSocket IP address"""
        if self.is_wsl:
            # WSL - OBS is running on Windows host
            try:
                result = subprocess.run(
                    ["ip", "route", "show", "default"], 
                    capture_output=True, text=True, check=True
                )
                for line in result.stdout.split('\n'):
                    if 'default via' in line:
                        return line.strip().split()[2]
            except:
                pass
        
        # macOS, Linux, Windows - OBS is local
        return "localhost"
    
    def _find_available_port(self, start_port: int) -> int:
        """Find an available port starting from start_port"""
        for port in range(start_port, start_port + 100):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        return start_port  # fallback
    
    def start_server(self) -> bool:
        """Start HTTP server for scene overlays"""
        if not self.scenes_dir.exists():
            print(f"❌ Scenes directory not found: {self.scenes_dir}")
            return False
        
        # Find available port
        available_port = self._find_available_port(self.port)
        if available_port != self.port:
            print(f"⚠️  Port {self.port} busy, using port {available_port}")
            self.port = available_port
        
        webserver_ip, obs_ip = self.get_network_addresses()
        
        try:
            # Change to scenes directory
            original_cwd = os.getcwd()
            os.chdir(self.scenes_dir)
            
            # Start HTTP server
            print(f"🚀 Starting HTTP server...")
            print(f"   Directory: {self.scenes_dir}")
            print(f"   Port: {self.port}")
            
            # Use subprocess to start server in background
            self.server_process = subprocess.Popen([
                sys.executable, "-m", "http.server", str(self.port)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Give server time to start
            time.sleep(1)
            
            # Check if server started successfully
            if self.server_process.poll() is None:
                print(f"✅ HTTP server running successfully!")
                print(f"🌐 Base URL: http://{webserver_ip}:{self.port}/")
                
                # Show scene URLs
                self._show_scene_urls(webserver_ip)
                
                # Show next steps
                self._show_next_steps(webserver_ip, obs_ip)
                
                # Restore directory
                os.chdir(original_cwd)
                return True
            else:
                error_output = self.server_process.stderr.read().decode()
                print(f"❌ Failed to start server: {error_output}")
                os.chdir(original_cwd)
                return False
                
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def _show_scene_urls(self, webserver_ip: str):
        """Display URLs for each scene"""
        html_files = list(self.scenes_dir.glob("*.html"))
        if html_files:
            print(f"\\n🎨 Scene URLs ({len(html_files)} scenes):")
            for html_file in sorted(html_files):
                scene_name = html_file.stem
                url = f"http://{webserver_ip}:{self.port}/{html_file.name}"
                print(f"   {scene_name:15} {url}")
    
    def _show_next_steps(self, webserver_ip: str, obs_ip: str):
        """Show next steps for OBS integration"""
        collection_name = self.metadata.get('collection_name', 'unknown')
        
        print(f"\\n📋 Next Steps:")
        print(f"   1. Keep this server running (Ctrl+C to stop)")
        print(f"   2. Inject scenes into OBS:")
        print(f"      python scripts/inject-obs.py --collection {collection_name} \\\\")
        print(f"                                  --webserver http://{webserver_ip}:{self.port} \\\\")
        print(f"                                  --obs-host {obs_ip}")
        
        print(f"\\n💡 Test in browser first:")
        print(f"   http://{webserver_ip}:{self.port}/")
    
    def wait_for_server(self):
        """Wait for server to finish (until Ctrl+C)"""
        if not self.server_process:
            return
            
        try:
            print(f"\\n🖥️  Server running. Press Ctrl+C to stop...")
            self.server_process.wait()
        except KeyboardInterrupt:
            print(f"\\n⏹️  Stopping server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
            print(f"✅ Server stopped successfully")
        except Exception as e:
            print(f"⚠️  Server error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Launch HTTP server for OBS scene overlays')
    parser.add_argument('scenes_dir', type=Path, help='Directory containing generated scenes')
    parser.add_argument('--port', type=int, default=8080, help='HTTP server port (default: 8080)')
    parser.add_argument('--test', action='store_true', help='Test network configuration only')
    
    args = parser.parse_args()
    
    if not args.scenes_dir.exists():
        print(f"❌ Scenes directory not found: {args.scenes_dir}")
        sys.exit(1)
    
    server = SceneWebserver(args.scenes_dir, args.port)
    
    # Load metadata if available
    server.load_metadata()
    
    if args.test:
        # Just show network configuration
        webserver_ip, obs_ip = server.get_network_addresses()
        print(f"\\n🧪 Network Test Complete")
        print(f"   Webserver would use: {webserver_ip}:{args.port}")
        print(f"   OBS would connect to: {obs_ip}:4455")
        return
    
    if not server.start_server():
        sys.exit(1)
    
    # Wait for server to finish
    server.wait_for_server()

if __name__ == "__main__":
    main()