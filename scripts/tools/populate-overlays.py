#!/usr/bin/env python3
"""
Overlay Population Script

This script populates HTML overlay templates with content from JSON resource files.
It supports multiple event templates and generates customized overlays for each event.

Usage:
    python populate-overlays.py --config event-config.json
    python populate-overlays.py --template python-workshop
    python populate-overlays.py --config custom-event.json --output custom-overlays/
    python populate-overlays.py --list-templates
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import re
from datetime import datetime
import shutil

class OverlayPopulator:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.templates_dir = self.project_root / "templates"
        self.overlays_dir = self.project_root / "overlays"
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        if config_path.startswith('/'):
            config_file = Path(config_path)
        else:
            # Try relative to templates directory first
            config_file = self.templates_dir / config_path
            if not config_file.exists():
                # Try relative to current directory
                config_file = Path(config_path)
                
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def load_template(self, template_name: str) -> Dict[str, Any]:
        """Load a predefined template"""
        template_file = self.templates_dir / f"{template_name}.json"
        if not template_file.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")
            
        return self.load_config(str(template_file))
    
    def list_templates(self) -> List[str]:
        """List available templates"""
        if not self.templates_dir.exists():
            return []
            
        templates = []
        for template_file in self.templates_dir.glob("*.json"):
            templates.append(template_file.stem)
        return sorted(templates)
    
    def populate_intro(self, config: Dict[str, Any], output_dir: Path) -> Path:
        """Populate intro.html with configuration data"""
        template_path = self.overlays_dir / "intro.html"
        output_path = output_dir / "intro.html"
        
        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract configuration values
        event = config.get('event', {})
        session = config.get('session', {})
        branding = config.get('branding', {})
        messages = config.get('messages', {})
        presenter = config.get('presenter', {})
        
        # Replace placeholders
        replacements = {
            'Java Development Mastery': event.get('title', 'Java Development Mastery'),
            'Building Enterprise Applications with Spring Boot': event.get('subtitle', 'Building Enterprise Applications with Spring Boot'),
            'Live Session': event.get('type', 'Live Session'),
            '90 minutes • Interactive': f"{event.get('duration', '90 minutes')} • {event.get('description', 'Interactive')}",
            'artivisi.com': branding.get('website', 'artivisi.com'),
            'ArtiVisi Intermedia': branding.get('company_name', 'ArtiVisi Intermedia'),
            'Custom Application Development': branding.get('company_tagline', 'Custom Application Development'),
        }
        
        # Apply text replacements
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)
        
        # Update tech stack if provided
        if session.get('tech_stack'):
            tech_stack_html = self._generate_tech_stack_html(session['tech_stack'])
            # Replace the entire tech stack section
            tech_pattern = r'<div class="tech-stack">.*?</div>'
            content = re.sub(tech_pattern, f'<div class="tech-stack">{tech_stack_html}</div>', 
                           content, flags=re.DOTALL)
        
        # Update default values in JavaScript
        js_replacements = {
            "urlParams.get('title') || 'Java Development Mastery'": f"urlParams.get('title') || '{event.get('title', 'Java Development Mastery')}'",
            "urlParams.get('subtitle') || 'Building Enterprise Applications with Spring Boot'": f"urlParams.get('subtitle') || '{event.get('subtitle', 'Building Enterprise Applications with Spring Boot')}'",
        }
        
        for old_js, new_js in js_replacements.items():
            content = content.replace(old_js, new_js)
        
        # Write populated template
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return output_path
    
    def populate_talking_head(self, config: Dict[str, Any], output_dir: Path) -> Path:
        """Populate talking-head.html with configuration data"""
        template_path = self.overlays_dir / "talking-head.html"
        output_path = output_dir / "talking-head.html"
        
        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract configuration values
        event = config.get('event', {})
        session = config.get('session', {})
        branding = config.get('branding', {})
        messages = config.get('messages', {})
        macropad = config.get('macropad', {})
        
        # Replace placeholders
        replacements = {
            'Welcome to the Session': messages.get('welcome', 'Welcome to the Session'),
            'Java Development & Software Engineering': f"{event.get('title', 'Java Development')} & Software Engineering",
            'Java Programming': session.get('current_topic', 'Java Programming'),
            'Layer 1: Tutorial Mode': f"Layer {macropad.get('current_layer', 1)}: {macropad.get('layer_name', 'Tutorial Mode')}",
            'ArtiVisi Intermedia': branding.get('company_name', 'ArtiVisi Intermedia'),
            'artivisi.com': branding.get('website', 'artivisi.com'),
        }
        
        # Apply text replacements
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)
        
        # Write populated template
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return output_path
    
    def populate_outro(self, config: Dict[str, Any], output_dir: Path) -> Path:
        """Populate outro.html with configuration data"""
        template_path = self.overlays_dir / "outro.html"
        output_path = output_dir / "outro.html"
        
        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract configuration values
        session = config.get('session', {})
        branding = config.get('branding', {})
        messages = config.get('messages', {})
        cta_cards = config.get('cta_cards', [])
        social_links = branding.get('social_links', [])
        
        # Replace placeholders
        replacements = {
            'Thank You!': messages.get('thanks', 'Thank You!'),
            'Hope you enjoyed this Java development session': messages.get('thanks_message', 'Hope you enjoyed this Java development session'),
            'What We Covered': messages.get('what_we_covered', 'What We Covered'),
            'ArtiVisi Intermedia': branding.get('company_name', 'ArtiVisi Intermedia'),
            'Custom Application Development': branding.get('company_tagline', 'Custom Application Development'),
        }
        
        # Apply text replacements
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)
        
        # Update session topics list if provided
        if session.get('topics'):
            topics_html = '\\n'.join([f'                <li>{topic}</li>' for topic in session['topics']])
            topics_pattern = r'<ul id="sessionTopics">.*?</ul>'
            topics_replacement = f'<ul id="sessionTopics">\\n{topics_html}\\n            </ul>'
            content = re.sub(topics_pattern, topics_replacement, content, flags=re.DOTALL)
        
        # Update CTA cards if provided
        if cta_cards:
            cta_html = self._generate_cta_cards_html(cta_cards)
            cta_pattern = r'<div class="cta-section">.*?</div>'
            content = re.sub(cta_pattern, f'<div class="cta-section">{cta_html}</div>', 
                           content, flags=re.DOTALL)
        
        # Update social links if provided
        if social_links:
            social_html = self._generate_social_links_html(social_links)
            social_pattern = r'<div class="social-links">.*?</div>'
            content = re.sub(social_pattern, f'<div class="social-links">{social_html}</div>', 
                           content, flags=re.DOTALL)
        
        # Write populated template
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return output_path
    
    def _generate_tech_stack_html(self, tech_stack) -> str:
        """Generate HTML for technology stack items"""
        html_items = []
        for i, tech in enumerate(tech_stack):
            delay = 1.5 + i * 0.2
            html_items.append(f'''
            <div class="tech-item" style="animation-delay: {delay}s;">
                <div class="tech-icon">{tech['icon']}</div>
                <div class="tech-name">{tech['name']}</div>
            </div>''')
        return '\\n'.join(html_items)
    
    def _generate_cta_cards_html(self, cta_cards) -> str:
        """Generate HTML for CTA cards"""
        html_items = []
        for i, card in enumerate(cta_cards):
            delay = 1.5 + i * 0.2
            html_items.append(f'''
            <div class="cta-card" style="animation-delay: {delay}s;">
                <span class="cta-icon">{card['icon']}</span>
                <h3>{card['title']}</h3>
                <p>{card['description']}</p>
            </div>''')
        return '\\n'.join(html_items)
    
    def _generate_social_links_html(self, social_links) -> str:
        """Generate HTML for social media links"""
        html_items = []
        for i, link in enumerate(social_links):
            delay = 2.5 + i * 0.2
            html_items.append(f'''
            <a href="{link['url']}" class="social-link" title="{link['title']}" style="animation-delay: {delay}s;">
                <span>{link['icon']}</span>
            </a>''')
        return '\\n'.join(html_items)
    
    def copy_assets(self, output_dir: Path):
        """Copy CSS, JS, and asset files to output directory"""
        # Copy CSS directory
        css_src = self.overlays_dir / "css"
        css_dst = output_dir / "css" 
        if css_src.exists():
            if css_dst.exists():
                shutil.rmtree(css_dst)
            shutil.copytree(css_src, css_dst)
        
        # Copy JS directory
        js_src = self.overlays_dir / "js"
        js_dst = output_dir / "js"
        if js_src.exists():
            if js_dst.exists():
                shutil.rmtree(js_dst)
            shutil.copytree(js_src, js_dst)
        
        # Copy assets directory
        assets_src = self.overlays_dir / "assets"
        assets_dst = output_dir / "assets"
        if assets_src.exists():
            if assets_dst.exists():
                shutil.rmtree(assets_dst)
            shutil.copytree(assets_src, assets_dst)
    
    def populate_all_overlays(self, config: Dict[str, Any], output_dir: Optional[str] = None) -> Path:
        """Populate all overlay templates with configuration"""
        if output_dir:
            output_path = Path(output_dir)
        else:
            # Create timestamped output directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            event_name = config.get('event', {}).get('title', 'event').lower().replace(' ', '-')
            output_path = self.project_root / "generated-overlays" / f"{event_name}_{timestamp}"
        
        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Creating overlays in: {output_path}")
        
        # Copy assets first
        print("📋 Copying assets...")
        self.copy_assets(output_path)
        
        # Populate each overlay type
        overlays = []
        
        print("🎬 Populating intro overlay...")
        intro_path = self.populate_intro(config, output_path)
        overlays.append(intro_path)
        
        print("👤 Populating talking head overlay...")
        talking_head_path = self.populate_talking_head(config, output_path)
        overlays.append(talking_head_path)
        
        print("🎉 Populating outro overlay...")
        outro_path = self.populate_outro(config, output_path)
        overlays.append(outro_path)
        
        # Copy other overlay files as-is for now
        other_overlays = ['code-demo.html', 'screen-only.html', 'brb.html', 'dual-cam.html']
        for overlay_name in other_overlays:
            src_path = self.overlays_dir / overlay_name
            dst_path = output_path / overlay_name
            if src_path.exists():
                print(f"📋 Copying {overlay_name}...")
                shutil.copy2(src_path, dst_path)
                overlays.append(dst_path)
        
        # Create index.html for easy preview
        self._create_preview_index(config, output_path, overlays)
        
        print(f"✅ Successfully populated {len(overlays)} overlays")
        print(f"🌐 Preview at: file://{output_path}/index.html")
        
        return output_path
    
    def _create_preview_index(self, config: Dict[str, Any], output_dir: Path, overlays: list):
        """Create an index.html file for previewing all overlays"""
        event_title = config.get('event', {}).get('title', 'Event Overlays')
        overlay_links = []
        
        for overlay_path in overlays:
            name = overlay_path.stem.replace('-', ' ').title()
            overlay_links.append(f'<li><a href="{overlay_path.name}" target="_blank">{name}</a></li>')
        
        index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{event_title} - Overlay Preview</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 40px; }}
        h1 {{ color: #1e293b; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 10px 0; }}
        a {{ 
            display: inline-block; 
            padding: 10px 20px; 
            background: #3b82f6; 
            color: white; 
            text-decoration: none; 
            border-radius: 6px;
            transition: background 0.2s;
        }}
        a:hover {{ background: #2563eb; }}
        .config {{ 
            background: #f8fafc; 
            border: 1px solid #e2e8f0; 
            border-radius: 6px; 
            padding: 20px; 
            margin: 20px 0;
        }}
        .config pre {{ margin: 0; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>🎬 {event_title}</h1>
    <p>Generated on {datetime.now().strftime("%Y-%m-%d at %H:%M:%S")}</p>
    
    <h2>📋 Available Overlays</h2>
    <ul>
        {''.join(overlay_links)}
    </ul>
    
    <div class="config">
        <h3>⚙️ Configuration Used</h3>
        <pre><code>{json.dumps(config, indent=2)}</code></pre>
    </div>
</body>
</html>'''
        
        with open(output_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(index_html)

def main():
    parser = argparse.ArgumentParser(description='Populate OBS overlay templates with event configuration')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--config', help='Path to JSON configuration file')
    group.add_argument('--template', help='Use a predefined template (e.g., python-workshop)')
    group.add_argument('--list-templates', action='store_true', help='List available templates')
    
    parser.add_argument('--output', help='Output directory for generated overlays')
    parser.add_argument('--preview', action='store_true', help='Open preview in browser after generation')
    
    args = parser.parse_args()
    
    try:
        populator = OverlayPopulator()
        
        if args.list_templates:
            templates = populator.list_templates()
            if templates:
                print("📋 Available templates:")
                for template in templates:
                    print(f"  • {template}")
            else:
                print("❌ No templates found")
            return
        
        # Load configuration
        if args.config:
            print(f"📖 Loading configuration: {args.config}")
            config = populator.load_config(args.config)
        elif args.template:
            print(f"📋 Loading template: {args.template}")
            config = populator.load_template(args.template)
        
        # Populate overlays
        output_dir = populator.populate_all_overlays(config, args.output)
        
        # Open preview if requested
        if args.preview:
            import webbrowser
            webbrowser.open(f"file://{output_dir}/index.html")
        
        print(f"\\n🎉 Overlay population completed successfully!")
        print(f"📂 Output directory: {output_dir}")
        print(f"🌐 Preview: file://{output_dir}/index.html")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()