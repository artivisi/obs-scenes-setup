# Project Context and Requirements

## User Background
- Experienced OBS user (used PNG overlays in the past)
- Creating programming tutorials (recording + possible streaming/video calls)
- Wants modern, maintainable, code-based approach
- Budget-conscious (avoiding Stream Deck, using 3x3 macropad)

## Key Requirements Discussed

### Scene Layouts Needed
1. **Talking Head** - Centered presenter, minimal overlays
2. **Code + Webcam** - Split layout for programming demos
3. **Screen Only** - Full screen capture for detailed code work
4. **Intro Scene** - Professional opening with branding
5. **Outro Scene** - Closing sequence

### Control Philosophy
- **Manual control is primary** - User wants full control
- **Auto-switching is optional** - Helpful suggestions, not forced changes
- **Manual override always wins** - If user switches manually, stay in manual mode
- **Hybrid mode** - Show suggestions but don't auto-switch

### Technical Preferences
- **Infrastructure as Code** - Everything version controlled
- **GitHub Pages hosting** - For overlay files (user confirmed no security concerns)
- **No expensive hardware** - 3x3 macropad instead of Stream Deck
- **Modern overlay approach** - HTML/CSS/JS instead of PNG with cutouts

### Hardware Context
- **3x3 Macropad** with potentiometers
  - 9 buttons for scene switching and controls
  - 3 potentiometers for volume/opacity/etc
  - Uses QMK firmware
- **Android device** for secondary remote control
- **No Stream Deck** (too expensive)

### Auto-Switching Features (Optional)
- **Application-based** - Switch scenes based on active window (VS Code, browser, terminal)
- **Audio-level based** - Switch based on speaking vs silence
- **Timer-based** - Auto intro/outro sequences
- **All with manual override** - Stop auto-switching when user takes manual control

### Scene Switching Logic
```
Manual Mode: Only respond to manual inputs
Auto Mode: Automatic switching based on triggers
Hybrid Mode: Show suggestions but don't auto-switch
```

### Control Methods Priority
1. **OBS Hotkeys** - Always work (F1-F5 for scenes)
2. **Macropad** - Physical buttons for main controls
3. **Android Remote** - Web interface or Touch Portal app
4. **Emergency Manual Override** - Force return to manual control

### Macropad Layout Concept (Multi-Layer with Visual Reference)

#### Layer 0 (Base) - Core Controls
```
[Record]   [Stop]     [Mute]
[Prev]     [Next]     [Layer+]
[Vol-]     [Vol+]     [Emergency]
```

#### Layer 1 - Solo Programming Mode
```
[Intro]    [Talk]     [Code]
[Split]    [Screen]   [Focus]
[Cam+]     [Cam-]     [Auto]
```

#### Layer 2 - Discussion/Interview Mode
```
[Intro]    [Dual]     [Focus A]
[Focus B]  [A+Screen] [B+Screen]
[Shared]   [Podcast]  [Balance]
```

#### Layer 3 - Zoom/Remote Mode
```
[Intro]    [Present]  [Moderate]
[Zoom]     [Grid]     [Screen]
[Local]    [Remote]   [Share]
```

#### Visual Reference System
- **OBS overlay** showing current layer and button functions
- **Color-coded functions** for quick recognition
- **Always visible** in OBS preview (not recorded)
- **Auto-updates** when layer changes

### Technical Evolution Context
## Technical Evolution Context
- **Modern approach**: HTML/CSS browser sources with dynamic content
- **Benefits**: Responsive design, animations, real-time updates, version control

### File Organization
- **docs/** folder for GitHub Pages
- **scene-collections/** for OBS JSON exports
- **scripts/** for Lua automation and Python tools
- **All version controlled** with git

## Implementation Priority
1. Start with basic HTML/CSS overlays
2. Create scene collection configurations
3. Build manual control system
4. Add optional auto-switching features
5. Integrate macropad and mobile remote
6. Create setup/import automation

## Key Technical Notes
- Use CSS Grid/Flexbox for responsive layouts
- Browser sources for all overlays
- Local file:// URLs work but GitHub Pages preferred
- OBS WebSocket for advanced remote control
- Vial firmware for macropad configuration
- Touch Portal or custom web interface for mobile

## Hardware Setup Details

### Camera: Nikon ZFC + Cam Link 4K
- **Connection**: USB capture card to laptop
- **Device Name Pattern**: "*Cam Link*" or "Elgato Cam Link 4K"
- **Resolution**: 1920x1080 or 1080x1080 (square for better framing)
- **Format**: MJPEG or YUV422 (auto-detect)

### Microphone: Hollyland Lark M2
- **Connection**: USB soundcard to laptop
- **Device Name Pattern**: "*USB Audio*" or "Hollyland Lark M2"
- **Sample Rate**: 48kHz (video production standard)
- **Channels**: Mono or Stereo depending on receiver setup

### Laptops (Dual Setup)
- **Primary**: MacBook Pro M1 (macOS)
- **Secondary**: Dell Latitude 2-in-1 (Windows)
- **Challenge**: USB device addresses change between connections and platforms

### Macropad: 3x3 + 1 Potentiometer
- **Layout**: 9 buttons for scene switching and controls
- **Potentiometer**: Headphone/Monitor volume (most versatile)
- **Firmware**: Vial-compatible (GUI-based configuration)
- **Connection**: USB to laptop

## Device Management Strategy

### USB Connection Best Practices
- **Consistent USB ports**: Always use same ports for same devices
- **Connection order**: Camera first, then microphone
- **Device naming**: Use device name patterns, not USB paths
- **Fallback sources**: Built-in camera/mic as backup

### Cross-Platform Compatibility
- **Platform-specific profiles**: macbook-recording.ini, dell-recording.ini
- **Device detection scripts**: Auto-find Cam Link and USB audio
- **Shared scene layouts**: Same visual setup, different device configs
- **Automatic source switching**: Detect available devices and configure

### Device Detection Requirements
- **Camera detection**: Find "Cam Link" pattern in video devices
- **Audio detection**: Find USB audio device pattern
- **Platform detection**: macOS vs Windows device enumeration
- **Error handling**: Graceful fallback to built-in devices
- **Status reporting**: Show which devices are connected/missing

## Budget and Constraints
- Avoid expensive hardware (no Stream Deck)
- Use free tools and services (GitHub Pages, OBS, etc)
- Maximize flexibility and reusability
- Focus on maintainable, shareable solutions
- Handle device connectivity robustly across platforms