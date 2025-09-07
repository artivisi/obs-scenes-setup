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
# Setup virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies (recommended method)
pip install -r requirements.txt

# Quick test with existing demo
python scripts/serve-scenes.py nested-demo/
python scripts/inject-obs.py --collection demo --webserver http://localhost:8080 --obs-host localhost

# When done developing
deactivate
```

### Virtual Environment Best Practices
```bash
# Always use virtual environments to avoid dependency conflicts
python3 -m venv venv

# Activate before running any scripts
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install only required dependencies
pip install obsws-python pystache pyyaml requests

# Check what's installed
pip list

# Save dependencies (for reproducibility)
pip freeze > requirements.txt

# Deactivate when done
deactivate
```

### Recording Configuration (MacBook Pro M1/M2/M3)
```bash
# Configure OBS for maximum quality recording on Apple Silicon
python scripts/configure-obs-recording.py --preset maximum

# Available presets:
# - maximum: 4K60 @ 50Mbps (best quality, large files)
# - high: 1440p60 @ 25Mbps (great quality, moderate files)  
# - streaming: 1080p60 @ 8Mbps (optimized for streaming/sharing)
# - standard: 1080p30 @ 12Mbps (standard recording)

# Configure remote OBS instance
python scripts/configure-obs-recording.py --obs-host 192.168.1.100 --preset high
```

### Streaming Configuration (1080p Optimized)
```bash
# Configure for YouTube streaming
python scripts/configure-obs-streaming.py --platform youtube --quality high

# Configure for Facebook Live
python scripts/configure-obs-streaming.py --platform facebook --quality standard

# Show available servers for a platform
python scripts/configure-obs-streaming.py --platform youtube --show-servers

# Quality presets:
# - ultra: 1080p60 with 20% higher bitrate
# - high: 1080p60 with platform-recommended bitrate
# - standard: 1080p30 with reduced bitrate
# - low: 720p30 for limited bandwidth

# Custom RTMP server
python scripts/configure-obs-streaming.py --platform custom --server rtmp://your-server/live --key your-stream-key

# Test connection only
python scripts/configure-obs-streaming.py --test

# Remote OBS configuration
python scripts/configure-obs-streaming.py --obs-host 192.168.1.100 --platform youtube
```

#### Streaming Script Technical Details

**Platform Configuration:**
- YouTube: CBR 6000 kbps, H.264 High Profile, 2-second keyframes
- Facebook: CBR 4000 kbps, RTMPS support, Main Profile
- Custom: User-configurable bitrates and servers

**Encoder Optimization:**
- macOS: Apple VideoToolbox hardware acceleration
- Cross-platform: x264 software encoding fallback
- Constant bitrate (CBR) for streaming stability
- Buffer size optimization (1-2x bitrate based on platform)

**Network Optimization:**
- Auto-reconnect with exponential backoff
- TCP No-Delay for reduced latency
- Bandwidth calculation and validation
- Platform-specific server selection

**Quality Calculations:**
```
Ultra:   Platform bitrate × 1.2 + audio bitrate
High:    Platform bitrate × 1.0 + audio bitrate  
Standard: Platform bitrate × 0.8 + audio bitrate
Low:     Platform bitrate × 0.6 + audio bitrate
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

**Recording Configurator** (`scripts/configure-obs-recording.py`):
- **Apple Silicon Optimization**: Hardware-accelerated encoding via VideoToolbox
- **Quality Presets**: 4K60 maximum down to 1080p30 standard
- **Storage Management**: Auto-creates ~/Movies/OBS/ directory
- **Platform Detection**: macOS-specific optimizations and settings

**Streaming Configurator** (`scripts/configure-obs-streaming.py`):
- **Platform Optimization**: YouTube, Facebook, Custom RTMP support
- **Quality Scaling**: Bandwidth-aware bitrate calculations
- **Network Optimization**: Auto-reconnect, TCP optimization
- **Hardware Acceleration**: Cross-platform encoder selection

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

## Modular Architecture Benefits

**Separation of Concerns**:
- **Scene Creation**: Platform-agnostic scene generation and injection
- **Recording Optimization**: Mac-specific hardware acceleration settings
- **Streaming Optimization**: Platform-specific bitrate and server configuration
- **Overlay Generation**: YAML-driven content with Mustache templating

**Cross-Platform Compatibility**:
- Scenes work on any OBS-compatible system
- Recording settings apply only to compatible hardware
- Streaming settings adapt to platform requirements
- Network detection handles WSL/macOS/Linux automatically

**Independent Usage**:
```bash
# Use scenes on any computer
python scripts/inject-obs.py --collection workshop --webserver http://server:8080

# Apply Mac recording settings only on MacBooks  
python scripts/configure-obs-recording.py --preset maximum

# Configure streaming independently of scenes/recording
python scripts/configure-obs-streaming.py --platform youtube --quality high
```

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
- Configure recording/streaming settings independently
- Clean up old collections manually as needed

**Cross-Platform Considerations**:
- WSL users: OBS runs on Windows host, requires IP detection
- All users: Webserver binds to appropriate interface automatically
- Network firewall: Ensure localhost/LAN HTTP access for overlays
- Hardware acceleration: Auto-detected per platform