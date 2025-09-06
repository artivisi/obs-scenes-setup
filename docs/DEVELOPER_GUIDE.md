# 🛠️ Developer Guide

Complete guide for extending, customizing, and contributing to the OBS scenes setup project.

## 🚀 Quick Start for Developers

### 1. Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/artivisi/obs-scenes-setup.git
cd obs-scenes-setup

# Install dependencies
python3 scripts/setup/install-dependencies.py

# Test the utilities
python3 scripts/examples/demo_utilities.py
```

### 2. Explore the Codebase

```bash
# Examine the utilities structure
ls -la scripts/utils/

# Run refactored scripts
python3 scripts/obs/list-sources.py           # Lists OBS scenes/sources
python3 scripts/obs/fix-overlay-urls.py       # Updates browser source URLs

# Try the complete workflow  
python3 scripts/workflow.py --quick
```

## 📁 Project Architecture

### New Modular Structure (2024)

```
scripts/
├── utils/                    # 🔧 Reusable utility modules
│   ├── obs_utils.py          # OBS operations with WSL auto-detection
│   ├── scene_generator.py    # Scene templates & layout management
│   ├── text_customizer.py    # Text processing & customization
│   └── __init__.py
├── obs/                      # OBS automation (refactored)
├── tools/                    # Development utilities  
├── examples/                 # Usage demonstrations
└── workflow.py               # Complete orchestration
```

### Key Design Principles

1. **🔄 DRY (Don't Repeat Yourself)** - Eliminated duplicate WSL detection and OBS connection code
2. **🧩 Modular Design** - Utilities can be imported and reused
3. **🌍 Cross-Platform** - Automatic WSL/Windows networking detection
4. **🛡️ Error Handling** - Graceful failures with informative messages
5. **📚 Self-Documenting** - Comprehensive docstrings and examples

## 🔧 Using the Utility Modules

### Basic OBS Operations

```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))

from obs_utils import OBSConnection, OBSSceneManager

# Connect to OBS with automatic WSL detection
with OBSConnection() as conn:
    scene_manager = OBSSceneManager(conn)
    
    # List all scenes
    scenes = scene_manager.list_all_scenes()
    print(f"Found {len(scenes)} scenes")
    
    # Iterate through scenes and sources
    for scene_name, sources in scene_manager.iterate_scenes_and_sources():
        print(f"Scene '{scene_name}': {len(sources)} sources")
```

### Creating Custom Scene Collections

```python
from scene_generator import SceneCollectionBuilder, CommonScenes

# Build a custom scene collection
builder = SceneCollectionBuilder("My Custom Scenes")

# Add standard scenes
builder.add_scene(CommonScenes.create_intro_scene("http://localhost:8080/intro.html"))
builder.add_scene(CommonScenes.create_talking_head_scene("camera-1", "http://localhost:8080/talking-head.html"))
builder.add_scene(CommonScenes.create_code_camera_scene("screen-1", "camera-1", "http://localhost:8080/code-demo.html"))

# Add transitions and export
builder.add_common_transitions()
collection = builder.build()

# Save for OBS import
builder.save_to_file(Path("my-custom-collection.json"))
```

### Event Customization

```python
from text_customizer import EventContentGenerator

# Generate event-specific configuration
config = EventContentGenerator.generate_event_config(
    event_type="workshop",
    title="Advanced React Development",
    presenter_name="Jane Doe",
    tech_stack=["javascript", "react", "nodejs", "docker"]
)

# Customize for specific language
config = EventContentGenerator.customize_for_language(config, "javascript")

# Access generated content
print(config['event']['title'])           # "Advanced React Development"
print(config['session']['tech_stack'])    # [{"name": "javascript", "icon": "⚡"}, ...]
```

## 🎯 Common Development Tasks

### Adding a New Scene Template

1. **Add to CommonScenes factory:**

```python
# In scripts/utils/scene_generator.py
@staticmethod
def create_my_custom_scene(param1: str, param2: str) -> SceneTemplate:
    """Create my custom scene template"""
    
    # Define sources
    main_source = SourceItem(
        name="Main Source",
        source_uuid=param1,
        transform=SceneLayoutManager.create_fullscreen_transform()
    )
    
    overlay_source = SourceItem(
        name="Custom Overlay",
        source_uuid=param2,
        transform=SceneLayoutManager.create_fullscreen_transform()
    )
    
    return SceneTemplate(
        name="🎯 My Custom Scene",
        description="Custom scene for specific use case",
        sources=[main_source, overlay_source],
        hotkey="F8"
    )
```

2. **Test the new template:**

```python
# Create test script
from scripts.utils.scene_generator import CommonScenes, SceneCollectionBuilder

# Test your new scene
custom_scene = CommonScenes.create_my_custom_scene("source-1", "overlay-1")
print(f"Created scene: {custom_scene.name}")

# Add to collection
builder = SceneCollectionBuilder("Test Collection")
builder.add_scene(custom_scene)
collection = builder.build()
```

### Adding WSL Support to New Scripts

```python
# Import the connection utilities
from scripts.utils.obs_utils import OBSConnection

# Use context manager for automatic WSL detection
def my_obs_function():
    try:
        with OBSConnection() as conn:
            # WSL detection happens automatically
            # conn.client is the raw OBS WebSocket client
            version = conn.get_version_info()
            print(f"Connected to OBS {version.obs_version}")
            
    except Exception as e:
        print(f"Failed to connect: {e}")
```

### Creating Custom Event Types

```python
# In scripts/utils/text_customizer.py, add to EVENT_TEMPLATES
EVENT_TEMPLATES["my_event_type"] = {
    "title_suffix": "Masterclass",
    "type": "Advanced Masterclass",
    "description": "Expert Level",
    "default_duration": "4 hours",
    "topics_prefix": "Masterclass Topics:",
    "cta_action": "Master The Skills"
}

# Use the new event type
config = EventContentGenerator.generate_event_config(
    event_type="my_event_type",
    title="Advanced System Design",
    presenter_name="Expert Developer"
)
```

## 🧪 Testing Your Changes

### Run the Demo Script

```bash
# Test all utilities together
python3 scripts/examples/demo_utilities.py

# Expected output:
# 🔌 OBS Connection Demo - WSL detection working
# 🎬 Scene Generation Demo - Templates generating correctly  
# ✏️ Text Customization Demo - Event configs working
# 🔄 Complete Workflow Demo - End-to-end functionality
```

### Test Individual Components

```bash
# Test OBS connection and WSL detection
python3 scripts/obs/list-sources.py

# Test URL fixing with custom overlays
python3 scripts/obs/fix-overlay-urls.py --overlay-path /path/to/custom/overlays

# Test complete workflow
python3 scripts/workflow.py --quick --template python-workshop
```

### Validate Your Changes

```bash
# Check that scenes are created correctly
python3 scripts/obs/auto-scene-creator.py --generate-json --output test.json
cat test.json | jq '.scenes | length'  # Should show correct number of scenes

# Verify overlay URLs are correct
grep -o "http://[^\"]*" test.json | sort | uniq
```

## 📦 Creating New Workflows

### Example: Custom Video Series Workflow

```python
#!/usr/bin/env python3
"""Custom workflow for video series"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "utils"))

from obs_utils import OBSConnection, OBSSceneManager
from scene_generator import SceneCollectionBuilder, CommonScenes
from text_customizer import EventContentGenerator

def create_video_series(series_title: str, episode_number: int):
    """Create OBS setup for video series episode"""
    
    # Generate episode-specific configuration
    config = EventContentGenerator.generate_event_config(
        event_type="tutorial",
        title=f"{series_title} - Episode {episode_number}",
        duration="30 minutes"
    )
    
    # Build scene collection  
    builder = SceneCollectionBuilder(f"{series_title} Ep{episode_number}")
    
    # Add series-specific scenes
    scenes = [
        CommonScenes.create_intro_scene("http://localhost:8080/intro.html"),
        CommonScenes.create_talking_head_scene("camera-1", "http://localhost:8080/talking-head.html"),
        CommonScenes.create_code_camera_scene("screen-1", "camera-1", "http://localhost:8080/code-demo.html"),
        CommonScenes.create_screen_only_scene("screen-1", "camera-1", "http://localhost:8080/screen-only.html")
    ]
    
    for scene in scenes:
        builder.add_scene(scene)
    
    # Apply to OBS
    try:
        with OBSConnection() as conn:
            scene_manager = OBSSceneManager(conn)
            scene_manager.cleanup_all_scenes()
            print(f"✅ Created episode {episode_number} setup")
            
    except Exception as e:
        print(f"❌ Failed to apply to OBS: {e}")
        # Save as JSON for manual import
        builder.save_to_file(Path(f"episode-{episode_number}.json"))
        print(f"💾 Saved as episode-{episode_number}.json")

if __name__ == "__main__":
    create_video_series("Python Mastery Series", 5)
```

## 🔍 Debugging Tips

### WSL Issues

```bash
# Check if WSL is detected correctly
cat /proc/version | grep -i microsoft

# Verify Windows host IP detection
ip route show default | awk '{print $3}'

# Test WSL network connectivity
curl -I http://$(ip route show default | awk '{print $3}'):4455
```

### OBS Connection Issues

```python
# Debug connection with verbose output
with OBSConnection(host="localhost", port=4455) as conn:
    print(f"Host resolved to: {conn.host}")
    print(f"Version: {conn.get_version_info()}")
    
    scene_manager = OBSSceneManager(conn)
    scenes = scene_manager.list_all_scenes()
    print(f"Available scenes: {[s['sceneName'] for s in scenes]}")
```

### Overlay Loading Issues

```bash
# Check if HTTP server is running
netstat -tuln | grep :8080  # Linux
ss -tuln | grep :8080       # Linux (newer)

# Test overlay accessibility
curl -I http://localhost:8080/intro.html

# Check overlay content  
curl http://localhost:8080/intro.html | head -10
```

## 🚀 Contributing Guidelines

### Code Style

1. **Follow existing patterns** - Use the same structure as existing utilities
2. **Add type hints** - Use Python type annotations for function parameters and returns
3. **Write docstrings** - Document all public methods and classes
4. **Handle errors gracefully** - Always provide informative error messages
5. **Test cross-platform** - Ensure code works on Windows, macOS, and Linux

### Example Contribution

```python
def my_new_utility_function(param: str, optional_param: Optional[int] = None) -> Dict[str, Any]:
    """
    Brief description of what this function does.
    
    Args:
        param: Description of the parameter
        optional_param: Description of optional parameter
        
    Returns:
        Dictionary containing the results
        
    Raises:
        ValueError: When parameter is invalid
        ConnectionError: When OBS connection fails
    """
    try:
        # Implementation here
        result = {"status": "success", "data": param}
        return result
        
    except Exception as e:
        raise ValueError(f"Failed to process {param}: {e}")
```

### Testing Your Contribution

1. **Run existing tests:** `python3 scripts/examples/demo_utilities.py`
2. **Test with OBS:** Verify your changes work with live OBS connection
3. **Test WSL compatibility:** If applicable, test in WSL environment
4. **Update documentation:** Add your changes to relevant documentation files

### Submitting Changes

1. **Fork the repository** and create a feature branch
2. **Make your changes** following the coding guidelines
3. **Test thoroughly** on your target platforms
4. **Update documentation** including API docs and examples
5. **Submit a pull request** with clear description of changes

## 📚 Additional Resources

### API Documentation
- **[🔧 Utilities API](UTILITIES_API.md)** - Complete API reference for all utility modules

### Project Documentation  
- **[🤖 Automated Setup](../AUTOMATED_SETUP.md)** - User guide for automated setup
- **[🏗️ Project Architecture](../PROJECT_NOTES.md)** - Technical deep-dive into the system
- **[🎹 Macropad Design](../MACROPAD_DESIGN.md)** - Hardware integration guide

### Live Examples
- **[🌐 Live Overlays](https://artivisi.com/obs-scenes-setup/)** - Preview gallery
- **[📚 Demo Scripts](../scripts/examples/)** - Usage examples and demonstrations

---

**🎯 Ready to contribute? The modular utilities make it easy to add new functionality while maintaining compatibility and reliability!**