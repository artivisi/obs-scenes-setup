# Automated OBS Scene Creation Guide

Skip the manual clicking! This guide shows you how to automatically create all your OBS scenes, sources, and configurations with a single command.

## Quick Start (Recommended)

### 1. Install Dependencies
```bash
# Install required Python libraries
python scripts/install-dependencies.py
```

### 2. Enable OBS WebSocket Server
1. **Open OBS Studio**
2. **Go to Tools → WebSocket Server Settings**
3. **Check "Enable WebSocket server"**
4. **Set Server Port: 4455** (default)
5. **Set Password** (optional but recommended)
6. **Click Apply/OK**

### 3. Create All Scenes Automatically
```bash
# Create scenes directly in OBS (RECOMMENDED)
python scripts/setup-scripts/auto-scene-creator.py --create-live --github-user [your-username]

# Or generate JSON file for manual import
python scripts/setup-scripts/auto-scene-creator.py --generate-json --github-user [your-username]
```

**That's it! 🎉** All 7 scenes with sources, overlays, and configurations are created automatically.

## What Gets Created

### 📺 7 Complete Scenes
1. **🎬 Intro Scene** - Professional intro with countdown
2. **👤 Talking Head** - Full camera view with overlay
3. **💻 Code + Camera** - Screen capture + PiP camera
4. **🖥️ Screen Only** - Full screen for detailed work
5. **📺 BRB / Technical** - Break screen with timer
6. **🎯 Outro Scene** - Professional outro with CTA
7. **👥 Dual Camera** - Interview setup with guest

### 🎥 Auto-Configured Sources
- **Browser Sources** with your GitHub Pages URLs
- **Camera Sources** with auto-detected devices
- **Screen Capture** optimized for coding
- **Audio Sources** with professional filters
- **Overlays** with Artivisi branding

### 🎛️ Professional Audio Setup
- **Noise Suppression** (RNNoise)
- **Compressor** for consistent levels
- **Limiter** to prevent peaking
- **Monitor + Output** configuration

## Advanced Usage

### Content-Specific Templates
```bash
# Java development focus
python scripts/setup-scripts/auto-scene-creator.py --create-live --template java

# Linux administration 
python scripts/setup-scripts/auto-scene-creator.py --create-live --template linux

# DevOps with diagrams
python scripts/setup-scripts/auto-scene-creator.py --create-live --template devops

# Interview-only setup
python scripts/setup-scripts/auto-scene-creator.py --create-live --template interview
```

### Generate JSON for Manual Import
```bash
# Create scene collection file
python scripts/setup-scripts/auto-scene-creator.py --generate-json --output my-scenes.json

# Then in OBS: Scene Collection → Import → Select my-scenes.json
```

### Custom OBS Connection
```bash
# Different host/port
python scripts/setup-scripts/auto-scene-creator.py --create-live --obs-host 192.168.1.100 --obs-port 4455

# With password
python scripts/setup-scripts/auto-scene-creator.py --create-live --obs-password mypassword
```

## Before You Start

### Prerequisites Checklist
- [ ] **OBS Studio 28+** installed and running
- [ ] **GitHub Pages** enabled with your overlays deployed
- [ ] **Python 3.7+** available
- [ ] **Camera/microphone** connected (will auto-detect)

### Quick Validation
```bash
# Test your complete setup first
python scripts/test-complete-setup.py --quick --github-user [your-username]

# Check device detection
python scripts/setup-scripts/device-manager.py --scan
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
python scripts/install-dependencies.py
# OR manually: pip install obsws-python requests
```

### "No devices detected"
**Solution**: Check hardware connections
```bash
# Run device scan
python scripts/setup-scripts/device-manager.py --scan

# For dual camera setup
python scripts/setup-scripts/usb-hub-validator.py --validate
```

### "GitHub Pages URLs not working"
**Solution**: Verify deployment
```bash
# Test overlay accessibility
python scripts/test-complete-setup.py --overlays-only --github-user [your-username]
```

### "Scenes created but sources missing"
**Cause**: Device detection failed or names don't match
**Solution**: 
1. Check camera/microphone are connected
2. Update device names in OBS manually
3. Re-run with verbose output for debugging

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
F7 - Dual Camera

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
| **Browser Sources** | 7+ sources, copy URLs manually | Auto-configured URLs |
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
python scripts/setup-scripts/auto-scene-creator.py --create-live --github-user [your-username]

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
   python scripts/setup-macropad.py
   ```
5. **Practice Workflow** - Get familiar with scene switching
6. **Start Creating Content!** 🎬

## Automated Macropad Setup

Skip the manual Vial configuration with automated macropad setup:

### Quick Macropad Setup
```bash
# Interactive setup wizard (recommended)
python scripts/setup-macropad.py

# Quick setup without prompts  
python scripts/setup-macropad.py --quick

# Test current setup
python scripts/setup-macropad.py --test
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

## Advanced Customization

### Modify Source Templates
Edit `scripts/setup-scripts/auto-scene-creator.py` to customize:
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
    python scripts/setup-scripts/auto-scene-creator.py --generate-json --template $template --output scenes-$template.json
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