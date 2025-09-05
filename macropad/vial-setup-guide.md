# Vial Macropad Setup Guide for OBS

This guide walks you through setting up your 3x3 macropad with clickable encoder for the Artivisi OBS tutorial system using Vial firmware.

## Prerequisites

### Hardware Requirements
- **3x3 Macropad** with rotary encoder (clickable)
- **USB Cable** for connection and firmware flashing
- **Computer** running Windows, macOS, or Linux

### Software Requirements
- **Vial GUI** - Download from https://get.vial.today/
- **QMK Toolbox** (for firmware flashing) - https://github.com/qmk/qmk_toolbox
- **OBS Studio 30.0+** with scenes configured

## Phase 1: Firmware Setup

### Step 1: Prepare Your Macropad
1. **Connect macropad** to computer via USB
2. **Check current firmware** - if it already supports Vial, skip to Phase 2
3. **Put macropad in bootloader mode** (usually hold boot button while plugging in)

### Step 2: Flash Vial Firmware
1. **Download appropriate firmware**:
   - Check your macropad model and MCU type
   - Download Vial-compatible firmware for your specific board
   - Common MCUs: Pro Micro (ATmega32U4), Elite-C (STM32F303)

2. **Flash firmware using QMK Toolbox**:
   ```
   1. Open QMK Toolbox
   2. Select your .hex/.bin firmware file
   3. Put macropad in bootloader mode
   4. Click "Flash" when device is detected
   5. Wait for "Flash complete" message
   ```

3. **Verify firmware**:
   - Macropad should reconnect as HID device
   - Test that keys register in a text editor
   - Encoder should scroll and click

## Phase 2: Vial Configuration

### Step 1: Open Vial and Load Device
1. **Launch Vial application**
2. **Connect your macropad** - it should appear in device list
3. **Select your device** from the dropdown

### Step 2: Import Base Configuration
1. **Load our config**: File → Load → `vial-config.json`
2. **Verify layout**: Check that 3x3 + encoder layout appears
3. **Test basic keys**: Click keys in Vial and verify physical key presses

### Step 3: Configure Layer 0 (Core Controls)

**Map the following keys in order:**

| Physical Position | Vial Key | Function | Keycode |
|-------------------|----------|----------|---------|
| Top-Left | Key 0 | REC/STOP | `LCTL(KC_R)` |
| Top-Center | Key 1 | PAUSE | `LCTL(KC_P)` |
| Top-Right | Key 2 | MUTE MIC | `LCTL(KC_M)` |
| Mid-Left | Key 3 | SCENE- | `KC_PGUP` |
| Mid-Center | Key 4 | SCENE+ | `KC_PGDN` |
| Mid-Right | Key 5 | MUTE ALL | `LCTL(LSFT(KC_M))` |
| Bottom-Left | Key 6 | MARKER | `LCTL(KC_K)` |
| Bottom-Center | Key 7 | SCREEN | `KC_F4` |
| Bottom-Right | Key 8 | PANIC | `KC_F5` |

**Configure Encoder:**
- **Clockwise**: `KC_VOLU` (Volume Up)
- **Counter-Clockwise**: `KC_VOLD` (Volume Down)
- **Click**: `MO(1)` (Momentary Layer 1) or custom layer switch

### Step 4: Test Layer 0
1. **Save configuration** (Ctrl+S in Vial)
2. **Open OBS Studio**
3. **Test each function**:
   - REC/STOP: Should start/stop recording
   - PAUSE: Should pause recording
   - MUTE MIC: Should mute/unmute microphone
   - SCENE+/-: Should navigate scenes
   - Volume: Should adjust system volume

## Phase 3: Advanced Layer Configuration

### Step 1: Configure Layer 1 (Tutorial Mode)
1. **Switch to Layer 1** in Vial
2. **Map tutorial-specific functions**:

| Position | Function | Keycode | Notes |
|----------|----------|---------|--------|
| 0 | INTRO | `KC_F1` | Intro scene |
| 1 | TALKING | `KC_F2` | Talking head |
| 2 | CODE | `KC_F3` | Code + camera |
| 3 | SPLIT | `LCTL(KC_1)` | Split layout |
| 4 | TERMINAL | `LCTL(KC_2)` | Terminal focus |
| 5 | BROWSER | `LCTL(KC_3)` | Browser scene |
| 6 | ZOOM IN | `LCTL(KC_PLUS)` | Increase font |
| 7 | ZOOM OUT | `LCTL(KC_MINS)` | Decrease font |
| 8 | OUTRO | `KC_F6` | Outro scene |

**Layer 1 Encoder:**
- **Rotate**: Custom function for webcam size adjustment
- **Click**: Return to Layer 0

### Step 2: Configure Layer 2 (Presentation Mode)
Similar process, mapping presentation-specific hotkeys for slides, diagrams, and dual camera interviews.

### Step 3: Configure Layer 3 (Production Mode)
Map advanced OBS controls for streaming and professional recording.

## Phase 4: OBS Studio Integration

### Step 1: Configure OBS Hotkeys
1. **Open OBS Studio**
2. **Go to File → Settings → Hotkeys**
3. **Map the following hotkeys** to match your macropad:

```
Recording:
- Start/Stop Recording: Ctrl+R
- Pause Recording: Ctrl+P  
- Add Chapter Marker: Ctrl+K

Audio:
- Toggle Microphone: Ctrl+M
- Mute All Audio: Ctrl+Shift+M

Scenes:
- Scene 1 (Intro): F1
- Scene 2 (Talking Head): F2  
- Scene 3 (Code + Camera): F3
- Scene 4 (Screen Only): F4
- Scene 5 (BRB/Technical): F5
- Scene 6 (Outro): F6
- Scene 7 (Dual Camera): F7
- Previous Scene: Page Up
- Next Scene: Page Down
```

### Step 2: Test Complete Workflow
1. **Start recording** using macropad
2. **Switch between scenes** using Scene+/- buttons
3. **Test mute functions** and verify visual feedback
4. **Try panic button** and ensure BRB scene activates
5. **Test volume control** and verify audio adjustment

## Phase 5: Visual Feedback Setup

### Step 1: Configure LED Indicators (if supported)
1. **RGB Underglow**: Set colors for each layer
   - Layer 0: Red
   - Layer 1: Green  
   - Layer 2: Blue
   - Layer 3: Yellow

2. **Per-Key RGB**: If available, set key colors based on function
   - Record: Red when recording, green when stopped
   - Mute: Red when muted, green when active

### Step 2: OBS Overlay Setup
Create a browser source overlay showing:
- Current macropad layer
- Active functions
- Recording status

**HTML for OBS Overlay:**
```html
<!-- Add to your existing overlays -->
<div class="macropad-indicator" id="macropadIndicator">
    <div class="layer-info">Layer 0: Core Controls</div>
    <div class="status-indicators">
        <span class="rec-status">REC</span>
        <span class="audio-status">🎤</span>
    </div>
</div>
```

## Phase 6: Testing and Validation

### Complete Testing Checklist
- [ ] **Basic Functions**: All Layer 0 functions work correctly
- [ ] **Scene Navigation**: Smooth transitions between scenes  
- [ ] **Audio Controls**: Mute/unmute with visual feedback
- [ ] **Recording**: Start/stop/pause functions reliable
- [ ] **Volume**: Encoder controls system audio smoothly
- [ ] **Layer Switching**: Can access and use other layers
- [ ] **Emergency Functions**: Panic button always accessible
- [ ] **Visual Feedback**: LED/overlay indicators match state

### Performance Testing
1. **Rapid Key Presses**: Test responsiveness under fast operation
2. **Layer Switching**: Verify no lag when changing layers
3. **Encoder Precision**: Check volume control is smooth and accurate
4. **USB Stability**: Test after disconnect/reconnect cycles

## Troubleshooting

### Common Issues

**Keys Not Responding**
- Check USB connection
- Verify firmware flashed correctly
- Test with different USB port/cable
- Check for conflicting software

**Wrong Hotkeys**
- Verify OBS hotkey configuration
- Check for application focus issues
- Test hotkeys work outside Vial/macropad
- Verify keycode syntax in Vial

**Encoder Issues**
- Adjust encoder sensitivity in Vial
- Check physical encoder connection
- Test encoder in different applications
- Verify click vs rotate functions

**Layer Switching Problems**
- Check layer switch key configuration
- Verify layer exists and has keys mapped
- Test layer indicator feedback
- Try manual layer switching in Vial

### Debug Mode
1. **Enable Vial Console**: View → Console
2. **Monitor key presses** in real-time
3. **Check layer changes** are detected
4. **Verify USB communication**

## Backup and Maintenance

### Save Configuration
1. **Export config**: File → Save As → `artivisi-macropad-config.json`
2. **Backup to cloud storage**
3. **Document any custom modifications**

### Regular Maintenance
- **Test all functions weekly**
- **Update Vial firmware** when new versions available
- **Clean physical keys** and encoder
- **Check USB cable** for wear

## Advanced Customization

### Custom Keycodes
Create custom functions for:
- **OBS Scene Transitions**: Fade, cut, slide
- **Application Launch**: Start specific software
- **System Controls**: Sleep, shutdown, restart
- **Streaming Controls**: Start/stop stream, chat integration

### Conditional Layers
Advanced users can implement:
- **Auto layer switching** based on active application
- **Time-based functions** (e.g., automatic breaks)
- **Integration with other tools** (Discord, Slack notifications)

## Next Steps

After successful setup:
1. **Practice workflows** until muscle memory develops
2. **Customize for your content** (adjust for Java/Linux/DevOps focus)
3. **Add Layer 2 and 3** as needed for presentations and advanced features
4. **Consider mobile remote** integration for additional control
5. **Document your personal shortcuts** and share with team

## Support Resources

- **Vial Documentation**: https://get.vial.today/docs/
- **QMK Documentation**: https://docs.qmk.fm/
- **OBS Hotkey Reference**: https://obsproject.com/wiki/Sources-Guide
- **Community Support**: r/MechanicalKeyboards, OBS Discord

Your professional macropad setup is now ready for tutorial recording! 🎬