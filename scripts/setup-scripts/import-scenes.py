#!/usr/bin/env python3
"""
OBS Scene Collection Import Script for Artivisi Programming Tutorials

This script helps automate the import and configuration of the OBS scene collection.
Run this after setting up OBS Studio to quickly configure your scenes with the
correct GitHub Pages URLs.

Requirements:
- OBS Studio installed
- Python 3.6+
- obs-websocket plugin (optional, for advanced features)

Usage:
    python import-scenes.py --github-username YOUR_USERNAME
    
Example:
    python import-scenes.py --github-username artivisi
"""

import json
import argparse
import sys
import os
import re
from pathlib import Path
from urllib.parse import urljoin

def validate_github_username(username):
    """Validate GitHub username format"""
    if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]){0,38}$', username):
        raise ValueError("Invalid GitHub username format")
    return username

def update_scene_collection(template_path, output_path, github_username, github_pages_url):
    """Update scene collection template with actual GitHub Pages URLs"""
    
    print(f"📖 Reading template from: {template_path}")
    
    with open(template_path, 'r') as f:
        scene_collection = json.load(f)
    
    # Update browser source URLs
    overlay_mappings = {
        'Intro Overlay': 'intro.html',
        'Talking Head Overlay': 'talking-head.html', 
        'Code Demo Overlay': 'code-demo.html',
        'Screen Only Overlay': 'screen-only.html',
        'BRB Overlay': 'brb.html',
        'Outro Overlay': 'outro.html'
    }
    
    updated_sources = 0
    
    for source in scene_collection.get('sources', []):
        if source.get('name') in overlay_mappings:
            overlay_file = overlay_mappings[source['name']]
            new_url = urljoin(github_pages_url, f'overlays/{overlay_file}')
            
            # Update the URL in settings
            if 'settings' in source and 'url' in source['settings']:
                old_url = source['settings']['url']
                source['settings']['url'] = new_url
                print(f"✅ Updated {source['name']}: {old_url} → {new_url}")
                updated_sources += 1
    
    # Update scene collection name
    original_name = scene_collection.get('name', 'Programming Tutorials - Artivisi')
    scene_collection['name'] = f"Programming Tutorials - {github_username}"
    
    print(f"📝 Updated scene collection name: {original_name} → {scene_collection['name']}")
    print(f"🔄 Updated {updated_sources} browser sources")
    
    # Write updated scene collection
    print(f"💾 Writing updated scene collection to: {output_path}")
    
    with open(output_path, 'w') as f:
        json.dump(scene_collection, f, indent=2)
    
    return scene_collection

def generate_import_instructions(github_pages_url, output_path):
    """Generate step-by-step import instructions"""
    
    instructions = f"""
🎬 OBS Scene Collection Import Instructions

Your scene collection has been customized and saved to:
{output_path}

📋 Import Steps:

1. Open OBS Studio

2. Import Scene Collection:
   • Go to: Scene Collection → Import
   • Select file: {output_path}
   • Click "Import"

3. Verify Browser Sources:
   • Check each scene to ensure overlays load correctly
   • Test URL: {github_pages_url}
   • Browser sources should show your GitHub Pages content

4. Configure Audio Sources:
   • Go to Settings → Audio
   • Set Mic/Auxiliary Device to your microphone
   • Set Desktop Audio Device if needed
   • Apply audio filters (see OBS_SETUP_GUIDE.md)

5. Configure Video Capture:
   • Go to each scene with "Main Camera" source
   • Right-click → Properties  
   • Select your camera device (Cam Link 4K, etc.)
   • Set resolution to 1920x1080 or 1080x1080

6. Test Hotkeys:
   • F1-F6: Scene switching
   • Ctrl+R: Start/Stop recording
   • Ctrl+M: Mute microphone
   • See OBS_SETUP_GUIDE.md for complete list

7. Verify Display Capture:
   • In scenes with "Screen Capture" source
   • Right-click → Properties
   • Select correct monitor/display
   • Test screen capture works

⚠️  Important Notes:

• Update GitHub Pages URLs if your username changes
• Customize overlay URLs with parameters (see OBS_SETUP_GUIDE.md)
• Test each scene before recording/streaming
• Configure audio monitoring for best results

🔧 Customization:

To modify overlay behavior, add URL parameters:
• Intro: {github_pages_url}overlays/intro.html?countdown=true
• Code Demo: {github_pages_url}overlays/code-demo.html?lang=java&recording=true
• Screen Only: {github_pages_url}overlays/screen-only.html?hidecam=true

📚 For detailed setup instructions, see:
• OBS_SETUP_GUIDE.md - Complete configuration guide
• MACROPAD_DESIGN.md - Physical control setup

🚀 Your professional OBS setup is ready!
"""
    
    return instructions

def main():
    parser = argparse.ArgumentParser(
        description='Import and configure OBS scene collection for Artivisi programming tutorials',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python import-scenes.py --github-username artivisi
  python import-scenes.py --github-username myusername --output my-scenes.json
        """
    )
    
    parser.add_argument(
        '--github-username', 
        required=True,
        help='Your GitHub username (for GitHub Pages URL generation)'
    )
    
    parser.add_argument(
        '--output',
        default='programming-tutorial-configured.json',
        help='Output filename for configured scene collection (default: programming-tutorial-configured.json)'
    )
    
    parser.add_argument(
        '--template',
        default='programming-tutorial.json', 
        help='Template scene collection file (default: programming-tutorial.json)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without writing files'
    )
    
    args = parser.parse_args()
    
    try:
        # Validate inputs
        github_username = validate_github_username(args.github_username)
        github_pages_url = f"https://{github_username}.github.io/obs-scenes-setup/"
        
        # Resolve file paths
        script_dir = Path(__file__).parent
        project_root = script_dir.parent.parent
        template_path = project_root / 'scene-collections' / args.template
        output_path = project_root / 'scene-collections' / args.output
        
        # Check template exists
        if not template_path.exists():
            print(f"❌ Template file not found: {template_path}")
            print(f"💡 Make sure you're running from the correct directory")
            sys.exit(1)
        
        print(f"🚀 Configuring OBS Scene Collection")
        print(f"👤 GitHub Username: {github_username}")
        print(f"🌐 GitHub Pages URL: {github_pages_url}")
        print(f"📄 Template: {template_path}")
        print(f"📄 Output: {output_path}")
        print()
        
        if args.dry_run:
            print("🔍 DRY RUN - No files will be modified")
            print()
        
        # Process scene collection
        if not args.dry_run:
            scene_collection = update_scene_collection(
                template_path, 
                output_path, 
                github_username, 
                github_pages_url
            )
        
        # Generate import instructions
        instructions = generate_import_instructions(github_pages_url, output_path)
        
        if not args.dry_run:
            instructions_path = output_path.with_suffix('.txt')
            with open(instructions_path, 'w') as f:
                f.write(instructions)
            print(f"📋 Import instructions saved to: {instructions_path}")
        
        print(instructions)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()