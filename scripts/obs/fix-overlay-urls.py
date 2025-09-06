#!/usr/bin/env python3
"""
Fix OBS Browser Source URLs for Custom Overlays

Updates all browser source URLs to use correct file:// paths for local overlays.
"""

import obsws_python as obs
import sys
from pathlib import Path
import argparse

def fix_overlay_urls(obs_host="localhost", obs_port=4455, obs_password="", overlay_path=None, use_http=True, http_host="localhost", http_port=8080):
    """Fix browser source URLs in OBS to point to correct overlay files"""
    
    if not overlay_path:
        overlay_path = Path(__file__).parent.parent.parent / "test-python-overlays"
    else:
        overlay_path = Path(overlay_path)
    
    if not overlay_path.exists():
        print(f"❌ Overlay path not found: {overlay_path}")
        return False
    
    # Get overlay URLs - use HTTP for WSL/cross-platform compatibility
    if use_http:
        base_url = f"http://{http_host}:{http_port}"
        overlay_files = {
            "Intro_Scene_Dynamic_Intro_Overlay": f"{base_url}/intro.html",
            "Talking_Head_Talking_Head_Overlay": f"{base_url}/talking-head.html", 
            "Code_+_Camera_Code_Demo_Overlay": f"{base_url}/code-demo.html",
            "Screen_Only_Screen_Only_Overlay": f"{base_url}/screen-only.html",
            "BRB_/_Technical_BRB_Overlay": f"{base_url}/brb.html",
            "Outro_Scene_Outro_Overlay": f"{base_url}/outro.html"
        }
        print(f"🌐 Using HTTP URLs with base: {base_url}")
    else:
        # Fallback to file:// URLs
        overlay_files = {
            "Intro_Scene_Dynamic_Intro_Overlay": f"file://{(overlay_path / 'intro.html').absolute()}",
            "Talking_Head_Talking_Head_Overlay": f"file://{(overlay_path / 'talking-head.html').absolute()}", 
            "Code_+_Camera_Code_Demo_Overlay": f"file://{(overlay_path / 'code-demo.html').absolute()}",
            "Screen_Only_Screen_Only_Overlay": f"file://{(overlay_path / 'screen-only.html').absolute()}",
            "BRB_/_Technical_BRB_Overlay": f"file://{(overlay_path / 'brb.html').absolute()}",
            "Outro_Scene_Outro_Overlay": f"file://{(overlay_path / 'outro.html').absolute()}"
        }
        print(f"📁 Using file:// URLs from: {overlay_path}")
    
    try:
        print(f"🔌 Connecting to OBS at {obs_host}:{obs_port}...")
        
        # Connect to OBS
        if obs_password:
            ws = obs.ReqClient(host=obs_host, port=obs_port, password=obs_password)
        else:
            ws = obs.ReqClient(host=obs_host, port=obs_port)
        
        version_info = ws.get_version()
        print(f"✅ Connected to OBS Studio {version_info.obs_version}")
        
        # Get all scenes
        scenes = ws.get_scene_list()
        print(f"📋 Found {len(scenes.scenes)} scenes")
        
        fixed_count = 0
        
        for scene in scenes.scenes:
            scene_name = scene['sceneName']
            print(f"\n🎬 Checking scene: {scene_name}")
            
            # Get scene items (sources)
            try:
                scene_items = ws.get_scene_item_list(scene_name)
                
                for item in scene_items.scene_items:
                    source_name = item['sourceName']
                    
                    # Check if this is a browser source overlay we need to fix
                    if source_name in overlay_files:
                        overlay_url = overlay_files[source_name]
                        
                        print(f"  📎 Updating {source_name}")
                        print(f"     URL: {overlay_url}")
                        
                        # Update browser source settings
                        try:
                            overlay_url = overlay_files[source_name]
                            ws.set_input_settings(
                                source_name, 
                                {
                                    "url": overlay_url,
                                    "width": 1920,
                                    "height": 1080,
                                    "fps": 30
                                },
                                True  # overlay parameter
                            )
                            print(f"     ✅ Updated successfully")
                            fixed_count += 1
                            
                        except Exception as e:
                            print(f"     ❌ Failed to update: {e}")
            
            except Exception as e:
                print(f"  ⚠️  Could not get scene items for {scene_name}: {e}")
        
        ws.disconnect()
        
        if fixed_count > 0:
            print(f"\n🎉 Successfully updated {fixed_count} overlay sources!")
            print("💡 Switch to each scene to verify overlays are displaying correctly")
        else:
            print(f"\n⚠️  No overlay sources found to update")
            print("💡 Make sure the scenes were created with the correct source names")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect or update: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Fix OBS browser source URLs for custom overlays')
    parser.add_argument('--obs-host', default='localhost', help='OBS WebSocket host')
    parser.add_argument('--obs-port', type=int, default=4455, help='OBS WebSocket port')
    parser.add_argument('--obs-password', default='', help='OBS WebSocket password')
    parser.add_argument('--overlay-path', help='Path to overlay directory')
    parser.add_argument('--http-host', default='localhost', help='HTTP server host for overlays')
    parser.add_argument('--http-port', type=int, default=8080, help='HTTP server port for overlays')
    parser.add_argument('--use-files', action='store_true', help='Use file:// URLs instead of HTTP')
    
    args = parser.parse_args()
    
    success = fix_overlay_urls(
        obs_host=args.obs_host,
        obs_port=args.obs_port, 
        obs_password=args.obs_password,
        overlay_path=args.overlay_path,
        use_http=not args.use_files,
        http_host=args.http_host,
        http_port=args.http_port
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()