#!/usr/bin/env python3
"""
Scene Generation Utilities
Reusable components for generating OBS scene configurations.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import json


@dataclass
class Transform:
    """OBS source transform properties"""
    pos: Dict[str, float]
    rot: float = 0.0
    scale: Dict[str, float] = None
    alignment: int = 5
    bounds_type: int = 0
    bounds_alignment: int = 0
    bounds: Dict[str, float] = None
    
    def __post_init__(self):
        if self.scale is None:
            self.scale = {"x": 1.0, "y": 1.0}
        if self.bounds is None:
            self.bounds = {"x": 0.0, "y": 0.0}


@dataclass
class Crop:
    """OBS source crop properties"""
    left: int = 0
    top: int = 0
    right: int = 0
    bottom: int = 0


@dataclass
class SourceItem:
    """OBS scene source item configuration"""
    name: str
    source_uuid: str
    visible: bool = True
    locked: bool = False
    transform: Transform = None
    crop: Crop = None
    scale_filter: str = "lanczos"
    blend_method: str = "default"
    blend_type: str = "normal"
    
    def __post_init__(self):
        if self.transform is None:
            self.transform = Transform(pos={"x": 0.0, "y": 0.0})
        if self.crop is None:
            self.crop = Crop()


@dataclass
class SceneTemplate:
    """Template for creating OBS scenes"""
    name: str
    description: str
    sources: List[SourceItem]
    hotkey: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "name": self.name,
            "description": self.description,
            "sources": [asdict(source) for source in self.sources],
            "hotkey": self.hotkey
        }


class SceneLayoutManager:
    """Manages common scene layouts and positioning"""
    
    # Standard canvas resolution
    CANVAS_WIDTH = 1920
    CANVAS_HEIGHT = 1080
    
    # Common margins
    MARGIN = 60
    SMALL_MARGIN = 30
    
    # Common camera sizes
    CAMERA_SIZES = {
        "large": {"width": 640, "height": 480},
        "medium": {"width": 400, "height": 300}, 
        "small": {"width": 240, "height": 180},
        "pip": {"width": 320, "height": 240}
    }
    
    @classmethod
    def get_position(cls, location: str, size: str = "medium") -> Dict[str, float]:
        """Get position coordinates for common locations"""
        camera_size = cls.CAMERA_SIZES.get(size, cls.CAMERA_SIZES["medium"])
        
        positions = {
            # Corners
            "top-left": {"x": cls.MARGIN, "y": cls.MARGIN},
            "top-right": {"x": cls.CANVAS_WIDTH - camera_size["width"] - cls.MARGIN, "y": cls.MARGIN},
            "bottom-left": {"x": cls.MARGIN, "y": cls.CANVAS_HEIGHT - camera_size["height"] - cls.MARGIN},
            "bottom-right": {"x": cls.CANVAS_WIDTH - camera_size["width"] - cls.MARGIN, 
                           "y": cls.CANVAS_HEIGHT - camera_size["height"] - cls.MARGIN},
            
            # Centers
            "center": {"x": (cls.CANVAS_WIDTH - camera_size["width"]) / 2, 
                      "y": (cls.CANVAS_HEIGHT - camera_size["height"]) / 2},
            "top-center": {"x": (cls.CANVAS_WIDTH - camera_size["width"]) / 2, "y": cls.MARGIN},
            "bottom-center": {"x": (cls.CANVAS_WIDTH - camera_size["width"]) / 2, 
                            "y": cls.CANVAS_HEIGHT - camera_size["height"] - cls.MARGIN},
            
            # Full canvas
            "fullscreen": {"x": 0.0, "y": 0.0}
        }
        
        return positions.get(location, positions["center"])
    
    @classmethod
    def get_scale_for_size(cls, target_size: str, source_resolution: Tuple[int, int] = (1920, 1080)) -> Dict[str, float]:
        """Calculate scale factors for target size"""
        camera_size = cls.CAMERA_SIZES.get(target_size, cls.CAMERA_SIZES["medium"])
        source_width, source_height = source_resolution
        
        scale_x = camera_size["width"] / source_width
        scale_y = camera_size["height"] / source_height
        
        return {"x": scale_x, "y": scale_y}
    
    @classmethod
    def create_camera_transform(cls, position: str, size: str = "medium", 
                               source_resolution: Tuple[int, int] = (1920, 1080)) -> Transform:
        """Create transform for camera positioning"""
        pos = cls.get_position(position, size)
        scale = cls.get_scale_for_size(size, source_resolution)
        camera_size = cls.CAMERA_SIZES[size]
        
        return Transform(
            pos=pos,
            scale=scale,
            bounds={"x": camera_size["width"], "y": camera_size["height"]},
            alignment=5
        )
    
    @classmethod
    def create_fullscreen_transform(cls) -> Transform:
        """Create transform for fullscreen sources"""
        return Transform(
            pos={"x": 0.0, "y": 0.0},
            scale={"x": 1.0, "y": 1.0},
            bounds={"x": cls.CANVAS_WIDTH, "y": cls.CANVAS_HEIGHT},
            alignment=5
        )


class CommonScenes:
    """Factory for creating common scene types"""
    
    @staticmethod
    def create_intro_scene(overlay_url: str) -> SceneTemplate:
        """Create intro scene template"""
        overlay_source = SourceItem(
            name="Intro Overlay",
            source_uuid="intro-overlay-uuid",
            transform=SceneLayoutManager.create_fullscreen_transform()
        )
        
        return SceneTemplate(
            name="🎬 Intro Scene",
            description="Event introduction with branding",
            sources=[overlay_source],
            hotkey="F1"
        )
    
    @staticmethod
    def create_talking_head_scene(camera_uuid: str, overlay_url: str) -> SceneTemplate:
        """Create talking head scene template"""
        camera_source = SourceItem(
            name="Main Camera",
            source_uuid=camera_uuid,
            transform=SceneLayoutManager.create_camera_transform("center", "large")
        )
        
        overlay_source = SourceItem(
            name="Talking Head Overlay", 
            source_uuid="talking-head-overlay-uuid",
            transform=SceneLayoutManager.create_fullscreen_transform()
        )
        
        return SceneTemplate(
            name="👤 Talking Head",
            description="Full camera view with minimal overlay",
            sources=[camera_source, overlay_source],
            hotkey="F2"
        )
    
    @staticmethod
    def create_code_camera_scene(screen_uuid: str, camera_uuid: str, overlay_url: str) -> SceneTemplate:
        """Create code + camera scene template"""
        screen_source = SourceItem(
            name="Screen Capture",
            source_uuid=screen_uuid,
            transform=SceneLayoutManager.create_fullscreen_transform()
        )
        
        camera_source = SourceItem(
            name="PiP Camera",
            source_uuid=camera_uuid,
            transform=SceneLayoutManager.create_camera_transform("top-right", "medium")
        )
        
        overlay_source = SourceItem(
            name="Code Demo Overlay",
            source_uuid="code-demo-overlay-uuid", 
            transform=SceneLayoutManager.create_fullscreen_transform()
        )
        
        return SceneTemplate(
            name="💻 Code + Camera",
            description="Screen capture with picture-in-picture camera",
            sources=[screen_source, camera_source, overlay_source],
            hotkey="F3"
        )
    
    @staticmethod
    def create_screen_only_scene(screen_uuid: str, camera_uuid: str, overlay_url: str) -> SceneTemplate:
        """Create screen-only scene template"""
        screen_source = SourceItem(
            name="Full Screen",
            source_uuid=screen_uuid,
            transform=SceneLayoutManager.create_fullscreen_transform()
        )
        
        camera_source = SourceItem(
            name="Mini Camera",
            source_uuid=camera_uuid,
            transform=SceneLayoutManager.create_camera_transform("bottom-right", "small")
        )
        
        overlay_source = SourceItem(
            name="Screen Only Overlay",
            source_uuid="screen-only-overlay-uuid",
            transform=SceneLayoutManager.create_fullscreen_transform()
        )
        
        return SceneTemplate(
            name="🖥️ Screen Only",
            description="Full screen with minimal camera overlay",
            sources=[screen_source, camera_source, overlay_source],
            hotkey="F4"
        )
    
    @staticmethod
    def create_dual_camera_scene(camera1_uuid: str, camera2_uuid: str, overlay_url: str) -> SceneTemplate:
        """Create dual camera scene template"""
        camera1_source = SourceItem(
            name="Main Camera",
            source_uuid=camera1_uuid,
            transform=Transform(
                pos={"x": SceneLayoutManager.MARGIN, "y": SceneLayoutManager.MARGIN},
                scale={"x": 0.333, "y": 0.444},
                bounds={"x": 640, "y": 480},
                alignment=5
            )
        )
        
        camera2_source = SourceItem(
            name="Secondary Camera", 
            source_uuid=camera2_uuid,
            transform=Transform(
                pos={"x": 1220, "y": SceneLayoutManager.MARGIN},
                scale={"x": 0.333, "y": 0.444},
                bounds={"x": 640, "y": 480},
                alignment=5
            )
        )
        
        overlay_source = SourceItem(
            name="Dual Camera Overlay",
            source_uuid="dual-cam-overlay-uuid",
            transform=SceneLayoutManager.create_fullscreen_transform()
        )
        
        return SceneTemplate(
            name="👥 Dual Camera / Interview",
            description="Two camera feeds side by side",
            sources=[camera1_source, camera2_source, overlay_source],
            hotkey="F7"
        )


class SceneCollectionBuilder:
    """Builds complete OBS scene collections"""
    
    def __init__(self, collection_name: str = "Generated Scenes"):
        self.collection_name = collection_name
        self.scenes = []
        self.sources = []
        self.current_scene = None
        self.transitions = []
        self.hotkeys = {}
    
    def add_scene(self, scene_template: SceneTemplate) -> 'SceneCollectionBuilder':
        """Add a scene to the collection"""
        self.scenes.append(scene_template)
        
        # Set first scene as current scene
        if not self.current_scene:
            self.current_scene = scene_template.name
            
        # Add hotkey mapping
        if scene_template.hotkey:
            self.hotkeys[scene_template.hotkey] = scene_template.name
            
        return self
    
    def add_common_transitions(self) -> 'SceneCollectionBuilder':
        """Add standard transitions"""
        self.transitions = [
            {"name": "Cut", "duration": 300, "hotkeys": ["T"], "id": 1},
            {"name": "Fade", "duration": 300, "hotkeys": [], "id": 2}
        ]
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build the complete scene collection"""
        return {
            "name": self.collection_name,
            "current_scene": self.current_scene,
            "current_program_scene": self.current_scene,
            "scene_order": [{"name": scene.name, "uuid": f"scene-{i}"} for i, scene in enumerate(self.scenes)],
            "scenes": [self._build_scene_dict(scene, i) for i, scene in enumerate(self.scenes)],
            "sources": self.sources,
            "quick_transitions": self.transitions,
            "current_transition": "Fade",
            "transition_duration": 300,
            "groups": [],
            "modules": {
                "auto-scene-switcher": {},
                "scripts": {},
                "output-timer": {}
            },
            "hotkeys": self._build_hotkeys()
        }
    
    def _build_scene_dict(self, scene: SceneTemplate, index: int) -> Dict[str, Any]:
        """Build scene dictionary for OBS format"""
        return {
            "uuid": f"scene-{index}",
            "id": index + 1,
            "name": scene.name,
            "sources": [asdict(source) for source in scene.sources]
        }
    
    def _build_hotkeys(self) -> Dict[str, Any]:
        """Build hotkey mappings"""
        hotkey_dict = {}
        for key, scene_name in self.hotkeys.items():
            obs_key = f"OBS_KEY_{key}"
            hotkey_dict[obs_key] = [{"scene_name": scene_name}]
        return hotkey_dict
    
    def save_to_file(self, output_path: Path) -> None:
        """Save scene collection to JSON file"""
        collection_data = self.build()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(collection_data, f, indent=2, ensure_ascii=False)