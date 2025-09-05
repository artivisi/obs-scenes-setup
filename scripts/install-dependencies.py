#!/usr/bin/env python3
"""
OBS Setup Dependencies Installer

This script installs the required Python dependencies for the automated
OBS scene creation system.

Usage:
    python install-dependencies.py
    python install-dependencies.py --check-only
"""

import subprocess
import sys
import argparse
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_package(package_name, import_name=None, description=""):
    """Install a Python package and verify import"""
    import_name = import_name or package_name
    
    print(f"📦 Installing {package_name}...")
    if description:
        print(f"   {description}")
    
    try:
        # Try importing first
        __import__(import_name)
        print(f"✅ {package_name} already installed")
        return True
        
    except ImportError:
        # Install the package
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package_name
            ])
            
            # Verify installation
            __import__(import_name)
            print(f"✅ {package_name} installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package_name}: {e}")
            return False
        except ImportError:
            print(f"❌ {package_name} installed but import failed")
            return False

def check_obs_websocket():
    """Check OBS WebSocket availability and provide setup instructions"""
    print("\n🔍 Checking OBS WebSocket setup...")
    
    try:
        import obsws_python
        print("✅ OBS WebSocket Python library available")
        return True
        
    except ImportError:
        print("⚠️  OBS WebSocket Python library not found")
        print("📋 Installing obs-websocket-py...")
        
        success = install_package(
            "obsws-python",
            "obsws_python", 
            "OBS WebSocket API client for Python"
        )
        
        if success:
            print("\n💡 OBS WebSocket Setup Instructions:")
            print("   1. Open OBS Studio")
            print("   2. Go to Tools → WebSocket Server Settings") 
            print("   3. Enable 'Enable WebSocket server'")
            print("   4. Set Server Port: 4455 (default)")
            print("   5. Set Server Password (optional but recommended)")
            print("   6. Click Apply")
            print("\n🔗 The automated scene creator can now connect to OBS!")
        
        return success

def check_requests():
    """Check if requests library is available"""
    return install_package(
        "requests",
        description="HTTP library for GitHub Pages validation"
    )

def create_requirements_file():
    """Create requirements.txt file"""
    requirements_content = """# OBS Setup Dependencies
obsws-python>=1.3.0
requests>=2.25.0

# Optional dependencies for enhanced functionality
asyncio-mqtt>=0.11.0  # For remote control features
websockets>=10.0      # WebSocket utilities
aiohttp>=3.8.0        # Async HTTP client
"""
    
    requirements_path = Path(__file__).parent.parent / "requirements.txt"
    
    try:
        with open(requirements_path, 'w') as f:
            f.write(requirements_content)
        
        print(f"📄 Created requirements.txt: {requirements_path}")
        print("💡 Install all dependencies with: pip install -r requirements.txt")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create requirements.txt: {e}")
        return False

def validate_obs_connection():
    """Test connection to OBS (if running)"""
    print("\n🧪 Testing OBS connection...")
    
    try:
        import obsws_python as obs
        
        # Try to connect (will fail if OBS not running, but that's OK)
        try:
            client = obs.ReqClient()
            version = client.get_version()
            print(f"✅ Connected to OBS Studio {version.obs_version}")
            print(f"📡 WebSocket version: {version.obs_web_socket_version}")
            client.disconnect()
            return True
            
        except Exception as e:
            print("⚠️  Could not connect to OBS (this is normal if OBS isn't running)")
            print("💡 Start OBS and enable WebSocket server to test connection")
            return True  # Not a failure - just not running
            
    except ImportError:
        print("❌ OBS WebSocket library not available")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Install dependencies for OBS automated setup"
    )
    
    parser.add_argument(
        '--check-only',
        action='store_true',
        help='Only check dependencies, do not install'
    )
    
    parser.add_argument(
        '--create-requirements',
        action='store_true',
        help='Create requirements.txt file'
    )
    
    args = parser.parse_args()
    
    print("🚀 OBS Setup Dependencies Check")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    if args.create_requirements:
        create_requirements_file()
        return
    
    success = True
    
    if args.check_only:
        print("\n🔍 Checking dependencies...")
        
        # Check each dependency
        dependencies = [
            ("obsws-python", "obsws_python"),
            ("requests", "requests")
        ]
        
        for package, import_name in dependencies:
            try:
                __import__(import_name)
                print(f"✅ {package} available")
            except ImportError:
                print(f"❌ {package} missing")
                success = False
    
    else:
        print("\n📦 Installing dependencies...")
        
        # Install required packages
        if not check_requests():
            success = False
        
        if not check_obs_websocket():
            success = False
        
        # Test OBS connection
        if success:
            validate_obs_connection()
    
    if success:
        print("\n🎉 Dependencies setup complete!")
        print("🚀 You can now run the automated scene creator:")
        print("   python scripts/setup-scripts/auto-scene-creator.py --help")
    else:
        print("\n❌ Some dependencies failed to install")
        print("💡 Try installing manually:")
        print("   pip install obsws-python requests")
        sys.exit(1)

if __name__ == '__main__':
    main()