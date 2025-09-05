# 📚 Documentation

This project maintains documentation in Markdown format for easy editing and version control. HTML versions are automatically generated for GitHub Pages.

## 🌐 View Documentation Online

**Documentation Site**: https://artivisi.github.io/obs-scenes-setup/

## Documentation Structure

### Source Files (Markdown)
The source documentation is maintained in Markdown for easy editing:
- `AUTOMATED_SETUP.md` - Automated OBS setup guide
- `OBS_SETUP_GUIDE.md` - Manual setup instructions
- `MACROPAD_DESIGN.md` - Macropad configuration
- `PROJECT_NOTES.md` - Technical architecture

### Generated HTML (GitHub Pages)
HTML versions are automatically generated via GitHub Actions:
- **🤖 [Automated Setup Guide](https://artivisi.github.io/obs-scenes-setup/guides/AUTOMATED_SETUP.html)**
- **🎛️ [Manual Setup Guide](https://artivisi.github.io/obs-scenes-setup/guides/OBS_SETUP_GUIDE.html)**
- **🎹 [Macropad Configuration](https://artivisi.github.io/obs-scenes-setup/guides/MACROPAD_DESIGN.html)**
- **📋 [Project Architecture](https://artivisi.github.io/obs-scenes-setup/guides/PROJECT_NOTES.html)**

### Live Overlay Previews
- **🎨 [All Overlays Gallery](https://artivisi.github.io/obs-scenes-setup/)** - Interactive preview gallery
- **👤 [Talking Head](https://artivisi.github.io/obs-scenes-setup/overlays/talking-head.html?test=true)**
- **💻 [Code Demo](https://artivisi.github.io/obs-scenes-setup/overlays/code-demo.html?test=true)**
- **🖥️ [Screen Only](https://artivisi.github.io/obs-scenes-setup/overlays/screen-only.html?test=true)**

## How It Works

1. **Edit Markdown** - Make changes to the `.md` files in the root directory
2. **Automatic Conversion** - GitHub Actions converts Markdown to HTML on push
3. **GitHub Pages** - Serves the HTML files from the `docs/` directory
4. **Live Updates** - Changes are automatically deployed to the documentation site

## For Contributors

### Editing Documentation
1. Edit the Markdown files directly (easier to maintain)
2. Push changes to GitHub
3. GitHub Actions automatically generates HTML
4. Changes appear on the documentation site within minutes

### Manual HTML Generation
If you need to generate HTML locally:
```bash
python scripts/convert-docs-to-html.py
```

### Benefits of This Approach
- ✅ **Single source of truth** - Markdown files are the canonical documentation
- ✅ **Easy editing** - Markdown is simpler to edit than HTML
- ✅ **Version control** - Track changes in readable Markdown format
- ✅ **Automatic deployment** - No manual HTML generation needed
- ✅ **Professional presentation** - HTML provides better formatting for users

Visit the documentation site for the best reading experience!