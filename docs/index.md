---
layout: default
title: OBS Scenes Setup - Professional Streaming Overlays
---

# OBS Scenes Setup

## Professional Streaming Overlays for Educational Content

Transform your OBS Studio setup with professional, dynamic overlays designed specifically for programming tutorials, workshops, and technical education. No coding required - just add our overlay URLs to your OBS Browser Sources.

<div style="text-align: center; margin: 40px 0;">
  <a href="#quick-start" class="button">Quick Start</a>
  <a href="#scenes-gallery" class="button">View Scenes</a>
  <a href="https://github.com/artivisi/obs-scenes-setup" class="button">GitHub Repo</a>
</div>

---

## 🚀 Quick Start {#quick-start}

### Step 1: Open OBS Studio
Ensure you have OBS Studio 28+ installed with Browser Source support.

### Step 2: Create a New Scene
- Right-click in the Scenes box
- Select "Add" → Name your scene (e.g., "Intro")

### Step 3: Add Browser Source
- Right-click in Sources → Add → Browser
- Configure with these settings:
  - **URL**: Copy from the [overlay URLs](#overlay-urls) below
  - **Width**: 1920
  - **Height**: 1080
  - **FPS**: 30

### Step 4: Add Your Content
- For camera scenes: Add Video Capture Device
- For screen scenes: Add Display/Window Capture
- Position sources according to the scene layout

---

## 📺 Scenes Gallery {#scenes-gallery}

### 🎬 Intro Scene
**Purpose**: Professional opening while attendees join  
**Features**: Event title, instructor info, animated backgrounds, countdown timer  
**Best For**: Session start, waiting for participants

<div class="scene-preview">
  <img src="assets/preview/intro-scene.png" alt="Intro Scene Preview" />
</div>

### 👤 Talking Head
**Purpose**: Full presenter focus with identification  
**Features**: Name/title overlay, company branding  
**Best For**: Introductions, explanations, Q&A sessions

<div class="scene-preview">
  <img src="assets/preview/talking-head.png" alt="Talking Head Preview" />
</div>

### 📊 50:50 Presentation
**Purpose**: Balanced view of slides and presenter  
**Features**: Screen sharing with camera overlay (top-center)  
**Camera Position**: 75% right, full height, 25% cropped sides  
**Best For**: PowerPoint, Keynote, slide presentations

<div class="scene-preview">
  <img src="assets/preview/presentation.png" alt="Presentation Preview" />
</div>

### 💻 Code Demo
**Purpose**: Live coding with presenter visibility  
**Features**: Full screen share, PiP camera (bottom-right)  
**Camera Size**: 25% scale  
**Best For**: IDE demos, terminal sessions, debugging

<div class="scene-preview">
  <img src="assets/preview/code-demo.png" alt="Code Demo Preview" />
</div>

### 🖥️ Screen Only
**Purpose**: Maximum screen visibility  
**Features**: Minimal overlay, topic indicator  
**Best For**: Detailed code review, documentation reading

<div class="scene-preview">
  <img src="assets/preview/screen-only.png" alt="Screen Only Preview" />
</div>

### 📺 BRB / Technical
**Purpose**: Professional break screen  
**Features**: Animated elements, status message  
**Best For**: Breaks, technical issues, scene transitions

<div class="scene-preview">
  <img src="assets/preview/brb.png" alt="BRB Preview" />
</div>

### 🎯 Outro Scene
**Purpose**: Professional session conclusion  
**Features**: Topics covered, social links, call-to-action  
**Best For**: Session end, networking info, next steps

<div class="scene-preview">
  <img src="assets/preview/outro.png" alt="Outro Preview" />
</div>

---

## 🔗 Overlay URLs {#overlay-urls}

Copy these URLs directly into your OBS Browser Sources:

### Production Overlays (Stable)
```
https://artivisi.com/obs-scenes-setup/overlays/intro.html
https://artivisi.com/obs-scenes-setup/overlays/talking-head.html
https://artivisi.com/obs-scenes-setup/overlays/presentation.html
https://artivisi.com/obs-scenes-setup/overlays/code-demo.html
https://artivisi.com/obs-scenes-setup/overlays/screen-only.html
https://artivisi.com/obs-scenes-setup/overlays/brb.html
https://artivisi.com/obs-scenes-setup/overlays/outro.html
```

### Beta Overlays (Latest Features)
```
https://artivisi.com/obs-scenes-setup/beta/intro.html
https://artivisi.com/obs-scenes-setup/beta/talking-head.html
https://artivisi.com/obs-scenes-setup/beta/presentation.html
https://artivisi.com/obs-scenes-setup/beta/code-demo.html
https://artivisi.com/obs-scenes-setup/beta/screen-only.html
https://artivisi.com/obs-scenes-setup/beta/brb.html
https://artivisi.com/obs-scenes-setup/beta/outro.html
```

---

## 📋 Complete OBS Setup Guide

### Creating the Full Scene Collection

#### 1. Intro Scene
1. Create new scene "🎬 Intro"
2. Add Browser Source with intro.html URL
3. No additional sources needed

#### 2. Talking Head Scene
1. Create new scene "👤 Talking Head"
2. Add Video Capture Device (your camera)
3. Right-click camera → Transform → Fit to Screen
4. Add Browser Source with talking-head.html URL
5. Ensure Browser Source is above camera in sources list

#### 3. 50:50 Presentation Scene
1. Create new scene "📊 Presentation"
2. Add Display/Window Capture (for slides)
3. Add Video Capture Device (your camera)
4. Transform camera:
   - Position: X=1440, Y=0
   - Size: 960x1080
   - Crop: Left=480, Right=480
5. Add Browser Source with presentation.html URL on top

#### 4. Code Demo Scene
1. Create new scene "💻 Code Demo"
2. Add Window Capture (your IDE/terminal)
3. Add Video Capture Device (your camera)
4. Transform camera:
   - Position: Bottom-right corner
   - Scale to 25% (480x270)
5. Add Browser Source with code-demo.html URL on top

#### 5. Screen Only Scene
1. Create new scene "🖥️ Screen Only"
2. Add Display/Window Capture
3. Add Browser Source with screen-only.html URL

#### 6. BRB Scene
1. Create new scene "📺 BRB"
2. Add Browser Source with brb.html URL
3. No additional sources needed

#### 7. Outro Scene
1. Create new scene "🎯 Outro"
2. Add Browser Source with outro.html URL
3. No additional sources needed

---

## ⚙️ Advanced Configuration

### Custom Branding

While the online overlays use default branding, you can customize them by:

1. **Fork the Repository**: [GitHub Repo](https://github.com/artivisi/obs-scenes-setup)
2. **Edit Configuration**: Modify `resources/event.yaml`
3. **Generate Custom Overlays**: Run the generation scripts
4. **Host on GitHub Pages**: Enable Pages in your fork
5. **Use Your URLs**: Replace artivisi.com with your GitHub Pages URL

### Browser Source Settings

#### Recommended Settings
- **Width**: 1920
- **Height**: 1080
- **FPS**: 30
- **CSS**: Leave empty (styles included in overlays)
- **Shutdown when not visible**: ✓ Checked
- **Refresh when scene becomes active**: ✓ Checked

#### Troubleshooting Overlays
- **Not Loading?** Check internet connection and URL
- **Wrong Size?** Ensure 1920x1080 resolution
- **Not Updating?** Right-click source → Refresh
- **Performance Issues?** Reduce FPS to 24 or enable hardware acceleration

### Hotkey Configuration

Set up scene switching hotkeys for smooth transitions:

1. File → Settings → Hotkeys
2. Recommended setup:
   - **F1**: Intro Scene
   - **F2**: Talking Head
   - **F3**: Presentation
   - **F4**: Code Demo
   - **F5**: Screen Only
   - **F6**: BRB
   - **F7**: Outro

---

## 🎨 Customization Options

### For Developers

Clone and customize the overlays:

```bash
# Clone repository
git clone https://github.com/artivisi/obs-scenes-setup.git
cd obs-scenes-setup

# Edit configuration
nano resources/event.yaml

# Generate custom overlays
python scripts/generate-scenes.py resources/event.yaml --output my-overlays/

# Serve locally for testing
python scripts/serve-scenes.py my-overlays/
```

### Configuration Options

```yaml
event:
  title: "Your Workshop Title"
  tagline: "Workshop Description"

instructor:
  name: "Your Name"
  title: "Your Title"

branding:
  company_name: "Your Company"
  website: "yourwebsite.com"
  primary_color: "#2e3192"
  accent_color: "#58c034"

session:
  current_topic: "Current Topic"
  start_time: "10:00 AM"
```

---

## 🤝 Community & Support

### Get Help
- [GitHub Issues](https://github.com/artivisi/obs-scenes-setup/issues)
- [Discussions](https://github.com/artivisi/obs-scenes-setup/discussions)
- [Wiki](https://github.com/artivisi/obs-scenes-setup/wiki)

### Contribute
- Submit overlay themes
- Report bugs
- Suggest features
- Improve documentation

### Credits
Created by [ArtiVisi Intermedia](https://artivisi.com) for the educational community.

---

## 📊 Comparison Table

| Scene Type | Camera | Screen | Overlay | Best Use Case |
|------------|--------|--------|---------|---------------|
| Intro | ❌ | ❌ | ✅ | Session start |
| Talking Head | ✅ Full | ❌ | ✅ | Direct teaching |
| 50:50 Presentation | ✅ Overlay | ✅ Full | ✅ | Slide presentations |
| Code Demo | ✅ PiP | ✅ Full | ✅ | Live coding |
| Screen Only | ❌ | ✅ Full | ✅ | Detailed review |
| BRB | ❌ | ❌ | ✅ | Breaks |
| Outro | ❌ | ❌ | ✅ | Session end |

---

## 🚦 System Requirements

### Minimum Requirements
- OBS Studio 28.0+
- Browser Source plugin (included by default)
- Internet connection for overlay loading
- 1920x1080 canvas resolution

### Recommended Setup
- OBS Studio 30.0+
- Hardware encoding (NVENC/QuickSync)
- 16GB RAM
- Stable internet connection
- Secondary monitor for OBS control

---

## 📱 Mobile & Tablet Support

While primarily designed for desktop streaming, the overlays are responsive and can be adapted for:
- Vertical streaming (9:16)
- Square format (1:1)
- Custom resolutions

Adjust Browser Source dimensions accordingly.

---

## 🔄 Updates & Changelog

### Latest Version (v2.0)
- ✅ Added Intro Scene with countdown timer
- ✅ Added 50:50 Presentation layout
- ✅ Improved scene ordering
- ✅ Enhanced overlay animations
- ✅ Cross-platform compatibility

### Coming Soon
- 🔜 Theme selector
- 🔜 Real-time customization
- 🔜 StreamDeck integration
- 🔜 Animated transitions

---

<div style="text-align: center; margin-top: 60px; padding: 40px; background: linear-gradient(135deg, #2e3192, #58c034); color: white; border-radius: 10px;">
  <h2>Ready to Professional Streaming?</h2>
  <p>Get started with our overlays in less than 5 minutes</p>
  <a href="#quick-start" class="button-white">Start Now</a>
</div>

---

<footer style="text-align: center; margin-top: 40px; padding: 20px; border-top: 1px solid #eee;">
  <p>© 2024 ArtiVisi Intermedia | <a href="https://artivisi.com">artivisi.com</a></p>
  <p>Open Source under MIT License</p>
</footer>