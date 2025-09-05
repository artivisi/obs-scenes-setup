# Vial Macropad Keymap Reference

## Hardware Configuration
- **3x3 Matrix**: 9 programmable keys
- **Rotary Encoder**: 1 clickable encoder (position 9)
- **Firmware**: Vial-compatible
- **LED Support**: RGB underglow (if available)

## Key Mapping Strategy

### Physical Layout
```
[0,0] [0,1] [0,2]
[1,0] [1,1] [1,2]
[2,0] [2,1] [2,2]
      [ENC]
```

## Layer Definitions

### Layer 0: CORE CONTROLS (Default)
Primary recording and streaming controls

| Position | Physical Key | Function | OBS Hotkey | Description |
|----------|--------------|----------|------------|-------------|
| [0,0] | Top-Left | REC/STOP | Ctrl+R | Toggle recording |
| [0,1] | Top-Center | PAUSE | Ctrl+P | Pause recording |
| [0,2] | Top-Right | MUTE MIC | Ctrl+M | Toggle microphone |
| [1,0] | Mid-Left | SCENE- | Page Up | Previous scene |
| [1,1] | Mid-Center | SCENE+ | Page Down | Next scene |
| [1,2] | Mid-Right | MUTE ALL | Ctrl+Shift+M | Mute all audio |
| [2,0] | Bottom-Left | MARKER | Ctrl+K | Add chapter marker |
| [2,1] | Bottom-Center | SCREEN | F4 | Screen-only scene |
| [2,2] | Bottom-Right | PANIC | F5 | Emergency BRB scene |
| ENC | Encoder Click | LAYER | - | Cycle layers |
| ENC | Encoder Rotate | VOLUME | - | Master volume |

### Layer 1: TUTORIAL MODE
Optimized for programming tutorials

| Position | Function | OBS Hotkey | Description |
|----------|----------|------------|-------------|
| [0,0] | INTRO | F1 | Intro scene |
| [0,1] | TALKING | F2 | Talking head scene |
| [0,2] | CODE | F3 | Code + camera scene |
| [1,0] | SPLIT | Ctrl+1 | Split screen layout |
| [1,1] | TERMINAL | Ctrl+2 | Terminal focus |
| [1,2] | BROWSER | Ctrl+3 | Browser/docs scene |
| [2,0] | ZOOM IN | Ctrl+Plus | Increase font size |
| [2,1] | ZOOM OUT | Ctrl+Minus | Decrease font size |
| [2,2] | OUTRO | F6 | Outro scene |
| ENC Rotate | CAM SIZE | - | Adjust webcam PiP size |

### Layer 2: PRESENTATION MODE  
For slides, diagrams, and dual camera interviews

| Position | Function | OBS Hotkey | Description |
|----------|----------|------------|-------------|
| [0,0] | INTRO | F1 | Presentation intro |
| [0,1] | SLIDES | Alt+1 | Slide deck scene |
| [0,2] | DIAGRAM | Alt+2 | Whiteboard/diagram |
| [1,0] | PIP-TL | Alt+3 | Camera top-left |
| [1,1] | PIP-BR | Alt+4 | Camera bottom-right |
| [1,2] | NO CAM | Alt+5 | Remove camera |
| [2,0] | POINTER | Alt+6 | Toggle pointer tool |
| [2,1] | DRAW | Alt+7 | Drawing overlay |
| [2,2] | DUAL CAM | F7 | Dual camera interview |
| ENC Rotate | OPACITY | - | Annotation opacity |

### Layer 3: PRODUCTION MODE
Advanced streaming and production controls

| Position | Function | OBS Hotkey | Description |
|----------|----------|------------|-------------|
| [0,0] | TRANS- | Ctrl+Alt+1 | Previous transition |
| [0,1] | CUT | Ctrl+Alt+2 | Instant cut |
| [0,2] | TRANS+ | Ctrl+Alt+3 | Next transition |
| [1,0] | STUDIO | Ctrl+Alt+4 | Toggle Studio Mode |
| [1,1] | PREVIEW | Ctrl+Alt+5 | Focus preview |
| [1,2] | PROGRAM | Ctrl+Alt+6 | Focus program |
| [2,0] | LOWER 3 | Ctrl+Alt+7 | Lower third overlay |
| [2,1] | OVERLAY | Ctrl+Alt+8 | Info overlay toggle |
| [2,2] | BRB | F5 | Be Right Back |
| ENC Rotate | TRANS TIME | - | Transition duration |

## Vial Configuration Steps

### 1. Initial Setup
1. Flash Vial-compatible firmware to your macropad
2. Open Vial software and load the configuration
3. Import `vial-config.json` as base layout

### 2. Key Assignment
```
Layer 0 (Default):
Key 0: Ctrl+R (Start/Stop Recording)  
Key 1: Ctrl+P (Pause Recording)
Key 2: Ctrl+M (Toggle Microphone)
Key 3: Page Up (Previous Scene)
Key 4: Page Down (Next Scene)
Key 5: Ctrl+Shift+M (Mute All)
Key 6: Ctrl+K (Add Marker)
Key 7: F4 (Screen Only Scene)
Key 8: F5 (BRB/Panic Scene)
Encoder: Volume Control + Layer Switch
```

### 3. Layer Configuration
- **Layer Switch**: Encoder click cycles 0→1→2→3→0
- **Visual Feedback**: LED color changes per layer
- **Audio Feedback**: Key press confirmation sounds

### 4. Advanced Features
- **Tap Dance**: Double-tap encoder to return to Layer 0
- **Hold Actions**: Hold encoder while rotating for fine control
- **Combo Keys**: Certain key combinations for emergency functions

## OBS Studio Hotkey Setup

### Required OBS Hotkeys
Configure these hotkeys in OBS Studio (File → Settings → Hotkeys):

```
Recording Controls:
- Start/Stop Recording: Ctrl+R
- Pause Recording: Ctrl+P
- Add Chapter Marker: Ctrl+K

Audio Controls:
- Toggle Microphone: Ctrl+M  
- Mute All Audio: Ctrl+Shift+M

Scene Controls:
- Scene 1 (Intro): F1
- Scene 2 (Talking Head): F2
- Scene 3 (Code + Camera): F3
- Scene 4 (Screen Only): F4
- Scene 5 (BRB/Technical): F5
- Scene 6 (Outro): F6
- Scene 7 (Dual Camera): F7
- Previous Scene: Page Up
- Next Scene: Page Down

Tutorial Mode:
- Split Screen: Ctrl+1
- Terminal Focus: Ctrl+2
- Browser Scene: Ctrl+3
- Zoom In: Ctrl+Plus
- Zoom Out: Ctrl+Minus

Presentation Mode:
- Slide Deck: Alt+1
- Diagram Mode: Alt+2
- Camera Top-Left: Alt+3
- Camera Bottom-Right: Alt+4
- Hide Camera: Alt+5
- Pointer Tool: Alt+6
- Draw Mode: Alt+7

Production Mode:
- Previous Transition: Ctrl+Alt+1
- Cut Transition: Ctrl+Alt+2
- Next Transition: Ctrl+Alt+3
- Studio Mode: Ctrl+Alt+4
- Focus Preview: Ctrl+Alt+5
- Focus Program: Ctrl+Alt+6
- Lower Third: Ctrl+Alt+7
- Info Overlay: Ctrl+Alt+8
```

## Layer Visual Indicators

### LED Color Scheme (if supported)
- **Layer 0**: Red (Core Controls)
- **Layer 1**: Green (Tutorial Mode)
- **Layer 2**: Blue (Presentation Mode)  
- **Layer 3**: Yellow (Production Mode)

### OBS Overlay Indicator
Include a small overlay in OBS scenes showing:
- Current layer number and name
- Active button functions
- Recording status
- Audio levels

## Emergency Procedures

### Panic Button (Layer 0, Key 8)
1. Immediately mute all audio
2. Switch to "Technical Difficulties" scene
3. Pause recording (don't stop to avoid file corruption)
4. Log timestamp for editing

### Recovery Actions
- **Double-click Encoder**: Force return to Layer 0
- **Hold Key 8 + Encoder**: Emergency OBS restart
- **Triple-click Encoder**: Safe mode (basic scenes only)

## Testing Checklist

### Layer 0 Testing
- [ ] Recording start/stop works
- [ ] Pause functions correctly
- [ ] Microphone mute visual feedback
- [ ] Scene navigation smooth
- [ ] Master volume responsive
- [ ] Panic button accessible

### Layer 1 Testing  
- [ ] Scene hotkeys match OBS configuration
- [ ] Webcam size adjustment smooth
- [ ] Zoom controls work in target applications
- [ ] Layer indicator updates correctly

### Layer 2 Testing
- [ ] Presentation scenes configured
- [ ] Camera positioning accurate
- [ ] Annotation tools functional
- [ ] Dual camera mode operational

### Layer 3 Testing
- [ ] Studio mode toggle works
- [ ] Transition controls smooth
- [ ] Lower third overlay appears
- [ ] Advanced features accessible

### General Testing
- [ ] Layer switching responsive
- [ ] No key conflicts with applications
- [ ] LED indicators match layer state
- [ ] Encoder rotation smooth and accurate
- [ ] Emergency functions always accessible

## Firmware Compatibility

### Recommended Firmware
- **Vial**: Latest version (0.7+)
- **VIA Support**: Optional secondary compatibility
- **Custom Features**: RGB underglow, rotary encoder support

### Flashing Instructions
1. Put macropad in bootloader mode
2. Use QMK Toolbox or Vial to flash firmware
3. Load configuration from `vial-config.json`
4. Test all keys and encoder functions
5. Calibrate encoder sensitivity

## Troubleshooting

### Common Issues
- **Keys not responding**: Check firmware flash, verify USB connection
- **Wrong hotkeys**: Verify OBS hotkey configuration matches keymap
- **Encoder issues**: Adjust debounce settings, check physical connections
- **Layer switching**: Verify encoder click detection, check layer logic

### Debug Mode
Enable Vial debug mode to see:
- Key press events
- Layer changes  
- Encoder rotation values
- USB communication status

## Customization Notes

### Per-Content Adjustments
- **Java Tutorials**: Optimize Layer 1 for IDE layouts
- **Linux Admin**: Terminal-focused shortcuts in Layer 1
- **DevOps**: Diagram tools priority in Layer 2
- **Project Management**: Professional streaming in Layer 3

### Future Enhancements
- **Conditional Layers**: Auto-switch based on OBS scene
- **Timing Integration**: Show recording duration on macropad
- **Remote Integration**: Control from mobile device
- **Backup Configurations**: Save/load different keymap profiles