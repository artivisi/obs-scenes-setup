# OBS Studio Setup Guide

Comprehensive guide for setting up OBS Studio with automated scene creation and professional overlay system for programming tutorials.

## 🚀 Quick Start (Recommended)

For immediate setup, use our **automated scene creator**:

```bash
# 1. Install dependencies
python scripts/setup/install-dependencies.py

# 2. Enable OBS WebSocket (Tools → WebSocket Server Settings)
# 3. Create all scenes automatically
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi
```

**Setup time: 2-3 minutes** ⚡

## Table of Contents

1. [Automated Setup](#automated-setup) **← Start Here**
2. [Manual Setup](#manual-setup) (if needed)
3. [Scene Reference](#scene-reference)
4. [Device Configuration](#device-configuration)
5. [Audio Processing](#audio-processing)
6. [Hotkey Configuration](#hotkey-configuration)
7. [Recording Settings](#recording-settings)
8. [Troubleshooting](#troubleshooting)

## Automated Setup

### Prerequisites

### Required Software
- **OBS Studio 28.0+** with WebSocket plugin
- **Python 3.7+** for automation scripts
- **Git** for version control
- **GitHub Pages** enabled (or local overlay files)

### Hardware Requirements
- **Camera**: Any USB camera or capture card
- **Microphone**: USB audio device or built-in mic
- **3x3 Macropad** (optional) with Vial firmware

### Step 1: Enable OBS WebSocket Server

1. Open OBS Studio
2. Go to **Tools → WebSocket Server Settings**
3. Check **"Enable WebSocket server"**
4. Set **Server Port: 4455** (default)
5. Set **Password** (optional)
6. Click **Apply/OK**

### Step 2: Run Automated Scene Creator

```bash
# Production mode with GitHub Pages overlays (RECOMMENDED)
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi

# Development mode with local overlay files
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi --offline

# Generate JSON file for manual import
python scripts/obs/auto-scene-creator.py --generate-json --output my-scenes.json
```

### What Gets Created Automatically

✅ **7 Professional Scenes** with proper source ordering  
✅ **Browser Sources** with correct GitHub Pages URLs  
✅ **Camera Auto-Detection** and configuration  
✅ **Audio Processing** with noise suppression, compression, and limiting  
✅ **Screen Capture** optimized for programming  
✅ **Source References** for easy editing (edit once, used everywhere)  

## Manual Setup

## Scene Reference

The automated system creates these 7 scenes with optimized layouts:

### Main Scenes (F1-F6)
1. **🎬 Intro Scene** - Professional intro with countdown
2. **👤 Talking Head** - Full camera view for presentations
3. **💻 Code + Camera** - Split layout with PiP camera
4. **🖥️ Screen Only** - Full screen capture for detailed work
5. **📺 BRB / Technical** - Break screen with timer
6. **🎯 Outro Scene** - Professional outro with call-to-action

### Source Scenes (Edit Once, Use Everywhere)
- **📹 Camera Sources** - Edit camera settings here
- **🎤 Audio Sources** - Edit microphone settings here  
- **🖥️ Screen Sources** - Edit screen capture settings here

All main scenes reference these source scenes, so you only need to configure devices once.

## Manual Scene Collection Setup (If Not Using Automation)

Only follow this section if you cannot use the automated setup:

### Create New Scene Collection

1. Go to **Scene Collection** → **New**
2. Name: `Programming Tutorials - Artivisi`
3. Manually create the 7 scenes listed above

## Device Configuration

### Camera Setup

The automated system configures cameras for you. For manual setup:

**Recommended Camera Settings:**
- **Resolution**: 1920x1080 or 1080x1080 (square for better framing)
- **FPS**: 30 (matches recording settings)
- **Format**: Auto-detect (MJPEG or YUV422)

**Multi-Camera Setup:**
- **Primary Camera**: Main presenter camera
- **Secondary Camera**: Guest or alternate angle
- Connect in consistent order for reliable operation

### Audio Configuration

The system automatically applies professional audio processing:

**Applied Filters:**
- **Noise Suppression** (RNNoise method)
- **Compressor** (10:1 ratio, -18dB threshold) 
- **Limiter** (-6dB threshold, 60ms release)

### Browser Source Configuration

All overlays use these optimized settings:
- **Width**: 1920, **Height**: 1080
- **FPS**: 30
- ✅ **Shutdown source when not visible**
- ✅ **Restart when active** (ensures fresh loading)
- ❌ **Reroute audio** (keep disabled)

**Overlay URLs:**
- Production: `https://artivisi.github.io/obs-scenes-setup/overlays/[scene].html`
- Development: `file://[project-path]/docs/overlays/[scene].html`

2. **Video Capture Device** - "Background Camera" (Optional)
   - Device: Your camera (Nikon ZFC/Cam Link 4K)
   - Resolution: `1920x1080` or `1080x1080`
   - Set **Transform** → **Fit to Screen** with 50% opacity for background

**URL Parameters for Customization:**
```
?title=Java Development Mastery
&subtitle=Building Enterprise Applications
&countdown=true
&autoexit=true
&duration=10
```

### Scene 2: 👤 Talking Head

**Sources to add:**

1. **Video Capture Device** - "Main Camera"
   - Device: Your camera
   - Resolution: `1920x1080` or `1080x1080`
   - Position: Center of screen

2. **Browser Source** - "Talking Head Overlay"
   - URL: `https://artivisi.github.io/obs-scenes-setup/overlays/talking-head.html`
   - Width: `1920`, Height: `1080`
   - ✅ Shutdown source when not visible
   - ✅ Refresh browser when scene becomes active

**URL Parameters:**
```
?topic=Java Programming
&recording=true
&hidetitle=false
```

### Scene 3: 💻 Code + Camera

**Sources to add:**

1. **Display Capture** - "Screen Capture"
   - Capture Method: Automatic
   - Position: Left side of screen
   - Transform: Scale to fit code area

2. **Video Capture Device** - "PiP Camera"
   - Device: Your camera
   - Position: Top-right corner
   - Transform: Scale to 400x300px

3. **Browser Source** - "Code Demo Overlay"
   - URL: `https://artivisi.github.io/obs-scenes-setup/overlays/code-demo.html`
   - Width: `1920`, Height: `1080`
   - Layer: Top layer

**URL Parameters:**
```
?lang=java
&file=Application.java
&topic=Spring Boot Development
&recording=true
```

### Scene 4: 🖥️ Screen Only

**Sources to add:**

1. **Display Capture** - "Full Screen"
   - Capture Method: Automatic
   - Transform: Fit to screen

2. **Video Capture Device** - "Mini Camera" (Optional)
   - Device: Your camera
   - Position: Bottom-right corner
   - Transform: Scale to 240x180px
   - Can be hidden with URL parameter

3. **Browser Source** - "Screen Only Overlay"
   - URL: `https://artivisi.github.io/obs-scenes-setup/overlays/screen-only.html`
   - Width: `1920`, Height: `1080`

**URL Parameters:**
```
?hidecam=false
&topic=Java Deep Dive
&recording=true
&progress=true
```

### Scene 5: 📺 BRB / Technical

**Sources to add:**

1. **Browser Source** - "BRB Overlay"
   - URL: `https://artivisi.github.io/obs-scenes-setup/overlays/brb.html`
   - Width: `1920`, Height: `1080`

**URL Parameters:**
```
?type=break          # break, technical, emergency
&duration=5          # minutes
&music=true
&message=Custom message here
```

### Scene 6: 🎯 Outro Scene

**Sources to add:**

1. **Browser Source** - "Outro Overlay"
   - URL: `https://artivisi.github.io/obs-scenes-setup/overlays/outro.html`
   - Width: `1920`, Height: `1080`

2. **Video Capture Device** - "Background Camera" (Optional)
   - Device: Your camera
   - Transform: Background with low opacity

**URL Parameters:**
```
?message=Hope you enjoyed this session
&type=java
```

### Scene 7: 👥 Dual Camera / Interview

**Sources to add:**

1. **Video Capture Device** - "Main Camera"
   - Device: Primary camera (Cam Link 1)
   - Position: Left side
   - Transform: Scale to 640x480px

2. **Video Capture Device** - "Secondary Camera"
   - Device: Second camera (Cam Link 2) 
   - Position: Right side
   - Transform: Scale to 640x480px

3. **Audio Input Capture** - "Guest Microphone"
   - Device: Second USB audio or Zoom audio
   - Add noise suppression and compression filters

4. **Browser Source** - "Dual Camera Overlay"
   - URL: `https://artivisi.github.io/obs-scenes-setup/overlays/dual-cam.html`
   - Width: `1920`, Height: `1080`

**URL Parameters:**
```
?layout=balanced        # balanced, host-focus, guest-focus
&host=Host Name
&guest=Guest Name
&platform=zoom         # zoom, teams, meet, local
&topics=true
&recording=true
```

**Layout Modes:**
- `balanced` - Equal-sized camera frames
- `host-focus` - Large host, small guest PiP
- `guest-focus` - Large guest, small host PiP

## Device Management

### Cross-Platform Setup

Before setting up scenes, ensure your dependencies are installed:

```bash
# Install required dependencies
python scripts/setup/install-dependencies.py

# Create automated scenes (recommended)
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi
```

### USB Hub Best Practices

**Recommended Connection Order:**
1. Connect USB hub to laptop first
2. Connect primary Cam Link (becomes /dev/video0 or Device 1)
3. Connect secondary Cam Link (becomes /dev/video1 or Device 2)  
4. Connect USB audio devices
5. Connect macropad last

**Device Naming Patterns:**
- **Primary Cam Link**: "*Cam Link*" or "Elgato Cam Link 4K"
- **Secondary Cam Link**: "*Cam Link*" (2nd device)
- **USB Audio**: "*USB Audio*" or "Hollyland Lark M2"

### Multi-Camera Setup Requirements

**Hardware Checklist:**
- [ ] USB 3.0 hub with sufficient power
- [ ] Primary Cam Link 4K + Nikon ZFC
- [ ] Secondary Cam Link 4K + second camera
- [ ] USB audio interface or two USB microphones
- [ ] Consistent USB port usage

**Audio Configuration for Interviews:**
1. **Host Audio**: USB audio device (Hollyland Lark M2)
2. **Guest Audio**: 
   - Local: Second USB microphone
   - Remote: Zoom/Teams audio capture
3. **Mix-Minus Setup**: Separate remote audio from local audio
4. **Monitor Audio**: Host hears guest, guest hears host (no echo)

## Hotkey Configuration

### Recommended Hotkey Setup

Go to **File** → **Settings** → **Hotkeys**

**Scene Switching:**
- `F1` - Intro Scene
- `F2` - Talking Head  
- `F3` - Code + Camera
- `F4` - Screen Only
- `F5` - BRB / Technical
- `F6` - Outro Scene
- `F7` - Dual Camera / Interview

**Recording Controls:**
- `Ctrl+R` - Start/Stop Recording
- `Ctrl+P` - Pause Recording
- `Ctrl+M` - Mute Microphone
- `Ctrl+Shift+M` - Mute All Audio

**Advanced Controls:**
- `Ctrl+1` through `Ctrl+7` - Direct scene access
- `Ctrl+Plus/Minus` - Volume adjustment
- `Ctrl+K` - Add Chapter Marker (if supported)

### Macropad Integration

If using the 3x3 macropad, configure **Vial** firmware to send these hotkeys:

**Layer 0 (Core Controls):**
```
[Ctrl+R] [Ctrl+P] [Ctrl+M]
[F2]     [F3]     [Ctrl+Shift+M] 
[Ctrl+K] [F4]     [Panic Button]
```

See `MACROPAD_DESIGN.md` for complete layer configurations.

## Audio Setup

### Audio Sources Configuration

1. **Microphone/Aux**:
   - Device: Hollyland Lark M2 (or your USB microphone)
   - Add **Noise Suppression** filter
   - Add **Compressor** filter for consistent levels
   - Add **Gain** filter if needed

2. **Desktop Audio**:
   - For system sounds, music, etc.
   - Usually lower volume than microphone

3. **Audio Monitoring**:
   - Set microphone to "Monitor and Output"
   - Use headphones to monitor your audio

### Recommended Audio Filters

**For Microphone:**
1. **Noise Suppression** - RNNoise (GPU) or Speex
2. **Compressor** - Ratio: 10:1, Threshold: -18dB
3. **Limiter** - Threshold: -6dB, Release: 60ms
4. **Gain** - Adjust to get consistent -12dB to -6dB levels

## Recording/Streaming Settings

### Video Settings

**File** → **Settings** → **Video**:
- Base Resolution: `1920x1080`
- Output Resolution: `1920x1080` 
- FPS: `30` (or `60` for smooth code scrolling)

### Output Settings

**File** → **Settings** → **Output**:

**Recording:**
- Recording Format: `mp4`
- Video Encoder: `x264` or `NVENC H.264` (if available)
- Rate Control: `CRF`
- CRF: `18-23` (lower = higher quality)
- Keyframe Interval: `2`
- CPU Preset: `fast` or `medium`

**Streaming (if applicable):**
- Video Bitrate: `2500-6000 Kbps` (based on upload speed)
- Audio Bitrate: `160 Kbps`
- Encoder: Same as recording

### Advanced Settings

**File** → **Settings** → **Advanced**:
- Color Format: `NV12`
- Color Space: `709`
- Color Range: `Partial`

## Testing Your Setup

### Pre-Recording Checklist

1. **Test Each Scene:**
   - Switch between all 6 scenes
   - Verify overlays load correctly
   - Check camera positioning
   - Test audio levels

2. **Browser Source Testing:**
   - Open overlay URLs in browser to verify they work
   - Test with different URL parameters
   - Verify animations play smoothly

3. **Recording Test:**
   - Record 30 seconds of each scene
   - Check output file quality
   - Verify audio sync
   - Test scene transitions

### Performance Optimization

**If experiencing lag or dropped frames:**

1. **Lower CPU Usage:**
   - Reduce x264 preset to `ultrafast`
   - Lower base resolution to `1600x900`
   - Reduce FPS to 30

2. **GPU Acceleration:**
   - Use NVENC encoder if available
   - Enable hardware acceleration in browsers

3. **Browser Source Optimization:**
   - Add `?test=true` to overlay URLs for simpler graphics
   - Disable "Refresh browser when scene becomes active" if stable

## Troubleshooting

### Common Issues

**❌ Overlay doesn't load**
- ✅ Check GitHub Pages URL is correct and accessible
- ✅ Verify GitHub Actions deployed successfully  
- ✅ Clear browser cache in OBS (right-click source → Refresh)

**❌ Camera not detected**
- ✅ Ensure Cam Link 4K drivers installed
- ✅ Check camera is powered on and connected
- ✅ Try different USB port
- ✅ Restart OBS Studio

**❌ Audio issues**
- ✅ Check microphone is set as default in system
- ✅ Verify USB audio device drivers
- ✅ Test microphone in other applications
- ✅ Check OBS audio mixer levels

**❌ Poor performance**
- ✅ Close unnecessary applications
- ✅ Lower OBS video resolution
- ✅ Use hardware encoding if available
- ✅ Check CPU and GPU usage

### Browser Source Debug

Add these parameters to overlay URLs for debugging:
```
?test=true           # Simplified graphics for testing
?debug=true          # Show debug information
?noanim=true         # Disable animations
```

### Scene Collection Export/Import

**To backup your setup:**
1. **Scene Collection** → **Export**
2. Save as `Artivisi-Programming-Tutorials.json`

**To restore:**
1. **Scene Collection** → **Import**  
2. Select your exported JSON file

## Next Steps

1. **Practice Transitions** - Get comfortable switching between scenes
2. **Test Recording Workflow** - Record a short practice session
3. **Configure Macropad** - Set up physical controls (see MACROPAD_DESIGN.md)
4. **Customize Overlays** - Modify URL parameters for your content
5. **Create Templates** - Save scene configurations for different topics

## Advanced Features

### Scene Transitions

**File** → **Settings** → **Scene Transitions**:
- Default: `Fade` (300ms)
- For intro/outro: `Stinger` or `Slide` transitions

### Studio Mode

Enable **Studio Mode** for preview/program workflow:
- Preview changes before going live
- Perfect for streaming or live recordings
- Use macropad Layer 3 for studio controls

### Multiple Audio Tracks

For advanced editing, record multiple audio tracks:
- Track 1: Microphone only
- Track 2: Desktop audio only
- Track 3: Mixed audio
- Configure in **Settings** → **Output** → **Recording**

---

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Verify your GitHub Pages deployment is working
3. Test overlays directly in browser first
4. Check OBS Studio logs: **Help** → **Log Files**

**Hardware-specific help:**
- **Cam Link 4K**: Elgato support documentation
- **Hollyland Lark M2**: Check USB audio driver installation
- **Macropad**: See MACROPAD_DESIGN.md for configuration

Your professional OBS tutorial setup is now ready! 🚀