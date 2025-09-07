#!/usr/bin/env python3
"""
Generate OBS Scene Collection JSON file for direct import into OBS Studio.
Creates a complete scene collection that users can import via Scene Collection → Import.
"""

import json
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

def load_config(config_path: Path) -> Dict[str, Any]:
    """Load YAML configuration"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def create_browser_source(name: str, url: str, width: int = 1920, height: int = 1080) -> Dict[str, Any]:
    """Create OBS browser source configuration"""
    return {
        "id": "browser_source",
        "name": name,
        "settings": {
            "url": url,
            "width": width,
            "height": height,
            "fps": 30,
            "css": "",
            "shutdown": True,
            "restart_when_active": True
        },
        "enabled": True,
        "visible": True,
        "transform": {
            "pos": {"x": 0.0, "y": 0.0},
            "rot": 0.0,
            "scale": {"x": 1.0, "y": 1.0},
            "crop": {"left": 0, "top": 0, "right": 0, "bottom": 0}
        }
    }

def create_video_source(name: str, device_id: str = "") -> Dict[str, Any]:
    """Create OBS video capture device source"""
    return {
        "id": "v4l2_input" if sys.platform.startswith('linux') else "dshow_input",
        "name": name,
        "settings": {
            "device_id": device_id,
            "resolution": "1920x1080",
            "fps": 30
        },
        "enabled": True,
        "visible": True,
        "transform": {
            "pos": {"x": 0.0, "y": 0.0},
            "rot": 0.0,
            "scale": {"x": 1.0, "y": 1.0},
            "crop": {"left": 0, "top": 0, "right": 0, "bottom": 0}
        }
    }

def create_display_source(name: str, display_id: int = 0) -> Dict[str, Any]:
    """Create OBS display capture source"""
    return {
        "id": "monitor_capture" if sys.platform == "darwin" else "xshm_input" if sys.platform.startswith('linux') else "monitor_capture",
        "name": name,
        "settings": {
            "display": display_id
        },
        "enabled": True,
        "visible": True,
        "transform": {
            "pos": {"x": 0.0, "y": 0.0},
            "rot": 0.0,
            "scale": {"x": 1.0, "y": 1.0},
            "crop": {"left": 0, "top": 0, "right": 0, "bottom": 0}
        }
    }

def create_scene_definitions(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create all scene definitions"""
    scenes = []
    
    # Scene definitions with sources
    scene_configs = [
        {
            "name": "🎬 Intro",
            "file": "intro.html",
            "sources": [
                ("overlay", "browser", "intro.html")
            ]
        },
        {
            "name": "👤 Talking Head", 
            "file": "talking-head.html",
            "sources": [
                ("camera", "video", ""),
                ("overlay", "browser", "talking-head.html")
            ]
        },
        {
            "name": "📊 Presentation",
            "file": "presentation.html", 
            "sources": [
                ("screen", "display", 0),
                ("camera", "video", ""),
                ("overlay", "browser", "presentation.html")
            ],
            "camera_transform": {
                "pos": {"x": 960.0, "y": 0.0},
                "scale": {"x": 1.0, "y": 1.0},
                "crop": {"left": 480, "right": 480, "top": 0, "bottom": 0}
            }
        },
        {
            "name": "💻 Code Demo",
            "file": "code-demo.html",
            "sources": [
                ("screen", "display", 0),
                ("camera", "video", ""),
                ("overlay", "browser", "code-demo.html")
            ],
            "camera_transform": {
                "pos": {"x": 1400.0, "y": 765.0},
                "scale": {"x": 0.25, "y": 0.25},
                "crop": {"left": 0, "right": 0, "top": 0, "bottom": 0}
            }
        },
        {
            "name": "🖥️ Screen Only",
            "file": "screen-only.html",
            "sources": [
                ("screen", "display", 0),
                ("overlay", "browser", "screen-only.html")
            ]
        },
        {
            "name": "📺 BRB",
            "file": "brb.html",
            "sources": [
                ("overlay", "browser", "brb.html")
            ]
        },
        {
            "name": "🎯 Outro",
            "file": "outro.html", 
            "sources": [
                ("overlay", "browser", "outro.html")
            ]
        }
    ]
    
    for scene_config in scene_configs:
        sources = []
        
        for source_name, source_type, source_param in scene_config["sources"]:
            if source_type == "browser":
                # Use placeholder path - users will update this after extraction
                source = create_browser_source(
                    f"{source_name.title()} Overlay",
                    f"file:///PATH/TO/EXTRACTED/FOLDER/{source_param}"
                )
            elif source_type == "video":
                source = create_video_source("Camera")
                # Apply camera transform if specified
                if "camera_transform" in scene_config and source_name == "camera":
                    source["transform"].update(scene_config["camera_transform"])
            elif source_type == "display":
                source = create_display_source("Screen Capture", source_param)
            
            sources.append(source)
        
        # Reverse order so overlay is on top
        sources.reverse()
        
        scene = {
            "name": scene_config["name"],
            "sources": sources,
            "settings": {},
            "id": len(scenes)
        }
        
        scenes.append(scene)
    
    return scenes

def generate_obs_collection(config: Dict[str, Any], output_path: Path) -> Dict[str, Any]:
    """Generate complete OBS scene collection"""
    
    collection_name = f"{config.get('event', {}).get('title', 'Workshop')}-Scenes"
    
    # Create scene collection structure
    obs_collection = {
        "name": collection_name,
        "current_scene": "🎬 Intro",
        "current_program_scene": "🎬 Intro", 
        "current_preview_scene": "👤 Talking Head",
        "transition": {
            "name": "Fade",
            "type": "fade_transition",
            "settings": {
                "duration": 300
            }
        },
        "scenes": create_scene_definitions(config),
        "sources": [],
        "groups": [],
        "quick_transitions": [],
        "current_transition": "Fade",
        "transition_duration": 300,
        "sync_offset": {
            "sec": 0,
            "nsec": 0
        },
        "studio_mode": False,
        "monitoring_type": 0,
        "properties": [],
        "hotkeys": {
            "OBSBasic.SelectScene": [
                {"key": "OBS_KEY_F1", "scene": "🎬 Intro"},
                {"key": "OBS_KEY_F2", "scene": "👤 Talking Head"},
                {"key": "OBS_KEY_F3", "scene": "📊 Presentation"},
                {"key": "OBS_KEY_F4", "scene": "💻 Code Demo"},
                {"key": "OBS_KEY_F5", "scene": "🖥️ Screen Only"},
                {"key": "OBS_KEY_F6", "scene": "📺 BRB"},
                {"key": "OBS_KEY_F7", "scene": "🎯 Outro"}
            ]
        },
        "metadata": {
            "generated_by": "obs-scenes-setup",
            "created_at": datetime.now().isoformat(),
            "event_title": config.get('event', {}).get('title', 'Workshop'),
            "instructor": config.get('instructor', {}).get('name', 'Instructor'),
            "version": "1.0.0"
        }
    }
    
    # Write to file
    collection_file = output_path / "obs-scene-collection.json"
    with open(collection_file, 'w') as f:
        json.dump(obs_collection, f, indent=2)
    
    # Also create a simplified metadata file
    metadata = {
        "collection_name": collection_name,
        "scenes_count": len(obs_collection["scenes"]),
        "generated_at": datetime.now().isoformat(),
        "installation_steps": [
            "Extract ZIP file to a folder",
            "Open OBS Studio",
            "Go to Scene Collection → Import", 
            "Select obs-scene-collection.json",
            "Update Browser Source URLs to point to extracted HTML files"
        ],
        "required_files": [
            "obs-scene-collection.json",
            "intro.html",
            "talking-head.html", 
            "presentation.html",
            "code-demo.html",
            "screen-only.html",
            "brb.html",
            "outro.html"
        ]
    }
    
    with open(output_path / "collection-metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return obs_collection

def main():
    """Main function"""
    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    config_path = project_root / 'resources' / 'event.yaml'
    output_dir = project_root / 'dist' / 'scene-collection'
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load configuration
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return 1
    
    print(f"📖 Loading config: {config_path}")
    config = load_config(config_path)
    
    # Generate OBS collection
    print(f"🎬 Generating OBS scene collection...")
    collection = generate_obs_collection(config, output_dir)
    
    print(f"✅ Generated OBS scene collection: {collection['name']}")
    print(f"📁 Output directory: {output_dir}")
    print(f"🎯 Scenes created: {len(collection['scenes'])}")
    
    # List generated files
    print("\n📋 Generated files:")
    for file in output_dir.glob('*.json'):
        print(f"   • {file.name}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())