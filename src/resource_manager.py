import pygame
from typing import Dict, Optional
import os

class ResourceManager:
    """资源管理器，负责加载和管理游戏资源"""
    def __init__(self):
        # 资源缓存
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music: Dict[str, str] = {}
        
        # 当前播放的音乐
        self.current_music: Optional[str] = None
        
        # 音量设置
        self.music_volume = 0.5
        self.sound_volume = 0.7
        
        # 初始化音频
        pygame.mixer.init()
        
        # 加载音频资源
        self._load_audio_resources()
    
    def _load_audio_resources(self):
        """加载音频资源"""
        # 加载背景音乐
        bgm_dir = "assets/audio/bgm"
        if os.path.exists(bgm_dir):
            for file in os.listdir(bgm_dir):
                if file.endswith(".mp3"):
                    name = os.path.splitext(file)[0]
                    self.music[name] = os.path.join(bgm_dir, file)
        
        # 加载音效
        sfx_dir = "assets/audio/sfx"
        if os.path.exists(sfx_dir):
            for file in os.listdir(sfx_dir):
                if file.endswith(".mp3"):
                    name = os.path.splitext(file)[0]
                    self.sounds[name] = pygame.mixer.Sound(os.path.join(sfx_dir, file))
                    self.sounds[name].set_volume(self.sound_volume)
    
    def load_image(self, path: str) -> pygame.Surface:
        """加载图片"""
        if path not in self.images:
            try:
                self.images[path] = pygame.image.load(path).convert_alpha()
            except pygame.error as e:
                print(f"无法加载图片 {path}: {e}")
                # 创建一个默认的紫色方块作为替代
                surface = pygame.Surface((32, 32))
                surface.fill((255, 0, 255))
                self.images[path] = surface
        return self.images[path]
    
    def play_music(self, name: str, loop: bool = True):
        """播放背景音乐"""
        if name in self.music and name != self.current_music:
            try:
                pygame.mixer.music.load(self.music[name])
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1 if loop else 0)
                self.current_music = name
            except pygame.error as e:
                print(f"无法播放音乐 {name}: {e}")
    
    def stop_music(self):
        """停止背景音乐"""
        pygame.mixer.music.stop()
        self.current_music = None
    
    def play_sound(self, name: str):
        """播放音效"""
        if name in self.sounds:
            try:
                self.sounds[name].play()
            except pygame.error as e:
                print(f"无法播放音效 {name}: {e}")
    
    def set_music_volume(self, volume: float):
        """设置背景音乐音量"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sound_volume(self, volume: float):
        """设置音效音量"""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
    
    def clear_cache(self):
        """清理资源缓存"""
        self.images.clear()
        self.sounds.clear()
        self.music.clear()
        self.current_music = None 