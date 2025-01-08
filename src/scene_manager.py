import pygame
from typing import Dict, Optional

class Scene:
    """场景基类"""
    def initialize(self):
        """初始化场景"""
        pass
    
    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        pass
    
    def update(self):
        """更新场景"""
        pass
    
    def render(self, screen: pygame.Surface):
        """渲染场景"""
        pass

class SceneManager:
    """场景管理器，负责管理和切换场景"""
    def __init__(self):
        self.scenes: Dict[str, Scene] = {}
        self.current_scene: Optional[Scene] = None
        self.current_scene_name: Optional[str] = None
    
    def register_scene(self, name: str, scene: Scene):
        """注册场景"""
        self.scenes[name] = scene
    
    def switch_scene(self, name: str):
        """切换场景"""
        if name in self.scenes:
            self.current_scene = self.scenes[name]
            self.current_scene_name = name
            self.current_scene.initialize()
    
    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        if self.current_scene:
            self.current_scene.handle_event(event)
    
    def update(self):
        """更新当前场景"""
        if self.current_scene:
            self.current_scene.update()
    
    def render(self, screen: pygame.Surface):
        """渲染当前场景"""
        if self.current_scene:
            self.current_scene.render(screen) 