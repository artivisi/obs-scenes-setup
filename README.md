# OBS Programming Tutorial Setup

Infrastructure-as-Code approach for OBS Studio scene management, designed for programming tutorials with support for recording, live streaming, and video calls.

## Project Overview

This project creates a version-controlled, reproducible OBS setup with:
- Multiple scene layouts (talking head, code demo, screen only, intro/outro)
- Code-based overlays using HTML/CSS/JavaScript
- Manual scene control with optional automation
- Support for 3x3 macropad or Android remote control
- GitHub Pages hosting for overlays

## Folder Structure

```
obs-tutorial-setup/
├── README.md                    # This file
├── PROJECT_NOTES.md            # Detailed project context
├── docs/                       # GitHub Pages content
│   ├── overlays/               # HTML/CSS/JS overlay files
│   │   ├── talking-head.html
│   │   ├── code-demo.html
│   │   ├── screen-only.html
│   │   ├── intro.html
│   │   ├── outro.html
│   │   ├── css/
│   │   │   ├── main.css
│   │   │   ├── animations.css
│   │   │   └── themes.css
│   │   ├── js/
│   │   │   ├── overlay-manager.js
│   │   │   └── obs-integration.js
│   │   └── assets/
│   │       ├── images/
│   │       ├── fonts/
│   │       └── sounds/
│   └── index.html              # Preview page for all overlays
├── scene-collections/          # OBS scene collection JSON files
│   ├── programming-tutorial.json
│   └── streaming-layout.json
├── profiles/                   # OBS profile configurations
│   ├── recording-profile.ini
│   └── streaming-profile.ini
├── scripts/                    # OBS Lua scripts and automation
│   ├── auto-scene-switcher.lua
│   ├── manual-control.lua
│   └── setup-scripts/
│       ├── import-scenes.py
│       ├── export-scenes.py
│       └── configure-obs.py
├── remote-control/             # Macropad and scenario configs
└── media/                      # Static media assets
    ├── intro-video.mp4
    ├── outro-video.mp4
    ├── background-music/
    └── sound-effects/
```

## Technology Stack

- **OBS Studio** - Main streaming/recording software
- **HTML/CSS/JavaScript** - Modern overlay system (replaces PNG overlays)
- **GitHub Pages** - Hosting for overlay files
- **Lua** - OBS scripting for automation
- **Python** - Setup and import/export scripts
- **QMK Firmware** - Macropad configuration (optional)

## Key Design Principles

1. **Manual Control Priority** - Auto-switching is optional, manual always wins
2. **Infrastructure as Code** - Everything version controlled and reproducible
3. **Modular Design** - Each overlay and script serves specific purpose
4. **Cross-Platform** - Works on Windows, macOS, Linux
5. **No External Dependencies** - Self-contained setup

## Control Methods

### Primary: Manual Scene Switching
- OBS hotkeys (F1-F5 for scenes)
- 3x3 Macropad with physical buttons
- Android remote app (Touch Portal or custom web interface)

### Optional: Automated Assistance
- Application-based scene suggestions
- Timer-based intro/outro
- Audio-level triggered switching (hybrid mode only)

## Scene Layouts

### 1. Talking Head
- Large centered webcam
- Minimal overlays
- Good for introductions and explanations

### 2. Code + Webcam
- Split layout with code area and webcam
- Picture-in-picture style
- Main programming tutorial layout

### 3. Screen Only
- Full screen capture
- Small or hidden webcam
- For detailed code demonstrations

### 4. Intro/Outro
- Branded layouts with animations
- Title cards and transitions
- Professional start/end sequences

## GitHub Pages Integration

## GitHub Pages Integration

**Complete setup hosted at:** `https://artivisi.github.io/obs-scenes-setup/`
- Automatic deployment on git push
- Same URLs work on any machine
- Easy sharing and collaboration
- Version controlled visual designs

## Next Steps for Claude Code

1. **Create initial overlay templates** - HTML/CSS for each scene type
2. **Build scene collection JSON** - OBS configuration files
3. **Develop Lua automation scripts** - Smart scene switching with manual override
4. **Create setup/import scripts** - Python automation for OBS configuration
5. **Design macropad integration** - QMK config and OBS hotkey mapping
6. **Build mobile remote interface** - Web-based remote control
7. **Generate documentation** - Usage guides and troubleshooting

## Hardware Setup Context

- **Camera**: Nikon ZFC via Cam Link 4K (USB capture card)
- **Microphone**: Hollyland Lark M2 via USB soundcard  
- **Control**: 3x3 macropad with 1 potentiometer (cost-effective alternative to Stream Deck)
- **Computers**: MacBook Pro M1 + Dell Latitude 2-in-1 (dual platform support)
- **Challenge**: USB device address changes require robust device detection

## Quick Start

### 1. Initial Setup
```bash
# Clone the repository
git clone https://github.com/[username]/obs-scenes-setup.git
cd obs-scenes-setup

# Enable GitHub Pages in repository settings
# - Go to Settings → Pages  
# - Source: Deploy from branch
# - Branch: main, Folder: /docs
```

### 2. Run Complete Integration Test
```bash
# Test entire setup (overlays, devices, scenes, macropad)
python scripts/test-complete-setup.py --full --github-user [your-username]

# Quick test (just overlays and basic validation)  
python scripts/test-complete-setup.py --quick --github-user [your-username]
```

### 3. Hardware Detection and Setup
```bash
# Scan for cameras and audio devices
python scripts/setup-scripts/device-manager.py --scan

# Generate device profile for OBS
python scripts/setup-scripts/device-manager.py --generate-profile

# Validate USB hub for dual camera setup
python scripts/setup-scripts/usb-hub-validator.py --validate
```

### 4. OBS Configuration (Choose One)

**Option A: Automated Scene Creation (RECOMMENDED)**
```bash
# Install dependencies
python scripts/install-dependencies.py

# Enable OBS WebSocket (Tools → WebSocket Server Settings)
# Then create all scenes automatically:
python scripts/setup-scripts/auto-scene-creator.py --create-live --github-user [your-username]
```

**Option B: Manual Import**
```bash
# Import scene collection with your GitHub Pages URLs
python scripts/setup-scripts/import-scenes.py --github-user [your-username]

# Or manually import: OBS → Scene Collection → Import
# File: scene-collections/programming-tutorial.json
```

### 5. Configure Macropad (Choose One)

**Option A: Automated Vial Setup (RECOMMENDED)**
```bash
# One-command macropad setup
python scripts/setup-macropad.py

# Or quick setup without prompts
python scripts/setup-macropad.py --quick
```

**Option B: Manual Setup**
Follow the detailed setup guides:
- **Vial Setup**: `macropad/vial-setup-guide.md`
- **Key Reference**: `macropad/keymap-reference.md`
- **Hardware Design**: [View online documentation](https://artivisi.github.io/obs-scenes-setup/guides/MACROPAD_DESIGN.html)

### 6. Validate Complete Setup
```bash
# Final validation test
python scripts/test-complete-setup.py --full --save-report setup-report.json

# Check that report shows "excellent" or "good" status
```

### 7. Start Recording! 🎬
- Open OBS Studio  
- Select "Programming Tutorials - Artivisi" scene collection
- Test scene switching with F1-F7 keys or macropad
- Start recording with Ctrl+R

## 📚 Complete Documentation

**🌐 GitHub Pages Documentation Site**: https://artivisi.github.io/obs-scenes-setup/

### Quick Access Links
- **🤖 [Automated Setup](https://artivisi.github.io/obs-scenes-setup/guides/AUTOMATED_SETUP.html)** - Skip manual clicking! Auto-create all scenes
- **🎛️ [Manual OBS Setup](https://artivisi.github.io/obs-scenes-setup/guides/OBS_SETUP_GUIDE.html)** - Complete step-by-step configuration
- **🎹 [Macropad Design](https://artivisi.github.io/obs-scenes-setup/guides/MACROPAD_DESIGN.html)** - 4-layer control system with Vial firmware
- **📋 [Project Architecture](https://artivisi.github.io/obs-scenes-setup/guides/PROJECT_NOTES.html)** - Technical deep-dive and system design

### Live Overlay Previews
- **👤 [Talking Head](https://artivisi.github.io/obs-scenes-setup/overlays/talking-head.html?test=true)** - Presenter-focused layout
- **💻 [Code Demo](https://artivisi.github.io/obs-scenes-setup/overlays/code-demo.html?test=true)** - Split screen + webcam
- **🖥️ [Screen Only](https://artivisi.github.io/obs-scenes-setup/overlays/screen-only.html?test=true)** - Full screen capture
- **🎬 [All Overlays](https://artivisi.github.io/obs-scenes-setup/)** - Complete preview gallery

Ready for professional programming tutorials! 🚀