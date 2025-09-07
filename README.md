# OBS Scenes Setup

## Project Description

Professional OBS Studio automation system for creating high-quality streaming setups for programming tutorials, workshops, and educational content. This project provides an Infrastructure-as-Code approach to OBS scene management, featuring dynamic HTML overlays, nested scene architecture to eliminate source duplication, and cross-platform compatibility. Perfect for instructors, content creators, and technical educators who want consistent, professional streaming setups without manual configuration.

## Software Requirements

### For Running Online Mode
- OBS Studio 28+ with Browser Source support
- Modern web browser (for accessing online overlays)
- Internet connection for overlay hosting

### For Running Offline Mode
- **All Platforms:**
  - OBS Studio 28+ with WebSocket Server enabled
  - Python 3.8+ 
  - Required Python packages: `obsws-python`, `pystache`, `pyyaml`, `requests`
  
- **Windows with WSL:**
  - WSL2 with Ubuntu/Debian
  - Windows Terminal (recommended)
  - OBS Studio running on Windows host
  
- **macOS:**
  - Homebrew (for Python installation)
  - OBS Studio for macOS
  
- **Ubuntu/Linux:**
  - OBS Studio (via apt, snap, or flatpak)
  - Python3-pip package

## Scenes Available

The system provides 7 professional scenes designed for educational content workflow:

### 🎬 **Intro Scene**
Professional opening scene featuring event title, instructor information, start time display, animated background elements, and optional countdown timer (press 'C' to activate). Perfect for session beginnings while attendees join.

### 👤 **Talking Head**
Full-screen camera view with instructor name and title overlay. Ideal for introductions, explanations, and direct audience engagement.

### 📊 **50:50 Presentation** 
Split-view scene showing slides/screen content with camera overlay positioned at top-center. Camera is cropped 25% from left and right for optimal framing. Perfect for PowerPoint presentations where both content and speaker are important.

### 💻 **Code Demo**
Screen sharing with picture-in-picture camera (25% scale) in bottom-right corner. Designed for live coding sessions, IDE demonstrations, and technical walkthroughs.

### 🖥️ **Screen Only**
Full-screen capture with minimal overlay showing current topic. Best for detailed code reviews, terminal sessions, or when maximum screen visibility is needed.

### 📺 **BRB / Technical**
Professional break screen with animated elements and status message. Use during breaks, technical difficulties, or scene transitions.

### 🎯 **Outro Scene**
Closing scene displaying topics covered, instructor information, social links, and company branding. Provides professional session conclusion with call-to-action elements.

## Offline Usage

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/obs-scenes-setup.git
cd obs-scenes-setup
```

### 2. Edit Text Resources
Edit the YAML configuration file to customize your event:
```bash
nano resources/event.yaml
```

Example configuration:
```yaml
event:
  title: "Python Web Development Workshop"
  tagline: "Building Modern APIs with FastAPI"
  
instructor:
  name: "Sarah Johnson"
  title: "Senior Python Developer"
  
branding:
  company_name: "ArtiVisi Intermedia"
  website: "artivisi.com"
  primary_color: "#2e3192"
  accent_color: "#58c034"
  
session:
  current_topic: "API Development"
  start_time: "10:00 AM"
```

### 3. Generate Scenes
```bash
python scripts/generate-scenes.py resources/event.yaml --output target/my-workshop
```

### 4. Start Webserver
```bash
python scripts/serve-scenes.py target/my-workshop/
# Server will start on http://0.0.0.0:8080
```

### 5. Inject to OBS

#### macOS/Ubuntu
```bash
# OBS must be running with WebSocket enabled
python scripts/inject-obs.py \
  --collection my-workshop \
  --webserver http://localhost:8080 \
  --obs-host localhost
```

#### Windows with WSL (Detailed Instructions)
1. **Enable OBS WebSocket (Windows):**
   - Open OBS Studio on Windows
   - Go to Tools → WebSocket Server Settings
   - Enable WebSocket Server
   - Note the port (default: 4455)
   - Set a password (optional)

2. **Find Windows Host IP from WSL:**
   ```bash
   # Get Windows host IP (WSL2)
   cat /etc/resolv.conf | grep nameserver | awk '{print $2}'
   # Example output: 172.29.128.1
   ```

3. **Find WSL IP for Webserver:**
   ```bash
   # Get WSL IP address
   ip addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'
   # Example output: 172.29.130.195
   ```

4. **Inject Scenes:**
   ```bash
   python scripts/inject-obs.py \
     --collection my-workshop \
     --webserver http://172.29.130.195:8080 \
     --obs-host 172.29.128.1
   ```

## Online Usage

For using pre-hosted scene collections without local setup:

### 1. Setup OBS Browser Sources

1. **Create Scene Collection:**
   - File → Scene Collection → New
   - Name it appropriately (e.g., "Workshop Scenes")

2. **Add Browser Sources for Each Scene:**
   
   For each scene type, create a new scene and add a Browser Source:
   - Right-click Sources → Add → Browser
   - Name: "Overlay"
   - URL: Use the online overlay URL
   - Width: 1920, Height: 1080
   - FPS: 30

3. **Online Overlay URLs (GitHub Pages Example):**
   ```
   https://yourusername.github.io/obs-scenes-setup/overlays/intro.html
   https://yourusername.github.io/obs-scenes-setup/overlays/talking-head.html
   https://yourusername.github.io/obs-scenes-setup/overlays/presentation.html
   https://yourusername.github.io/obs-scenes-setup/overlays/code-demo.html
   https://yourusername.github.io/obs-scenes-setup/overlays/screen-only.html
   https://yourusername.github.io/obs-scenes-setup/overlays/brb.html
   https://yourusername.github.io/obs-scenes-setup/overlays/outro.html
   ```

4. **Add Video Sources Manually:**
   - For camera scenes: Add Video Capture Device
   - For screen scenes: Add Display Capture or Window Capture
   - Position according to scene requirements

### 2. Using ArtiVisi's Public Overlays

Pre-configured overlays are available at:
```
https://artivisi.com/obs-scenes-setup/
```

Simply use these URLs in your Browser Sources for instant professional overlays.

## Extend

### Adding New Themes

1. **Create Theme Directory:**
   ```bash
   mkdir themes/my-theme
   ```

2. **Create Mustache Templates:**
   Create HTML templates with Mustache variables:
   ```html
   <!-- themes/my-theme/intro.mustache.html -->
   <!DOCTYPE html>
   <html>
   <head>
       <title>{{event.title}}</title>
       <style>
           /* Your custom styles */
           body {
               background: {{branding.primary_color}};
           }
       </style>
   </head>
   <body>
       <h1>{{event.title}}</h1>
       <p>{{instructor.name}}</p>
   </body>
   </html>
   ```

3. **Available Mustache Variables:**
   - `{{event.title}}` - Event name
   - `{{event.tagline}}` - Event description
   - `{{instructor.name}}` - Presenter name
   - `{{instructor.title}}` - Presenter title
   - `{{branding.company_name}}` - Company name
   - `{{branding.website}}` - Company website
   - `{{branding.primary_color}}` - Primary brand color
   - `{{branding.accent_color}}` - Accent color
   - `{{session.current_topic}}` - Current topic
   - `{{session.start_time}}` - Session start time

### Selecting/Activating Themes

1. **Via Command Line:**
   ```bash
   python scripts/generate-scenes.py resources/event.yaml \
     --output target/my-workshop \
     --theme my-theme
   ```

2. **Set Default Theme:**
   Edit `scripts/generate-scenes.py` and change the default theme:
   ```python
   DEFAULT_THEME = "my-theme"
   ```

3. **Theme Structure Requirements:**
   Each theme must include these templates:
   - `intro.mustache.html`
   - `talking-head.mustache.html`
   - `presentation.mustache.html`
   - `code-demo.mustache.html`
   - `screen-only.mustache.html`
   - `brb.mustache.html`
   - `outro.mustache.html`

## Architecture Overview

See [CLAUDE.md](CLAUDE.md) for detailed technical documentation and development guidelines.

## Contributing

1. Test changes with example configurations
2. Verify cross-platform compatibility (WSL, macOS, Linux)
3. Update documentation for any API changes
4. Test complete workflow: generate → serve → inject

## License

MIT License - Professional streaming setup automation for educational content.