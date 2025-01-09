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
        self.fonts: Dict[str, Dict[int, pygame.font.Font]] = {}
        
        # 当前播放的音乐
        self.current_music: Optional[str] = None
        
        # 音量设置
        self.music_volume = 0.5
        self.sound_volume = 0.7
        
        print("初始化资源管理器")
        
        # 初始化音频
        try:
            pygame.mixer.init()
            print("音频系统初始化成功")
        except pygame.error as e:
            print(f"音频系统初始化失败: {e}")
        
        # 加载音频资源
        self._load_audio_resources()
        
        # 加载字体资源
        self._load_font_resources()
    
    def _load_audio_resources(self):
        """加载音频资源"""
        print("开始加载音频资源")
        
        # 加载背景音乐
        bgm_dir = "assets/audio/bgm"
        if os.path.exists(bgm_dir):
            print(f"扫描背景音乐目录: {bgm_dir}")
            for file in os.listdir(bgm_dir):
                if file.endswith(".mp3"):
                    name = os.path.splitext(file)[0]
                    self.music[name] = os.path.join(bgm_dir, file)
                    print(f"找到背景音乐: {name}")
        else:
            print(f"警告：背景音乐目录不存在: {bgm_dir}")
        
        # 加载音效
        sfx_dir = "assets/audio/sfx"
        if os.path.exists(sfx_dir):
            print(f"扫描音效目录: {sfx_dir}")
            for file in os.listdir(sfx_dir):
                if file.endswith(".mp3"):
                    name = os.path.splitext(file)[0]
                    try:
                        self.sounds[name] = pygame.mixer.Sound(os.path.join(sfx_dir, file))
                        self.sounds[name].set_volume(self.sound_volume)
                        print(f"加载音效: {name}")
                    except pygame.error as e:
                        print(f"加载音效失败 {name}: {e}")
        else:
            print(f"警告：音效目录不存在: {sfx_dir}")
        
        print(f"音频资源加载完成 - 背景音乐: {len(self.music)}个, 音效: {len(self.sounds)}个")
    
    def _load_font_resources(self):
        """加载字体资源"""
        print("开始加载字体资源")
        
        # 字体文件路径
        font_path = "assets/fonts/SourceHanSans-Regular.ttc"
        
        if not os.path.exists(font_path):
            print(f"警告：字体文件不存在: {font_path}")
            print("将使用系统默认字体")
            return
        
        try:
            # 预加载常用字号
            sizes = [16, 24, 32, 48, 64, 96]
            self.fonts['source_han_sans'] = {}
            
            for size in sizes:
                try:
                    self.fonts['source_han_sans'][size] = pygame.font.Font(font_path, size)
                    print(f"加载字体 source_han_sans 大小 {size}")
                except pygame.error as e:
                    print(f"加载字体失败 source_han_sans 大小 {size}: {e}")
                    # 使用系统默认字体作为后备
                    self.fonts['source_han_sans'][size] = pygame.font.SysFont(None, size)
            
            print("字体资源加载完成")
        except Exception as e:
            print(f"字体加载过程中发生错误: {e}")
            print("将使用系统默认字体")
    
    def get_font(self, size: int, font_name: str = 'source_han_sans') -> pygame.font.Font:
        """获取指定大小的字体"""
        if font_name not in self.fonts:
            print(f"警告：字体 {font_name} 不存在，使用系统默认字体")
            return pygame.font.SysFont(None, size)
        
        if size not in self.fonts[font_name]:
            print(f"加载新字号 {size} 的字体 {font_name}")
            try:
                font_path = "assets/fonts/SourceHanSans-Regular.ttc"
                if os.path.exists(font_path):
                    self.fonts[font_name][size] = pygame.font.Font(font_path, size)
                else:
                    self.fonts[font_name][size] = pygame.font.SysFont(None, size)
            except pygame.error as e:
                print(f"加载字体失败: {e}")
                self.fonts[font_name][size] = pygame.font.SysFont(None, size)
        
        return self.fonts[font_name][size]
    
    def load_image(self, path: str) -> pygame.Surface:
        """加载图片"""
        if path not in self.images:
            print(f"加载图片: {path}")
            try:
                self.images[path] = pygame.image.load(path).convert_alpha()
                print(f"图片加载成功: {path}")
            except pygame.error as e:
                print(f"无法加载图片 {path}: {e}")
                print("创建默认紫色方块作为替代")
                # 创建一个默认的紫色方块作为替代
                surface = pygame.Surface((32, 32))
                surface.fill((255, 0, 255))
                self.images[path] = surface
        return self.images[path]
    
    def play_music(self, name: str, loop: bool = True):
        """播放背景音乐"""
        if name in self.music and name != self.current_music:
            print(f"播放背景音乐: {name} {'(循环)' if loop else ''}")
            try:
                pygame.mixer.music.load(self.music[name])
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1 if loop else 0)
                self.current_music = name
                print(f"背景音乐 {name} 开始播放")
            except pygame.error as e:
                print(f"无法播放音乐 {name}: {e}")
        elif name not in self.music:
            print(f"错误：未找到背景音乐 {name}")
            print(f"当前可用的背景音乐: {', '.join(self.music.keys())}")
    
    def stop_music(self):
        """停止背景音乐"""
        if self.current_music:
            print(f"停止背景音乐: {self.current_music}")
            pygame.mixer.music.stop()
            self.current_music = None
    
    def play_sound(self, name: str):
        """播放音效"""
        if name in self.sounds:
            print(f"播放音效: {name}")
            try:
                self.sounds[name].play()
            except pygame.error as e:
                print(f"无法播放音效 {name}: {e}")
        else:
            print(f"错误：未找到音效 {name}")
            print(f"当前可用的音效: {', '.join(self.sounds.keys())}")
    
    def set_music_volume(self, volume: float):
        """设置背景音乐音量"""
        old_volume = self.music_volume
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        print(f"背景音乐音量从 {old_volume:.1%} 调整为 {self.music_volume:.1%}")
    
    def set_sound_volume(self, volume: float):
        """设置音效音量"""
        old_volume = self.sound_volume
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
        print(f"音效音量从 {old_volume:.1%} 调整为 {self.sound_volume:.1%}")
    
    def clear_cache(self):
        """清理资源缓存"""
        print("清理资源缓存")
        print(f"清理前 - 图片: {len(self.images)}个, 音效: {len(self.sounds)}个, 背景音乐: {len(self.music)}个")
        self.images.clear()
        self.sounds.clear()
        self.music.clear()
        self.current_music = None
        print("资源缓存已清理") 