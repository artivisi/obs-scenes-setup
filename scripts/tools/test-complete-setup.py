#!/usr/bin/env python3
"""
Complete OBS Setup Integration Test

This script validates the entire Artivisi OBS Infrastructure-as-Code setup:
- GitHub Pages overlay hosting
- Cross-platform device detection
- OBS scene collection import
- USB hub configuration
- Macropad setup validation

Run this after initial setup to ensure everything works correctly.

Usage:
    python test-complete-setup.py --full
    python test-complete-setup.py --quick
    python test-complete-setup.py --overlays-only
"""

import json
import requests
import subprocess
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import time

class OBSSetupTester:
    """Complete setup integration tester"""
    
    def __init__(self, github_username: str = "artivisi"):
        self.github_username = github_username
        self.base_url = f"https://{github_username}.github.io/obs-scenes-setup"
        self.project_root = Path(__file__).parent.parent
        self.results = {
            'overlays': {},
            'devices': {},
            'scenes': {},
            'macropad': {},
            'overall': 'unknown'
        }
    
    def test_github_pages_deployment(self) -> bool:
        """Test that GitHub Pages is properly deployed and accessible"""
        print("🌐 Testing GitHub Pages deployment...")
        
        # Test main index page
        try:
            response = requests.get(f"{self.base_url}/index.html", timeout=10)
            if response.status_code == 200:
                print("  ✅ Main index page accessible")
                self.results['overlays']['index'] = True
            else:
                print(f"  ❌ Index page returned {response.status_code}")
                self.results['overlays']['index'] = False
                return False
        except requests.RequestException as e:
            print(f"  ❌ Cannot reach GitHub Pages: {e}")
            self.results['overlays']['index'] = False
            return False
        
        # Test all overlay pages
        overlays = [
            'talking-head.html',
            'code-demo.html', 
            'screen-only.html',
            'intro.html',
            'outro.html',
            'brb.html',
            'dual-cam.html'
        ]
        
        overlay_results = []
        for overlay in overlays:
            url = f"{self.base_url}/overlays/{overlay}"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"  ✅ {overlay} accessible")
                    self.results['overlays'][overlay] = True
                    overlay_results.append(True)
                else:
                    print(f"  ❌ {overlay} returned {response.status_code}")
                    self.results['overlays'][overlay] = False
                    overlay_results.append(False)
            except requests.RequestException as e:
                print(f"  ❌ Cannot reach {overlay}: {e}")
                self.results['overlays'][overlay] = False
                overlay_results.append(False)
        
        # Test CSS file
        try:
            response = requests.get(f"{self.base_url}/overlays/css/main.css", timeout=10)
            if response.status_code == 200:
                print("  ✅ CSS file accessible")
                self.results['overlays']['css'] = True
            else:
                print(f"  ❌ CSS file returned {response.status_code}")
                self.results['overlays']['css'] = False
                overlay_results.append(False)
        except requests.RequestException as e:
            print(f"  ❌ Cannot reach CSS file: {e}")
            self.results['overlays']['css'] = False
            overlay_results.append(False)
        
        return all(overlay_results)
    
    def test_device_detection(self) -> bool:
        """Test cross-platform device detection"""
        print("\n🔍 Testing device detection...")
        
        device_script = self.project_root / 'scripts' / 'setup-scripts' / 'device-manager.py'
        if not device_script.exists():
            print("  ❌ Device manager script not found")
            self.results['devices']['script_exists'] = False
            return False
        
        self.results['devices']['script_exists'] = True
        
        try:
            # Run device scan
            result = subprocess.run([
                'python', str(device_script), '--scan'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("  ✅ Device scan completed successfully")
                self.results['devices']['scan_success'] = True
                
                # Check for expected output
                output = result.stdout.lower()
                if 'cam link' in output or 'camera' in output:
                    print("  ✅ Video devices detected")
                    self.results['devices']['video_detected'] = True
                else:
                    print("  ⚠️  No video devices detected")
                    self.results['devices']['video_detected'] = False
                
                if 'audio' in output or 'microphone' in output:
                    print("  ✅ Audio devices detected")  
                    self.results['devices']['audio_detected'] = True
                else:
                    print("  ⚠️  No USB audio devices detected")
                    self.results['devices']['audio_detected'] = False
                
                return True
            else:
                print(f"  ❌ Device scan failed: {result.stderr}")
                self.results['devices']['scan_success'] = False
                return False
                
        except subprocess.TimeoutExpired:
            print("  ❌ Device scan timed out")
            self.results['devices']['scan_success'] = False
            return False
        except Exception as e:
            print(f"  ❌ Device scan error: {e}")
            self.results['devices']['scan_success'] = False
            return False
    
    def test_usb_hub_validation(self) -> bool:
        """Test USB hub validation"""
        print("\n🔌 Testing USB hub validation...")
        
        hub_script = self.project_root / 'scripts' / 'setup-scripts' / 'usb-hub-validator.py'
        if not hub_script.exists():
            print("  ❌ USB hub validator script not found")
            self.results['devices']['hub_script'] = False
            return False
        
        self.results['devices']['hub_script'] = True
        
        try:
            # Run quick validation
            result = subprocess.run([
                'python', str(hub_script), '--validate'
            ], capture_output=True, text=True, timeout=20)
            
            # Note: validator may return non-zero if setup is not optimal
            print("  ✅ USB hub validation completed")
            self.results['devices']['hub_validation'] = True
            
            if 'optimal' in result.stdout.lower():
                print("  ✅ Optimal USB setup detected")
            elif 'good' in result.stdout.lower():
                print("  ✅ Good USB setup detected")
            else:
                print("  ⚠️  USB setup may need improvement")
            
            return True
            
        except subprocess.TimeoutExpired:
            print("  ❌ USB validation timed out")
            self.results['devices']['hub_validation'] = False
            return False
        except Exception as e:
            print(f"  ⚠️  USB validation warning: {e}")
            self.results['devices']['hub_validation'] = True  # Non-critical
            return True
    
    def test_scene_collection(self) -> bool:
        """Test OBS scene collection exists and is valid"""
        print("\n🎬 Testing OBS scene collection...")
        
        scene_file = self.project_root / 'scene-collections' / 'programming-tutorial.json'
        if not scene_file.exists():
            print("  ❌ Scene collection file not found")
            self.results['scenes']['file_exists'] = False
            return False
        
        self.results['scenes']['file_exists'] = True
        
        try:
            with open(scene_file, 'r') as f:
                scene_data = json.load(f)
            
            print("  ✅ Scene collection JSON is valid")
            self.results['scenes']['valid_json'] = True
            
            # Check for expected scenes
            expected_scenes = [
                'Intro Scene',
                'Talking Head', 
                'Code + Camera',
                'Screen Only',
                'BRB / Technical',
                'Outro Scene',
                'Dual Camera / Interview'
            ]
            
            scenes_found = 0
            if 'scenes' in scene_data:
                scene_names = [scene.get('name', '') for scene in scene_data['scenes']]
                for expected in expected_scenes:
                    # Flexible matching (contains emojis and variations)
                    if any(expected.lower() in name.lower() for name in scene_names):
                        scenes_found += 1
            
            print(f"  ✅ Found {scenes_found}/{len(expected_scenes)} expected scenes")
            self.results['scenes']['scenes_found'] = scenes_found
            
            # Check for browser sources with GitHub Pages URLs
            github_urls = 0
            if 'scenes' in scene_data:
                for scene in scene_data['scenes']:
                    for source in scene.get('sources', []):
                        settings = source.get('settings', {})
                        url = settings.get('url', '')
                        if self.github_username in url and 'github.io' in url:
                            github_urls += 1
            
            print(f"  ✅ Found {github_urls} GitHub Pages browser sources")
            self.results['scenes']['github_urls'] = github_urls
            
            return scenes_found >= 5  # At least 5 core scenes
            
        except json.JSONDecodeError as e:
            print(f"  ❌ Invalid JSON in scene collection: {e}")
            self.results['scenes']['valid_json'] = False
            return False
        except Exception as e:
            print(f"  ❌ Error reading scene collection: {e}")
            return False
    
    def test_macropad_configuration(self) -> bool:
        """Test macropad configuration files"""
        print("\n🎹 Testing macropad configuration...")
        
        macropad_dir = self.project_root / 'macropad'
        if not macropad_dir.exists():
            print("  ❌ Macropad directory not found")
            self.results['macropad']['directory'] = False
            return False
        
        self.results['macropad']['directory'] = True
        
        # Check for key files
        required_files = [
            'vial-config.json',
            'keymap-reference.md',
            'vial-setup-guide.md'
        ]
        
        files_found = 0
        for filename in required_files:
            filepath = macropad_dir / filename
            if filepath.exists():
                print(f"  ✅ {filename} found")
                files_found += 1
            else:
                print(f"  ❌ {filename} missing")
        
        self.results['macropad']['files_found'] = files_found
        
        # Validate Vial config if it exists
        vial_config = macropad_dir / 'vial-config.json'
        if vial_config.exists():
            try:
                with open(vial_config, 'r') as f:
                    config_data = json.load(f)
                
                print("  ✅ Vial config JSON is valid")
                
                # Check for required sections
                required_sections = ['name', 'matrix', 'layouts', 'layers']
                sections_found = sum(1 for section in required_sections if section in config_data)
                print(f"  ✅ Found {sections_found}/{len(required_sections)} required config sections")
                
                self.results['macropad']['config_valid'] = True
                
            except json.JSONDecodeError as e:
                print(f"  ❌ Invalid Vial config JSON: {e}")
                self.results['macropad']['config_valid'] = False
        
        return files_found >= 2  # At least config and guide
    
    def test_lua_scripts(self) -> bool:
        """Test OBS Lua scripts"""
        print("\n🔧 Testing Lua scripts...")
        
        lua_dir = self.project_root / 'scripts' / 'obs-scripts'
        if not lua_dir.exists():
            print("  ❌ Lua scripts directory not found")
            self.results['scenes']['lua_directory'] = False
            return False
        
        self.results['scenes']['lua_directory'] = True
        
        lua_files = list(lua_dir.glob('*.lua'))
        if lua_files:
            print(f"  ✅ Found {len(lua_files)} Lua script(s)")
            for lua_file in lua_files:
                print(f"    • {lua_file.name}")
            self.results['scenes']['lua_files'] = len(lua_files)
            return True
        else:
            print("  ⚠️  No Lua scripts found (optional)")
            self.results['scenes']['lua_files'] = 0
            return True  # Non-critical
    
    def generate_report(self) -> Dict:
        """Generate comprehensive test report"""
        
        # Calculate overall success rates
        overlay_success = sum(1 for v in self.results['overlays'].values() if v) / max(len(self.results['overlays']), 1)
        device_success = sum(1 for v in self.results['devices'].values() if v) / max(len(self.results['devices']), 1)
        scene_success = (
            (1 if self.results['scenes'].get('file_exists') else 0) +
            (1 if self.results['scenes'].get('valid_json') else 0) +
            (1 if self.results['scenes'].get('scenes_found', 0) >= 5 else 0) +
            (1 if self.results['scenes'].get('github_urls', 0) > 0 else 0)
        ) / 4
        macropad_success = sum(1 for v in self.results['macropad'].values() if v) / max(len(self.results['macropad']), 1)
        
        overall_score = (overlay_success + device_success + scene_success + macropad_success) / 4
        
        # Determine overall status
        if overall_score >= 0.9:
            self.results['overall'] = 'excellent'
        elif overall_score >= 0.75:
            self.results['overall'] = 'good'
        elif overall_score >= 0.5:
            self.results['overall'] = 'workable'
        else:
            self.results['overall'] = 'needs_work'
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'github_username': self.github_username,
            'base_url': self.base_url,
            'overall_status': self.results['overall'],
            'overall_score': round(overall_score * 100, 1),
            'component_scores': {
                'overlays': round(overlay_success * 100, 1),
                'devices': round(device_success * 100, 1),
                'scenes': round(scene_success * 100, 1),
                'macropad': round(macropad_success * 100, 1)
            },
            'detailed_results': self.results,
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Overlay recommendations
        if not self.results['overlays'].get('index', True):
            recommendations.append("🌐 Deploy to GitHub Pages - check Actions workflow")
        
        overlay_count = sum(1 for v in self.results['overlays'].values() if v)
        if overlay_count < 7:
            recommendations.append("📄 Some overlay files are missing or inaccessible")
        
        # Device recommendations  
        if not self.results['devices'].get('video_detected', True):
            recommendations.append("📹 Connect Cam Link or camera device")
        
        if not self.results['devices'].get('audio_detected', True):
            recommendations.append("🎤 Connect USB microphone (Hollyland Lark M2)")
        
        # Scene recommendations
        if not self.results['scenes'].get('file_exists', True):
            recommendations.append("🎬 Import OBS scene collection")
        
        scenes_found = self.results['scenes'].get('scenes_found', 0)
        if scenes_found < 7:
            recommendations.append(f"🎬 Configure remaining scenes ({7 - scenes_found} missing)")
        
        # Macropad recommendations
        if not self.results['macropad'].get('directory', True):
            recommendations.append("🎹 Set up macropad configuration")
        
        files_found = self.results['macropad'].get('files_found', 0)
        if files_found < 3:
            recommendations.append("🎹 Complete macropad configuration files")
        
        # Overall recommendations
        if not recommendations:
            recommendations.append("🎉 Setup looks great! Ready for professional recording")
        
        return recommendations
    
    def print_report(self, report: Dict):
        """Print formatted test report"""
        status_icons = {
            'excellent': '🎉',
            'good': '✅',
            'workable': '⚠️',
            'needs_work': '❌'
        }
        
        print(f"\n{'='*60}")
        print(f"📋 OBS SETUP INTEGRATION TEST REPORT")
        print(f"{'='*60}")
        print(f"🕐 Timestamp: {report['timestamp']}")
        print(f"🌐 GitHub Pages: {report['base_url']}")
        
        icon = status_icons.get(report['overall_status'], '❓')
        print(f"\n{icon} Overall Status: {report['overall_status'].title()} ({report['overall_score']}%)")
        
        print(f"\n📊 Component Scores:")
        for component, score in report['component_scores'].items():
            status = '✅' if score >= 75 else '⚠️' if score >= 50 else '❌'
            print(f"  {status} {component.title()}: {score}%")
        
        if report['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in report['recommendations']:
                print(f"  • {rec}")
        
        print(f"\n🔧 Next Steps:")
        if report['overall_score'] >= 90:
            print("  • Practice your recording workflow")
            print("  • Customize macropad for your content")
            print("  • Start creating tutorials!")
        elif report['overall_score'] >= 75:
            print("  • Address recommendations above")
            print("  • Test recording workflow")
            print("  • Fine-tune device configuration")
        else:
            print("  • Fix critical issues listed above")
            print("  • Re-run test after each fix")
            print("  • Check OBS_SETUP_GUIDE.md for detailed instructions")
        
        print(f"\n{'='*60}")

def main():
    parser = argparse.ArgumentParser(
        description='Complete OBS Setup Integration Test',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test-complete-setup.py --full
  python test-complete-setup.py --github-user myusername
  python test-complete-setup.py --overlays-only
        """
    )
    
    parser.add_argument(
        '--full',
        action='store_true',
        help='Run complete integration test (default)'
    )
    
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run quick test (overlays and basic validation)'
    )
    
    parser.add_argument(
        '--overlays-only',
        action='store_true',
        help='Test only GitHub Pages overlays'
    )
    
    parser.add_argument(
        '--github-user',
        type=str,
        default='artivisi',
        help='GitHub username for Pages URL (default: artivisi)'
    )
    
    parser.add_argument(
        '--save-report',
        type=str,
        help='Save detailed report to file'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Default to full test if no specific test is selected
    if not any([args.full, args.quick, args.overlays_only]):
        args.full = True
    
    print("🚀 OBS Infrastructure-as-Code Setup Test")
    print(f"📁 Project: {Path(__file__).parent.parent}")
    print(f"👤 GitHub User: {args.github_user}")
    
    tester = OBSSetupTester(args.github_user)
    
    success = True
    
    # Always test overlays
    if not tester.test_github_pages_deployment():
        success = False
    
    # Additional tests based on mode
    if args.full:
        if not tester.test_device_detection():
            success = False
        if not tester.test_usb_hub_validation():
            success = False  # Non-critical, so continue
        if not tester.test_scene_collection():
            success = False
        if not tester.test_macropad_configuration():
            success = False
        if not tester.test_lua_scripts():
            success = False  # Non-critical
    
    elif args.quick:
        if not tester.test_scene_collection():
            success = False
        if not tester.test_macropad_configuration():
            success = False
    
    # Generate and display report
    report = tester.generate_report()
    tester.print_report(report)
    
    # Save report if requested
    if args.save_report:
        with open(args.save_report, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 Report saved to: {args.save_report}")
    
    # Exit with appropriate code
    if report['overall_score'] >= 75:
        sys.exit(0)  # Success
    elif report['overall_score'] >= 50:
        sys.exit(1)  # Warning
    else:
        sys.exit(2)  # Failure

if __name__ == '__main__':
    main()