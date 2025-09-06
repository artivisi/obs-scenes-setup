# OBS Programming Tutorial Setup

**Professional OBS automation in 2-3 minutes!** Complete Infrastructure-as-Code system for programming tutorials with automated scene creation, event-specific overlays, and professional audio processing.

🚀 **2-3 minute total setup**  
🎆 **Zero manual configuration**  
🎥 **Professional scene templates**  
🛠️ **Cross-platform automation**  
🎹 **Hardware integration ready**

## 🎆 Project Overview

Complete Infrastructure-as-Code system delivering:
- **7 professional scene templates** with proper audio processing
- **Event-specific overlay generation** from JSON templates
- **Automatic HTTP server for overlays** (works seamlessly with WSL, macOS, Linux)
- **Content-specific templates** (Java, Linux, DevOps, Interview)
- **Vial macropad automation** with 4-layer control system
- **Cross-platform networking** with automatic WSL/Windows compatibility

## 🚀 Easy Workflow Options

### ⚡ Quick Setup (2-3 minutes)
```bash
# Complete workflow with sensible defaults
python scripts/workflow.py --quick

# Or use specific template 
python scripts/workflow.py --quick --template python-workshop
```

### 🎯 Event-Specific Setup (Recommended)
```bash
# Complete custom workflow: environment → event config → overlays → OBS
python scripts/workflow.py --event my-workshop

# Or start with a template
python scripts/workflow.py --event my-workshop --template java
```

**Interactive prompts will ask for:**
- Event title & subtitle
- Presenter name & details  
- Company branding
- Session topics

### 🌐 Generic Setup (Online Mode)
```bash
# Traditional setup with online overlays
python scripts/setup/install-dependencies.py
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi
```

🎉 **Result:** 7 professional scenes + audio processing + custom overlays

### Advanced Options
```bash
# Environment setup only
python scripts/workflow.py --setup

# Generate custom overlays only
python3 scripts/tools/populate-overlays.py --template python-workshop --preview

# Use custom overlays with OBS
python scripts/obs/auto-scene-creator.py --create-live --overlay-path my-overlays --github-user artivisi

# Generate JSON for manual import (no WebSocket needed)
python scripts/obs/auto-scene-creator.py --generate-json --output my-scenes.json
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
│   ├── resources/              # 🎯 Event-specific content templates
│   │   ├── event-config.json   # Default event configuration
│   │   ├── templates/          # Predefined event templates
│   │   └── README.md          # Resource system documentation
│   └── index.html              # 🌐 Live preview gallery
├── scene-collections/          # 💾 Generated OBS scene files
├── macropad/                   # 🎹 Vial configuration and guides
└── scripts/                    # 🤖 Complete automation system
    ├── workflow.py             # 🚀 Complete workflow orchestration
    ├── README.md               # 🛠️ Complete script documentation
    ├── utils/                  # 🔧 Reusable utility modules
    │   ├── obs_utils.py        # OBS connection & operations (WSL auto-detect)
    │   ├── scene_generator.py  # Scene templates & layout management
    │   ├── text_customizer.py  # Text processing & event customization
    │   └── __init__.py
    ├── setup/                  # System setup and hardware
    │   ├── install-dependencies.py # 📦 Install packages & validate
    │   └── setup-macropad.py       # 🎹 Automated Vial configuration
    ├── obs/                    # OBS automation engine
    │   ├── auto-scene-creator.py   # 🎬 Main automation script
    │   ├── list-sources.py         # 📋 Debug OBS sources (refactored)
    │   ├── fix-overlay-urls.py     # 🔧 Update browser source URLs (refactored)
    │   └── lua-scripts/           # Enhanced OBS control
    ├── tools/                  # Development utilities
    │   ├── populate-overlays.py    # 🎯 Generate event-specific overlays
    │   └── convert-docs-to-html.py # 📚 Documentation generator
    └── examples/               # 📚 Usage examples and demonstrations
        └── demo_utilities.py   # 🧪 Utility module demonstrations
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
- **Event-specific overlay generation** with JSON templates
- **Professional audio chain** (noise suppression, compression, limiting)
- **Content-specific optimizations** (Java, Linux, DevOps)

### 🛠️ Developer-Friendly
- **Infrastructure as Code** - everything version controlled
- **Event-specific templates** - easily customize overlays via JSON
- **Online/offline modes** for production and development
- **Template system** for different content types
- **Modular utilities** - reusable components for custom workflows
- **WSL auto-detection** - seamless Windows/Linux development
- **Comprehensive documentation** with live examples

## 📚 Complete Documentation

**🌐 Live Documentation:** https://artivisi.com/obs-scenes-setup/

### 📜 Quick Access Guides
- **[🤖 Automated Setup](AUTOMATED_SETUP.md)** - Start here! Auto-create all scenes in 2-3 minutes
- **[🎯 Overlay Resources](docs/resources/README.md)** - Event-specific overlay generation system
- **[📋 Manual OBS Setup](OBS_SETUP_GUIDE.md)** - Step-by-step manual configuration if needed
- **[🎹 Macropad Design](MACROPAD_DESIGN.md)** - 4-layer control system with Vial firmware
- **[🏗️ Project Architecture](PROJECT_NOTES.md)** - Technical deep-dive and system design
- **[🛠️ Script Documentation](scripts/README.md)** - Complete automation toolkit reference

### 🔧 Developer Resources  
- **[🧪 Utilities API](docs/UTILITIES_API.md)** - Complete API reference for reusable modules
- **[🛠️ Developer Guide](docs/DEVELOPER_GUIDE.md)** - Extending, customizing, and contributing
- **[📚 Usage Examples](scripts/examples/)** - Demonstrations and code samples

### 🎬 Live Overlay Previews  
- **[👤 Talking Head](https://artivisi.com/obs-scenes-setup/overlays/talking-head.html)** - Presenter-focused layout
- **[💻 Code Demo](https://artivisi.com/obs-scenes-setup/overlays/code-demo.html)** - Split screen + webcam  
- **[🖥️ Screen Only](https://artivisi.com/obs-scenes-setup/overlays/screen-only.html)** - Full screen capture
- **[🎬 All Overlays](https://artivisi.com/obs-scenes-setup/)** - Complete preview gallery

## 🎆 Ready to Start?

**New workflow (recommended):**
1. **`python scripts/workflow.py --quick`** ← **Fastest setup**
2. **Or customize:** `python scripts/workflow.py --event my-workshop`
3. **Start recording!** 🎥

**Traditional setup:**
1. **[📖 Read the Automated Setup Guide](AUTOMATED_SETUP.md)**
2. **Enable OBS WebSocket** → Run scripts → Done!

## 🛠️ Supported Hardware

### 📷 Camera Support
- **USB cameras** (built-in webcams, USB webcams)
- **Capture cards** (Elgato Cam Link 4K, generic HDMI-to-USB)
- **Professional cameras** via HDMI output + capture card
- **Multi-camera setups** for interviews and guest appearances

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
- **macOS** (M1/Intel) with native camera and audio support  
- **Windows** (10/11) with DirectShow compatibility
- **Linux** with V4L2 video device support
- **WSL + Windows** automatic network bridge detection
- **Automatic HTTP server** with cross-platform IP detection
- **Consistent behavior** across all platforms

## 🏠 Architecture Principles

1. **🚀 Speed First** - 2-3 minute setup vs hours of manual work
2. **🛠️ Infrastructure as Code** - Everything version controlled and reproducible  
3. **🌍 Cross-Platform** - Identical behavior on macOS, Windows, Linux
4. **🎨 Professional Quality** - Audio processing, proper layering, event-specific content
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