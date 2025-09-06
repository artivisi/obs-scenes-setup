#!/usr/bin/env python3
"""
Fix OBS Browser Source URLs for Custom Overlays

Updates all browser source URLs to use correct file:// paths for local overlays.
"""

import sys
import argparse
from pathlib import Path

# Add utils directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
from obs_utils import OBSConnection, OBSSceneManager, OBSSourceManager


def fix_overlay_urls(obs_host="localhost", obs_port=4455, obs_password="", overlay_path=None, use_http=True, http_host="localhost", http_port=8080):
    """Fix browser source URLs in OBS to point to correct overlay files"""
    
    if not overlay_path:
        overlay_path = Path(__file__).parent.parent.parent / "test-python-overlays"
    else:
        overlay_path = Path(overlay_path)
    
    if not overlay_path.exists():
        print(f"❌ Overlay path does not exist: {overlay_path}")
        return False
    
    # Build base URL
    if use_http:
        base_url = f"http://{http_host}:{http_port}"
        print(f"🌐 Using HTTP URLs with base: {base_url}")
    else:
        base_url = f"file://{overlay_path.absolute()}"
        print(f"📁 Using file:// URLs with base: {base_url}")
    
    overlay_files = {
        "intro": "intro.html",
        "talking-head": "talking-head.html", 
        "code-demo": "code-demo.html",
        "screen-only": "screen-only.html",
        "outro": "outro.html",
        "brb": "brb.html",
        "dual-cam": "dual-cam.html"
    }
    
    try:
        with OBSConnection(obs_host, obs_port, obs_password) as conn:
            scene_manager = OBSSceneManager(conn)
            source_manager = OBSSourceManager(conn)
            
            scenes_and_sources = scene_manager.iterate_scenes_and_sources()
            print(f"📋 Found {len(scenes_and_sources)} scenes\n")
            
            updated_count = 0
            
            for scene_name, sources in scenes_and_sources:
                print(f"🎬 Checking scene: {scene_name}")
                
                if not sources:
                    print()
                    continue
                
                for item in sources:
                    source_name = item['sourceName']
                    source_type = item.get('sourceType', 'unknown')
                    
                    # Only process browser sources
                    if source_type != 'OBS_SOURCE_TYPE_INPUT':
                        continue
                    
                    settings = source_manager.get_source_settings(source_name)
                    if not settings or 'url' not in settings:
                        continue
                    
                    current_url = settings['url']
                    
                    # Skip if URL is already correct
                    if base_url in current_url:
                        continue
                    
                    # Determine overlay type from source name
                    overlay_type = None
                    source_lower = source_name.lower()
                    
                    for overlay_key, filename in overlay_files.items():
                        if overlay_key.replace('-', '').replace('_', '') in source_lower.replace('-', '').replace('_', ''):
                            overlay_type = overlay_key
                            break
                    
                    if not overlay_type:
                        continue
                    
                    # Build new URL
                    new_url = f"{base_url}/{overlay_files[overlay_type]}"
                    
                    print(f"  📎 Updating {source_name}")
                    print(f"     URL: {new_url}")
                    
                    # Update the source
                    if source_manager.update_browser_source_url(source_name, new_url):
                        print(f"     ✅ Updated successfully")
                        updated_count += 1
                
                print()
            
            print(f"🎉 Successfully updated {updated_count} overlay sources!")
            if updated_count > 0:
                print("💡 Switch to each scene to verify overlays are displaying correctly")
            
            return True
            
    except Exception as e:
        print(f"❌ Failed to fix overlay URLs: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Fix OBS browser source URLs for custom overlays')
    parser.add_argument('--obs-host', default='localhost', help='OBS WebSocket host')
    parser.add_argument('--obs-port', type=int, default=4455, help='OBS WebSocket port')
    parser.add_argument('--obs-password', default='', help='OBS WebSocket password')
    parser.add_argument('--overlay-path', help='Path to overlay directory')
    parser.add_argument('--use-file', action='store_true', help='Use file:// URLs instead of HTTP')
    parser.add_argument('--http-host', default='localhost', help='HTTP server host for overlays')
    parser.add_argument('--http-port', type=int, default=8080, help='HTTP server port for overlays')
    
    args = parser.parse_args()
    
    success = fix_overlay_urls(
        obs_host=args.obs_host,
        obs_port=args.obs_port, 
        obs_password=args.obs_password,
        overlay_path=args.overlay_path,
        use_http=not args.use_file,
        http_host=args.http_host,
        http_port=args.http_port
    )
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()