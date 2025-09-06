# Technical Documentation

## Architecture Overview

This OBS automation system uses an Infrastructure-as-Code approach with a 4-stage workflow pipeline:

1. **Environment Setup** - Dependency installation and system validation
2. **Event Configuration** - JSON-based event customization
3. **Overlay Generation** - HTML/CSS/JS overlay creation from templates
4. **OBS Integration** - Automated scene creation via WebSocket

## Core Components

### Workflow Orchestration (`scripts/workflow.py`)
- Master controller managing the complete pipeline
- Supports quick setup (2-3 minutes) and full customization
- Template support for different content types

### OBS Integration (`scripts/obs/auto-scene-creator.py`)
- Creates 7 professional scenes automatically
- Cross-platform device detection
- Automatic HTTP server for local overlay serving
- Professional audio filter chain configuration

### Overlay System (`scripts/tools/populate-overlays.py`)
- Dynamic HTML/CSS/JS overlays
- Event-specific content generation
- GitHub Pages hosting with offline fallback

## Utility Modules

### `scripts/utils/obs_utils.py`
- OBS WebSocket connection management
- Automatic WSL/Windows bridge detection
- Scene and source management classes

### `scripts/utils/scene_generator.py`
- Scene layout templates and positioning
- Transform calculations for sources
- Scene collection building utilities

### `scripts/utils/text_customizer.py`
- Text processing and content personalization
- Event-specific text replacement

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

| Scene | Hotkey | Description |
|-------|--------|-------------|
| 🎬 Intro | F1 | Professional intro with countdown |
| 👤 Talking Head | F2 | Full camera for presentations |
| 💻 Code + Camera | F3 | Split screen with PiP camera |
| 🖥️ Screen Only | F4 | Full screen capture |
| 📺 BRB/Technical | F5 | Break screen |
| 🎯 Outro | F6 | Professional closing |

## Audio Processing Chain

Each microphone source automatically receives:
1. **Noise Suppression** (RNNoise method)
2. **Compressor** (10:1 ratio, -18dB threshold)
3. **Limiter** (-6dB threshold, 60ms release)

## Event Configuration Schema

```json
{
  "event": {
    "title": "Event Title",
    "subtitle": "Event Subtitle",
    "duration": "90 minutes",
    "type": "Workshop"
  },
  "presenter": {
    "name": "Name",
    "title": "Title",
    "company": "Company"
  },
  "session": {
    "topics": ["Topic 1", "Topic 2"],
    "tech_stack": [
      {"icon": "🎯", "name": "Technology"}
    ]
  }
}
```

## API Reference

### Workflow Class
```python
workflow = OBSWorkflow(github_user="username")
workflow.quick_setup(template="java")
workflow.full_workflow(event_name="my-event", template="python-workshop")
```

### Scene Creator Class
```python
creator = AutoSceneCreator(
    github_user="username",
    offline_mode=True,
    custom_overlay_path="path/to/overlays"
)
await creator.create_all_scenes_live()
```

### Overlay Populator Class
```python
populator = OverlayPopulator()
populator.populate_all_overlays(config, output_dir)
```

## Macropad Integration (Optional)

### Vial Configuration
The system supports a 4-layer macropad configuration:
- **Layer 0**: OBS Control (scene switching, recording)
- **Layer 1**: Tutorial Mode (zoom, annotations)
- **Layer 2**: Development (IDE shortcuts)
- **Layer 3**: System Control (audio, display)

### Key Mappings
- F1-F6: Scene switching
- F13-F24: Recording/streaming control
- Custom macros for common actions

## Development Guidelines

### Adding New Scene Templates
1. Define layout in `scene_generator.py`
2. Create HTML overlay in `docs/overlays/`
3. Update scene creation in `auto-scene-creator.py`

### Creating Event Templates
1. Add JSON template in `docs/resources/templates/`
2. Test with `populate-overlays.py`
3. Verify with full workflow

### Cross-Platform Considerations
- Use `pathlib.Path` for all file operations
- Handle WSL networking automatically
- Test on Windows, Linux, and macOS

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
- Cameras/microphones are auto-detected
- Manual configuration available in OBS after scene creation
- Check system permissions for device access