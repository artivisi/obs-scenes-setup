# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an OBS Studio automation system for creating professional programming tutorial setups. The system provides Infrastructure-as-Code approach to OBS scene creation with automated nested scene architecture, HTML overlay generation, and cross-platform compatibility.

## Current Architecture (2025)

The system uses a **modern 3-step workflow**:
1. **Scene Generation**: YAML resources → Mustache HTML templates → Scene collection JSON
2. **Webserver**: Local HTTP server for overlay hosting with cross-platform networking
3. **OBS Injection**: WebSocket-based scene creation with nested architecture

## Key Commands

### Modern Workflow (Current Implementation)
```bash
# Generate scenes from YAML resources
python scripts/generate-scenes.py --resource resources/event.yaml --output my-workshop/

# Serve generated scenes locally
python scripts/serve-scenes.py my-workshop/

# Inject scenes into OBS (creates unique timestamped collection)
python scripts/inject-obs.py --collection my-workshop --webserver http://localhost:8080 --obs-host localhost
```

### Cross-Platform Usage
```bash
# WSL/Windows setup (webserver binds to 0.0.0.0, OBS on Windows host)
python scripts/serve-scenes.py my-workshop/
python scripts/inject-obs.py --collection my-workshop --webserver http://172.29.130.195:8080 --obs-host 172.29.128.1

# macOS/Linux setup (standard localhost)
python scripts/inject-obs.py --collection my-workshop --webserver http://localhost:8080
```

### Development and Testing
```bash
# Install dependencies
python scripts/setup/install-dependencies.py

# Quick test with existing demo
python scripts/serve-scenes.py nested-demo/
python scripts/inject-obs.py --collection demo --webserver http://localhost:8080 --obs-host localhost
```

## Architecture

### Core Components

**Scene Generator** (`scripts/generate-scenes.py`):
- Loads YAML event resources for easy text editing
- Uses Mustache templating for dynamic HTML overlay generation
- Creates kebab-case collection names with random suffixes for uniqueness
- Outputs complete scene collection with metadata JSON

**Webserver** (`scripts/serve-scenes.py`):
- Environment-aware HTTP server with WSL/macOS/Linux detection
- Automatic 0.0.0.0 binding for cross-platform overlay access
- Process management with PID tracking and graceful shutdown
- Serves HTML overlays and scene metadata to OBS

**OBS Injector** (`scripts/inject-obs.py`):
- **Nested Scene Architecture**: Eliminates source duplication via dedicated source scenes
- **Unique Collections**: Timestamp-based names prevent conflicts
- **Cross-Platform**: WSL host IP detection for Windows/Linux hybrid setups
- **Window Capture Priority**: Prefers application capture over display capture
- **Smart Scene Ordering**: Automatically orders scenes for logical workflow (LIFO-aware)

### Nested Scene Architecture

**Source Scenes** (configured once):
- 📹 **Camera**: DirectShow camera input with audio filters
- 🖥️ **Screen**: Window Capture (preferred) or Display Capture fallback
- 🎤 **Audio**: Global audio configuration

**Session Scenes** (reference source scenes, ordered for workflow):
- 🎬 **Intro Scene**: Professional intro with event info + countdown timer
- 👤 **Talking Head**: Full-screen camera + speaker info overlay
- 📊 **50:50 Presentation**: Full screen + camera overlay (top-center, 25% cropped)
- 💻 **Code Demo**: Screen + PiP camera (25% scale, bottom-right) + overlay
- 🖥️ **Screen Only**: Full-screen capture + overlay
- 📺 **BRB / Technical**: Overlay only
- 🎯 **Outro Scene**: Overlay only with topics covered + social links

### Overlay System

**Modern HTML/CSS Overlays**:
- Mustache templating with YAML data injection
- Responsive design with doubled font sizes for readability
- Consistent branding: ArtiVisi + API Development + status indicators
- Perfect PiP alignment with green camera frame borders

**Resource Structure**:
```
resources/event.yaml          # Easy-to-edit event details
themes/default/*.mustache.html # HTML templates
{output}/*.html               # Generated overlays
{output}/scene-collection.json # OBS metadata
```

### Network Architecture

**Cross-Platform Detection**:
- WSL detection via `/proc/version` 
- Windows host IP discovery via `ip route show`
- Automatic webserver binding (0.0.0.0 vs localhost)
- Smart OBS WebSocket connection handling

## Development Guidelines

### File Structure
```
scripts/
├── generate-scenes.py    # YAML → HTML generation
├── serve-scenes.py      # Cross-platform webserver
├── inject-obs.py        # OBS WebSocket injection
├── setup/               # Dependency installation
└── utils/               # Shared utilities

resources/event.yaml     # Event text resources (YAML)
themes/default/          # Mustache templates
nested-demo/            # Example generated output
```

### Scene Development Workflow

1. **Edit Content**: Modify `resources/event.yaml` for event details
2. **Generate**: Run `generate-scenes.py` to create HTML overlays
3. **Test Locally**: Use `serve-scenes.py` + browser to preview
4. **Deploy**: Run `inject-obs.py` to create OBS scene collection

### Adding New Scene Types

1. Create new Mustache template in `themes/default/`
2. Add scene metadata to generation logic
3. Update injector scene creation in `inject-obs.py`
4. Test complete workflow with real OBS setup

### Cross-Platform Testing

- **WSL**: Test webserver 0.0.0.0 binding and Windows host detection
- **macOS**: Verify localhost networking and device detection
- **Linux**: Test standard networking and audio pipeline

## Common Tasks

### Creating New Events
1. Copy and modify `resources/event.yaml`
2. Update branding, topics, and instructor details
3. Generate and test with new content

### Debugging Scene Issues
- Check OBS WebSocket connection (Tools → WebSocket Server Settings)
- Verify overlay URLs are accessible in browser
- Use browser dev tools to check overlay rendering
- Test PiP camera alignment with generated frames

### Performance Optimization
- HTML overlays load faster than PNG graphics
- Nested scenes eliminate source duplication
- Window Capture reduces system load vs Display Capture
- Local webserver provides low-latency overlay updates

## Important Notes

**OBS Setup Requirements**:
- WebSocket server enabled (default port 4455)
- Scene collections auto-managed with timestamps
- Audio processing chain automatically configured
- Source scenes require one-time device configuration

**Production Workflow**:
- Generate scenes from YAML resources
- Test locally with webserver
- Deploy to OBS with unique collection names
- Clean up old collections manually as needed

**Cross-Platform Considerations**:
- WSL users: OBS runs on Windows host, requires IP detection
- All users: Webserver binds to appropriate interface automatically
- Network firewall: Ensure localhost/LAN HTTP access for overlays