# OBS Scenes Setup

Professional OBS scene automation for programming tutorials and workshops using Infrastructure-as-Code principles.

## Quick Start

```bash
# 1. Generate scenes from YAML resources
python scripts/generate-scenes.py --resource resources/event.yaml --output my-workshop/

# 2. Start local webserver
python scripts/serve-scenes.py my-workshop/

# 3. Inject into OBS
python scripts/inject-obs.py --collection my-workshop --webserver http://localhost:8080 --obs-host localhost
```

## Features

- **🎬 Nested Scene Architecture**: Eliminates source duplication
- **📱 HTML Overlays**: Dynamic, responsive overlays with Mustache templating
- **🔄 Cross-Platform**: WSL, macOS, Linux support with automatic networking
- **⚡ Instant Deployment**: Timestamp-based unique scene collections
- **🎨 Professional Layout**: Consistent branding and typography
- **🖼️ Perfect Alignment**: PiP camera frames with pixel-perfect positioning

## Scene Types

- **📺 BRB / Technical**: Break/transition overlay
- **👤 Talking Head**: Full-screen presenter with speaker info
- **💻 Code Demo**: Screen share + PiP camera with aligned frame
- **🖥️ Screen Only**: Full-screen capture with minimal overlay
- **🎯 Outro Scene**: Session conclusion overlay

## Requirements

- OBS Studio with WebSocket enabled (Tools → WebSocket Server Settings)
- Python 3.8+ with `obsws-python`, `pystache`, `pyyaml`
- Run `python scripts/setup/install-dependencies.py` to install

## Live Examples

🌐 **View example scenes**: [https://artivisi.github.io/obs-scenes-setup/example-scenes/](https://artivisi.github.io/obs-scenes-setup/example-scenes/)

These are generated from the default theme and can be directly imported into OBS as Browser Sources.

## Architecture

### Nested Scene Concept

**Source Scenes** (configure once):
- 📹 Camera: Your webcam/capture device
- 🖥️ Screen: Window/display capture
- 🎤 Audio: Microphone settings

**Session Scenes** (inherit from sources):
- All scenes reference source scenes via OBS nested architecture
- Change camera once → updates all scenes automatically
- No source duplication = cleaner OBS setup

### Content Pipeline

```
resources/event.yaml → themes/default/*.mustache.html → {output}/*.html → OBS WebSocket
       ↑                        ↑                            ↑               ↑
   Easy editing            Template engine              Generated HTML    Live scenes
```

## Cross-Platform Usage

**WSL + Windows OBS:**
```bash
# WSL serves on 0.0.0.0, connects to Windows host OBS
python scripts/serve-scenes.py my-workshop/
python scripts/inject-obs.py --collection demo --webserver http://172.29.130.195:8080 --obs-host 172.29.128.1
```

**macOS/Linux:**
```bash
# Standard localhost networking
python scripts/inject-obs.py --collection demo --webserver http://localhost:8080
```

## Development

See [CLAUDE.md](CLAUDE.md) for detailed architecture and development guidelines.

**Key Scripts:**
- `generate-scenes.py` - YAML → HTML generation
- `serve-scenes.py` - Cross-platform webserver
- `inject-obs.py` - OBS WebSocket integration

**File Structure:**
```
resources/event.yaml      # Event details (easy editing)
themes/default/          # Mustache HTML templates  
scripts/                # Python automation tools
nested-demo/            # Example output
```

## Contributing

1. Test changes with `nested-demo/` example
2. Verify cross-platform compatibility (WSL, macOS, Linux)
3. Update documentation for any API changes
4. Test complete workflow: generate → serve → inject

## License

MIT License - Professional streaming setup automation for educational content.