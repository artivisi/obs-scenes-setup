# OBS Scenes Setup

Automated OBS Studio scene creation for programming tutorials and content creation. Set up professional streaming scenes in 2-3 minutes.

## Quick Start

### Option 1: Fastest Setup (2-3 minutes)
```bash
# Install dependencies and create scenes with defaults
python scripts/workflow.py --quick

# Or use a specific template
python scripts/workflow.py --quick --template python-workshop
```

### Option 2: Custom Event Setup
```bash
# Interactive setup with your event details
python scripts/workflow.py --event my-workshop

# Or start with a template
python scripts/workflow.py --event my-workshop --template java
```

### Option 3: Direct OBS Creation
```bash
# Just create OBS scenes (if you already have overlays)
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi
```

## What You Get

✅ **7 Professional Scenes**
- 🎬 Intro Scene (F1) - Professional intro with countdown
- 👤 Talking Head (F2) - Full camera view
- 💻 Code + Camera (F3) - Split screen with PiP
- 🖥️ Screen Only (F4) - Full screen capture
- 📺 BRB/Technical (F5) - Break screen
- 🎯 Outro Scene (F6) - Professional closing

✅ **Professional Audio** - Automatic noise suppression, compression, and limiting

✅ **Dynamic Overlays** - HTML/CSS overlays with your branding

✅ **Cross-Platform** - Works on Windows, Linux, macOS, and WSL

## Prerequisites

- Python 3.8+
- OBS Studio 28+ with WebSocket enabled
- Git (for cloning the repository)

## Installation

```bash
# Clone the repository
git clone https://github.com/artivisi/obs-scenes-setup.git
cd obs-scenes-setup

# Run the quick setup
python scripts/workflow.py --quick
```

## Enable OBS WebSocket

1. Open OBS Studio
2. Go to Tools → WebSocket Server Settings
3. Check "Enable WebSocket server"
4. Use default port 4455 (no password needed for local use)

## Advanced Usage

### Generate Custom Overlays
```bash
python scripts/tools/populate-overlays.py --template python-workshop --preview
```

### Use Custom Overlays
```bash
python scripts/obs/auto-scene-creator.py --create-live --overlay-path my-overlays
```

### Export Scene Collection
```bash
python scripts/obs/auto-scene-creator.py --generate-json --output my-scenes.json
```

## Templates Available

- `java` - Java development with Spring Boot
- `python-workshop` - Python with FastAPI
- `linux-admin` - Linux administration
- More templates in `docs/resources/templates/`

## Documentation

- [Technical Documentation](docs/TECHNICAL.md) - Architecture and API details
- [Claude Code Integration](CLAUDE.md) - AI assistant configuration

## Project Structure

```
obs-scenes-setup/
├── scripts/           # Automation scripts
│   ├── workflow.py    # Main workflow orchestrator
│   ├── obs/          # OBS integration
│   ├── tools/        # Overlay generation
│   └── utils/        # Utility modules
├── docs/             # Documentation and web assets
│   ├── overlays/     # HTML overlay templates
│   └── resources/    # Event templates
└── generated-overlays/ # Your custom overlays (created automatically)
```

## Support

- Issues: [GitHub Issues](https://github.com/artivisi/obs-scenes-setup/issues)
- Documentation: [Technical Details](docs/TECHNICAL.md)

## License

MIT License - Feel free to customize and use for your content creation!