---
layout: default
title: OBS Scenes Setup - Professional Streaming Overlays
---

# OBS Scenes Setup

## Transform Your OBS Studio with Professional Overlays

Create stunning educational content with our complete OBS scene collection. Perfect for programming tutorials, workshops, webinars, and technical presentations.

<div style="text-align: center; margin: 40px 0;">
  <div style="margin-bottom: 20px;">
    <a href="downloads/" class="button" style="background: #dc3545; font-size: 1.4em; padding: 20px 50px; margin: 10px; display: inline-block;">📥 Download Scene Collection</a>
  </div>
  <div>
    <a href="#get-started" class="button" style="background: #28a745; font-size: 1.1em; padding: 12px 30px; margin: 8px; display: inline-block;">🚀 Get Started</a>
    <a href="#preview-scenes" class="button" style="padding: 12px 25px; margin: 8px; display: inline-block;">👁️ Preview Scenes</a>
    <a href="https://github.com/artivisi/obs-scenes-setup" class="button" style="padding: 12px 25px; margin: 8px; display: inline-block;">📦 GitHub</a>
  </div>
</div>

---

## ✨ What You Get

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0;">
  <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; color: #333;">
    <h3>🎬 7 Professional Scenes</h3>
    <p>Complete set including Intro, Outro, Presentation, Code Demo, and more</p>
  </div>
  <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; color: #333;">
    <h3>🎨 Modern Animations</h3>
    <p>Smooth transitions, animated backgrounds, and professional effects</p>
  </div>
  <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; color: #333;">
    <h3>⚡ Ready to Use</h3>
    <p>Pre-configured layouts, hotkeys (F1-F7), and perfect positioning</p>
  </div>
  <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; color: #333;">
    <h3>🔧 Fully Customizable</h3>
    <p>Edit text, colors, and branding to match your style</p>
  </div>
</div>

---

## 🚀 Get Started {#get-started}

Choose your setup method based on your technical comfort level:

### Option 0: Download Scene Collection (Fastest) ⭐

**Perfect for non-technical users who want everything ready in one click.**

1. **[📥 Download Scene Collection](downloads/)** - Get the complete ZIP package
2. **Extract files** to your desired folder  
3. **Import to OBS**: Scene Collection → Import → Select `scene-collection.json`
4. **Configure Browser Sources**: Update file paths to point to your extracted overlay files

✅ **No git required** • ✅ **No Python required** • ✅ **Works offline**

### Option 1: Use Our Hosted Overlays (Online)

Perfect if you just want to start streaming right away.

1. **Copy these URLs into OBS Browser Sources:**

```
https://artivisi.com/obs-scenes-setup/overlays/intro.html
https://artivisi.com/obs-scenes-setup/overlays/talking-head.html
https://artivisi.com/obs-scenes-setup/overlays/presentation.html
https://artivisi.com/obs-scenes-setup/overlays/code-demo.html
https://artivisi.com/obs-scenes-setup/overlays/screen-only.html
https://artivisi.com/obs-scenes-setup/overlays/brb.html
https://artivisi.com/obs-scenes-setup/overlays/outro.html
```

2. **Add to OBS:**
   - Create new scene in OBS
   - Add Browser Source
   - Paste URL, set to 1920x1080
   - Add your camera/screen capture as needed

### Option 2: Generate Your Own (Customizable)

For those who want to customize the overlays with their own branding.

```bash
# Clone and customize
git clone https://github.com/artivisi/obs-scenes-setup.git
cd obs-scenes-setup

# Edit your event details
nano resources/event.yaml

# Generate overlays
python scripts/generate-scenes.py resources/event.yaml --output my-event/

# Serve locally
python scripts/serve-scenes.py my-event/

# Auto-inject to OBS (optional)
python scripts/inject-obs.py --collection my-event --webserver http://localhost:8080
```

---

## 👁️ Preview Scenes {#preview-scenes}

Click any scene to see a live preview of how it looks:

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0;">
  
  <div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
    <a href="previews/intro-preview.html" target="_blank">
      <div style="background: linear-gradient(135deg, #667eea, #764ba2); height: 150px; display: flex; align-items: center; justify-content: center; color: white; font-size: 2em;">
        🎬 Intro
      </div>
    </a>
    <div style="padding: 15px;">
      <strong>Intro Scene</strong><br>
      Professional opening with countdown timer
    </div>
  </div>

  <div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
    <a href="previews/talking-head-preview.html" target="_blank">
      <div style="background: linear-gradient(135deg, #667eea, #764ba2); height: 150px; display: flex; align-items: center; justify-content: center; color: white; font-size: 2em;">
        👤 Talking Head
      </div>
    </a>
    <div style="padding: 15px;">
      <strong>Talking Head</strong><br>
      Full camera with name overlay
    </div>
  </div>

  <div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
    <a href="previews/presentation-preview.html" target="_blank">
      <div style="background: linear-gradient(135deg, #667eea, #764ba2); height: 150px; display: flex; align-items: center; justify-content: center; color: white; font-size: 2em;">
        📊 50:50
      </div>
    </a>
    <div style="padding: 15px;">
      <strong>Presentation</strong><br>
      Screen + camera side by side
    </div>
  </div>

  <div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
    <a href="previews/code-demo-preview.html" target="_blank">
      <div style="background: linear-gradient(135deg, #667eea, #764ba2); height: 150px; display: flex; align-items: center; justify-content: center; color: white; font-size: 2em;">
        💻 Code Demo
      </div>
    </a>
    <div style="padding: 15px;">
      <strong>Code Demo</strong><br>
      Screen with PiP camera
    </div>
  </div>

  <div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
    <a href="previews/screen-only-preview.html" target="_blank">
      <div style="background: linear-gradient(135deg, #667eea, #764ba2); height: 150px; display: flex; align-items: center; justify-content: center; color: white; font-size: 2em;">
        🖥️ Screen
      </div>
    </a>
    <div style="padding: 15px;">
      <strong>Screen Only</strong><br>
      Full screen with minimal overlay
    </div>
  </div>

  <div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
    <a href="previews/brb-preview.html" target="_blank">
      <div style="background: linear-gradient(135deg, #667eea, #764ba2); height: 150px; display: flex; align-items: center; justify-content: center; color: white; font-size: 2em;">
        📺 BRB
      </div>
    </a>
    <div style="padding: 15px;">
      <strong>Be Right Back</strong><br>
      Animated break screen
    </div>
  </div>

  <div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
    <a href="previews/outro-preview.html" target="_blank">
      <div style="background: linear-gradient(135deg, #667eea, #764ba2); height: 150px; display: flex; align-items: center; justify-content: center; color: white; font-size: 2em;">
        🎯 Outro
      </div>
    </a>
    <div style="padding: 15px;">
      <strong>Outro Scene</strong><br>
      Thank you with social links
    </div>
  </div>

</div>

---

## 🎯 Perfect For

- 📚 **Programming Tutorials** - Live coding sessions with professional presentation
- 🎓 **Educational Workshops** - Engaging overlays for teaching and training
- 💼 **Technical Presentations** - Professional look for webinars and meetings
- 🎮 **Code Streaming** - Stand out on Twitch/YouTube with polished overlays
- 📹 **Course Recording** - Consistent branding for online courses

---

## 🛠️ Technical Details

### Requirements
- **OBS Studio 28.0+** with Browser Source plugin (included by default)
- **Resolution**: 1920x1080 (Full HD)
- **No coding required** for basic usage

### What's Included
- **7 HTML overlay files** with embedded CSS animations
- **Mustache templates** for customization
- **Python scripts** for automation (optional)
- **WebSocket integration** for advanced users
- **Full documentation** and examples

### Customization Options
- **Event details**: Title, instructor name, company branding
- **Colors**: Primary and accent colors
- **Content**: Session topics, social links
- **Layout**: Camera positions and scaling

---

## 📖 Documentation

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 30px 0;">
  <a href="documentation" style="background: #f8f9fa; padding: 20px; border-radius: 8px; text-decoration: none; color: #333; display: block;">
    <strong>📚 Full Documentation</strong><br>
    Complete setup and customization guide
  </a>
  <a href="quick-reference" style="background: #f8f9fa; padding: 20px; border-radius: 8px; text-decoration: none; color: #333; display: block;">
    <strong>⚡ Quick Reference</strong><br>
    Copy-paste commands and URLs
  </a>
  <a href="https://github.com/artivisi/obs-scenes-setup" style="background: #f8f9fa; padding: 20px; border-radius: 8px; text-decoration: none; color: #333; display: block;">
    <strong>💻 Source Code</strong><br>
    Fork on GitHub
  </a>
  <a href="https://github.com/artivisi/obs-scenes-setup/issues" style="background: #f8f9fa; padding: 20px; border-radius: 8px; text-decoration: none; color: #333; display: block;">
    <strong>💬 Get Help</strong><br>
    Report issues or ask questions
  </a>
</div>

---

## 🚀 Advanced Features

### For Developers

If you're comfortable with code, unlock these advanced features:

- **Automated Scene Injection**: Use WebSocket to automatically create all scenes
- **Custom Themes**: Create your own visual themes with Mustache templates
- **CI/CD Integration**: GitHub Actions for automated overlay generation
- **Bulk Generation**: Create multiple event-specific overlays
- **API Integration**: Pull event data from external sources

```python
# Example: Auto-inject with custom branding
python scripts/inject-obs.py \
  --collection "My-Workshop" \
  --webserver http://localhost:8080 \
  --obs-host localhost
```

### Cross-Platform Support

Works seamlessly across all platforms:
- ✅ **Windows** (including WSL)
- ✅ **macOS** 
- ✅ **Linux** (Ubuntu, Fedora, etc.)

---

## 👥 Community

### Created By
**[ArtiVisi Intermedia](https://artivisi.com)**  
Delivering Solutions, Creating Values

### Contributing
We welcome contributions! Feel free to:
- Submit overlay themes
- Report bugs
- Suggest features
- Improve documentation

### License
Open source under MIT License

---

<div style="text-align: center; margin-top: 60px; padding: 40px; background: linear-gradient(135deg, #2e3192, #58c034); color: white; border-radius: 10px;">
  <h2>Ready to Level Up Your Streaming?</h2>
  <p style="font-size: 1.2em; margin: 20px 0;">Join hundreds of educators using our professional overlays</p>
  <a href="#get-started" class="button" style="background: white; color: #2e3192; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">Get Started Now →</a>
</div>