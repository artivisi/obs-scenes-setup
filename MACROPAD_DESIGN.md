# Macropad Configuration Design

## Hardware: 3x3 + Clickable Encoder
- **9 programmable buttons**
- **1 rotary encoder with push function**
- **Vial firmware** for easy reconfiguration

## Layer System Overview

Given your content focus (Java, Linux, DevOps, Software Engineering, Project Management), I recommend a **4-layer system** with the encoder click as layer switcher:

### Encoder Functions (Global Across All Layers)
- **Rotate**: Audio control (see details per layer)
- **Click**: Cycle through layers (0→1→2→3→0)
- **Hold + Rotate**: Fine adjustment (slower increments)

## Layer 0: CORE CONTROLS (Red LED indicator)
Primary recording/streaming controls - always return here for basics

```
[REC/STOP] [PAUSE]    [MUTE MIC]
[SCENE-]   [SCENE+]   [MUTE ALL]
[MARKER]   [SCREEN]   [PANIC]
```

**Button Functions:**
1. **REC/STOP**: Toggle recording (red when recording)
2. **PAUSE**: Pause/unpause recording
3. **MUTE MIC**: Toggle microphone (red when muted)
4. **SCENE-**: Previous scene in collection
5. **SCENE+**: Next scene in collection
6. **MUTE ALL**: Toggle all audio sources
7. **MARKER**: Add chapter marker/note
8. **SCREEN**: Quick toggle to screen-only view
9. **PANIC**: Kill all audio, switch to safe scene

**Encoder**: Master volume control

## Layer 1: TUTORIAL MODE (Green LED indicator)
Optimized for programming tutorials and demos

```
[INTRO]    [TALKING]  [CODE]
[SPLIT]    [TERMINAL] [BROWSER]
[ZOOM IN]  [ZOOM OUT] [OUTRO]
```

**Button Functions:**
1. **INTRO**: Intro scene with title card
2. **TALKING**: Talking head (full cam, no screen)
3. **CODE**: IDE/code editor focus with small cam
4. **SPLIT**: 50/50 split screen + cam
5. **TERMINAL**: Terminal focus scene
6. **BROWSER**: Browser/docs scene
7. **ZOOM IN**: Increase code zoom/font size
8. **ZOOM OUT**: Decrease code zoom/font size
9. **OUTRO**: Outro scene with credits

**Encoder**: Webcam opacity/size adjustment

## Layer 2: PRESENTATION MODE (Blue LED indicator)
For slides, diagrams, and architectural discussions

```
[INTRO]    [SLIDES]   [DIAGRAM]
[PIP-TL]   [PIP-BR]   [NO CAM]
[POINTER]  [DRAW]     [CLEAR]
```

**Button Functions:**
1. **INTRO**: Presentation intro
2. **SLIDES**: Slide deck with corner cam
3. **DIAGRAM**: Whiteboard/diagram tools
4. **PIP-TL**: Picture-in-picture top-left
5. **PIP-BR**: Picture-in-picture bottom-right
6. **NO CAM**: Remove camera completely
7. **POINTER**: Toggle pointer/highlight tool
8. **DRAW**: Toggle drawing overlay
9. **CLEAR**: Clear all annotations

**Encoder**: Slide annotation opacity

## Layer 3: PRODUCTION MODE (Yellow LED indicator)
Advanced controls for professional streaming

```
[TRANS-]   [CUT]      [TRANS+]
[STUDIO]   [PREVIEW]  [PROGRAM]
[LOWER 3]  [OVERLAY]  [BRB]
```

**Button Functions:**
1. **TRANS-**: Previous transition type
2. **CUT**: Instant cut transition
3. **TRANS+**: Next transition type
4. **STUDIO**: Toggle Studio Mode
5. **PREVIEW**: Focus preview window
6. **PROGRAM**: Focus program window
7. **LOWER 3**: Toggle lower third title
8. **OVERLAY**: Toggle info overlay
9. **BRB**: Be Right Back scene

**Encoder**: Transition duration adjustment

## Visual Feedback System

### OBS Overlay Indicator
- **Always visible** in OBS (not in recording)
- Shows current layer and button functions
- Color-coded by layer
- Semi-transparent overlay in corner

### Physical Feedback
- **LED colors** if your macropad supports it
- **Button press feedback** via OBS sound effects
- **Encoder detents** for precise control

## Implementation Priority

1. **Start with Layer 0** - Core controls only
2. **Add Layer 1** - Most useful for tutorials
3. **Implement visual feedback** - Critical for usability
4. **Add Layers 2 & 3** - As needed

## Hotkey Mapping Strategy

### OBS Hotkeys (to be mapped)
```
Layer 0:
- Ctrl+R: Start/Stop Recording
- Ctrl+P: Pause Recording
- Ctrl+M: Mute Mic
- F1-F9: Direct scene access
- Ctrl+Shift+M: Mute All
- Ctrl+K: Add Chapter Marker

Layer 1:
- Ctrl+1 through Ctrl+9: Tutorial scenes
- Ctrl+Plus/Minus: Zoom controls

Layer 2:
- Alt+1 through Alt+9: Presentation scenes

Layer 3:
- Ctrl+Alt+1 through 9: Production controls
```

## Vial Configuration Notes

### Layer Switching Logic
```c
// Encoder click cycles through layers
if (encoder_clicked) {
    current_layer = (current_layer + 1) % 4;
    update_led_color(layer_colors[current_layer]);
    show_layer_overlay(current_layer);
}
```

### Encoder Acceleration
- **Slow turn**: ±1 increment
- **Fast turn**: ±5 increments
- **Hold + turn**: ±0.1 increments (fine control)

## Quick Start Guide

### Initial Setup (Layer 0 only)
1. Map buttons 1, 3, 6 (REC, MUTE MIC, MUTE ALL)
2. Map encoder to master volume
3. Test basic recording workflow

### Progressive Enhancement
- Add scenes and map Scene+/- buttons
- Implement Layer 1 for tutorials
- Add visual feedback overlay
- Expand to other layers as needed

## Emergency Workflows

### Panic Button (Button 9, Layer 0)
1. Mute all audio sources
2. Switch to "Technical Difficulties" scene
3. Stop streaming (if active)
4. Log timestamp for debugging

### Quick Recovery
- **Double-click encoder**: Return to Layer 0
- **Hold Button 9**: Force restart OBS connection
- **Triple-click encoder**: Toggle safe mode (basic scenes only)

## Content-Specific Optimizations

### Java Development
- Layer 1, Button 3: Optimized for IDE layout
- Pre-configured for IntelliJ IDEA window detection

### Linux Administration
- Layer 1, Button 5: Terminal-focused scene
- Automatic font size adjustment for readability

### DevOps Workflows
- Layer 2: Diagram tools for architecture
- Quick access to browser for documentation

### Project Management
- Layer 2: Presentation mode for slides
- Layer 3: Professional streaming for meetings

## Testing Checklist

- [ ] Each button responds correctly
- [ ] Encoder rotation smooth and predictable
- [ ] Layer switching visual feedback works
- [ ] Emergency controls accessible from all layers
- [ ] Audio controls independent per layer
- [ ] Scene transitions smooth
- [ ] Hotkeys don't conflict with applications