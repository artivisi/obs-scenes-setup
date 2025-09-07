---
layout: default
title: Documentation - OBS Scenes Setup
---

# Complete Documentation

## Table of Contents
- [Installation](#installation)
- [Scene Layouts](#scene-layouts)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)
- [FAQ](#faq)

---

## Installation {#installation}

### Method 1: Online Overlays (Recommended)

No installation required! Simply use our hosted overlays directly in OBS:

1. Open OBS Studio
2. Add Browser Source
3. Use our overlay URLs
4. Configure your camera/screen captures

### Method 2: Self-Hosted

For complete control and customization:

#### Prerequisites
- Python 3.8+
- OBS Studio 28+ with WebSocket enabled
- Git

#### Installation Steps

```bash
# Clone repository
git clone https://github.com/artivisi/obs-scenes-setup.git
cd obs-scenes-setup

# Install dependencies
pip install obsws-python pystache pyyaml requests

# Or use the setup script
python scripts/setup/install-dependencies.py
```

#### Generate Custom Overlays

```bash
# Edit your event configuration
nano resources/event.yaml

# Generate overlays
python scripts/generate-scenes.py resources/event.yaml --output my-event/

# Start local server
python scripts/serve-scenes.py my-event/

# Inject into OBS
python scripts/inject-obs.py --collection my-event --webserver http://localhost:8080
```

---

## Scene Layouts {#scene-layouts}

### Scene Dimensions & Positioning

All scenes are designed for **1920x1080** resolution (16:9 aspect ratio).

#### Intro Scene Layout
- **Canvas**: Full screen gradient background
- **Title Position**: Center, 4.5rem font
- **Instructor Info**: Bottom center
- **Branding**: Bottom right
- **Status Badge**: Top left

#### Talking Head Layout
- **Camera**: Full screen (1920x1080)
- **Name Overlay**: Bottom left
- **Topic Banner**: Top right
- **Safe Zones**: 60px margins

#### 50:50 Presentation Layout
- **Screen**: Full screen base layer (1920x1080)
- **Camera Overlay**:
  - Position: X=960, Y=0 (top center)
  - Size: 960x1080 (after cropping)
  - Crop: 25% left, 25% right (480px each side)
- **Speaker Label**: Bottom right
- **Slide Info**: Top left

#### Code Demo Layout
- **Screen**: Full screen (1920x1080)
- **Camera PiP**:
  - Position: Bottom right (X=1400, Y=765)
  - Size: 480x270 (25% scale)
  - Border: 3px accent color
- **Topic Banner**: Top left

#### Screen Only Layout
- **Screen**: Full screen (1920x1080)
- **Minimal Overlay**: Topic bar at bottom
- **Status Indicator**: Top right

---

## Customization {#customization}

### Creating Custom Themes

#### 1. Theme Structure
```
themes/
├── my-theme/
│   ├── intro.mustache.html
│   ├── talking-head.mustache.html
│   ├── presentation.mustache.html
│   ├── code-demo.mustache.html
│   ├── screen-only.mustache.html
│   ├── brb.mustache.html
│   └── outro.mustache.html
```

#### 2. Available Variables

```mustache
{{event.title}}           - Event name
{{event.tagline}}        - Event description
{{event.date}}           - Event date
{{event.time}}           - Event time

{{instructor.name}}      - Presenter name
{{instructor.title}}     - Presenter title
{{instructor.bio}}       - Presenter biography
{{instructor.avatar}}    - Avatar URL

{{branding.company_name}} - Company name
{{branding.website}}      - Company website
{{branding.logo}}        - Logo URL
{{branding.primary_color}} - Primary hex color
{{branding.accent_color}}  - Accent hex color

{{session.current_topic}} - Current topic
{{session.start_time}}    - Session start
{{session.duration}}      - Session length
{{session.slide_number}}  - Current slide
{{session.slide_title}}   - Slide title
```

#### 3. CSS Customization

```css
/* Color Scheme */
:root {
  --primary: {{branding.primary_color}};
  --accent: {{branding.accent_color}};
  --text: #ffffff;
  --background: rgba(0,0,0,0.8);
}

/* Typography */
body {
  font-family: 'Your Font', system-ui;
  font-size: 16px;
  line-height: 1.6;
}

/* Animations */
@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}
```

### Dynamic Content Updates

#### Using JavaScript

```javascript
// Update time display
setInterval(() => {
  const now = new Date();
  document.getElementById('time').textContent = 
    now.toLocaleTimeString();
}, 1000);

// Countdown timer
let countdown = 10;
function startCountdown() {
  const timer = setInterval(() => {
    countdown--;
    document.getElementById('countdown').textContent = countdown;
    if (countdown <= 0) clearInterval(timer);
  }, 1000);
}
```

#### WebSocket Integration

```javascript
// Connect to custom WebSocket for real-time updates
const ws = new WebSocket('ws://localhost:8081');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  document.getElementById('topic').textContent = data.topic;
  document.getElementById('slide').textContent = data.slide;
};
```

---

## Troubleshooting {#troubleshooting}

### Common Issues

#### Browser Source Not Loading

**Problem**: Overlay appears blank or shows error
**Solutions**:
1. Check internet connection
2. Verify URL is correct
3. Try refreshing: Right-click source → Refresh
4. Check OBS logs: Help → Log Files → View Current Log

#### Wrong Overlay Size

**Problem**: Overlay doesn't fit screen
**Solutions**:
1. Set Browser Source to 1920x1080
2. Ensure OBS canvas is 1920x1080: Settings → Video
3. Reset transform: Right-click → Transform → Reset

#### Performance Issues

**Problem**: High CPU usage or lag
**Solutions**:
1. Reduce Browser Source FPS to 24
2. Enable hardware acceleration in OBS
3. Close unnecessary browser tabs
4. Use production overlays instead of beta

#### WebSocket Connection Failed

**Problem**: Can't inject scenes automatically
**Solutions**:
1. Enable WebSocket: Tools → WebSocket Server Settings
2. Check firewall settings
3. Verify port 4455 is open
4. Try without password first

### Platform-Specific Issues

#### Windows + WSL

```bash
# Get Windows IP from WSL
cat /etc/resolv.conf | grep nameserver

# Get WSL IP for webserver
hostname -I | awk '{print $1}'

# Test connection
curl http://[WINDOWS_IP]:4455
```

#### macOS

```bash
# Allow OBS through firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /Applications/OBS.app
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /Applications/OBS.app
```

#### Linux

```bash
# Install OBS dependencies
sudo apt-get install obs-studio
sudo apt-get install python3-pip
pip3 install obsws-python
```

---

## API Reference {#api-reference}

### Scene Generator API

```python
from scripts.generate_scenes import SceneGenerator

# Initialize generator
generator = SceneGenerator(
    resource_file="resources/event.yaml",
    output_dir="output/",
    theme="default"
)

# Generate scenes
scenes = generator.generate()
```

### OBS Injector API

```python
from scripts.inject_obs import OBSSceneInjector

# Initialize injector
injector = OBSSceneInjector(
    collection_name="my-workshop",
    webserver_url="http://localhost:8080",
    obs_host="localhost",
    obs_port=4455,
    obs_password=None
)

# Connect and inject
injector.connect()
injector.inject_scenes()
injector.disconnect()
```

### Webserver API

```python
from scripts.serve_scenes import SceneServer

# Start server
server = SceneServer(
    directory="my-overlays/",
    port=8080,
    host="0.0.0.0"
)
server.start()
```

---

## FAQ {#faq}

### General Questions

**Q: Can I use these overlays for commercial projects?**
A: Yes! The project is MIT licensed. Attribution appreciated but not required.

**Q: Do the overlays work with Streamlabs OBS?**
A: Yes, any streaming software that supports Browser Sources will work.

**Q: Can I customize colors without coding?**
A: Currently requires editing YAML configuration. GUI coming soon.

**Q: Are the overlays mobile-responsive?**
A: Designed for 1920x1080 but can be adapted for other resolutions.

### Technical Questions

**Q: How much bandwidth do overlays use?**
A: Minimal - approximately 50KB initial load, then cached.

**Q: Can I use local images in overlays?**
A: Yes, place images in assets/ folder and reference relatively.

**Q: Do overlays support transparency?**
A: Yes, all overlays have transparent backgrounds for layering.

**Q: Can I animate overlay elements?**
A: Yes, using CSS animations and JavaScript.

### Integration Questions

**Q: Does this work with StreamDeck?**
A: Yes, use StreamDeck's OBS integration to switch scenes.

**Q: Can I trigger overlay changes via API?**
A: Yes, using WebSocket connections or URL parameters.

**Q: Is RTMP streaming supported?**
A: OBS handles streaming; overlays work with any output method.

**Q: Can I use with multiple cameras?**
A: Yes, create additional source scenes for each camera.

---

## Advanced Topics

### Multi-Language Support

```yaml
# resources/event-es.yaml
event:
  title: "Taller de Desarrollo Web"
  tagline: "Construyendo APIs Modernas"
  
instructor:
  name: "Juan Pérez"
  title: "Desarrollador Senior"
```

### Custom Animations

```css
/* Slide transition */
.slide-in {
  animation: slideIn 0.5s ease-out;
}

/* Pulse effect */
.pulse {
  animation: pulse 2s infinite;
}

/* Fade sequence */
.fade-sequence > * {
  animation: fadeIn 0.5s ease-out forwards;
  animation-delay: calc(var(--index) * 0.1s);
}
```

### Webhook Integration

```javascript
// Send scene change notifications
function notifySceneChange(sceneName) {
  fetch('https://your-webhook.com/scene-change', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      scene: sceneName,
      timestamp: new Date().toISOString()
    })
  });
}
```

### Performance Optimization

```html
<!-- Preload critical resources -->
<link rel="preload" href="fonts/main.woff2" as="font" crossorigin>
<link rel="preload" href="css/critical.css" as="style">

<!-- Lazy load images -->
<img loading="lazy" src="assets/background.jpg" alt="Background">

<!-- Optimize animations -->
<style>
  .animated {
    will-change: transform;
    transform: translateZ(0);
  }
</style>
```

---

## Resources

### Official Links
- [GitHub Repository](https://github.com/artivisi/obs-scenes-setup)
- [Issue Tracker](https://github.com/artivisi/obs-scenes-setup/issues)
- [Discussions](https://github.com/artivisi/obs-scenes-setup/discussions)
- [Release Notes](https://github.com/artivisi/obs-scenes-setup/releases)

### Community Resources
- [OBS Forums Thread](#)
- [Reddit Community](#)
- [Discord Server](#)
- [YouTube Tutorials](#)

### Related Projects
- [OBS Studio](https://obsproject.com)
- [OBS WebSocket](https://github.com/obsproject/obs-websocket)
- [StreamDeck Plugin](https://github.com/Elgato/StreamDeck-OBS)

---

<footer style="text-align: center; margin-top: 40px; padding: 20px; border-top: 1px solid #eee;">
  <p>Last Updated: {{ site.time | date: '%B %d, %Y' }}</p>
  <p><a href="https://github.com/artivisi/obs-scenes-setup">View on GitHub</a> | <a href="/">Back to Home</a></p>
</footer>