#!/usr/bin/env python3
"""
Text Customization Utilities
Reusable components for customizing overlay text content.
"""

import re
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path


class TextTemplate:
    """Handles text template processing with placeholders"""
    
    def __init__(self, template_content: str):
        self.template = template_content
        self.placeholders = self._extract_placeholders()
    
    def _extract_placeholders(self) -> List[str]:
        """Extract placeholder patterns from template"""
        # Find patterns like {{placeholder}} or {placeholder}
        pattern = r'\{\{?([^}]+)\}?\}'
        return list(set(re.findall(pattern, self.template)))
    
    def substitute(self, replacements: Dict[str, str]) -> str:
        """Replace placeholders with actual values"""
        result = self.template
        
        for placeholder, value in replacements.items():
            # Support both {{placeholder}} and {placeholder} formats
            patterns = [
                f"{{{{{placeholder}}}}}",  # {{placeholder}}
                f"{{{placeholder}}}",      # {placeholder}
                placeholder                # direct replacement
            ]
            
            for pattern in patterns:
                result = result.replace(pattern, str(value))
        
        return result
    
    def get_missing_placeholders(self, replacements: Dict[str, str]) -> List[str]:
        """Get list of placeholders not provided in replacements"""
        provided = set(replacements.keys())
        required = set(self.placeholders)
        return list(required - provided)


class EventContentGenerator:
    """Generates content for different event types"""
    
    EVENT_TEMPLATES = {
        "workshop": {
            "title_suffix": "Workshop",
            "type": "Hands-on Workshop", 
            "description": "Interactive",
            "default_duration": "2 hours",
            "topics_prefix": "What You'll Learn:",
            "cta_action": "Start Building"
        },
        "tutorial": {
            "title_suffix": "Tutorial",
            "type": "Step-by-step Tutorial",
            "description": "Guided Learning",
            "default_duration": "90 minutes", 
            "topics_prefix": "Tutorial Topics:",
            "cta_action": "Follow Along"
        },
        "presentation": {
            "title_suffix": "Presentation",
            "type": "Technical Presentation",
            "description": "Knowledge Sharing",
            "default_duration": "45 minutes",
            "topics_prefix": "Key Topics:",
            "cta_action": "Learn More"
        },
        "interview": {
            "title_suffix": "Interview",
            "type": "Expert Interview", 
            "description": "Q&A Session",
            "default_duration": "60 minutes",
            "topics_prefix": "Discussion Points:",
            "cta_action": "Join Discussion"
        }
    }
    
    TECH_STACK_ICONS = {
        "java": "☕",
        "python": "🐍",
        "javascript": "⚡",
        "typescript": "📘",
        "react": "⚛️",
        "vue": "💚",
        "angular": "🔺",
        "spring": "🍃",
        "django": "🎸",
        "flask": "🌶️",
        "nodejs": "💚",
        "docker": "🐳",
        "kubernetes": "⚙️",
        "linux": "🐧",
        "bash": "💻",
        "git": "📝",
        "aws": "☁️",
        "azure": "☁️",
        "gcp": "☁️"
    }
    
    @classmethod
    def generate_event_config(cls, event_type: str, title: str, **kwargs) -> Dict[str, Any]:
        """Generate complete event configuration"""
        template = cls.EVENT_TEMPLATES.get(event_type, cls.EVENT_TEMPLATES["workshop"])
        
        # Build tech stack with icons
        tech_stack = kwargs.get('tech_stack', [])
        if isinstance(tech_stack, list):
            tech_with_icons = []
            for tech in tech_stack:
                icon = cls.TECH_STACK_ICONS.get(tech.lower(), "🔧")
                tech_with_icons.append({
                    "name": tech,
                    "icon": icon
                })
        else:
            tech_with_icons = tech_stack
        
        # Generate configuration
        config = {
            "event": {
                "title": title,
                "subtitle": kwargs.get('subtitle', f"{title} {template['title_suffix']}"),
                "type": template['type'],
                "description": template['description'],
                "duration": kwargs.get('duration', template['default_duration']),
                "date": kwargs.get('date', datetime.now().strftime("%Y-%m-%d"))
            },
            "session": {
                "current_topic": kwargs.get('current_topic', title),
                "tech_stack": tech_with_icons,
                "topics": kwargs.get('topics', [
                    f"Getting started with {title}",
                    "Core concepts and best practices",
                    "Hands-on examples and demos",
                    "Q&A and troubleshooting"
                ])
            },
            "presenter": {
                "name": kwargs.get('presenter_name', 'Expert Presenter'),
                "title": kwargs.get('presenter_title', 'Senior Developer'),
                "company": kwargs.get('presenter_company', 'Tech Company'),
                "bio": kwargs.get('presenter_bio', f'Experienced {title} developer and instructor')
            },
            "branding": {
                "company_name": kwargs.get('company_name', 'ArtiVisi Intermedia'),
                "company_tagline": kwargs.get('company_tagline', 'Custom Application Development'),
                "website": kwargs.get('website', 'artivisi.com'),
                "primary_color": kwargs.get('primary_color', '#3b82f6'),
                "social_links": kwargs.get('social_links', [
                    {"platform": "GitHub", "url": "https://github.com/artivisi", "icon": "🐙"},
                    {"platform": "LinkedIn", "url": "https://linkedin.com/company/artivisi", "icon": "💼"},
                    {"platform": "Website", "url": "https://artivisi.com", "icon": "🌐"}
                ])
            },
            "messages": {
                "welcome": kwargs.get('welcome_message', f"Welcome to {title}"),
                "thanks": kwargs.get('thanks_message', "Thank You!"),
                "thanks_message": kwargs.get('thanks_detail', f"Hope you enjoyed this {title.lower()} session"),
                "what_we_covered": template['topics_prefix']
            },
            "cta_cards": kwargs.get('cta_cards', [
                {
                    "title": "Start Your Journey",
                    "description": f"Begin your {title.lower()} development journey today",
                    "icon": "🚀"
                },
                {
                    "title": "Get Support", 
                    "description": "Join our community for help and resources",
                    "icon": "🤝"
                },
                {
                    "title": "Advanced Training",
                    "description": "Take your skills to the next level",
                    "icon": "📚"
                }
            ]),
            "macropad": {
                "current_layer": 1,
                "layer_name": "Tutorial Mode",
                "layers": {
                    "0": "Default Mode",
                    "1": "Tutorial Mode", 
                    "2": "Demo Mode",
                    "3": "Q&A Mode"
                }
            }
        }
        
        return config
    
    @classmethod
    def customize_for_language(cls, config: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Customize configuration for specific programming language"""
        customizations = {
            "java": {
                "session": {
                    "current_topic": "Java Development",
                    "topics": [
                        "Java fundamentals and OOP concepts",
                        "Spring Boot application development", 
                        "Database integration with JPA",
                        "Testing with JUnit and Mockito",
                        "Deployment and best practices"
                    ]
                },
                "branding": {
                    "primary_color": "#f89820"
                }
            },
            "python": {
                "session": {
                    "current_topic": "Python Development",
                    "topics": [
                        "Python fundamentals and syntax",
                        "Web development with Django/Flask",
                        "Data analysis and visualization", 
                        "API development and testing",
                        "Deployment and package management"
                    ]
                },
                "branding": {
                    "primary_color": "#3776ab"
                }
            },
            "javascript": {
                "session": {
                    "current_topic": "JavaScript Development", 
                    "topics": [
                        "Modern JavaScript (ES6+) features",
                        "Frontend frameworks (React/Vue)",
                        "Node.js backend development",
                        "Testing and debugging techniques",
                        "Performance optimization"
                    ]
                },
                "branding": {
                    "primary_color": "#f7df1e"
                }
            },
            "linux": {
                "session": {
                    "current_topic": "Linux System Administration",
                    "topics": [
                        "Command line fundamentals",
                        "System administration tasks",
                        "Shell scripting automation",
                        "Security and permissions",
                        "Server deployment and monitoring"
                    ]
                },
                "branding": {
                    "primary_color": "#fcc419"
                }
            }
        }
        
        # Deep merge customizations
        if language.lower() in customizations:
            lang_config = customizations[language.lower()]
            for section, values in lang_config.items():
                if section in config:
                    config[section].update(values)
                else:
                    config[section] = values
        
        return config


class OverlayTextProcessor:
    """Processes text content for HTML overlays"""
    
    @staticmethod
    def generate_tech_stack_html(tech_stack: List[Dict[str, str]]) -> str:
        """Generate HTML for technology stack display"""
        html_items = []
        for i, tech in enumerate(tech_stack):
            delay = 1.5 + i * 0.2
            html_items.append(f'''
            <div class="tech-item" style="animation-delay: {delay}s;">
                <div class="tech-icon">{tech['icon']}</div>
                <div class="tech-name">{tech['name']}</div>
            </div>''')
        return '\\n'.join(html_items)
    
    @staticmethod
    def generate_cta_cards_html(cta_cards: List[Dict[str, str]]) -> str:
        """Generate HTML for call-to-action cards"""
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
    
    @staticmethod
    def generate_social_links_html(social_links: List[Dict[str, str]]) -> str:
        """Generate HTML for social media links"""
        html_items = []
        for i, link in enumerate(social_links):
            delay = 2.5 + i * 0.2
            html_items.append(f'''
            <a href="{link['url']}" class="social-link" title="{link['platform']}" style="animation-delay: {delay}s;">
                <span>{link['icon']}</span>
            </a>''')
        return '\\n'.join(html_items)
    
    @staticmethod
    def generate_topics_list_html(topics: List[str]) -> str:
        """Generate HTML for topics list"""
        return '\\n'.join([f'                <li>{topic}</li>' for topic in topics])
    
    @staticmethod
    def process_overlay_content(template_content: str, config: Dict[str, Any]) -> str:
        """Process complete overlay template with configuration"""
        processor = TextTemplate(template_content)
        
        # Flatten config for easy replacement
        replacements = {}
        
        # Extract nested values with dot notation
        def flatten_dict(d: Dict[str, Any], prefix: str = '') -> None:
            for key, value in d.items():
                full_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    flatten_dict(value, full_key)
                else:
                    replacements[full_key] = str(value)
                    replacements[key] = str(value)  # Also add without prefix
        
        flatten_dict(config)
        
        # Process template
        return processor.substitute(replacements)