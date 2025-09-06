#!/usr/bin/env python3
"""List all sources in OBS to debug overlay source names"""

import obsws_python as obs
import sys
import argparse

def list_all_sources(obs_host="localhost", obs_port=4455, obs_password=""):
    """List all sources in OBS scenes"""
    
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
        print(f"📋 Found {len(scenes.scenes)} scenes\n")
        
        for scene in scenes.scenes:
            scene_name = scene['sceneName']
            print(f"🎬 Scene: {scene_name}")
            
            try:
                scene_items = ws.get_scene_item_list(scene_name)
                
                if scene_items.scene_items:
                    for item in scene_items.scene_items:
                        source_name = item['sourceName']
                        source_type = item.get('sourceType', 'unknown')
                        print(f"   📎 {source_name} ({source_type})")
                        
                        # If it's a browser source, show current URL
                        if source_type == 'browser_source':
                            try:
                                settings = ws.get_input_settings(source_name)
                                url = settings.input_settings.get('url', 'No URL set')
                                print(f"      🌐 URL: {url}")
                            except:
                                print(f"      ❌ Could not get settings")
                else:
                    print("   (no sources)")
                    
            except Exception as e:
                print(f"   ❌ Error getting scene items: {e}")
            
            print()
        
        ws.disconnect()
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='List all OBS sources for debugging')
    parser.add_argument('--obs-host', default='localhost', help='OBS WebSocket host')
    parser.add_argument('--obs-port', type=int, default=4455, help='OBS WebSocket port') 
    parser.add_argument('--obs-password', default='', help='OBS WebSocket password')
    
    args = parser.parse_args()
    
    success = list_all_sources(
        obs_host=args.obs_host,
        obs_port=args.obs_port,
        obs_password=args.obs_password
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()