#!/usr/bin/env python3
"""List all sources in OBS to debug overlay source names"""

import sys
import argparse
from pathlib import Path

# Add utils directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
from obs_utils import OBSConnection, OBSSceneManager, OBSSourceManager


def list_all_sources(obs_host="localhost", obs_port=4455, obs_password=""):
    """List all sources in OBS scenes"""
    
    try:
        # Use utility classes for connection and scene management
        with OBSConnection(obs_host, obs_port, obs_password) as conn:
            scene_manager = OBSSceneManager(conn)
            source_manager = OBSSourceManager(conn)
            
            # Get all scenes and sources
            scenes_and_sources = scene_manager.iterate_scenes_and_sources()
            print(f"📋 Found {len(scenes_and_sources)} scenes\n")
            
            for scene_name, sources in scenes_and_sources:
                print(f"🎬 Scene: {scene_name}")
                
                if sources:
                    for item in sources:
                        source_name = item['sourceName']
                        source_type = item.get('sourceType', 'unknown')
                        print(f"   📎 {source_name} ({source_type})")
                        
                        # If it's a browser source, show current URL
                        if source_type == 'OBS_SOURCE_TYPE_INPUT':
                            settings = source_manager.get_source_settings(source_name)
                            if settings and 'url' in settings:
                                url = settings['url']
                                print(f"      🌐 URL: {url}")
                else:
                    print("   (no sources)")
                    
        print()
        
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='List all sources in OBS scenes')
    parser.add_argument('--obs-host', default='localhost', help='OBS WebSocket host')
    parser.add_argument('--obs-port', type=int, default=4455, help='OBS WebSocket port')  
    parser.add_argument('--obs-password', default='', help='OBS WebSocket password')
    
    args = parser.parse_args()
    
    list_all_sources(args.obs_host, args.obs_port, args.obs_password)


if __name__ == "__main__":
    main()