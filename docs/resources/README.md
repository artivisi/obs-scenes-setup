# Overlay Resource System

This system extracts all text labels and content from overlay files into easily editable resource files that can be configured before events and populated into final overlays via script.

## 🚀 Quick Start

```bash
# List available templates
python3 scripts/tools/populate-overlays.py --list-templates

# Generate overlays from a template
python3 scripts/tools/populate-overlays.py --template python-workshop --output my-event

# Generate overlays from custom config
python3 scripts/tools/populate-overlays.py --config docs/resources/event-config.json --output my-event

# Generate overlays and open preview
python3 scripts/tools/populate-overlays.py --template linux-admin --preview
```

## 📁 File Structure

```
docs/resources/
├── README.md                    # This file
├── event-config.json           # Default event configuration
├── templates/                  # Predefined event templates  
│   ├── python-workshop.json    # Python workshop template
│   └── linux-admin.json       # Linux administration template
└── generated/                  # Output location for generated overlays
```

## ⚙️ Configuration Format

The resource files use JSON format with these sections:

### 🎬 Event Information
```json
{
  "event": {
    "title": "Java Development Mastery",
    "subtitle": "Building Enterprise Applications with Spring Boot", 
    "date": "2024-12-07",
    "duration": "90 minutes",
    "type": "Live Session",
    "description": "Interactive"
  }
}
```

### 👤 Presenter Information
```json
{
  "presenter": {
    "name": "Endy Muhardin",
    "title": "Senior Developer", 
    "experience": "10+ years in Enterprise Java",
    "specialty": "Spring Boot & Microservices",
    "company": "ArtiVisi Intermedia"
  }
}
```

### 📚 Session Content
```json
{
  "session": {
    "topics": [
      "Spring Boot Fundamentals",
      "REST API Development",
      "Database Integration"
    ],
    "tech_stack": [
      {"icon": "☕", "name": "Java 17"},
      {"icon": "🍃", "name": "Spring Boot"}
    ],
    "current_topic": "Java Programming"
  }
}
```

### 🎨 Branding & Social
```json
{
  "branding": {
    "company_name": "ArtiVisi Intermedia",
    "company_tagline": "Custom Application Development", 
    "website": "artivisi.com",
    "social_links": [
      {"title": "GitHub", "url": "https://github.com/artivisi", "icon": "🐙"},
      {"title": "LinkedIn", "url": "https://linkedin.com/company/artivisi", "icon": "💼"}
    ]
  }
}
```

### 💬 Messages & Text
```json
{
  "messages": {
    "welcome": "Welcome to the Session",
    "thanks": "Thank You!",
    "thanks_message": "Hope you enjoyed this Java development session",
    "recording_status": "REC",
    "countdown_text": "Starting in"
  }
}
```

### 🎯 Call-to-Action Cards  
```json
{
  "cta_cards": [
    {
      "icon": "👍",
      "title": "Like & Subscribe", 
      "description": "Help us reach more developers!"
    }
  ]
}
```

## 📝 Creating New Templates

1. **Copy existing template:**
   ```bash
   cp docs/resources/templates/python-workshop.json docs/resources/templates/my-event.json
   ```

2. **Edit the JSON file** with your event-specific content

3. **Test the template:**
   ```bash
   python3 scripts/tools/populate-overlays.py --template my-event --preview
   ```

## 🎨 Supported Overlays

The system currently populates these overlay types:

- **🎬 intro.html** - Opening sequence with title, tech stack, presenter info
- **👤 talking-head.html** - Main presenter view with topic indicators  
- **🎉 outro.html** - Closing sequence with session summary, CTA cards
- **📋 Other overlays** - Copied as-is (code-demo, screen-only, brb, dual-cam)

## 🔧 How It Works

1. **Template Loading** - Loads JSON configuration from file or template
2. **Text Replacement** - Replaces hardcoded text in HTML with config values
3. **Dynamic Content** - Generates HTML sections like tech stack, CTA cards, social links
4. **Asset Copying** - Copies CSS, JS, and image assets to output directory
5. **Preview Generation** - Creates index.html for easy overlay preview

## 🎯 Benefits

- **✅ Event-specific Content** - Easy customization for different events/topics
- **✅ Template Reusability** - Predefined templates for common event types  
- **✅ Version Control** - All text content tracked in JSON files
- **✅ Batch Generation** - Generate all overlays with one command
- **✅ Preview Support** - Built-in preview system for testing
- **✅ Asset Management** - Automatic copying of CSS/JS/image files

## 🚀 Integration with OBS

The generated overlays work seamlessly with the existing OBS automation system:

```bash
# Generate event-specific overlays
python3 scripts/tools/populate-overlays.py --template my-event --output event-overlays

# Use with OBS scene creator (use local files)
python3 scripts/obs/auto-scene-creator.py --create-live --offline --overlay-path event-overlays
```

## 🎯 How to Customize Event Texts

### Method 1: Quick Interactive Setup
```bash
# The workflow script will prompt you for key details
python scripts/workflow.py --event my-workshop
```

**You'll be prompted for:**
- **Event Title** (e.g., "Python FastAPI Workshop")
- **Event Subtitle** (e.g., "Building Production APIs")  
- **Presenter Name** (e.g., "Sarah Johnson")
- **Additional details** (auto-filled from template)

### Method 2: Direct JSON Editing
```bash
# 1. Copy the base configuration
cp docs/resources/event-config.json my-workshop.json

# 2. Edit with your favorite text editor
code my-workshop.json  # or nano, vim, etc.

# 3. Generate overlays with your customizations
python3 scripts/tools/populate-overlays.py --config my-workshop.json --output my-workshop-overlays
```

### Method 3: Start with Template
```bash
# 1. Copy a template that's closest to your event
cp docs/resources/templates/python-workshop.json my-event.json

# 2. Edit the JSON file with your specific content
# 3. Generate overlays
python3 scripts/tools/populate-overlays.py --config my-event.json --output my-event-overlays
```

## ✏️ What to Edit in the JSON

### Essential Information to Change
```json
{
  "event": {
    "title": "📝 Change this to your event title",
    "subtitle": "📝 Change this to your event subtitle",
    "date": "📝 Event date (2024-12-15)",
    "duration": "📝 How long (90 minutes, 2 hours, etc.)"
  },
  "presenter": {
    "name": "📝 Your name or speaker name", 
    "title": "📝 Job title (Senior Developer, etc.)",
    "experience": "📝 Experience description",
    "company": "📝 Your company name"
  },
  "session": {
    "topics": [
      "📝 Replace with your actual topics",
      "📝 Topic 2", 
      "📝 Topic 3"
    ],
    "current_topic": "📝 Main topic for overlay display"
  },
  "branding": {
    "company_name": "📝 Your company name",
    "website": "📝 yourcompany.com"
  }
}
```

### Optional Customizations
```json
{
  "messages": {
    "welcome": "📝 Custom welcome message",
    "thanks": "📝 Custom thank you message",
    "recording_status": "📝 LIVE, REC, or custom status"
  },
  "cta_cards": [
    {
      "title": "📝 Custom call-to-action",
      "description": "📝 What you want viewers to do"
    }
  ]
}
```

## 📚 Examples

### Example 1: Corporate Java Training
```json
{
  "event": {
    "title": "Enterprise Java Development",
    "subtitle": "Spring Boot Microservices Architecture",
    "date": "2024-01-15",
    "duration": "3 hours"
  },
  "presenter": {
    "name": "Michael Chen",
    "title": "Senior Java Architect", 
    "experience": "15+ years in Enterprise Java",
    "company": "TechCorp Solutions"
  },
  "session": {
    "topics": [
      "Spring Boot Fundamentals",
      "Microservices Design Patterns", 
      "API Gateway Implementation",
      "Production Deployment Strategies"
    ]
  }
}
```

### Example 2: Python Beginner Workshop  
```json
{
  "event": {
    "title": "Python for Beginners",
    "subtitle": "Your First Steps in Programming",
    "date": "2024-02-10", 
    "duration": "90 minutes"
  },
  "presenter": {
    "name": "Sarah Rodriguez",
    "title": "Python Instructor",
    "experience": "5+ years teaching Python",
    "company": "Code Learning Academy"
  },
  "messages": {
    "welcome": "Welcome to Python Basics!",
    "thanks": "Great job learning Python!",
    "thanks_message": "You're ready to build amazing things with Python!"
  }
}
```

### Example 3: DevOps Masterclass
```json
{
  "event": {
    "title": "DevOps Automation Masterclass", 
    "subtitle": "CI/CD with Docker and Kubernetes",
    "date": "2024-03-05",
    "duration": "4 hours"
  },
  "presenter": {
    "name": "David Kim",
    "title": "DevOps Lead Engineer",
    "specialty": "Container Orchestration & Cloud Architecture",
    "company": "CloudTech Solutions"
  },
  "session": {
    "topics": [
      "Container Fundamentals",
      "Kubernetes Deployment",
      "CI/CD Pipeline Setup", 
      "Production Monitoring"
    ],
    "tech_stack": [
      {"icon": "🐋", "name": "Docker"},
      {"icon": "☸️", "name": "Kubernetes"},
      {"icon": "🔄", "name": "Jenkins"},
      {"icon": "📊", "name": "Prometheus"}
    ]
  }
}
```

## 🚀 Quick Setup Workflow

### For Regular Content Creators
```bash
# 1. Create your standard template
cp docs/resources/event-config.json my-standard-template.json
# Edit with your standard company info, branding, etc.

# 2. For each new event, copy and customize
cp my-standard-template.json todays-workshop.json
# Edit just the event title, topics, and date

# 3. Generate and use
python3 scripts/tools/populate-overlays.py --config todays-workshop.json --output todays-overlays
python scripts/obs/auto-scene-creator.py --create-live --overlay-path todays-overlays
```

This system transforms the overlay creation process from manual HTML editing to simple JSON configuration, making it easy to prepare professional overlays for any event in minutes.