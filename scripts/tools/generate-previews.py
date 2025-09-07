#!/usr/bin/env python3
"""
Generate preview pages from Mustache templates with opaque backgrounds for better visibility.
"""

import os
import sys
import yaml
import pystache
from pathlib import Path

def load_config(config_path):
    """Load YAML configuration file"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_template_files(theme_dir):
    """Get all mustache template files"""
    template_dir = Path(theme_dir)
    return list(template_dir.glob('*.mustache.html'))

def add_preview_styles(html_content):
    """Add opaque background styles for preview visibility"""
    preview_css = """
        /* PREVIEW STYLES - Added for documentation visibility */
        .preview-label {
            position: absolute !important;
            top: 20px !important;
            right: 20px !important;
            background: rgba(255,255,255,0.2) !important;
            padding: 10px 20px !important;
            border-radius: 20px !important;
            font-size: 1rem !important;
            backdrop-filter: blur(10px) !important;
            z-index: 100 !important;
        }
        
        /* Make camera areas visible with gradient backgrounds */
        .camera-placeholder,
        .camera-frame,
        .camera-content {
            background: radial-gradient(circle, #4a4a4a 40%, #2a2a2a 100%) !important;
        }
        
        /* Make screen areas visible with pattern backgrounds */
        .screen-placeholder {
            background: linear-gradient(45deg, #2a2a2a 25%, transparent 25%, transparent 75%, #2a2a2a 75%, #2a2a2a),
                        linear-gradient(45deg, #2a2a2a 25%, transparent 25%, transparent 75%, #2a2a2a 75%, #2a2a2a) !important;
            background-size: 40px 40px !important;
            background-position: 0 0, 20px 20px !important;
        }
        
        /* Ensure body backgrounds are opaque for visibility */
        body {
            background: linear-gradient(135deg, #2e3192 0%, #58c034 100%) !important;
        }
    """
    
    # Insert preview CSS before closing </style> tag
    if '</style>' in html_content:
        html_content = html_content.replace('</style>', preview_css + '\n    </style>')
    
    # Add preview label after <body> tag
    preview_label = '\n    <!-- Preview Label -->\n    <div class="preview-label">📖 Documentation Preview</div>\n'
    if '<body>' in html_content:
        html_content = html_content.replace('<body>', '<body>' + preview_label)
    
    return html_content

def generate_preview(template_path, config, output_dir):
    """Generate a single preview file"""
    # Extract name without .mustache.html suffix
    template_name = template_path.name.replace('.mustache.html', '')  # e.g., 'intro' from 'intro.mustache.html'
    
    # Read template
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Render with pystache
    renderer = pystache.Renderer()
    html_content = renderer.render(template_content, config)
    
    # Add preview-specific styling and elements
    preview_content = add_preview_styles(html_content)
    
    # Update title to indicate it's a preview
    scene_titles = {
        'intro': 'Intro Scene - Preview',
        'talking-head': 'Talking Head Scene - Preview', 
        'presentation': '50:50 Presentation Scene - Preview',
        'code-demo': 'Code Demo Scene - Preview',
        'screen-only': 'Screen Only Scene - Preview',
        'brb': 'BRB (Be Right Back) Scene - Preview',
        'outro': 'Outro Scene - Preview'
    }
    
    if template_name in scene_titles:
        # Replace title in HTML
        old_title_pattern = f'<title>{config.get("event", {}).get("title", "Workshop")} - {template_name.replace("-", " ").title()}</title>'
        new_title = f'<title>{scene_titles[template_name]}</title>'
        preview_content = preview_content.replace(old_title_pattern, new_title)
        
        # Also try more generic replacement
        import re
        preview_content = re.sub(r'<title>.*?</title>', new_title, preview_content, flags=re.IGNORECASE)
    
    # Write preview file
    output_file = output_dir / f'{template_name}-preview.html'
    with open(output_file, 'w') as f:
        f.write(preview_content)
    
    print(f"✅ Generated preview: {output_file}")
    return output_file

def main():
    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    
    # Default paths
    config_path = project_root / 'resources' / 'event.yaml'
    theme_dir = project_root / 'themes' / 'default'
    output_dir = project_root / 'docs' / 'previews'
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        theme_dir = Path(sys.argv[2])
    if len(sys.argv) > 3:
        output_dir = Path(sys.argv[3])
    
    # Validate inputs
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return 1
    
    if not theme_dir.exists():
        print(f"❌ Theme directory not found: {theme_dir}")
        return 1
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load configuration
    print(f"📖 Loading config: {config_path}")
    config = load_config(config_path)
    
    # Get template files
    template_files = get_template_files(theme_dir)
    if not template_files:
        print(f"❌ No template files found in: {theme_dir}")
        return 1
    
    print(f"🎨 Found {len(template_files)} templates")
    
    # Generate previews
    generated_files = []
    for template_path in template_files:
        try:
            output_file = generate_preview(template_path, config, output_dir)
            generated_files.append(output_file)
        except Exception as e:
            print(f"❌ Error generating preview for {template_path.name}: {e}")
    
    print(f"\n🎉 Generated {len(generated_files)} preview files in {output_dir}")
    
    # List generated files
    for file_path in generated_files:
        print(f"   📄 {file_path.name}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())