# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an OBS Studio automation system for creating professional programming tutorial setups. The system provides Infrastructure-as-Code approach to OBS scene creation with automated overlay generation, cross-platform compatibility, and hardware integration.

## Key Commands

### Main Workflow Commands
```bash
# Quick setup with defaults (2-3 minutes)
python scripts/workflow.py --quick

# Custom event setup with interactive configuration
python scripts/workflow.py --event my-workshop

# Use predefined template
python scripts/workflow.py --event my-workshop --template java

# Environment setup only
python scripts/workflow.py --setup
```

### Direct OBS Scene Creation
```bash
# Create live OBS scenes with online overlays
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi

# Create with custom/local overlays
python scripts/obs/auto-scene-creator.py --create-live --offline --overlay-path custom-overlays

# Generate JSON scene collection (no WebSocket needed)
python scripts/obs/auto-scene-creator.py --generate-json --output scenes.json
```

### Overlay Generation
```bash
# Generate event-specific overlays
python scripts/tools/populate-overlays.py --template python-workshop --preview

# Custom overlay generation
python scripts/tools/populate-overlays.py --config event-config.json --output my-overlays/
```

### Development and Testing
```bash
# Install dependencies
python scripts/setup/install-dependencies.py

# List OBS sources (debugging)
python scripts/obs/list-sources.py

# Fix overlay URLs in existing scenes
python scripts/obs/fix-overlay-urls.py
```

## Architecture

### Core Components

**Workflow System** (`scripts/workflow.py`):
- Master orchestration script that manages the complete workflow
- Handles environment setup → event configuration → overlay generation → OBS integration
- Supports quick setup, custom events, and template-based workflows

**OBS Integration** (`scripts/obs/auto-scene-creator.py`):
- Creates 7 professional scene templates: talking-head, code-demo, screen-only, intro, outro, brb, dual-cam
- Automatic audio filter chain: noise suppression, compression, limiting
- Cross-platform device detection and WebSocket connectivity
- Supports both live scene creation and JSON export modes

**Overlay System** (`docs/overlays/`, `scripts/tools/populate-overlays.py`):
- HTML/CSS/JS based overlays replacing traditional PNG graphics
- Event-specific content generation from JSON templates
- GitHub Pages hosting with offline development support
- Template system for different content types (Java, Python, Linux, etc.)

**Utility Modules** (`scripts/utils/`):
- `obs_utils.py`: OBS WebSocket connection management with WSL auto-detection
- `scene_generator.py`: Scene template definitions and layout management  
- `text_customizer.py`: Text processing and event content customization

### Network Architecture
- Automatic WSL/Windows bridge detection for cross-platform development
- Local HTTP server for overlay hosting during development
- GitHub Pages integration for production overlay hosting
- Smart IP detection for consistent cross-platform behavior

### Hardware Integration
- USB camera and audio device auto-detection
- Support for capture cards and professional cameras
- Macropad integration via Vial firmware (optional)
- Cross-platform audio processing chain

## Development Guidelines

### File Structure Conventions
- All scripts are in `scripts/` with clear subdirectory organization
- Overlay templates in `docs/overlays/` with GitHub Pages deployment
- Event configurations and templates in `docs/resources/`
- Generated content uses timestamps for uniqueness

### Python Dependencies
The system automatically installs these key dependencies:
- `obsws-python`: OBS WebSocket communication
- `pathlib`: Cross-platform path handling
- Standard library modules (no external framework dependencies)

### Cross-Platform Considerations
- WSL environment auto-detection for Windows/Linux hybrid setups
- Platform-specific device enumeration for cameras and audio
- Network interface detection for local overlay serving
- Path handling works consistently across macOS, Windows, Linux

### Error Handling Patterns
- Graceful fallback to JSON mode if OBS WebSocket unavailable  
- Default overlay fallback if custom generation fails
- Comprehensive device detection with fallback options
- Clear error messages with suggested resolution steps

## Common Tasks

### Adding New Scene Templates
1. Define scene layout in `scripts/utils/scene_generator.py`
2. Create corresponding HTML overlay in `docs/overlays/`
3. Update scene creation logic in `scripts/obs/auto-scene-creator.py`

### Creating New Event Templates
1. Add JSON template in `docs/resources/templates/`
2. Test overlay generation with `populate-overlays.py`
3. Verify end-to-end workflow with `workflow.py`

### Debugging OBS Issues
- Use `scripts/obs/list-sources.py` to examine current OBS setup
- Check WebSocket connectivity with connection test utilities
- Verify overlay URLs are accessible via browser
- Use `--generate-json` mode for offline debugging

## Important Notes

- OBS WebSocket must be enabled (Tools → WebSocket Server Settings)
- The system creates 7 standard scenes with professional audio processing
- Overlays are hosted via GitHub Pages at `https://artivisi.com/obs-scenes-setup/`
- All automation preserves existing OBS scenes and settings
- Custom overlays are generated with timestamp-based directories to avoid conflicts