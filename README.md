# OBS Programming Tutorial Setup

**Professional OBS automation in 2-3 minutes!** Complete Infrastructure-as-Code system for programming tutorials with automated scene creation, device detection, and professional audio processing.

🚀 **2-3 minute total setup**  
🎆 **Zero manual configuration**  
🎥 **Professional scene templates**  
🛠️ **Cross-platform automation**  
🎹 **Hardware integration ready**

## 🎆 Project Overview

Complete Infrastructure-as-Code system delivering:
- **7 professional scene templates** with proper audio processing
- **Automated device detection** (cameras, microphones, screen capture)
- **GitHub Pages + local overlay support** for online/offline development
- **Content-specific templates** (Java, Linux, DevOps, Interview)
- **Vial macropad automation** with 4-layer control system
- **Cross-platform compatibility** (macOS, Windows, Linux)

## 🚀 One-Command Setup

**Professional OBS setup in under 3 minutes:**

```bash
# 1. Install dependencies (30 seconds)
python scripts/setup/install-dependencies.py

# 2. Enable OBS WebSocket (Tools → WebSocket Server Settings)

# 3. Create complete professional setup (1-2 minutes) 
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi
```

🎉 **Done!** 7 scenes + professional audio + device detection + overlays

### Alternative Modes
```bash
# Development mode with local overlay files
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi --offline

# Generate JSON for manual import (no WebSocket needed)
python scripts/obs/auto-scene-creator.py --generate-json --output my-scenes.json

# Content-specific templates
python scripts/obs/auto-scene-creator.py --create-live --template java --github-user artivisi
```

## 📦 Project Structure

```
obs-scenes-setup/
├── README.md                    # This file - start here!
├── AUTOMATED_SETUP.md          # 🤖 Skip manual setup - auto-create everything 
├── OBS_SETUP_GUIDE.md          # 📋 Manual setup if needed
├── MACROPAD_DESIGN.md          # 🎹 4-layer macropad with Vial
├── PROJECT_NOTES.md            # 🏗️ Technical architecture details
├── docs/                       # 🌐 GitHub Pages hosting
│   ├── overlays/               # 🎨 HTML/CSS/JS overlay system
│   │   ├── intro.html          # Professional intro with countdown
│   │   ├── talking-head.html   # Presenter-focused layout
│   │   ├── code-demo.html      # Split screen + webcam
│   │   ├── screen-only.html    # Full screen capture
│   │   ├── brb.html           # Break screen with timer
│   │   ├── outro.html         # Professional closing
│   │   ├── dual-cam.html      # Interview/guest layout
│   │   └── css/main.css       # Professional styling
│   └── index.html              # 🌐 Live preview gallery
├── scene-collections/          # 💾 Generated OBS scene files
├── macropad/                   # 🎹 Vial configuration and guides
└── scripts/                    # 🤖 Complete automation system
    ├── README.md               # 🛠️ Complete script documentation
    ├── setup/                  # System setup and hardware
    │   ├── install-dependencies.py # 📦 Install packages & validate
    │   └── setup-macropad.py       # 🎹 Automated Vial configuration
    ├── obs/                    # OBS automation engine
    │   ├── auto-scene-creator.py   # 🎬 Main automation script
    │   └── lua-scripts/           # Enhanced OBS control
    └── tools/                  # Development utilities
        └── convert-docs-to-html.py # 📚 Documentation generator
```

## Technology Stack

- **OBS Studio** - Main streaming/recording software
- **HTML/CSS/JavaScript** - Modern overlay system (replaces PNG overlays)
- **GitHub Pages** - Hosting for overlay files
- **Lua** - OBS scripting for automation
- **Python** - Setup and import/export scripts
- **QMK/Vial Firmware** - Macropad configuration (optional)

## 🌐 GitHub Pages Integration

**Live setup at:** https://artivisi.com/obs-scenes-setup/

✅ **Automatic deployment** on git push  
✅ **Universal URLs** work on any machine  
✅ **Easy collaboration** and sharing  
✅ **Version controlled** visual designs  
✅ **Offline mode support** for development

## 🏆 What Makes This Special

### 🚀 Speed & Reliability
- **2-3 minute setup** vs 30+ minutes manual
- **Zero configuration errors** - everything automated
- **Professional results** every time
- **Cross-platform compatibility** (macOS, Windows, Linux)

### 🎨 Professional Quality
- **7 scene templates** designed for programming content  
- **Professional audio chain** (noise suppression, compression, limiting)
- **Smart device detection** and configuration
- **Content-specific optimizations** (Java, Linux, DevOps)

### 🛠️ Developer-Friendly
- **Infrastructure as Code** - everything version controlled
- **Online/offline modes** for production and development
- **Template system** for different content types
- **Comprehensive documentation** with live examples

## 📚 Complete Documentation

**🌐 Live Documentation:** https://artivisi.com/obs-scenes-setup/

### 📜 Quick Access Guides
- **[🤖 Automated Setup](AUTOMATED_SETUP.md)** - Start here! Auto-create all scenes in 2-3 minutes
- **[📋 Manual OBS Setup](OBS_SETUP_GUIDE.md)** - Step-by-step manual configuration if needed
- **[🎹 Macropad Design](MACROPAD_DESIGN.md)** - 4-layer control system with Vial firmware
- **[🏗️ Project Architecture](PROJECT_NOTES.md)** - Technical deep-dive and system design
- **[🛠️ Script Documentation](scripts/README.md)** - Complete automation toolkit reference

### 🎬 Live Overlay Previews  
- **[👤 Talking Head](https://artivisi.com/obs-scenes-setup/overlays/talking-head.html)** - Presenter-focused layout
- **[💻 Code Demo](https://artivisi.com/obs-scenes-setup/overlays/code-demo.html)** - Split screen + webcam  
- **[🖥️ Screen Only](https://artivisi.com/obs-scenes-setup/overlays/screen-only.html)** - Full screen capture
- **[🎬 All Overlays](https://artivisi.com/obs-scenes-setup/)** - Complete preview gallery

## 🎆 Ready to Start?

1. **[📖 Read the Automated Setup Guide](AUTOMATED_SETUP.md)** ← **Start here**
2. **Enable OBS WebSocket** (Tools → WebSocket Server Settings)  
3. **Run one command** and get professional OBS setup in 2-3 minutes
4. **Start creating content!** 🎥

## 🛠️ Supported Hardware

### 📷 Camera Support
- **USB cameras** (built-in webcams, USB webcams)
- **Capture cards** (Elgato Cam Link 4K, generic HDMI-to-USB)
- **Professional cameras** via HDMI output + capture card
- **Multi-camera setups** with automatic device detection

### 🎤 Audio Support  
- **USB microphones** (dynamic, condenser, wireless receivers)
- **USB audio interfaces** (XLR microphone support)
- **Built-in microphones** as fallback
- **Mix-minus setups** for interviews and remote calls

### 🎹 Control Hardware
- **3x3 macropad** with Vial firmware (cost-effective Stream Deck alternative)
- **Rotary encoders** for volume/opacity control
- **Standard keyboards** with hotkey support
- **Mobile devices** via web interface (planned)

### 💻 Platform Compatibility
- **macOS** (M1/Intel) with AVFoundation camera detection
- **Windows** (10/11) with DirectShow device enumeration
- **Linux** with V4L2 video device support
- **Consistent behavior** across all platforms

## 🏠 Architecture Principles

1. **🚀 Speed First** - 2-3 minute setup vs hours of manual work
2. **🛠️ Infrastructure as Code** - Everything version controlled and reproducible  
3. **🌍 Cross-Platform** - Identical behavior on macOS, Windows, Linux
4. **🎨 Professional Quality** - Audio processing, proper layering, device detection
5. **🔄 Maintenance-Free** - Auto-updates, comprehensive error handling
6. **🤝 Developer-Friendly** - Clear documentation, extensible templates

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

## Control Methods Priority
1. **OBS Hotkeys** - Always work (F1-F5 for scenes)
2. **Macropad** - Physical buttons for main controls
3. **Android Remote** - Web interface or Touch Portal app
4. **Emergency Manual Override** - Force return to manual control

---

**Professional OBS setup in 2-3 minutes. Infrastructure as Code. Cross-platform automation. Ready to record.** 🎆