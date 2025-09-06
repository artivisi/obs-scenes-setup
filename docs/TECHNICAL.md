# Technical Documentation

## Architecture Overview

This OBS automation system uses an Infrastructure-as-Code approach with a streamlined 3-step workflow:

1. **Scene Generation** - Create HTML overlays from YAML resources using Mustache templates
2. **Local Serving** - Host generated content via cross-platform HTTP server  
3. **OBS Injection** - Automated scene creation with nested architecture via WebSocket

## Core Components

### Scene Generation (`scripts/generate-scenes.py`)
- Processes YAML event resources through Mustache templates
- Generates complete HTML overlay sets with CSS/JS
- Creates unique timestamped output directories
- Supports theme system for consistent styling

### Scene Serving (`scripts/serve-scenes.py`) 
- Cross-platform HTTP server (0.0.0.0:8080)
- Automatic WSL/Windows networking detection
- Serves generated HTML overlays to OBS
- Real-time overlay updates during development

### OBS Injection (`scripts/inject-obs.py`)
- Creates nested scene architecture eliminating source duplication
- Implements 5 core scene types with professional layouts
- Cross-platform WebSocket connectivity with WSL auto-detection
- Unique collection naming with timestamp suffixes

## Utility Modules

### `scripts/utils/obs_utils.py`
- OBS WebSocket connection management
- Automatic WSL/Windows bridge detection
- Scene and source management classes

## Network Architecture

### WSL Support
The system automatically detects WSL environments and configures networking:
- Windows host IP detection for OBS WebSocket
- ETH0 IP address for HTTP server
- Cross-platform path handling

### Overlay Serving Priority
1. **Custom overlays** - User-generated content
2. **Local overlays** - Offline mode with HTTP server
3. **GitHub Pages** - Online mode fallback

## Scene Templates

| Scene | Description |
|-------|--------------|
| 👤 Talking Head | Full camera for presentations with speaker info |
| 💻 Code + Camera | Split screen with PiP camera frame |
| 🖥️ Screen Only | Full screen capture with minimal overlay |
| 📺 BRB / Technical | Break screen with event branding |
| 🎯 Outro | Professional closing with contact info |

## Nested Scene Architecture

**Source Scenes** (created once):
- 📹 Camera: Webcam/capture device input
- 🖥️ Screen: Window/display capture source

**Session Scenes** (reference sources):
- All scenes use nested scene architecture
- Camera and screen sources are referenced, not duplicated
- Change source once → updates all scenes automatically

## Event Configuration Schema (YAML)

```yaml
event:
  title: "Python Web Development Workshop"
  subtitle: "Building Modern Applications"
  duration: "2 hours"
  type: "Workshop"

instructor:
  name: "Sarah Johnson"
  title: "Senior Python Developer"
  company: "ArtiVisi Intermedia"

session:
  topics:
    - "FastAPI Development"
    - "Database Integration"
    - "API Testing"
  tech_stack:
    - icon: "🐍"
      name: "Python"
    - icon: "⚡"
      name: "FastAPI"
```

## API Reference

### Scene Generator Class
```python
generator = SceneGenerator(resource_file="resources/event.yaml")
generator.load_resources()
output_dir = generator.generate_scenes()
```

### OBS Injection Class  
```python
injector = OBSInjector(
    collection_name="my-workshop",
    webserver_url="http://localhost:8080",
    obs_host="localhost"
)
injector.inject_scenes()
```

## Cross-Platform Support

### WSL Environment
- Automatic Windows host IP detection (172.29.128.1)
- ETH0 interface detection for HTTP server binding
- Cross-platform path handling

### Network Configuration
- HTTP server binds to 0.0.0.0:8080 for cross-platform access
- OBS WebSocket connects to appropriate host IP
- Smart fallback to localhost when not in WSL

## Development Guidelines

### Adding New Scene Templates
1. Create Mustache template in `themes/default/scene-name.mustache.html`
2. Test generation with `scripts/generate-scenes.py` 
3. Verify layout and positioning in OBS

### Creating Event Templates
1. Add YAML resource in `resources/`
2. Test with scene generation workflow
3. Verify end-to-end functionality

### Cross-Platform Considerations
- Use `pathlib.Path` for all file operations
- Handle WSL networking automatically 
- Generated files go to `target/` directory (gitignored)

## Troubleshooting

### OBS WebSocket Connection
- Ensure OBS WebSocket is enabled (Tools → WebSocket Server Settings)
- Default port: 4455
- WSL users: automatically detects Windows host IP

### Overlay Issues
- Check HTTP server is running (port 8080)
- Verify overlay files exist in specified directory
- Test URLs in browser before OBS integration

### Device Detection
- USB cameras prioritized over integrated webcams
- Window Capture preferred over Display Capture
- Manual configuration available in OBS after scene creation