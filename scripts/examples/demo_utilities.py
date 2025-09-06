#!/usr/bin/env python3
"""
Demonstration of OBS Utilities Usage

This script shows how to use the refactored utility modules for common OBS tasks.
"""

import sys
from pathlib import Path

# Add utils directory to path  
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))

from obs_utils import OBSConnection, OBSSceneManager, OBSSourceManager
from scene_generator import CommonScenes, SceneCollectionBuilder, SceneLayoutManager
from text_customizer import EventContentGenerator, TextTemplate


def demo_obs_connection():
    """Demonstrate OBS connection utilities"""
    print("🔌 OBS Connection Demo")
    print("=" * 50)
    
    try:
        # Auto-connecting with WSL detection
        with OBSConnection() as conn:
            print(f"📡 Connected to OBS: {conn.get_version_info().obs_version}")
            
            # Use scene manager
            scene_manager = OBSSceneManager(conn)
            scenes = scene_manager.list_all_scenes()
            print(f"📋 Found {len(scenes)} scenes")
            
            # List scenes and sources  
            for scene_name, sources in scene_manager.iterate_scenes_and_sources():
                print(f"  🎬 {scene_name}: {len(sources)} sources")
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    
    print()


def demo_scene_generation():
    """Demonstrate scene generation utilities"""
    print("🎬 Scene Generation Demo")
    print("=" * 50)
    
    # Create scene collection
    builder = SceneCollectionBuilder("Demo Collection")
    
    # Add common scenes
    intro_scene = CommonScenes.create_intro_scene("http://localhost:8080/intro.html")
    talking_head = CommonScenes.create_talking_head_scene("camera-uuid", "http://localhost:8080/talking-head.html")
    code_camera = CommonScenes.create_code_camera_scene("screen-uuid", "camera-uuid", "http://localhost:8080/code-demo.html")
    
    builder.add_scene(intro_scene).add_scene(talking_head).add_scene(code_camera)
    builder.add_common_transitions()
    
    # Build and show structure
    collection = builder.build()
    print(f"📋 Collection: {collection['name']}")
    print(f"🎬 Scenes: {len(collection['scenes'])}")
    print(f"🔄 Transitions: {len(collection['quick_transitions'])}")
    print(f"⌨️  Hotkeys: {len(collection['hotkeys'])}")
    
    # Show layout positioning
    print("\\n📍 Layout Positioning:")
    positions = ["top-left", "top-right", "bottom-left", "bottom-right", "center"]
    for pos in positions:
        coords = SceneLayoutManager.get_position(pos, "medium")
        print(f"  {pos}: x={coords['x']}, y={coords['y']}")
    
    print()


def demo_text_customization():
    """Demonstrate text customization utilities"""
    print("✏️  Text Customization Demo")
    print("=" * 50)
    
    # Generate event configuration
    config = EventContentGenerator.generate_event_config(
        event_type="workshop",
        title="Advanced Python Development",
        presenter_name="Sarah Johnson",
        presenter_title="Senior Python Developer",
        tech_stack=["python", "django", "docker", "aws"],
        duration="3 hours"
    )
    
    print(f"📝 Event: {config['event']['title']}")
    print(f"👤 Presenter: {config['presenter']['name']}")
    print(f"🏢 Company: {config['branding']['company_name']}")
    print(f"⏱️  Duration: {config['event']['duration']}")
    print(f"🛠️  Tech Stack: {[tech['name'] for tech in config['session']['tech_stack']]}")
    
    # Demonstrate template processing
    template_content = """
    <h1>{{event.title}}</h1>
    <p>Presenter: {{presenter.name}}</p>
    <p>Duration: {{event.duration}}</p>
    """
    
    template = TextTemplate(template_content)
    processed = template.substitute({
        "event.title": config['event']['title'],
        "presenter.name": config['presenter']['name'], 
        "event.duration": config['event']['duration']
    })
    
    print(f"\\n📄 Processed Template:")
    print(processed.strip())
    
    print()


def demo_full_workflow():
    """Demonstrate complete workflow using utilities"""
    print("🔄 Complete Workflow Demo")
    print("=" * 50)
    
    print("1. 📝 Generate event configuration...")
    config = EventContentGenerator.generate_event_config(
        event_type="tutorial",
        title="React Development Fundamentals",
        tech_stack=["javascript", "react", "nodejs"]
    )
    
    print("2. 🎬 Create scene templates...")
    builder = SceneCollectionBuilder("React Tutorial Scenes")
    
    # Add scenes for the tutorial
    scenes = [
        CommonScenes.create_intro_scene("http://localhost:8080/intro.html"),
        CommonScenes.create_talking_head_scene("camera-1", "http://localhost:8080/talking-head.html"),
        CommonScenes.create_code_camera_scene("screen-1", "camera-1", "http://localhost:8080/code-demo.html"),
        CommonScenes.create_screen_only_scene("screen-1", "camera-1", "http://localhost:8080/screen-only.html")
    ]
    
    for scene in scenes:
        builder.add_scene(scene)
    
    builder.add_common_transitions()
    collection = builder.build()
    
    print("3. 🔗 Connect to OBS and show current state...")
    try:
        with OBSConnection() as conn:
            scene_manager = OBSSceneManager(conn)
            current_scenes = scene_manager.list_all_scenes()
            print(f"   Current OBS scenes: {len(current_scenes)}")
            
            # Could apply the generated collection here
            
    except Exception as e:
        print(f"   ⚠️  OBS not available: {e}")
    
    print("4. ✅ Workflow complete!")
    print(f"   Generated {len(collection['scenes'])} scenes for '{config['event']['title']}'")
    
    print()


def main():
    """Run all demonstrations"""
    print("🚀 OBS Utilities Demonstration")
    print("=" * 80)
    print()
    
    demo_obs_connection()
    demo_scene_generation()
    demo_text_customization()
    demo_full_workflow()
    
    print("✨ All demonstrations completed!")
    print("\\n💡 Key Benefits of Refactored Utilities:")
    print("   • Eliminated duplicate code across 3 scripts")
    print("   • Automatic WSL detection and IP management") 
    print("   • Reusable scene generation templates")
    print("   • Flexible text processing and customization")
    print("   • Clean context manager pattern for OBS connections")
    print("   • Modular design for easy extension")


if __name__ == "__main__":
    main()