#!/usr/bin/env python3
"""
Convert Markdown documentation to HTML for GitHub Pages

This script converts markdown documentation files to styled HTML
for better presentation on GitHub Pages.
"""

import re
from pathlib import Path
from typing import Dict, List

def create_html_template() -> str:
    """Create the HTML template for documentation pages"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - OBS Infrastructure-as-Code</title>
    <meta name="description" content="{description}">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            color: #333;
        }}
        
        .nav-bar {{
            background: linear-gradient(135deg, #2e3192 0%, #58c034 100%);
            color: white;
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .nav-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .nav-brand {{
            font-size: 1.2rem;
            font-weight: 600;
            text-decoration: none;
            color: white;
        }}
        
        .nav-links {{
            display: flex;
            gap: 2rem;
        }}
        
        .nav-links a {{
            color: rgba(255,255,255,0.9);
            text-decoration: none;
            transition: color 0.3s ease;
        }}
        
        .nav-links a:hover {{
            color: white;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .doc-header {{
            background: white;
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .doc-title {{
            color: #2e3192;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        
        .doc-subtitle {{
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 1.5rem;
        }}
        
        .breadcrumb {{
            font-size: 0.9rem;
            color: #58c034;
            margin-bottom: 1rem;
        }}
        
        .breadcrumb a {{
            color: #58c034;
            text-decoration: none;
        }}
        
        .content {{
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}
        
        .content h1 {{
            color: #2e3192;
            font-size: 2rem;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #58c034;
        }}
        
        .content h2 {{
            color: #2e3192;
            font-size: 1.5rem;
            margin: 1.5rem 0 1rem 0;
        }}
        
        .content h3 {{
            color: #2e3192;
            font-size: 1.2rem;
            margin: 1rem 0 0.5rem 0;
        }}
        
        .content p {{
            margin-bottom: 1rem;
            line-height: 1.7;
        }}
        
        .content ul, .content ol {{
            margin: 1rem 0 1rem 2rem;
        }}
        
        .content li {{
            margin-bottom: 0.5rem;
        }}
        
        .content code {{
            background: #f8f9fa;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
        }}
        
        .content pre {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1rem 0;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9rem;
        }}
        
        .content pre code {{
            background: none;
            padding: 0;
            color: inherit;
        }}
        
        .content blockquote {{
            border-left: 4px solid #58c034;
            padding-left: 1rem;
            margin: 1rem 0;
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 4px;
        }}
        
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .content th, .content td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .content th {{
            background: #2e3192;
            color: white;
            font-weight: 600;
        }}
        
        .content tr:hover {{
            background: #f8f9fa;
        }}
        
        .warning {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }}
        
        .warning::before {{
            content: "⚠️ ";
            font-weight: bold;
        }}
        
        .info {{
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }}
        
        .info::before {{
            content: "💡 ";
            font-weight: bold;
        }}
        
        .success {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }}
        
        .success::before {{
            content: "✅ ";
            font-weight: bold;
        }}
        
        .toc {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .toc h3 {{
            color: #2e3192;
            margin-bottom: 1rem;
        }}
        
        .toc ul {{
            list-style-type: none;
            margin: 0;
            padding: 0;
        }}
        
        .toc li {{
            margin-bottom: 0.5rem;
        }}
        
        .toc a {{
            color: #58c034;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .toc a:hover {{
            text-decoration: underline;
        }}
        
        .back-to-top {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: #58c034;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 1.2rem;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            opacity: 0;
            visibility: hidden;
        }}
        
        .back-to-top.visible {{
            opacity: 1;
            visibility: visible;
        }}
        
        .back-to-top:hover {{
            background: #45a029;
            transform: translateY(-2px);
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}
            
            .nav-container {{
                padding: 0 1rem;
                flex-direction: column;
                gap: 1rem;
            }}
            
            .nav-links {{
                gap: 1rem;
            }}
            
            .doc-title {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <nav class="nav-bar">
        <div class="nav-container">
            <a href="../index.html" class="nav-brand">🎬 OBS Infrastructure-as-Code</a>
            <div class="nav-links">
                <a href="../index.html">Home</a>
                <a href="AUTOMATED_SETUP.html">Automation</a>
                <a href="OBS_SETUP_GUIDE.html">Manual Setup</a>
                <a href="MACROPAD_DESIGN.html">Macropad</a>
                <a href="../overlays/">Overlays</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="doc-header">
            <div class="breadcrumb">
                <a href="../index.html">Home</a> / <a href="#">{breadcrumb}</a>
            </div>
            <h1 class="doc-title">{title}</h1>
            <p class="doc-subtitle">{description}</p>
        </div>

        {toc}

        <div class="content">
            {content}
        </div>
    </div>

    <button class="back-to-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})" title="Back to top">
        ↑
    </button>

    <script>
        // Show/hide back to top button
        window.addEventListener('scroll', function() {{
            const button = document.querySelector('.back-to-top');
            if (window.pageYOffset > 300) {{
                button.classList.add('visible');
            }} else {{
                button.classList.remove('visible');
            }}
        }});

        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});
    </script>
</body>
</html>"""

def markdown_to_html(markdown_content: str) -> str:
    """Convert markdown content to HTML"""
    # Convert headers
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', markdown_content, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Convert code blocks
    html = re.sub(r'```(\w*)\n(.*?)\n```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    
    # Convert inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Convert bold and italic
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
    
    # Convert links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    # Convert lists
    lines = html.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        if re.match(r'^- ', line):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            item_content = re.sub(r'^- ', '', line)
            result_lines.append(f'<li>{item_content}</li>')
        elif re.match(r'^\d+\. ', line):
            if not in_list:
                result_lines.append('<ol>')
                in_list = True
            item_content = re.sub(r'^\d+\. ', '', line)
            result_lines.append(f'<li>{item_content}</li>')
        else:
            if in_list:
                result_lines.append('</ul>' if result_lines[-1].startswith('<li>') and '- ' in markdown_content else '</ol>')
                in_list = False
            
            # Convert paragraphs
            if line.strip() and not line.startswith('<'):
                # Check for special callouts
                if line.strip().startswith('⚠️') or 'warning' in line.lower():
                    result_lines.append(f'<div class="warning">{line.strip()}</div>')
                elif line.strip().startswith('💡') or 'note:' in line.lower():
                    result_lines.append(f'<div class="info">{line.strip()}</div>')
                elif line.strip().startswith('✅'):
                    result_lines.append(f'<div class="success">{line.strip()}</div>')
                else:
                    result_lines.append(f'<p>{line}</p>')
            elif line.strip():
                result_lines.append(line)
    
    if in_list:
        result_lines.append('</ul>')
    
    return '\n'.join(result_lines)

def generate_toc(content: str) -> str:
    """Generate table of contents from markdown content"""
    headers = re.findall(r'^(#{1,3}) (.+)$', content, re.MULTILINE)
    if not headers:
        return ""
    
    toc_html = '<div class="toc"><h3>📋 Table of Contents</h3><ul>'
    
    for level, title in headers:
        anchor = title.lower().replace(' ', '-').replace('/', '').replace('?', '').replace('!', '')
        anchor = re.sub(r'[^\w\-]', '', anchor)
        
        indent = len(level) - 1
        style = f"margin-left: {indent * 1.5}rem;" if indent > 0 else ""
        
        toc_html += f'<li style="{style}"><a href="#{anchor}">{title}</a></li>'
    
    toc_html += '</ul></div>'
    return toc_html

def convert_markdown_file(md_path: Path, output_path: Path, title: str, description: str, breadcrumb: str):
    """Convert a single markdown file to HTML"""
    with open(md_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Generate TOC
    toc_html = generate_toc(markdown_content)
    
    # Convert markdown to HTML
    html_content = markdown_to_html(markdown_content)
    
    # Create final HTML
    template = create_html_template()
    final_html = template.format(
        title=title,
        description=description,
        breadcrumb=breadcrumb,
        toc=toc_html,
        content=html_content
    )
    
    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✅ Converted: {md_path.name} → {output_path.name}")

def main():
    """Convert all documentation files"""
    # Script is in scripts/tools/, so go up 2 levels to project root
    root_dir = Path(__file__).parent.parent.parent
    docs_dir = root_dir / "docs"
    guides_dir = docs_dir / "guides"
    
    # Ensure directories exist
    guides_dir.mkdir(exist_ok=True)
    
    # Define conversion mappings
    conversions = [
        {
            'input': root_dir / 'AUTOMATED_SETUP.md',
            'output': guides_dir / 'AUTOMATED_SETUP.html',
            'title': 'Automated OBS Setup',
            'description': 'Skip the manual clicking! Complete automation guide for OBS scene creation.',
            'breadcrumb': 'Automated Setup'
        },
        {
            'input': root_dir / 'OBS_SETUP_GUIDE.md',
            'output': guides_dir / 'OBS_SETUP_GUIDE.html',
            'title': 'Manual OBS Setup Guide',
            'description': 'Comprehensive step-by-step manual configuration for professional OBS setup.',
            'breadcrumb': 'Manual Setup'
        },
        {
            'input': root_dir / 'MACROPAD_DESIGN.md',
            'output': guides_dir / 'MACROPAD_DESIGN.html',
            'title': 'Macropad Configuration',
            'description': '4-layer macropad system with Vial firmware for OBS control.',
            'breadcrumb': 'Macropad'
        },
        {
            'input': root_dir / 'PROJECT_NOTES.md',
            'output': guides_dir / 'PROJECT_NOTES.html',
            'title': 'Project Architecture',
            'description': 'Technical deep-dive into the Infrastructure-as-Code approach.',
            'breadcrumb': 'Architecture'
        },
        {
            'input': root_dir / 'WORKFLOW_GUIDE.md',
            'output': guides_dir / 'WORKFLOW_GUIDE.html',
            'title': 'Complete Workflow Guide',
            'description': 'Master the new streamlined workflow for event-specific OBS setups.',
            'breadcrumb': 'Workflow Guide'
        },
        {
            'input': root_dir / 'docs' / 'resources' / 'README.md',
            'output': guides_dir / 'OVERLAY_RESOURCES.html',
            'title': 'Overlay Resource System',
            'description': 'Generate event-specific overlays from JSON templates.',
            'breadcrumb': 'Overlay Resources'
        }
    ]
    
    print("🔄 Converting Markdown documentation to HTML...")
    
    for conversion in conversions:
        if conversion['input'].exists():
            convert_markdown_file(
                conversion['input'],
                conversion['output'],
                conversion['title'],
                conversion['description'],
                conversion['breadcrumb']
            )
        else:
            print(f"⚠️  File not found: {conversion['input']}")
    
    print(f"\n🎉 Documentation conversion complete!")
    print(f"📁 HTML files created in: {guides_dir}")
    print(f"🌐 Access via: https://artivisi.github.io/obs-scenes-setup/")

if __name__ == '__main__':
    main()