import pygame
from typing import Optional, Tuple
from .character import Character
import math

class Player(Character):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        
        # 玩家特有属性
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        
        # 资源
        self.fragments = 0  # 碎片
        self.stars = 0      # 星星
        
        # 技能相关
        self.skill_cooldown = 5.0  # 技能冷却时间（秒）
        self.last_skill_time = 0
        self.is_skill_ready = True
        
        # 移动控制
        self.move_keys = {
            pygame.K_w: (0, -1),
            pygame.K_s: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0)
        }
    
    def update(self):
        """更新玩家状态"""
        super().update()
        
        # 更新技能冷却
        current_time = pygame.time.get_ticks()
        if not self.is_skill_ready and current_time - self.last_skill_time >= self.skill_cooldown * 1000:
            self.is_skill_ready = True
    
    def handle_input(self, keys, mouse_pos: Tuple[int, int], mouse_buttons: Tuple[int, ...]):
        """处理输入"""
        # 处理移动
        dx = dy = 0
        for key, (move_x, move_y) in self.move_keys.items():
            if keys[key]:
                dx += move_x
                dy += move_y
        
        # 标准化移动向量
        if dx != 0 or dy != 0:
            length = math.sqrt(dx * dx + dy * dy)
            dx /= length
            dy /= length
            self.move(dx, dy)
        
        # 处理旋转（朝向鼠标）
        center_x, center_y = self.get_center()
        mouse_x, mouse_y = mouse_pos
        angle = math.degrees(math.atan2(mouse_y - center_y, mouse_x - center_x))
        self.set_rotation(angle)
        
        # 处理攻击
        if mouse_buttons[0]:  # 左键射击
            self.attack()
        
        if mouse_buttons[2] and self.is_skill_ready:  # 右键技能
            self.use_skill()
    
    def use_skill(self):
        """使用技能"""
        if not self.is_skill_ready:
            return
        
        self.is_skill_ready = False
        self.last_skill_time = pygame.time.get_ticks()
        # 具体技能效果由子类实现
    
    def add_experience(self, amount: int):
        """增加经验值"""
        self.experience += amount
        while self.experience >= self.experience_to_next_level:
            self.level_up()
    
    def level_up(self):
        """升级"""
        self.experience -= self.experience_to_next_level
        self.level += 1
        self.experience_to_next_level = int(self.experience_to_next_level * 1.2)
        # 具体升级效果由子类实现
    
    def add_fragments(self, amount: int):
        """增加碎片"""
        self.fragments += amount
    
    def add_stars(self, amount: int):
        """增加星星"""
        self.stars += amount
    
    def get_skill_cooldown_percentage(self) -> float:
        """获取技能冷却进度（0-1）"""
        if self.is_skill_ready:
            return 1.0
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_skill_time) / 1000
        return min(elapsed / self.skill_cooldown, 1.0) 