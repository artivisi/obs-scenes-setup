# Initial Setup Checklist

## Before Starting with Claude Code

### 1. Create GitHub Repository
- [ ] Create new repo: `obs-tutorial-setup`
- [ ] Enable GitHub Pages in Settings
- [ ] Set source to `/docs` folder
- [ ] Note your GitHub Pages URL: `https://yourusername.github.io/obs-tutorial-setup/`

### 2. Local Workspace Setup
- [ ] Clone repo to local machine
- [ ] Create folder structure (see README.md)
- [ ] Navigate to project folder in terminal
- [ ] Ensure Claude Code is installed and working

### 3. Required Information for Claude Code
When starting in Claude Code, provide:
- Your GitHub username (for Pages URL generation)
- Your preferred screen resolution (1920x1080, 2560x1440, etc.)
- Your brand colors/theme preferences
- Specific programming languages you'll be teaching

### 4. Hardware Information
- [ ] Confirm 3x3 macropad model/firmware type
- [ ] Note which potentiometer controls you want (volume, opacity, etc.)
- [ ] Android device model for remote control testing

## What Claude Code Should Build First

### Phase 1: Basic Overlays
1. **talking-head.html** - Simple centered layout
2. **code-demo.html** - Split screen with webcam
3. **screen-only.html** - Full screen capture
4. **main.css** - Shared styling and themes

### Phase 2: Scene Configuration
1. **programming-tutorial.json** - OBS scene collection
2. **Basic setup script** - Import scenes into OBS

### Phase 3: Control Systems
1. **manual-control.lua** - Priority manual switching
2. **Macropad configuration** - QMK keymap
3. **Mobile remote** - Simple web interface

### Phase 4: Automation (Optional)
1. **auto-scene-switcher.lua** - Smart suggestions
2. **Advanced remote features**
3. **Setup automation scripts**

## Files to Create in This Session

Tell Claude Code to start with these files:
1. `docs/overlays/talking-head.html`
2. `docs/overlays/css/main.css`
3. `docs/index.html` (preview page)
4. `scene-collections/programming-tutorial.json`
5. `scripts/manual-control.lua`

## Testing Workflow
1. Create overlays in `docs/overlays/`
2. Test locally with `file://` URLs in OBS
3. Push to GitHub for Pages hosting
4. Update OBS to use GitHub Pages URLs
5. Test scene switching and controls

## Important Notes for Claude Code
- Focus on **manual control first**, automation second
- Use **modern CSS Grid/Flexbox** for layouts
- Make everything **responsive** for different screen sizes
- Keep overlays **simple and clean** - programming tutorials need clarity
- **Test frequently** in OBS Browser Sources during development

Ready to start! Run `claude-code` in your project directory and reference these files.