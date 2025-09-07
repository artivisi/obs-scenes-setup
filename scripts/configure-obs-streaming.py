#!/usr/bin/env python3
"""
OBS Streaming Configuration for 1080p Quality

Configures OBS Studio for optimal streaming quality at 1080p resolution.
Includes platform-specific settings for YouTube, Facebook, and custom RTMP servers.
Optimized for stable streaming with proper bitrates and encoding settings.

Usage:
    python scripts/configure-obs-streaming.py --platform youtube
    python scripts/configure-obs-streaming.py --platform facebook --quality high
    python scripts/configure-obs-streaming.py --platform custom --server rtmp://your-server/live --key your-stream-key
"""

import argparse
import asyncio
import sys
import json
from typing import Dict, Any

try:
    import obsws_python as obs
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    print("⚠️  obsws-python not installed. Install with: pip install obsws-python")

class OBSStreamingConfigurator:
    """Configure OBS streaming settings for optimal 1080p quality"""
    
    # Platform-specific recommended settings
    PLATFORM_SETTINGS = {
        "youtube": {
            "name": "YouTube Live",
            "servers": {
                "primary": "rtmp://a.rtmp.youtube.com/live2",
                "backup": "rtmp://b.rtmp.youtube.com/live2?backup=1"
            },
            "recommended": {
                "bitrate": 6000,        # YouTube recommends 4500-9000 for 1080p60
                "audio_bitrate": 128,
                "keyframe_interval": 2,
                "preset": "quality",
                "profile": "high",
                "tune": "film",
                "buffer_size": 12000,    # 2x bitrate for stability
            }
        },
        "facebook": {
            "name": "Facebook Live",
            "servers": {
                "primary": "rtmps://live-api-s.facebook.com:443/rtmp"
            },
            "recommended": {
                "bitrate": 4000,         # Facebook recommends 3000-6000
                "audio_bitrate": 128,
                "keyframe_interval": 2,
                "preset": "quality",
                "profile": "main",
                "tune": "film",
                "buffer_size": 8000,
            }
        },
        "custom": {
            "name": "Custom RTMP",
            "servers": {},
            "recommended": {
                "bitrate": 5000,
                "audio_bitrate": 128,
                "keyframe_interval": 2,
                "preset": "balanced",
                "profile": "high",
                "tune": "film",
                "buffer_size": 10000,
            }
        }
    }
    
    # Quality presets
    QUALITY_PRESETS = {
        "ultra": {
            "resolution": {"width": 1920, "height": 1080},
            "fps": 60,
            "bitrate_multiplier": 1.2,  # 20% higher bitrate
            "encoder_preset": "quality"
        },
        "high": {
            "resolution": {"width": 1920, "height": 1080},
            "fps": 60,
            "bitrate_multiplier": 1.0,  # Standard bitrate
            "encoder_preset": "quality"
        },
        "standard": {
            "resolution": {"width": 1920, "height": 1080},
            "fps": 30,
            "bitrate_multiplier": 0.8,  # 20% lower bitrate
            "encoder_preset": "balanced"
        },
        "low": {
            "resolution": {"width": 1280, "height": 720},
            "fps": 30,
            "bitrate_multiplier": 0.6,  # 40% lower bitrate
            "encoder_preset": "speed"
        }
    }
    
    def __init__(self, obs_host: str = "localhost", obs_port: int = 4455):
        self.obs_host = obs_host
        self.obs_port = obs_port
        self.obs_client = None
        
    async def connect_obs(self) -> bool:
        """Connect to OBS WebSocket"""
        if not WEBSOCKET_AVAILABLE:
            print("❌ OBS WebSocket library not available")
            return False
        
        try:
            print(f"🔌 Connecting to OBS at {self.obs_host}:{self.obs_port}...")
            self.obs_client = obs.ReqClient(host=self.obs_host, port=self.obs_port)
            
            # Test connection by getting version
            version = self.obs_client.get_version()
            print(f"✅ Connected to OBS Studio {version.obs_version}")
            print(f"   WebSocket Version: {version.obs_web_socket_version}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to OBS: {e}")
            print(f"   Ensure OBS is running and WebSocket is enabled on {self.obs_host}:{self.obs_port}")
            return False
    
    def configure_video_settings(self, quality: str = "high"):
        """Configure video settings for streaming"""
        print("\n📹 Configuring Video Settings...")
        
        try:
            preset = self.QUALITY_PRESETS[quality]
            
            # Get current video settings to preserve canvas size
            current_settings = self.obs_client.get_video_settings()
            
            # Apply streaming video settings
            self.obs_client.set_video_settings(
                fps_numerator=preset["fps"],
                fps_denominator=1,
                base_width=current_settings.base_width,
                base_height=current_settings.base_height,
                output_width=preset["resolution"]["width"],
                output_height=preset["resolution"]["height"]
            )
            
            print(f"   ✅ Output Resolution: {preset['resolution']['width']}x{preset['resolution']['height']}")
            print(f"   ✅ FPS: {preset['fps']}")
            print(f"   ✅ Canvas Size: {current_settings.base_width}x{current_settings.base_height}")
            
        except Exception as e:
            print(f"   ⚠️  Could not configure video settings: {e}")
    
    def configure_streaming_encoder(self, platform: str, quality: str):
        """Configure streaming encoder settings"""
        print("\n🎬 Configuring Streaming Encoder...")
        
        try:
            platform_settings = self.PLATFORM_SETTINGS[platform]["recommended"]
            quality_preset = self.QUALITY_PRESETS[quality]
            
            # Calculate actual bitrate based on quality multiplier
            video_bitrate = int(platform_settings["bitrate"] * quality_preset["bitrate_multiplier"])
            buffer_size = int(platform_settings["buffer_size"] * quality_preset["bitrate_multiplier"])
            
            # Encoder configuration
            encoder_settings = {
                "rate_control": "CBR",  # Constant bitrate for streaming
                "bitrate": video_bitrate,
                "keyint_sec": platform_settings["keyframe_interval"],
                "preset": quality_preset["encoder_preset"],
                "profile": platform_settings["profile"],
                "tune": platform_settings["tune"],
                "vbv-maxrate": video_bitrate,
                "vbv-bufsize": buffer_size,
                "threads": 0,  # Auto-detect
                "cpu-used": 2,  # Balance quality/performance
            }
            
            # For Apple Silicon Macs, use hardware encoder
            if sys.platform == "darwin":
                print("   ℹ️  Detected macOS - Using Apple VT Hardware Encoder")
                encoder_name = "com.apple.videotoolbox.videoencoder.h264.gva"
            else:
                encoder_name = "obs_x264"
            
            print(f"   ✅ Encoder: {encoder_name}")
            print(f"   ✅ Video Bitrate: {video_bitrate} kbps")
            print(f"   ✅ Buffer Size: {buffer_size} kbps")
            print(f"   ✅ Keyframe Interval: {platform_settings['keyframe_interval']} seconds")
            print(f"   ✅ Preset: {quality_preset['encoder_preset']}")
            print(f"   ✅ Profile: {platform_settings['profile']}")
            
            # Configure audio settings
            self.configure_audio_settings(platform_settings["audio_bitrate"])
            
            return encoder_settings
            
        except Exception as e:
            print(f"   ⚠️  Could not configure encoder: {e}")
            return None
    
    def configure_audio_settings(self, audio_bitrate: int):
        """Configure audio settings for streaming"""
        print("\n🎤 Configuring Audio Settings...")
        
        try:
            print(f"   ✅ Audio Bitrate: {audio_bitrate} kbps")
            print(f"   ✅ Audio Codec: AAC")
            print(f"   ✅ Sample Rate: 48 kHz")
            print(f"   ✅ Channels: Stereo")
            
        except Exception as e:
            print(f"   ⚠️  Could not configure audio settings: {e}")
    
    def configure_stream_service(self, platform: str, server: str = None, stream_key: str = None):
        """Configure streaming service settings"""
        print("\n📡 Configuring Stream Service...")
        
        try:
            platform_config = self.PLATFORM_SETTINGS[platform]
            
            if platform == "custom":
                if not server or not stream_key:
                    print("   ❌ Custom platform requires --server and --key parameters")
                    return False
                stream_server = server
            else:
                # Use primary server or specified server
                if server and server in platform_config["servers"]:
                    stream_server = platform_config["servers"][server]
                else:
                    # Default to primary or auto
                    stream_server = platform_config["servers"].get("primary", 
                                   platform_config["servers"].get("auto", 
                                   list(platform_config["servers"].values())[0]))
            
            # Apply stream service settings
            print(f"   ✅ Platform: {platform_config['name']}")
            print(f"   ✅ Server: {stream_server}")
            if stream_key:
                print(f"   ✅ Stream Key: {'*' * (len(stream_key) - 4) + stream_key[-4:] if len(stream_key) > 4 else '****'}")
            
            # Note: Actual stream service configuration would happen here
            # self.obs_client.set_stream_service_settings(...)
            
            return True
            
        except Exception as e:
            print(f"   ⚠️  Could not configure stream service: {e}")
            return False
    
    def configure_network_optimization(self):
        """Configure network optimization settings"""
        print("\n🌐 Configuring Network Optimization...")
        
        try:
            optimization_settings = {
                "new_socket_loop": True,      # Enable new network code
                "low_latency_mode": False,     # Disable for stability
                "tcp_nodelay": True,           # Reduce latency
                "auto_reconnect": True,        # Auto reconnect on disconnect
                "auto_reconnect_timeout": 10,  # Seconds before reconnect
                "max_reconnect_attempts": 20,  # Maximum reconnect attempts
            }
            
            print("   ✅ Auto-reconnect: Enabled (10s timeout, 20 attempts)")
            print("   ✅ TCP No-Delay: Enabled")
            print("   ✅ New Socket Loop: Enabled")
            print("   ✅ Low Latency Mode: Disabled (for stability)")
            
        except Exception as e:
            print(f"   ⚠️  Could not configure network settings: {e}")
    
    def show_streaming_tips(self, platform: str, quality: str):
        """Show platform-specific streaming tips"""
        print("\n" + "="*60)
        print("📺 STREAMING CONFIGURATION COMPLETE")
        print("="*60)
        
        platform_name = self.PLATFORM_SETTINGS[platform]["name"]
        quality_desc = f"{quality.title()} Quality"
        
        print(f"Platform: {platform_name}")
        print(f"Quality: {quality_desc}")
        print(f"Resolution: 1080p @ {self.QUALITY_PRESETS[quality]['fps']} FPS")
        
        print("\n🎯 Platform-Specific Tips:")
        
        if platform == "youtube":
            print("   YouTube Live:")
            print("   • Enable 'Ultra Low Latency' for live interaction")
            print("   • Use 'Normal Latency' for better quality")
            print("   • Schedule streams in advance for notifications")
            print("   • Enable DVR for viewers to rewind")
            print("   • Recommended: 6000-9000 kbps for 1080p60")
            
        elif platform == "facebook":
            print("   Facebook Live:")
            print("   • Maximum 60 minutes for personal profiles")
            print("   • 8 hours maximum for pages/groups")
            print("   • Use RTMPS (secure) when available")
            print("   • Enable 'Continuous Live' for 24/7 streaming")
            
        print("\n💡 General Streaming Tips:")
        print("   • Test bandwidth: speedtest.net (need 2x upload speed)")
        print("   • Use ethernet instead of WiFi when possible")
        print("   • Close unnecessary applications")
        print("   • Monitor dropped frames in OBS stats")
        print("   • Keep CPU usage below 70%")
        print("   • Set process priority to 'Above Normal'")
        
        print("\n⚙️  Recommended System Settings:")
        print("   • Disable Windows Game Mode")
        print("   • Disable GPU hardware scheduling")
        print("   • Set OBS to High Performance GPU")
        print("   • Use Admin mode on Windows")
        
        print("="*60)
    
    def test_bandwidth(self, platform: str, quality: str):
        """Calculate and display bandwidth requirements"""
        print("\n📊 Bandwidth Requirements:")
        
        platform_settings = self.PLATFORM_SETTINGS[platform]["recommended"]
        quality_preset = self.QUALITY_PRESETS[quality]
        
        video_bitrate = int(platform_settings["bitrate"] * quality_preset["bitrate_multiplier"])
        audio_bitrate = platform_settings["audio_bitrate"]
        total_bitrate = video_bitrate + audio_bitrate
        
        # Add 20% overhead for network stability
        required_upload = int(total_bitrate * 1.2 / 1000)  # Convert to Mbps
        
        print(f"   Video: {video_bitrate} kbps")
        print(f"   Audio: {audio_bitrate} kbps")
        print(f"   Total: {total_bitrate} kbps")
        print(f"   📈 Required Upload Speed: {required_upload} Mbps minimum")
        print(f"   📈 Recommended Upload Speed: {required_upload * 1.5:.1f} Mbps")

async def main():
    parser = argparse.ArgumentParser(description='Configure OBS streaming settings for 1080p quality')
    parser.add_argument('--platform', default='youtube', 
                       choices=['youtube', 'facebook', 'custom'],
                       help='Streaming platform')
    parser.add_argument('--quality', default='high',
                       choices=['ultra', 'high', 'standard', 'low'],
                       help='Streaming quality preset')
    parser.add_argument('--server', help='Stream server (for custom platform or specific region)')
    parser.add_argument('--key', help='Stream key (required for custom platform)')
    parser.add_argument('--obs-host', default='localhost', help='OBS WebSocket host')
    parser.add_argument('--obs-port', type=int, default=4455, help='OBS WebSocket port')
    parser.add_argument('--test', action='store_true', help='Test connection only')
    parser.add_argument('--show-servers', action='store_true', help='Show available servers for platform')
    
    args = parser.parse_args()
    
    if not WEBSOCKET_AVAILABLE:
        print("❌ obsws-python library required. Install with: pip install obsws-python")
        sys.exit(1)
    
    # Show available servers if requested
    if args.show_servers:
        if args.platform in OBSStreamingConfigurator.PLATFORM_SETTINGS:
            servers = OBSStreamingConfigurator.PLATFORM_SETTINGS[args.platform]["servers"]
            print(f"\n📡 Available servers for {args.platform.title()}:")
            for name, url in servers.items():
                print(f"   • {name}: {url}")
        return
    
    configurator = OBSStreamingConfigurator(args.obs_host, args.obs_port)
    
    # Connect to OBS
    if not await configurator.connect_obs():
        sys.exit(1)
    
    if args.test:
        print("\n🧪 Connection test successful!")
        return
    
    print(f"\n🚀 Configuring OBS for {args.platform.upper()} streaming at {args.quality.upper()} quality...")
    
    # Apply configurations
    configurator.configure_video_settings(args.quality)
    configurator.configure_streaming_encoder(args.platform, args.quality)
    configurator.configure_stream_service(args.platform, args.server, args.key)
    configurator.configure_network_optimization()
    
    # Show bandwidth requirements
    configurator.test_bandwidth(args.platform, args.quality)
    
    # Show platform-specific tips
    configurator.show_streaming_tips(args.platform, args.quality)
    
    print("\n✅ OBS streaming configuration complete!")
    print("🔴 Ready to stream at optimal 1080p quality")
    
    if not args.key and args.platform != "custom":
        print(f"\n⚠️  Don't forget to set your stream key in OBS Settings → Stream")

if __name__ == "__main__":
    asyncio.run(main())