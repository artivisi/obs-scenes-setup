#!/usr/bin/env python3
"""
Simple Macropad Setup CLI

One-command setup for your OBS macropad with Vial firmware.
Handles device detection, keymap generation, and setup instructions.

Usage:
    python setup-macropad.py                    # Interactive setup
    python setup-macropad.py --quick            # Quick automated setup
    python setup-macropad.py --test             # Test current setup
"""

import argparse
import sys
from pathlib import Path

# Import our automation module
sys.path.append(str(Path(__file__).parent / 'setup-scripts'))

try:
    from vial_setup_automation import VialAutomation
except ImportError:
    print("❌ Vial automation module not found")
    print("💡 Make sure you're running from the project root directory")
    sys.exit(1)

def interactive_setup():
    """Interactive setup wizard"""
    print("🎹 OBS Macropad Setup Wizard")
    print("=" * 40)
    
    automation = VialAutomation()
    
    # Step 1: Device Detection
    print("\n📍 Step 1: Detecting macropad...")
    device_info = automation.detect_vial_device()
    
    if not device_info:
        print("\n⚠️  No macropad detected!")
        print("📋 Before continuing, make sure:")
        print("   • Macropad is connected via USB")
        print("   • Vial firmware is flashed to the device")
        print("   • Device drivers are installed")
        
        continue_anyway = input("\n❓ Continue setup anyway? (y/N): ").lower().strip()
        if continue_anyway != 'y':
            print("Setup cancelled. Connect your macropad and try again.")
            return False
    else:
        print("✅ Macropad detected successfully!")
    
    # Step 2: Configuration Generation
    print("\n📍 Step 2: Generating configuration...")
    
    output_dir = automation.macropad_dir
    keymap_file = output_dir / "obs-control-keymap.json"
    instructions_file = output_dir / "automated-setup-instructions.md"
    
    # Generate keymap
    if automation.generate_vial_keymap(keymap_file):
        print("✅ Keymap configuration generated")
    else:
        print("❌ Failed to generate keymap")
        return False
    
    # Generate instructions
    if automation.generate_setup_instructions(instructions_file):
        print("✅ Setup instructions generated")
    else:
        print("❌ Failed to generate instructions")
        return False
    
    # Step 3: Validation
    print("\n📍 Step 3: Validating configuration...")
    if automation.validate_configuration(keymap_file):
        print("✅ Configuration validated successfully")
    else:
        print("❌ Configuration validation failed")
        return False
    
    # Step 4: Next Steps
    print("\n🎉 Macropad setup complete!")
    print(f"📁 Files created in: {output_dir}")
    print("\n📋 Next steps:")
    print("   1. Open Vial GUI application")
    print("   2. Connect your macropad")
    print(f"   3. Load keymap file: {keymap_file.name}")
    print(f"   4. Follow detailed instructions: {instructions_file.name}")
    
    # Ask about opening instructions
    try:
        open_instructions = input("\n❓ Open setup instructions now? (Y/n): ").lower().strip()
        if open_instructions != 'n':
            # Try to open the instructions file
            import subprocess
            import platform as plt
            
            if plt.system() == "Darwin":  # macOS
                subprocess.run(["open", str(instructions_file)])
            elif plt.system() == "Windows":
                subprocess.run(["start", str(instructions_file)], shell=True)
            else:  # Linux
                subprocess.run(["xdg-open", str(instructions_file)])
                
            print(f"📖 Instructions opened: {instructions_file}")
    except Exception:
        print(f"💡 Manually open: {instructions_file}")
    
    return True

def quick_setup():
    """Quick automated setup"""
    print("⚡ Quick Macropad Setup")
    print("=" * 30)
    
    automation = VialAutomation()
    
    print("🔍 Detecting device...")
    automation.detect_vial_device()
    
    print("🎹 Generating keymap...")
    keymap_file = automation.macropad_dir / "obs-control-keymap.json"
    automation.generate_vial_keymap(keymap_file)
    
    print("📋 Generating instructions...")
    instructions_file = automation.macropad_dir / "automated-setup-instructions.md"
    automation.generate_setup_instructions(instructions_file)
    
    print("✅ Validating...")
    automation.validate_configuration(keymap_file)
    
    print("\n🎉 Quick setup complete!")
    print(f"📁 Load in Vial: {keymap_file}")
    print(f"📖 Instructions: {instructions_file}")

def test_setup():
    """Test current macropad setup"""
    print("🧪 Testing Macropad Setup")
    print("=" * 30)
    
    automation = VialAutomation()
    
    # Test device detection
    print("\n📍 Testing device detection...")
    device_info = automation.detect_vial_device()
    
    if device_info:
        print("✅ Device detection: PASS")
    else:
        print("❌ Device detection: FAIL")
        print("   • Check USB connection")
        print("   • Verify Vial firmware")
    
    # Test configuration files
    print("\n📍 Testing configuration files...")
    
    keymap_file = automation.macropad_dir / "obs-control-keymap.json"
    instructions_file = automation.macropad_dir / "automated-setup-instructions.md"
    
    files_exist = keymap_file.exists() and instructions_file.exists()
    if files_exist:
        print("✅ Configuration files: EXIST")
    else:
        print("❌ Configuration files: MISSING")
        print("   • Run setup first")
    
    # Test validation
    if files_exist:
        print("\n📍 Testing configuration validation...")
        if automation.validate_configuration(keymap_file):
            print("✅ Configuration validation: PASS")
        else:
            print("❌ Configuration validation: FAIL")
    
    # Test key mappings
    print("\n📍 Key Mapping Summary:")
    for layer in automation.layers:
        print(f"   Layer {layer.layer_id} ({layer.name}): {len(layer.key_bindings)} keys")
    
    print("\n📋 Test Results Summary:")
    if device_info and files_exist:
        print("🎉 Setup appears ready for use!")
        print("💡 Test in Vial GUI to confirm functionality")
    else:
        print("⚠️  Setup incomplete - run full setup")

def main():
    parser = argparse.ArgumentParser(
        description='Simple OBS Macropad Setup',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup-macropad.py              # Interactive setup wizard
  python setup-macropad.py --quick      # Quick automated setup
  python setup-macropad.py --test       # Test current setup
        """
    )
    
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Quick automated setup without prompts'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test current macropad setup'
    )
    
    args = parser.parse_args()
    
    try:
        if args.quick:
            quick_setup()
        elif args.test:
            test_setup()
        else:
            # Interactive setup
            success = interactive_setup()
            if not success:
                print("\n❌ Setup failed. Check the errors above and try again.")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Please report this issue if it persists")
        sys.exit(1)

if __name__ == '__main__':
    main()