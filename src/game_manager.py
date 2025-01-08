import pygame
from typing import Optional

class GameManager:
    """游戏管理器，负责管理游戏的全局状态"""
    def __init__(self):
        # 游戏状态
        self.running = True
        self.paused = False
        
        # 游戏设置
        self.screen_width = 1280
        self.screen_height = 720
        self.fps = 60
        
        # 游戏统计
        self.total_score = 0
        self.total_fragments = 0
        self.total_stars = 0
        self.total_play_time = 0
        
        # 游戏时钟
        self.clock = pygame.time.Clock()
        self.last_update_time = pygame.time.get_ticks()
    
    def update(self):
        """更新游戏状态"""
        if not self.paused:
            current_time = pygame.time.get_ticks()
            delta_time = current_time - self.last_update_time
            self.last_update_time = current_time
            
            # 更新游戏时间
            self.total_play_time += delta_time
    
    def pause(self):
        """暂停游戏"""
        self.paused = True
    
    def resume(self):
        """恢复游戏"""
        self.paused = False
        self.last_update_time = pygame.time.get_ticks()
    
    def quit(self):
        """退出游戏"""
        self.running = False
    
    def add_score(self, score: int):
        """增加得分"""
        self.total_score += score
    
    def add_fragments(self, amount: int):
        """增加碎片"""
        self.total_fragments += amount
    
    def add_stars(self, amount: int):
        """增加星星"""
        self.total_stars += amount
    
    def get_play_time_str(self) -> str:
        """获取游戏时间字符串"""
        total_seconds = self.total_play_time // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}" 