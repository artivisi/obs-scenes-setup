#!/usr/bin/env python3
"""
OBS Content Creation Workflow

Complete workflow from event preparation to OBS scene creation.
Supports offline-first workflow with online fallback for maximum customization.

Workflow Sequence:
1. Environment Setup - Install dependencies and validate system
2. Event Configuration - Create/edit event-specific content templates  
3. Overlay Generation - Generate custom overlays from templates
4. OBS Integration - Create OBS scenes using custom or default overlays

Usage:
    python scripts/workflow.py --setup                    # Full environment setup
    python scripts/workflow.py --event my-event          # Create event-specific overlays + OBS
    python scripts/workflow.py --template python-workshop # Use predefined template
    python scripts/workflow.py --quick                   # Quick setup with defaults
"""

import json
import argparse
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import shutil

class OBSWorkflow:
    """Complete OBS content creation workflow"""
    
    def __init__(self, github_user: str = "artivisi"):
        self.github_user = github_user
        self.project_root = Path(__file__).parent.parent
        self.scripts_dir = self.project_root / "scripts"
        self.resources_dir = self.project_root / "templates"
        
    def step1_environment_setup(self) -> bool:
        """Step 1: Set up environment and dependencies"""
        print("🔧 Step 1: Environment Setup")
        print("=" * 50)
        
        try:
            # Install dependencies
            print("📦 Installing dependencies...")
            result = subprocess.run([
                sys.executable, str(self.scripts_dir / "setup" / "install-dependencies.py")
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Failed to install dependencies: {result.stderr}")
                return False
            
            print("✅ Dependencies installed successfully")
            
            # Check OBS WebSocket
            print("🔌 Checking OBS WebSocket availability...")
            try:
                import obsws_python
                print("✅ OBS WebSocket library available")
            except ImportError:
                print("⚠️  OBS WebSocket not available - JSON mode only")
            
            print("🎉 Environment setup complete!")
            return True
            
        except Exception as e:
            print(f"❌ Environment setup failed: {e}")
            return False
    
    def step2_configure_event(self, event_name: str, template: Optional[str] = None, 
                             interactive: bool = True) -> Optional[Path]:
        """Step 2: Configure event-specific content"""
        print("📝 Step 2: Event Configuration") 
        print("=" * 50)
        
        try:
            # Create event configuration
            if template:
                print(f"📋 Using template: {template}")
                config_path = self.resources_dir / f"{template}.json"
                if not config_path.exists():
                    print(f"❌ Template not found: {template}")
                    return None
            else:
                print(f"📄 Creating custom event: {event_name}")
                config_path = self.resources_dir / "default.json"
            
            # Load configuration
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Interactive editing if requested
            if interactive and not template:
                print("\\n✏️  Interactive event configuration:")
                config = self._interactive_config_edit(config, event_name)
            
            # Save event-specific configuration
            event_config_path = self.project_root / f"{event_name}-config.json"
            with open(event_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            
            print(f"✅ Event configuration saved: {event_config_path}")
            print(f"📋 Event: {config.get('event', {}).get('title', event_name)}")
            print(f"👤 Presenter: {config.get('presenter', {}).get('name', 'Not specified')}")
            
            return event_config_path
            
        except Exception as e:
            print(f"❌ Event configuration failed: {e}")
            return None
    
    def step3_generate_overlays(self, config_path: Path, event_name: str) -> Optional[Path]:
        """Step 3: Generate custom overlays from configuration"""
        print("🎨 Step 3: Overlay Generation")
        print("=" * 50)
        
        try:
            # Generate event-specific overlays
            overlay_output_dir = self.project_root / f"{event_name}-overlays"
            
            print(f"🎬 Generating overlays for: {event_name}")
            result = subprocess.run([
                sys.executable, str(self.scripts_dir / "tools" / "populate-overlays.py"),
                "--config", str(config_path),
                "--output", str(overlay_output_dir)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Overlay generation failed: {result.stderr}")
                return None
            
            print(result.stdout)
            print(f"✅ Custom overlays generated: {overlay_output_dir}")
            
            return overlay_output_dir
            
        except Exception as e:
            print(f"❌ Overlay generation failed: {e}")
            return None
    
    def step4_create_obs_scenes(self, overlay_path: Optional[Path] = None, 
                               mode: str = "offline", create_live: bool = True) -> bool:
        """Step 4: Create OBS scenes with custom or default overlays"""
        print("🎬 Step 4: OBS Scene Creation")
        print("=" * 50)
        
        try:
            # Build command for OBS scene creation
            cmd = [
                sys.executable, str(self.scripts_dir / "obs" / "auto-scene-creator.py")
            ]
            
            if create_live:
                cmd.extend(["--create-live"])
                print("🔴 Creating scenes in OBS (live mode)")
            else:
                output_json = self.project_root / "generated-scenes.json"
                cmd.extend(["--generate-json", "--output", str(output_json)])
                print(f"📄 Generating scene collection JSON: {output_json}")
            
            cmd.extend(["--github-user", self.github_user])
            
            # Prioritize custom overlays (offline mode)
            if overlay_path and overlay_path.exists():
                cmd.extend(["--offline", "--overlay-path", str(overlay_path)])
                print(f"🎨 Using custom overlays: {overlay_path}")
            elif mode == "offline":
                cmd.extend(["--offline"])  
                print("🏠 Using local default overlays")
            else:
                print(f"🌐 Using online overlays: {self.github_user}")
            
            # Execute OBS scene creation
            print("⚡ Executing scene creation...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ OBS scene creation failed: {result.stderr}")
                return False
            
            print(result.stdout)
            print("✅ OBS scenes created successfully!")
            
            return True
            
        except Exception as e:
            print(f"❌ OBS scene creation failed: {e}")
            return False
    
    def _interactive_config_edit(self, config: Dict[str, Any], event_name: str) -> Dict[str, Any]:
        """Interactive configuration editing"""
        print(f"\\n📝 Customizing event: {event_name}")
        
        # Event details
        event = config.get('event', {})
        title = input(f"Event title [{event.get('title', event_name)}]: ").strip()
        if title:
            event['title'] = title
            
        subtitle = input(f"Event subtitle [{event.get('subtitle', '')}]: ").strip()
        if subtitle:
            event['subtitle'] = subtitle
        
        # Presenter details
        presenter = config.get('presenter', {})
        presenter_name = input(f"Presenter name [{presenter.get('name', '')}]: ").strip()
        if presenter_name:
            presenter['name'] = presenter_name
            
        # Update configuration
        config['event'] = event
        config['presenter'] = presenter
        
        return config
    
    def quick_setup(self, template: str = "java", event_name: Optional[str] = None) -> bool:
        """Quick setup with sensible defaults"""
        print("⚡ Quick Setup Mode")
        print("=" * 50)
        
        if not event_name:
            event_name = f"event-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Run all steps automatically
        if not self.step1_environment_setup():
            return False
        
        config_path = self.step2_configure_event(event_name, template=template, interactive=False)
        if not config_path:
            return False
        
        overlay_path = self.step3_generate_overlays(config_path, event_name)
        if not overlay_path:
            print("⚠️  Using default overlays instead")
            overlay_path = None
        
        return self.step4_create_obs_scenes(overlay_path, mode="offline", create_live=True)
    
    def full_workflow(self, event_name: str, template: Optional[str] = None) -> bool:
        """Complete workflow with all steps"""
        print(f"🚀 Complete OBS Workflow: {event_name}")
        print("=" * 80)
        
        # Step 1: Environment Setup
        if not self.step1_environment_setup():
            return False
        print()
        
        # Step 2: Event Configuration  
        config_path = self.step2_configure_event(event_name, template=template)
        if not config_path:
            return False
        print()
        
        # Step 3: Generate Overlays
        overlay_path = self.step3_generate_overlays(config_path, event_name)
        if not overlay_path:
            print("⚠️  Continuing with default overlays")
            overlay_path = None
        print()
        
        # Step 4: Create OBS Scenes
        success = self.step4_create_obs_scenes(overlay_path, mode="offline", create_live=True)
        print()
        
        if success:
            print("🎉 Complete workflow finished successfully!")
            print(f"📂 Event files saved in: {event_name}-*")
            print("🎬 OBS scenes ready for recording!")
        else:
            print("❌ Workflow completed with errors")
        
        return success

def main():
    parser = argparse.ArgumentParser(description='Complete OBS content creation workflow')
    
    # Workflow modes
    parser.add_argument('--setup', action='store_true', help='Environment setup only')
    parser.add_argument('--event', help='Create event-specific setup')
    parser.add_argument('--template', help='Use predefined template')
    parser.add_argument('--quick', action='store_true', help='Quick setup with defaults')
    
    # Configuration options
    parser.add_argument('--github-user', default='artivisi', help='GitHub username for online mode')
    parser.add_argument('--no-interactive', action='store_true', help='Skip interactive configuration')
    parser.add_argument('--json-only', action='store_true', help='Generate JSON only (no live OBS)')
    
    args = parser.parse_args()
    
    if not any([args.setup, args.event, args.quick]):
        parser.print_help()
        print()
        print("🚀 Quick Examples:")
        print("  python scripts/workflow.py --quick                    # Quick setup with Java template")
        print("  python scripts/workflow.py --event my-workshop        # Full custom event workflow")
        print("  python scripts/workflow.py --template python-workshop # Use Python template")
        print("  python scripts/workflow.py --setup                    # Environment setup only")
        return
    
    workflow = OBSWorkflow(github_user=args.github_user)
    
    try:
        if args.setup:
            # Environment setup only
            success = workflow.step1_environment_setup()
        elif args.quick:
            # Quick setup
            template = args.template or "java"
            success = workflow.quick_setup(template=template)
        elif args.event:
            # Full event workflow
            success = workflow.full_workflow(args.event, template=args.template)
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\\n⏹️  Workflow cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()