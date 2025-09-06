# Complete OBS Workflow Guide

This guide shows the new streamlined workflow for creating professional OBS setups with event-specific customization.

## 🎯 Workflow Philosophy

**Offline-First with Online Fallback:**
- **Primary:** Custom event-specific overlays (offline mode)
- **Secondary:** Local default overlays (offline mode)  
- **Fallback:** Online GitHub Pages overlays

**Logical Sequence:**
1. **Environment Setup** - Install dependencies, validate system
2. **Event Configuration** - Define event content, branding, presenter info
3. **Overlay Generation** - Create custom overlays from templates
4. **OBS Integration** - Generate scenes using custom or default overlays

## 🚀 Quick Reference

### ⚡ Fastest Setup (1-2 minutes)
```bash
python scripts/workflow.py --quick
```
**Result:** Professional OBS setup with Java template and custom overlays

### 🎯 Custom Event (3-4 minutes) 
```bash
python scripts/workflow.py --event my-workshop
```
**Result:** Full customization with your event details, branding, and content

### 📋 Template-Based
```bash
python scripts/workflow.py --event my-workshop --template python-workshop
```
**Result:** Custom event starting from Python workshop template

## 📝 Detailed Workflows

### Workflow 1: Quick Setup
**Best for:** Getting started quickly, testing, standard Java content

```bash
# Complete setup with defaults
python scripts/workflow.py --quick

# Quick setup with specific template
python scripts/workflow.py --quick --template python-workshop
```

**What happens:**
1. ✅ Environment setup (dependencies, validation)
2. ✅ Load template configuration (Java or specified)
3. ✅ Generate custom overlays with template content
4. ✅ Create OBS scenes using custom overlays (offline mode)
5. ✅ Ready to record!

### Workflow 2: Custom Event Setup
**Best for:** Specific workshops, branded content, professional presentations

```bash
# Interactive custom event
python scripts/workflow.py --event my-python-workshop

# Custom event with template starting point
python scripts/workflow.py --event my-python-workshop --template python-workshop
```

**Interactive Configuration Process:**
1. ✅ Environment setup
2. ✅ **Event Details Prompts:**
   - Event title: "Python Web Development Workshop"
   - Event subtitle: "Building Modern APIs with FastAPI"
   - Presenter name: "Your Name"
   - Event date and duration
3. ✅ Generate event-specific overlays with your information
4. ✅ Create OBS scenes using your custom overlays
5. ✅ Save configuration for future use

**Example Interactive Session:**
```
📝 Customizing event: my-python-workshop
Event title [Python Web Development]: Python FastAPI Masterclass
Event subtitle [Building Modern APIs with FastAPI]: From Basics to Production
Presenter name []: Sarah Johnson
```

### Workflow 3: Manual Step-by-Step
**Best for:** Understanding the process, troubleshooting, advanced customization

```bash
# Step 1: Environment setup
python scripts/workflow.py --setup

# Step 2: Create event configuration file
cp docs/resources/event-config.json my-event.json
# Edit my-event.json with your content

# Step 3: Generate overlays
python scripts/tools/populate-overlays.py --config my-event.json --output my-overlays --preview

# Step 4: Create OBS scenes  
python scripts/obs/auto-scene-creator.py --create-live --overlay-path my-overlays
```

## 🎨 Event Text Customization

### Method 1: Interactive Configuration (Easiest)
```bash
python scripts/workflow.py --event my-workshop
```
**Prompts you'll see:**
- **Event title** (e.g., "Java Development Masterclass")
- **Event subtitle** (e.g., "Spring Boot from Basics to Production")  
- **Presenter name** (e.g., "Sarah Johnson")
- **Company/Organization** (auto-filled from template)

### Method 2: Direct JSON Editing (Full Control)
```bash
# 1. Copy base configuration
cp docs/resources/event-config.json my-event.json

# 2. Edit with your text editor
nano my-event.json  # or code my-event.json

# 3. Generate overlays from your config
python scripts/tools/populate-overlays.py --config my-event.json --output my-overlays

# 4. Create OBS scenes
python scripts/obs/auto-scene-creator.py --create-live --overlay-path my-overlays
```

### Method 3: Template-Based Customization
```bash
# 1. List available templates
python scripts/tools/populate-overlays.py --list-templates

# 2. Start with template, then customize
python scripts/workflow.py --event my-event --template python-workshop
```

## 📝 What You Can Customize

### Event Information
```json
{
  "event": {
    "title": "Your Event Title",
    "subtitle": "Your Event Subtitle",
    "date": "2024-12-15",
    "duration": "90 minutes",
    "type": "Workshop", 
    "description": "Hands-on Learning"
  }
}
```

### Presenter Details
```json
{
  "presenter": {
    "name": "Your Name",
    "title": "Senior Developer",
    "experience": "10+ years in Python",
    "specialty": "FastAPI & Microservices",
    "company": "Your Company"
  }
}
```

### Session Content
```json
{
  "session": {
    "topics": [
      "Topic 1: Introduction",
      "Topic 2: Core Concepts", 
      "Topic 3: Advanced Features",
      "Topic 4: Best Practices"
    ],
    "current_topic": "Python Programming"
  }
}
```

### Messages & Labels
```json
{
  "messages": {
    "welcome": "Welcome to the Workshop",
    "thanks": "Thank You!",
    "thanks_message": "Hope you enjoyed this Python session",
    "recording_status": "LIVE",
    "countdown_text": "Starting in"
  }
}
```

### Company Branding
```json
{
  "branding": {
    "company_name": "Your Company",
    "company_tagline": "Your Company Tagline",
    "website": "yourcompany.com"
  }
}
```

## 🎯 Customization Examples

### Example 1: Java Corporate Training
```json
{
  "event": {
    "title": "Enterprise Java Development",
    "subtitle": "Microservices Architecture with Spring Cloud"
  },
  "presenter": {
    "name": "Michael Chen", 
    "title": "Lead Architect",
    "company": "TechCorp Solutions"
  },
  "session": {
    "topics": [
      "Spring Boot Fundamentals",
      "Microservices Design Patterns",
      "API Gateway Implementation", 
      "Production Deployment"
    ]
  }
}
```

### Example 2: Python Bootcamp
```json
{
  "event": {
    "title": "Python Web Development Bootcamp",
    "subtitle": "Build Real-World Applications"
  },
  "presenter": {
    "name": "Sarah Rodriguez",
    "title": "Full-Stack Developer", 
    "company": "Code Academy Pro"
  },
  "messages": {
    "welcome": "Welcome to Python Bootcamp",
    "recording_status": "LIVE",
    "thanks_message": "Ready to build amazing Python apps!"
  }
}
```

### Example 3: Linux System Administration
```json
{
  "event": {
    "title": "Linux Server Administration",
    "subtitle": "Production System Management"
  },
  "presenter": {
    "name": "David Kim",
    "title": "DevOps Engineer",
    "specialty": "Container Orchestration & Security"
  },
  "session": {
    "topics": [
      "System Hardening",
      "Container Management", 
      "Monitoring & Logging",
      "Security Best Practices"
    ]
  }
}
```

## 🔧 Advanced Customization

### Custom Template Creation
1. **Copy existing template:**
   ```bash
   cp docs/resources/templates/python-workshop.json docs/resources/templates/my-template.json
   ```

2. **Edit all sections with your defaults:**
   - Company branding information
   - Standard presenter details
   - Common session types
   - Preferred messaging

3. **Use your custom template:**
   ```bash
   python scripts/workflow.py --event my-event --template my-template
   ```

### Tech Stack Customization
```json
{
  "session": {
    "tech_stack": [
      {"icon": "🐍", "name": "Python 3.11"},
      {"icon": "⚡", "name": "FastAPI"},
      {"icon": "🗄️", "name": "PostgreSQL"},
      {"icon": "🚀", "name": "Docker"}
    ]
  }
}
```

### Call-to-Action Cards
```json
{
  "cta_cards": [
    {
      "icon": "📧",
      "title": "Join Our Newsletter", 
      "description": "Get weekly Python tips and tutorials!"
    },
    {
      "icon": "💼",
      "title": "Hire Our Team",
      "description": "Need expert Python development? Contact us!"
    }
  ]
}
```

## 🔧 Advanced Usage

### Environment Setup Only
```bash
python scripts/workflow.py --setup
```
**Use case:** First-time setup, troubleshooting dependencies

### Overlay Generation Only  
```bash
python scripts/tools/populate-overlays.py --template python-workshop --preview
```
**Use case:** Testing overlay designs, creating assets for later use

### OBS Scene Creation with Custom Overlays
```bash
python scripts/obs/auto-scene-creator.py --create-live --overlay-path my-overlays
```
**Use case:** Using pre-generated custom overlays

### Generate JSON for Manual Import
```bash
python scripts/obs/auto-scene-creator.py --generate-json --output my-scenes.json
```
**Use case:** Sharing scene collections, manual OBS setup

## 🎯 Best Practices

### For Regular Content Creation
1. **Create event templates** for your common content types
2. **Use workflow.py --quick** for rapid setup
3. **Customize event details** via interactive mode

### For Professional Presentations
1. **Use full event workflow** with branding
2. **Test overlays** with `--preview` first
3. **Generate custom graphics** and add to overlay assets

### For Development/Testing
1. **Use manual steps** for understanding and debugging
2. **Test offline mode** before relying on online overlays
3. **Version control** your event configurations

## 🌐 Online vs Offline Modes

### Offline Mode (Default/Recommended)
- ✅ Works without internet
- ✅ Full customization control
- ✅ Fast loading times
- ✅ No external dependencies
- **Used by:** workflow.py, custom overlays

### Online Mode (Fallback)
- ✅ Always up-to-date default overlays
- ✅ Shared across machines
- ⚠️ Requires internet connection
- **Used by:** Traditional setup without customization

## 🏗️ File Organization

After running workflows, you'll have:
```
project-root/
├── my-event-config.json        # Your event configuration
├── my-event-overlays/          # Generated custom overlays
│   ├── intro.html              # Custom intro with your content
│   ├── outro.html              # Custom outro with your branding  
│   ├── talking-head.html       # Custom presenter info
│   └── assets/                 # CSS, JS, images
└── generated-scenes.json       # OBS scene collection (if generated)
```

## ⚡ Migration from Old Workflow

**Old way:**
```bash
python scripts/setup/install-dependencies.py
python scripts/obs/auto-scene-creator.py --create-live --github-user artivisi
```

**New way (equivalent):**
```bash
python scripts/workflow.py --quick
```

**New way (better):**
```bash
python scripts/workflow.py --event my-content
```

The new workflow provides the same results with much more customization power and a cleaner process.

## 🎉 Summary

The new workflow transforms OBS setup from a technical process into a content creation workflow:

1. **Think about your content** (event, topic, audience)
2. **Run one command** with your event details
3. **Get professional results** with your branding and content
4. **Start recording** with confidence

This approach prioritizes customization and content-specific results while maintaining the speed and automation that made the original system powerful.