---
layout: default
title: Quick Reference - OBS Scenes Setup
---

# Quick Reference Guide

## 🎯 Overlay URLs

### Copy & Paste Ready

```
https://artivisi.com/obs-scenes-setup/overlays/intro.html
https://artivisi.com/obs-scenes-setup/overlays/talking-head.html
https://artivisi.com/obs-scenes-setup/overlays/presentation.html
https://artivisi.com/obs-scenes-setup/overlays/code-demo.html
https://artivisi.com/obs-scenes-setup/overlays/screen-only.html
https://artivisi.com/obs-scenes-setup/overlays/brb.html
https://artivisi.com/obs-scenes-setup/overlays/outro.html
```

---

## 📐 Scene Specifications

### Browser Source Settings
- **Resolution**: 1920 x 1080
- **FPS**: 30
- **CSS**: (leave empty)
- **✓** Shutdown when not visible
- **✓** Refresh when scene becomes active

### Camera Positions

#### Talking Head
- **Size**: Full screen (1920x1080)
- **Position**: (0, 0)
- **Scale**: 100%

#### 50:50 Presentation
- **Size**: 960x1080 (after crop)
- **Position**: (960, 0)
- **Crop**: L=480, R=480, T=0, B=0
- **Scale**: 100%

#### Code Demo PiP
- **Size**: 480x270
- **Position**: (1400, 765)
- **Scale**: 25%

---

## ⌨️ Recommended Hotkeys

| Key | Scene | Use Case |
|-----|-------|----------|
| F1 | 🎬 Intro | Starting session |
| F2 | 👤 Talking Head | Direct teaching |
| F3 | 📊 Presentation | Slides + speaker |
| F4 | 💻 Code Demo | Live coding |
| F5 | 🖥️ Screen Only | Detailed view |
| F6 | 📺 BRB | Taking a break |
| F7 | 🎯 Outro | Ending session |

---

## 🖥️ Command Line Quick Start

### Generate Scenes
```bash
python scripts/generate-scenes.py resources/event.yaml --output my-event/
```

### Start Server
```bash
python scripts/serve-scenes.py my-event/
```

### Inject to OBS
```bash
python scripts/inject-obs.py --collection my-event --webserver http://localhost:8080
```

### WSL to Windows
```bash
# Get IPs
WINDOWS_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
WSL_IP=$(hostname -I | awk '{print $1}')

# Inject
python scripts/inject-obs.py \
  --collection my-event \
  --webserver http://$WSL_IP:8080 \
  --obs-host $WINDOWS_IP
```

---

## 📝 YAML Configuration

### Minimal Config
```yaml
event:
  title: "My Workshop"
instructor:
  name: "Your Name"
branding:
  company_name: "Company"
  website: "site.com"
```

### Full Config
```yaml
event:
  title: "Python Web Development"
  tagline: "Building Modern APIs"
  date: "2024-03-15"
  time: "10:00 AM EST"

instructor:
  name: "Sarah Johnson"
  title: "Senior Developer"
  bio: "10 years experience"
  avatar: "https://example.com/avatar.jpg"

branding:
  company_name: "ArtiVisi"
  website: "artivisi.com"
  logo: "https://example.com/logo.png"
  primary_color: "#2e3192"
  accent_color: "#58c034"

session:
  current_topic: "API Development"
  start_time: "10:00 AM"
  duration: "2 hours"
  slide_number: 1
  slide_title: "Introduction"

social:
  github: "artivisi"
  twitter: "@artivisi"
  linkedin: "artivisi"
  youtube: "artivisi"
```

---

## 🎨 CSS Variables

Use these in custom themes:

```css
:root {
  /* Colors from YAML */
  --primary: {{branding.primary_color}};
  --accent: {{branding.accent_color}};
  
  /* Standard Palette */
  --text-primary: #ffffff;
  --text-secondary: rgba(255,255,255,0.8);
  --background: rgba(0,0,0,0.8);
  --overlay: rgba(255,255,255,0.1);
  
  /* Spacing */
  --margin: 30px;
  --padding: 20px;
  --radius: 8px;
  
  /* Typography */
  --font-main: 'Segoe UI', system-ui, sans-serif;
  --font-size-sm: 1.2rem;
  --font-size-md: 1.6rem;
  --font-size-lg: 2.4rem;
  --font-size-xl: 4rem;
}
```

---

## 🔧 Troubleshooting Checklist

### Overlay Not Showing?
- [ ] URL is correct and accessible
- [ ] Browser Source is 1920x1080
- [ ] Browser Source is on top layer
- [ ] Internet connection active
- [ ] Try refresh (right-click → Refresh)

### WebSocket Not Connecting?
- [ ] OBS WebSocket enabled
- [ ] Port 4455 accessible
- [ ] Correct host IP
- [ ] No password (or correct password)
- [ ] Firewall allows connection

### Performance Issues?
- [ ] Reduce FPS to 24
- [ ] Enable hardware acceleration
- [ ] Close other applications
- [ ] Use wired internet
- [ ] Update OBS Studio

---

## 📦 File Structure

```
obs-scenes-setup/
├── docs/                 # GitHub Pages
│   ├── index.md         # Homepage
│   ├── documentation.md # Full docs
│   └── overlays/        # Hosted overlays
├── themes/              # Overlay themes
│   └── default/         # Default theme
├── scripts/             # Python tools
│   ├── generate-scenes.py
│   ├── serve-scenes.py
│   └── inject-obs.py
├── resources/           # Configuration
│   └── event.yaml      # Event details
└── target/             # Generated output
```

---

## 🚀 Quick Commands

### Install Dependencies
```bash
pip install obsws-python pystache pyyaml requests
```

### Test Connection
```bash
python -c "from obsws_python import OBSReqClient; obs = OBSReqClient(host='localhost'); print('Connected!')"
```

### List Scenes
```bash
python scripts/obs/list-sources.py
```

### Generate with Theme
```bash
python scripts/generate-scenes.py resources/event.yaml --theme dark --output dark-theme/
```

---

## 📊 Scene Feature Matrix

| Feature | Intro | Talk | Present | Code | Screen | BRB | Outro |
|---------|-------|------|---------|------|--------|-----|-------|
| Camera | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Screen | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Overlay | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Animation | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Timer | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Social | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 🔗 Related Links

- [OBS Studio Download](https://obsproject.com)
- [OBS WebSocket Plugin](https://github.com/obsproject/obs-websocket)
- [Python Documentation](https://docs.python.org)
- [Mustache Templates](https://mustache.github.io)
- [GitHub Pages Setup](https://pages.github.com)

---

<div style="text-align: center; margin-top: 40px; padding: 20px; background: #f0f0f0; border-radius: 8px;">
  <h3>Need More Help?</h3>
  <p>Check the <a href="/documentation">full documentation</a> or <a href="https://github.com/artivisi/obs-scenes-setup/issues">open an issue</a></p>
</div>