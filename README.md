# OBS Programming Tutorial Setup

Infrastructure-as-Code approach for OBS Studio scene management, designed for programming tutorials with support for recording, live streaming, and video calls.

## Project Overview

This project creates a version-controlled, reproducible OBS setup with:
- Multiple scene layouts (talking head, code demo, screen only, intro/outro)
- Code-based overlays using HTML/CSS/JavaScript
- Manual scene control with optional automation  
- Support for 3x3 macropad or Android remote control
- GitHub Pages hosting for overlays
- **Complete Infrastructure-as-Code automation** with organized script structure

## 🚀 Quick Start

**For immediate setup on fresh OBS:**
```bash
# 1. Install dependencies
python scripts/setup/install-dependencies.py

# 2. Create scenes with online overlays (GitHub Pages)
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi

# OR for offline development (local overlay files)
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi --offline
```
**Total setup time: 2-3 minutes** ⚡

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
├── scripts/                    # Organized automation scripts
│   ├── README.md               # Complete script documentation
│   ├── setup/                  # System setup and hardware config
│   │   ├── install-dependencies.py
│   │   ├── setup-macropad.py
│   │   ├── vial-setup-automation.py
│   │   └── usb-hub-validator.py
│   ├── obs/                    # OBS Studio automation and control
│   │   ├── auto-scene-creator.py    # Scene creation via WebSocket (supports --offline mode)
│   │   └── lua-scripts/            # OBS Lua scripts
│   │       ├── manual-control.lua   # Manual scene control
│   │       └── scene-indicators.lua # Visual feedback
│   └── tools/                  # Development and maintenance
│       └── convert-docs-to-html.py  # Documentation generation
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
python scripts/tools/test-complete-setup.py --full --github-user artivisi

# Quick test (just overlays and basic validation)  
python scripts/tools/test-complete-setup.py --quick --github-user artivisi
```

### 3. Create OBS Scenes

```bash
# Enable OBS WebSocket first (Tools → WebSocket Server Settings)

# Option A: Production mode with GitHub Pages overlays
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi

# Option B: Development mode with local overlay files  
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi --offline

# Option C: Generate JSON for manual import
python scripts/obs/auto-scene-creator.py --generate-json --output my-scenes.json [--offline]
```

### 5. Configure Macropad (Choose One)

**Option A: Automated Vial Setup (RECOMMENDED)**
```bash
# One-command macropad setup
python scripts/setup/setup-macropad.py

# Or quick setup without prompts
python scripts/setup/setup-macropad.py --quick
```

**Option B: Manual Setup**
Follow the detailed setup guides:
- **Vial Setup**: `macropad/vial-setup-guide.md`
- **Key Reference**: `macropad/keymap-reference.md`
- **Hardware Design**: [View online documentation](https://artivisi.github.io/obs-scenes-setup/guides/MACROPAD_DESIGN.html)

### 6. Test Your Setup

```bash
# Test overlays are accessible
curl -I https://artivisi.github.io/obs-scenes-setup/overlays/intro.html
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