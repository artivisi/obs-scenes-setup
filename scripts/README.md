# OBS Infrastructure-as-Code Scripts

**Complete automation toolkit** for professional OBS tutorial recording setup.

🚀 **2-3 minute total setup time**  
🤖 **Zero manual configuration**  
🛠️ **Cross-platform device detection**  
🎬 **Professional scene templates**

## 📁 Directory Structure

```
scripts/
├── setup/          # System setup and hardware configuration
├── obs/            # OBS Studio automation and control
├── tools/          # Development and maintenance tools
└── README.md       # This file
```

## 🚀 One-Command Setup

```bash
# Complete setup in one command (after enabling OBS WebSocket)
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi
```
**That's it!** Your professional OBS setup is ready in 2-3 minutes.

## 📋 Step-by-Step Setup

### 1. System Dependencies (30 seconds)
```bash
# Install Python libraries and validate environment
python scripts/setup/install-dependencies.py
```

### 2. OBS Scene Creation (1-2 minutes)
```bash
# Enable OBS WebSocket first (Tools → WebSocket Server Settings)

# Production setup with GitHub Pages overlays (RECOMMENDED)
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi

# Development setup with local overlay files
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi --offline

# Generate JSON file for manual import (no WebSocket needed)
python scripts/obs/auto-scene-creator.py --generate-json --output professional-scenes.json
```

### 3. Hardware Configuration (Optional)
```bash
# Automated macropad setup with Vial
python scripts/setup/setup-macropad.py

# Generate updated documentation
python scripts/tools/convert-docs-to-html.py
```

## 📋 Script Reference

### Setup Scripts (`scripts/setup/`)

| Script | Purpose | Key Features |
|--------|---------|-------------|
| **`install-dependencies.py`** | Install Python packages and system dependencies | ✅ Cross-platform package management<br>✅ Hardware validation<br>✅ Dependency checking |
| **`setup-macropad.py`** | Automated Vial macropad configuration | ✅ 4-layer OBS control system<br>✅ Auto-generates keymap<br>✅ Interactive setup wizard |
| **`vial-setup-automation.py`** | Vial firmware automation engine | ✅ JSON keymap generation<br>✅ Layer management<br>✅ Hotkey mapping |

### OBS Automation (`scripts/obs/`)

| Script | Purpose | Key Features |
|--------|---------|-------------|
| **`auto-scene-creator.py`** | Complete OBS scene automation system | ✅ **7 professional scenes** with proper layering<br>✅ **Device auto-detection** (camera, audio)<br>✅ **Professional audio processing** (noise, compression, limiting)<br>✅ **Online/offline overlay support**<br>✅ **Content-specific templates** (Java, Linux, DevOps)<br>✅ **Cross-platform compatibility**<br>✅ **WebSocket + JSON export modes** |

### Lua Scripts (`scripts/obs/lua-scripts/`)

| Script | Purpose | Installation |
|--------|---------|--------------|
| **`manual-control.lua`** | Enhanced manual scene control with priority system | OBS → Scripts → Add |
| **`scene-indicators.lua`** | Visual feedback for scene changes | OBS → Scripts → Add |

### Development Tools (`scripts/tools/`)

| Script | Purpose | Key Features |
|--------|---------|-------------|
| **`convert-docs-to-html.py`** | Documentation generation system | ✅ **Markdown to HTML conversion**<br>✅ **GitHub Pages deployment**<br>✅ **Cross-referenced documentation**<br>✅ **Automated guide updates** |

## 🎯 Workflow Examples

### 🆕 Brand New Setup (First Time)
```bash
# 1. Install dependencies and validate system (30 seconds)
python scripts/setup/install-dependencies.py

# 2. Enable OBS WebSocket (Tools → WebSocket Server Settings)

# 3. Create complete professional setup (1-2 minutes)
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi

# 4. Configure macropad (optional, 1 minute)
python scripts/setup/setup-macropad.py --quick

# 5. Test everything is working
curl -I https://artivisi.github.io/obs-scenes-setup/overlays/intro.html
```
**Total time: 3-4 minutes → Ready to record!**

### 🔄 Daily Content Creation
```bash
# Switch to different content template as needed
python scripts/obs/auto-scene-creator.py --create-live --template java --github-user artivisi
```

### 🛠️ Development & Testing
```bash
# Use local overlay files for development
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi --offline

# Test multiple templates
for template in java linux devops; do
    python scripts/obs/auto-scene-creator.py --generate-json --template $template --output test-$template.json
done

# Regenerate documentation after changes
python scripts/tools/convert-docs-to-html.py
```

### 🎥 Multi-Machine Setup
```bash
# Generate portable scene collection
python scripts/obs/auto-scene-creator.py --generate-json --output portable-setup.json --github-user artivisi

# Import on any machine with OBS
# No Python required - just Scene Collection → Import → Select JSON
```

## 🔧 Configuration Options

### 🔗 Universal Script Options

**Connection Settings:**
- `--obs-host` - OBS WebSocket host (default: localhost)
- `--obs-port` - OBS WebSocket port (default: 4455)
- `--obs-password` - WebSocket password (if set in OBS)

**Content Settings:**
- `--github-user` - Your GitHub username for overlay URLs (default: artivisi)
- `--template` - Scene template (standard, java, linux, devops, interview)
- `--offline` - Use local files instead of GitHub Pages URLs

**Output Control:**
- `--output` - JSON output filename for scene collections
- `--create-live` - Create scenes directly in OBS via WebSocket
- `--generate-json` - Generate scene collection file for manual import

## 📚 Complete Documentation

**🌐 Live Documentation:** https://artivisi.github.io/obs-scenes-setup/

### 📖 Essential Guides
- **[🤖 Automated Setup](../AUTOMATED_SETUP.md)** - Skip manual clicking! Auto-create everything
- **[📋 Manual OBS Setup](../OBS_SETUP_GUIDE.md)** - Step-by-step manual configuration 
- **[🎹 Macropad Design](../MACROPAD_DESIGN.md)** - 4-layer control system with Vial
- **[🏗️ Project Architecture](../PROJECT_NOTES.md)** - Technical deep-dive and system design

### 🎬 Overlay Previews
- **[👤 Talking Head](https://artivisi.github.io/obs-scenes-setup/overlays/talking-head.html)** - Presenter-focused layout
- **[💻 Code Demo](https://artivisi.github.io/obs-scenes-setup/overlays/code-demo.html)** - Split screen + webcam
- **[🖥️ Screen Only](https://artivisi.github.io/obs-scenes-setup/overlays/screen-only.html)** - Full screen capture
- **[🎬 All Overlays](https://artivisi.github.io/obs-scenes-setup/)** - Complete preview gallery

## 🎬 Professional OBS System in Minutes

Complete Infrastructure-as-Code automation delivers:

### 🎭 Scene Management
- ✅ **7 professional scene templates** (Intro, Talking Head, Code+Cam, Screen Only, BRB, Outro)
- ✅ **Content-specific variations** (Java, Linux, DevOps, Interview layouts)
- ✅ **Source reference system** (edit once, used everywhere)
- ✅ **Proper layer ordering** (overlays on top, backgrounds below)

### 🛠️ Technical Excellence
- ✅ **Professional audio chain** (RNNoise suppression, 10:1 compression, peak limiting)
- ✅ **Cross-platform device detection** (macOS AVFoundation, Windows DirectShow, Linux V4L2)
- ✅ **Smart overlay management** (GitHub Pages production + local development)
- ✅ **Automated source configuration** (cameras, microphones, screen capture)

### 🎮 Hardware Integration
- ✅ **Vial macropad automation** (4-layer control system with auto-generated keymaps)
- ✅ **USB device management** (consistent device detection across reconnections)
- ✅ **Multi-camera support** (dual Cam Link 4K setup with proper addressing)
- ✅ **Audio routing** (mix-minus for interviews, monitor without feedback)

### 📊 Reliability & Maintenance
- ✅ **Comprehensive error handling** (graceful fallbacks, clear error messages)
- ✅ **Version controlled configs** (reproducible setups across machines)
- ✅ **Documentation automation** (always up-to-date guides)

**🎯 Ready for professional content creation in under 3 minutes!**