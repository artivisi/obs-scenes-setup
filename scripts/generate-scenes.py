#!/usr/bin/env python3
"""
Scene Generator with Text Resources and HTML Templating

This script parses YAML text resources and generates HTML scenes using 
Mustache templating. Scenes are grouped into named scene collections
with safe encoding to avoid collisions.

Usage:
    python scripts/generate-scenes.py resources/event.yaml
    python scripts/generate-scenes.py resources/event.yaml --output my-scenes
"""

import yaml
import argparse
import sys
import re
import secrets
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import shutil

try:
    import pystache
    MUSTACHE_AVAILABLE = True
except ImportError:
    MUSTACHE_AVAILABLE = False
    print("⚠️  pystache not installed. Install with: pip install pystache")

class SceneGenerator:
    """Generate HTML scenes from YAML resources using Mustache templates"""
    
    def __init__(self, resource_file: Path):
        self.project_root = Path(__file__).parent.parent
        self.resource_file = resource_file
        self.themes_dir = self.project_root / "themes"
        self.templates_dir = self.themes_dir / "default"  # Default theme
        self.resources = {}
        self.output_dir = None
        self.collection_name = ""
        
    def load_resources(self) -> bool:
        """Load YAML text resources"""
        try:
            print(f"📖 Loading text resources: {self.resource_file}")
            with open(self.resource_file, 'r', encoding='utf-8') as f:
                self.resources = yaml.safe_load(f)
            
            # Generate collection name with safe encoding
            event_title = self.resources.get('event', {}).get('title', 'OBS-Event')
            safe_title = self._to_kebab_case(event_title)
            random_suffix = secrets.token_hex(4)
            self.collection_name = f"{safe_title}-{random_suffix}"
            
            print(f"✅ Resources loaded successfully")
            print(f"🏷️  Scene collection: {self.collection_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load resources: {e}")
            return False
    
    def _to_kebab_case(self, text: str) -> str:
        """Convert text to kebab-case for safe file naming"""
        # Remove special characters, convert to lowercase, replace spaces with hyphens
        text = re.sub(r'[^\w\s-]', '', text.lower())
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')
    
    def generate_scenes(self, output_dir: Path = None) -> Path:
        """Generate all scenes using Mustache templates"""
        if not MUSTACHE_AVAILABLE:
            print("❌ Cannot generate scenes without pystache library")
            return None
            
        if output_dir:
            self.output_dir = output_dir
        else:
            # Create timestamped output directory in target/
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_dir = self.project_root / "target" / f"{self.collection_name}_{timestamp}"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Generating scenes in: {self.output_dir}")
        
        # Copy assets first
        self._copy_assets()
        
        # Generate scenes from templates
        scene_files = []
        template_files = list(self.templates_dir.glob("*.mustache.html"))
        
        if not template_files:
            print("⚠️  No Mustache templates found. Using fallback overlays...")
            self._copy_fallback_overlays()
            return self.output_dir
        
        for template_file in template_files:
            scene_name = template_file.stem.replace('.mustache', '')
            output_file = self.output_dir / f"{scene_name}.html"
            
            if self._render_template(template_file, output_file):
                scene_files.append(output_file)
                print(f"✅ Generated: {scene_name}.html")
        
        # Create scene collection metadata
        self._create_scene_metadata(scene_files)
        
        print(f"🎉 Generated {len(scene_files)} scenes successfully!")
        print(f"📂 Output directory: {self.output_dir}")
        
        return self.output_dir
    
    def _render_template(self, template_file: Path, output_file: Path) -> bool:
        """Render a single Mustache template with resources"""
        try:
            # Read template
            with open(template_file, 'r', encoding='utf-8') as f:
                template = f.read()
            
            # Render with Mustache
            renderer = pystache.Renderer()
            rendered = renderer.render(template, self.resources)
            
            # Write output
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(rendered)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to render {template_file.name}: {e}")
            return False
    
    def _copy_assets(self):
        """Copy CSS, JS, and asset files to output directory"""
        # Create basic CSS for generated scenes
        css_dst = self.output_dir / "css"
        css_dst.mkdir(exist_ok=True)
        
        # Create minimal CSS file
        basic_css = """
/* Generated Scene Styles */
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', system-ui, sans-serif; }
"""
        with open(css_dst / "main.css", 'w') as f:
            f.write(basic_css)
        
        print("📋 Created basic CSS assets")
    
    def _copy_fallback_overlays(self):
        """Create fallback scenes when no templates exist"""
        print("⚠️  No Mustache templates found, creating basic scenes...")
        
        basic_scene = """<!DOCTYPE html>
<html><head><title>Basic Scene</title></head>
<body><h1>Scene Ready</h1><p>Basic scene placeholder</p></body>
</html>"""
        
        basic_scenes = ['intro', 'talking-head', 'code-demo', 'screen-only', 'brb', 'outro']
        for scene_name in basic_scenes:
            scene_file = self.output_dir / f"{scene_name}.html"
            with open(scene_file, 'w') as f:
                f.write(basic_scene)
            print(f"📋 Created basic: {scene_name}.html")
    
    def _create_scene_metadata(self, scene_files: list):
        """Create metadata file for scene collection"""
        metadata = {
            'collection_name': self.collection_name,
            'generated_at': datetime.now().isoformat(),
            'event_title': self.resources.get('event', {}).get('title', 'Unknown Event'),
            'instructor': self.resources.get('instructor', {}).get('name', 'Unknown'),
            'scenes': [f.name for f in scene_files],
            'total_scenes': len(scene_files),
            'resource_file': str(self.resource_file),
            'webserver_info': {
                'recommended_port': 8080,
                'serve_directory': str(self.output_dir),
                'python_command': f"python3 -m http.server 8080 --directory {self.output_dir}"
            }
        }
        
        # Write metadata
        metadata_file = self.output_dir / "scene-collection.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            import json
            json.dump(metadata, f, indent=2)
        
        print(f"📋 Scene collection metadata: {metadata_file}")
        
        # Create README for the generated scenes
        readme_content = f"""# {self.collection_name}

Generated scenes for: **{metadata['event_title']}**  
Instructor: {metadata['instructor']}  
Generated: {metadata['generated_at']}

## Scenes ({metadata['total_scenes']} total)
{chr(10).join(f"- {scene}" for scene in metadata['scenes'])}

## Usage

1. **Start webserver:**
   ```bash
   cd {self.project_root.name}
   {metadata['webserver_info']['python_command']}
   ```

2. **Import into OBS:**
   Use the OBS injection script with collection name: `{self.collection_name}`

## Files
- `scene-collection.json` - Metadata and configuration
- `*.html` - Scene overlay files  
- `css/`, `js/`, `assets/` - Supporting resources
"""
        
        readme_file = self.output_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"📖 Generated README: {readme_file}")

def main():
    parser = argparse.ArgumentParser(description='Generate OBS scenes from YAML resources using Mustache templates')
    parser.add_argument('resource_file', type=Path, help='YAML resource file (e.g., resources/event.yaml)')
    parser.add_argument('--output', type=Path, help='Output directory (default: auto-generated)')
    parser.add_argument('--list-templates', action='store_true', help='List available Mustache templates')
    
    args = parser.parse_args()
    
    if args.list_templates:
        project_root = Path(__file__).parent.parent
        templates_dir = project_root / "templates"
        templates = list(templates_dir.glob("*.mustache.html"))
        
        if templates:
            print("📋 Available Mustache templates:")
            for template in templates:
                scene_name = template.stem.replace('.mustache', '')
                print(f"  • {scene_name} ({template.name})")
        else:
            print("❌ No Mustache templates found in templates/")
        return
    
    if not args.resource_file.exists():
        print(f"❌ Resource file not found: {args.resource_file}")
        sys.exit(1)
    
    if not MUSTACHE_AVAILABLE:
        print("❌ pystache library required. Install with: pip install pystache")
        sys.exit(1)
    
    try:
        generator = SceneGenerator(args.resource_file)
        
        if not generator.load_resources():
            sys.exit(1)
        
        output_dir = generator.generate_scenes(args.output)
        
        if output_dir:
            print(f"\n🎉 Scene generation complete!")
            print(f"📂 Scenes directory: {output_dir}")
            print(f"🏷️  Collection name: {generator.collection_name}")
            
            # Display webserver command based on environment  
            metadata_file = output_dir / "scene-collection.json"
            if metadata_file.exists():
                import json
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                serve_dir = metadata['webserver_info']['serve_directory']
                if not serve_dir.startswith('/'):
                    serve_dir = str(Path(serve_dir).resolve())
                print(f"\n🌐 Next: Start webserver:")
                print(f"   python3 -m http.server 8080 --directory {serve_dir}")
        
    except Exception as e:
        print(f"❌ Scene generation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()