# OBS Infrastructure-as-Code Scripts

Organized automation scripts for professional OBS setup.

## 📁 Directory Structure

```
scripts/
├── core/           # Core infrastructure scripts (empty - reserved for future)
├── setup/          # Initial system setup and hardware configuration
├── obs/            # OBS Studio automation and control
├── tools/          # Development and maintenance tools
└── README.md       # This file
```

## 🚀 Quick Start

### 1. System Setup
```bash
# Install all dependencies
python scripts/setup/install-dependencies.py

# Configure macropad (Vial)
python scripts/setup/setup-macropad.py

# Validate USB hub setup
python scripts/setup/usb-hub-validator.py
```

### 2. OBS Configuration
```bash
# Create scenes with GitHub Pages overlays (production)
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi

# Or create scenes with local overlays (development)
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi --offline

# Generate scene collection JSON for manual import
python scripts/obs/auto-scene-creator.py --generate-json --output my-scenes.json [--offline]
```

### 3. Development Tools
```bash
# Test complete system
python scripts/tools/test-complete-setup.py

# Generate documentation
python scripts/tools/convert-docs-to-html.py
```

## 📋 Script Reference

### Setup Scripts (`scripts/setup/`)

| Script | Purpose | Usage |
|--------|---------|-------|
| `install-dependencies.py` | Install Python packages and system dependencies | `python scripts/setup/install-dependencies.py` |
| `setup-macropad.py` | Interactive macropad configuration wizard | `python scripts/setup/setup-macropad.py` |
| `vial-setup-automation.py` | Automated Vial macropad configuration | Used by setup-macropad.py |
| `usb-hub-validator.py` | Validate USB hub and device connectivity | `python scripts/setup/usb-hub-validator.py` |

### OBS Scripts (`scripts/obs/`)

| Script | Purpose | Usage |
|--------|---------|-------|
| `auto-scene-creator.py` | Create OBS scenes via WebSocket API (supports --offline mode) | `python scripts/obs/auto-scene-creator.py --create-live [--offline]` |

### Lua Scripts (`scripts/obs/lua-scripts/`)

| Script | Purpose | Installation |
|--------|---------|--------------|
| `manual-control.lua` | Enhanced manual scene control with hotkeys | OBS → Scripts → Add |
| `scene-indicators.lua` | Visual feedback for scene changes | OBS → Scripts → Add |

### Tools Scripts (`scripts/tools/`)

| Script | Purpose | Usage |
|--------|---------|-------|
| `test-complete-setup.py` | Comprehensive system testing | `python scripts/tools/test-complete-setup.py` |
| `convert-docs-to-html.py` | Generate HTML documentation from Markdown | `python scripts/tools/convert-docs-to-html.py` |

## 🎯 Common Workflows

### Fresh OBS Installation
```bash
# 1. Setup system
python scripts/setup/install-dependencies.py

# 2. Create scenes automatically
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi

# 3. Test everything
curl -I https://artivisi.github.io/obs-scenes-setup/overlays/intro.html
```

### Development/Testing
```bash
# Use local overlays for development
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi --offline

# Generate documentation
python scripts/tools/convert-docs-to-html.py
```

## 🔧 Configuration

Most scripts support these common options:
- `--obs-host`: OBS WebSocket host (default: localhost)
- `--obs-port`: OBS WebSocket port (default: 4455)  
- `--obs-password`: OBS WebSocket password
- `--github-user`: GitHub username for overlay URLs (default: artivisi)
- `--offline`: Use local overlay files instead of GitHub Pages URLs

## 📚 Documentation

- [Complete Setup Guide](../docs/OBS_SETUP_GUIDE.md)
- [Macropad Configuration](../docs/MACROPAD_DESIGN.md)
- [GitHub Pages Overlays](https://artivisi.github.io/obs-scenes-setup/)

## 🎬 Your Professional OBS System

This script collection provides complete Infrastructure-as-Code automation for a professional programming tutorial setup with:

- ✅ 7 pre-configured scenes with GitHub Pages overlays
- ✅ Automated camera detection and configuration  
- ✅ Professional audio processing and mix-minus setup
- ✅ Cross-platform USB device management
- ✅ Vial macropad automation with 4-layer control system
- ✅ Comprehensive testing and validation tools

**Total setup time: 2-3 minutes** ⚡