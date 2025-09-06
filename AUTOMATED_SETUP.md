# Automated OBS Scene Creation Guide

**Skip 30+ minutes of manual clicking!** Multiple workflow options from quick setup to full customization.

⚡ **Quick setup: 1-2 minutes**  
🎯 **Custom events: 3-4 minutes**  
✅ **Zero configuration errors**  
🎨 **Event-specific overlays**

## 🚀 Workflow Options

### ⚡ Quick Setup (1-2 minutes) - **RECOMMENDED**
```bash
# Complete workflow with sensible defaults
python scripts/workflow.py --quick

# With specific template
python scripts/workflow.py --quick --template python-workshop
```
**What it does:** Environment setup → Template selection → Custom overlays → OBS scenes

### 🎯 Event-Specific Setup (3-4 minutes) - **MOST POWERFUL**
```bash
# Custom event with interactive configuration
python scripts/workflow.py --event my-workshop

# Custom event with template starting point
python scripts/workflow.py --event my-workshop --template java
```
**What it does:** Full workflow with custom event content and branding

### 🌐 Traditional Setup (Manual Steps)

#### Step 1: Install Dependencies (30 seconds)
```bash
python scripts/setup/install-dependencies.py
```

#### Step 2: Enable OBS WebSocket (1 minute)
1. **Open OBS Studio**
2. **Tools → WebSocket Server Settings**
3. **✅ Enable WebSocket server**
4. **Server Port: 4455** (default)
5. **Password**: Leave blank or set your own
6. **Apply/OK**

#### Step 3: Create Scenes (1 minute)
```bash
# Online mode with default overlays
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi

# Offline mode with local overlays
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi --offline

# Custom overlays (after generating with populate-overlays.py)
python scripts/obs/auto-scene-creator.py --create-live --overlay-path my-overlays
```

**That's it! 🎉** 
- 7 professional scenes created
- Audio processing configured
- Professional overlays ready
- Ready to record immediately

## 🛠️ What Gets Created Automatically

### 🎬 7 Professional Scenes
1. **🎬 Intro Scene** (F1) - Professional intro with countdown and branding
2. **👤 Talking Head** (F2) - Full presenter view for explanations
3. **💻 Code + Camera** (F3) - Split screen with Picture-in-Picture camera
4. **🖥️ Screen Only** (F4) - Full screen capture for detailed code work
5. **📺 BRB / Technical** (F5) - Break screen with animated timer
6. **🎯 Outro Scene** (F6) - Professional closing with call-to-action

### 📎 Source Management System
- **📹 Camera Sources** - Edit camera settings once, used everywhere
- **🎤 Audio Sources** - Centralized microphone configuration
- **🖥️ Screen Sources** - Shared screen capture settings
- **⚙️ Scene References** - Changes propagate automatically

### 🛠️ Professional Audio Processing
- **🎙️ Noise Suppression** - RNNoise algorithm for crystal clear voice
- **🔊 Dynamic Compression** - 10:1 ratio for consistent levels
- **⚠️ Peak Limiter** - Prevents audio clipping and distortion
- **🎧 Monitor Output** - Hear yourself without feedback

### 🌐 Smart URL Management
- **Production Mode**: Uses GitHub Pages URLs (always works)
- **Development Mode**: Uses local file:// URLs (for testing)
- **Automatic Detection**: Chooses best overlay source
- **Error Recovery**: Fallback to safe defaults

### 📱 Cross-Platform Compatibility
- **macOS**: Native camera and audio support
- **Windows**: DirectShow compatibility
- **Linux**: V4L2 video device support
- **Professional Audio**: USB microphone and interface support
- **Capture Cards**: Elgato Cam Link 4K and similar devices

## 🎯 Advanced Templates

### Content-Specific Scene Templates
```bash
# Java development with IDE optimization
python scripts/obs/auto-scene-creator.py --create-live --template java --github-user artivisi

# Linux administration with terminal focus
python scripts/obs/auto-scene-creator.py --create-live --template linux --github-user artivisi

# DevOps with architecture diagrams
python scripts/obs/auto-scene-creator.py --create-live --template devops --github-user artivisi

# Interview-only scenes (no coding layouts)
python scripts/obs/auto-scene-creator.py --create-live --template interview --github-user artivisi
```

### Template Customizations
- **Java Template**: IntelliJ IDEA window detection, Java-specific overlays
- **Linux Template**: Terminal-focused scenes, command highlighting
- **DevOps Template**: Architecture diagram overlays, microservices layouts
- **Interview Template**: Dual camera support, guest audio processing

### 💾 Generate JSON for Manual Import
```bash
# Production scene collection (GitHub Pages)
python scripts/obs/auto-scene-creator.py --generate-json --output artivisi-scenes.json --github-user artivisi

# Development scene collection (local files)
python scripts/obs/auto-scene-creator.py --generate-json --output artivisi-local.json --github-user artivisi --offline

# Template-specific collections
python scripts/obs/auto-scene-creator.py --generate-json --template java --output java-tutorial.json
```

**Import Process:**
1. Open OBS Studio
2. **Scene Collection → Import**
3. Select your generated JSON file
4. Scenes appear immediately with all sources configured

### 🌐 Remote OBS Connection
```bash
# Connect to OBS on different computer
python scripts/obs/auto-scene-creator.py --create-live --obs-host 192.168.1.100 --obs-port 4455

# Secure connection with password
python scripts/obs/auto-scene-creator.py --create-live --obs-password your-websocket-password

# Complete remote setup
python scripts/obs/auto-scene-creator.py --create-live --obs-host studio-pc.local --obs-port 4455 --obs-password secure123 --github-user artivisi
```

## Before You Start

### Prerequisites Checklist
- [ ] **OBS Studio 28+** installed and running
- [ ] **GitHub Pages** enabled with your overlays deployed
- [ ] **Python 3.7+** available
- [ ] **Camera/microphone** connected and working in OBS

### Quick Validation
```bash
# Test your dependencies are installed
python scripts/setup/install-dependencies.py

# Test overlay access
curl -I https://artivisi.com/obs-scenes-setup/overlays/intro.html
```

## Troubleshooting

### "Cannot connect to OBS"
**Solution**: Enable WebSocket server in OBS
1. Tools → WebSocket Server Settings
2. Enable WebSocket server
3. Port: 4455, Password: (optional)

### "obsws-python not found" 
**Solution**: Install dependencies
```bash
python scripts/setup/install-dependencies.py
# OR manually: pip install obsws-python requests
```

### "Browser source not loading"  
**Solution**: Check overlay URLs and network connectivity
```bash
# Test overlay accessibility
curl -I https://artivisi.com/obs-scenes-setup/overlays/intro.html

# Use offline mode if network issues
python scripts/obs/auto-scene-creator.py --create-live --offline --github-user artivisi
```

### "GitHub Pages URLs not working"
**Solution**: Use offline mode for development or verify deployment
```bash
# Use local overlays instead
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi --offline

# Or test overlay accessibility
curl -I https://artivisi.github.io/obs-scenes-setup/overlays/intro.html
```

### "Scenes created but sources missing"
**Cause**: Camera or microphone not available in OBS
**Solution**: 
1. Check camera/microphone are connected and working in OBS
2. Update source names in OBS manually if needed
3. Re-run scene creation with verbose output for debugging

## Manual Adjustments After Creation

The automated setup creates everything, but you might want to adjust:

### 1. Device Names
- **Video sources** may need device selection if multiple cameras
- **Audio sources** may need correct microphone selection

### 2. Positioning and Scaling  
- **Camera positions** are auto-calculated but can be tweaked
- **Screen capture** areas may need adjustment for your display

### 3. Hotkeys Assignment
```bash
# Recommended hotkey assignments (set manually in OBS):
F1 - Intro Scene
F2 - Talking Head  
F3 - Code + Camera
F4 - Screen Only
F5 - BRB / Technical
F6 - Outro Scene

Ctrl+R - Start/Stop Recording
Ctrl+P - Pause Recording  
Ctrl+M - Mute Microphone
```

### 4. Audio Levels
- Check **microphone levels** (-12dB to -6dB target)
- Adjust **desktop audio** volume (usually lower than mic)
- Test **noise suppression** effectiveness

## Comparison: Manual vs Automated

| Task | Manual Process | Automated Process |
|------|---------------|-------------------|
| **Scene Creation** | Click 7 times, name each | 1 command |
| **Browser Sources** | 7+ sources, copy URLs manually | Auto-configured URLs (online/offline) |
| **Camera Setup** | Find device names, configure each | Auto-detected and assigned |
| **Audio Filters** | Add 3+ filters per source manually | Professional filters auto-applied |
| **Positioning** | Click and drag each source | Calculated positions |
| **Error Rate** | High (typos, wrong URLs, missing filters) | Low (validated configurations) |
| **Time Required** | 30-60 minutes | 2-3 minutes |
| **Reproducibility** | Manual steps, hard to replicate | Identical results every time |

## Integration with Existing Workflow

### If You Already Have Scenes
```bash
# Backup existing scenes first
# Scene Collection → Export → Save current setup

# Create new collection with automation
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi

# Switch between collections as needed
```

### If You Have Custom Sources
The automated creator won't interfere with:
- **Existing scenes** (creates new ones)
- **Global sources** (adds professional audio filters)
- **Settings** (preserves your OBS configuration)

## Next Steps After Automation

1. **Test Each Scene** - Switch through F1-F7 to verify
2. **Adjust Camera Positioning** - Fine-tune if needed  
3. **Set Recording Settings** - Configure output quality
4. **Setup Macropad** - Automated setup available!
   ```bash
   # One-command macropad configuration
   python scripts/setup/setup-macropad.py
   ```
5. **Practice Workflow** - Get familiar with scene switching
6. **Start Creating Content!** 🎬

## Automated Macropad Setup

Skip the manual Vial configuration with automated macropad setup:

### Quick Macropad Setup
```bash
# Interactive setup wizard (recommended)
python scripts/setup/setup-macropad.py

# Quick setup without prompts  
python scripts/setup/setup-macropad.py --quick

# Test current setup
python scripts/setup/setup-macropad.py --test
```

### What It Does
- ✅ **Detects connected macropad** automatically
- ✅ **Generates Vial keymap** with 4-layer OBS control system
- ✅ **Creates setup instructions** with step-by-step guidance
- ✅ **Validates configuration** to ensure correctness
- ✅ **Maps all OBS hotkeys** for seamless integration

### Generated Files
- `macropad/obs-control-keymap.json` - Vial configuration file
- `macropad/automated-setup-instructions.md` - Setup guide

Simply load the generated keymap in Vial GUI and you're ready to go!

## 🎯 Event-Specific Overlay Customization

Want to customize overlays for your specific event/workshop? Use the overlay resource system:

### 🚀 Quick Event Setup
```bash
# List available event templates
python3 scripts/tools/populate-overlays.py --list-templates

# Generate Python workshop overlays
python3 scripts/tools/populate-overlays.py --template python-workshop --preview

# Generate Linux admin training overlays
python3 scripts/tools/populate-overlays.py --template linux-admin --output linux-training

# Create custom event configuration
cp docs/resources/event-config.json my-event.json
# Edit my-event.json with your event details
python3 scripts/tools/populate-overlays.py --config my-event.json --preview
```

### 🔧 Use Custom Overlays with OBS
```bash
# Generate event overlays first
python3 scripts/tools/populate-overlays.py --template my-event --output my-event-overlays

# Create OBS scenes using your custom overlays
python scripts/obs/auto-scene-creator.py --create-live --offline --overlay-path my-event-overlays
```

**📋 See [docs/resources/README.md](docs/resources/README.md) for complete overlay customization guide.**

## Advanced Customization

### Modify Source Templates
Edit `scripts/obs/auto-scene-creator.py` to customize:
- **Overlay URLs** with different parameters
- **Camera positions** and scaling
- **Audio filter** settings
- **Scene names** and descriptions

### Create Custom Templates  
Add your own template functions:
```python
def _create_my_custom_scenes(self) -> List[SceneConfig]:
    # Your custom scene configurations
    pass
```

### Batch Operations
```bash
# Create multiple variations
for template in java linux devops; do
    python scripts/obs/auto-scene-creator.py --generate-json --template $template --output scenes-$template.json
done
```

---

## Why Use Automated Setup?

✅ **Eliminates human error** - No more typos in URLs or missing sources  
✅ **Consistent results** - Same setup every time, on any machine  
✅ **Saves time** - 2 minutes vs 30+ minutes of clicking  
✅ **Professional quality** - Proper audio filters and positioning  
✅ **Version controlled** - Scene configurations in code  
✅ **Easy sharing** - Team members get identical setups  
✅ **Quick iteration** - Test changes rapidly  

**Ready to automate your OBS setup? Run the commands above and start creating professional content in minutes instead of hours!** 🚀