# OBS Studio Setup Guide

Complete guide for setting up OBS Studio to use the Artivisi overlay system for programming tutorials.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Scene Collection Setup](#scene-collection-setup)
3. [Source Configuration](#source-configuration)
4. [Hotkey Configuration](#hotkey-configuration)
5. [Audio Setup](#audio-setup)
6. [Recording/Streaming Settings](#recordingstreaming-settings)
7. [Testing Your Setup](#testing-your-setup)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software
- **OBS Studio 30.0+** (latest version recommended)
- **Web browser** for testing overlays
- **Your GitHub Pages URL** ready: `https://artivisi.github.io/obs-scenes-setup/`

### Hardware Requirements
- **Camera**: Nikon ZFC via Cam Link 4K (or any USB camera)
- **Microphone**: Hollyland Lark M2 via USB (or any USB microphone)
- **3x3 Macropad** (optional but recommended)

## Scene Collection Setup

### Step 1: Create New Scene Collection

1. Open OBS Studio
2. Go to **Scene Collection** → **New**
3. Name it: `Programming Tutorials - Artivisi`
4. Click **OK**

### Step 2: Create Base Scenes

Create these 7 scenes (click **+** in Scenes panel):

1. **🎬 Intro Scene**
2. **👤 Talking Head** 
3. **💻 Code + Camera**
4. **🖥️ Screen Only**
5. **📺 BRB / Technical**
6. **🎯 Outro Scene**
7. **👥 Dual Camera / Interview** (for guest interviews)

## Source Configuration

### Scene 1: 🎬 Intro Scene

**Sources to add:**

1. **Browser Source** - "Intro Overlay"
   - URL: `https://artivisi.github.io/obs-scenes-setup/overlays/intro.html`
   - Width: `1920`, Height: `1080`
   - ✅ Custom CSS: Leave blank
   - ✅ Shutdown source when not visible
   - ✅ Refresh browser when scene becomes active

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

### Cross-Platform Device Detection

Before setting up scenes, run the device detection script:

```bash
# Scan all available devices
python scripts/obs/device-manager.py --scan

# Generate platform-specific profile
python scripts/obs/device-manager.py --generate-profile

# Test device connectivity
python scripts/obs/device-manager.py --test-devices
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