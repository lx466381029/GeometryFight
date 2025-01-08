from .player import Player
import pygame
import math
from typing import List, Optional

class Bullet:
    def __init__(self, x: float, y: float, dx: float, dy: float, speed: float, damage: float):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.radius = 3
        self.is_active = True
    
    def update(self):
        """更新子弹位置"""
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
    
    def render(self, screen: pygame.Surface):
        """渲染子弹"""
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius)

class Soldier(Player):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        
        # 士兵特有属性
        self.max_health = 120  # 较高的生命值
        self.health = self.max_health
        self.speed = 4.0      # 中等速度
        self.damage = 15      # 中等伤害
        self.attack_speed = 2.0  # 较快的攻击速度
        
        # 子弹属性
        self.bullet_speed = 10.0
        self.bullets: List[Bullet] = []
        
        # 技能：快速射击
        self.skill_cooldown = 8.0
        self.skill_duration = 3.0
        self.skill_attack_speed_bonus = 1.0  # 技能期间攻击速度翻倍
        self.skill_end_time: Optional[int] = None
    
    def update(self):
        """更新士兵状态"""
        super().update()
        
        # 更新技能状态
        if self.skill_end_time is not None:
            current_time = pygame.time.get_ticks()
            if current_time >= self.skill_end_time:
                self.end_skill()
        
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            # 检查子弹是否超出屏幕
            if not bullet.is_active:
                self.bullets.remove(bullet)
    
    def attack(self):
        """射击"""
        if not self.can_attack():
            return
        
        super().attack()
        
        # 创建子弹
        center_x, center_y = self.get_center()
        dx, dy = self.get_direction()
        bullet = Bullet(
            center_x, 
            center_y, 
            dx, 
            dy, 
            self.bullet_speed,
            self.get_damage()
        )
        self.bullets.append(bullet)
    
    def use_skill(self):
        """使用技能：快速射击"""
        if not self.is_skill_ready:
            return
        
        super().use_skill()
        
        # 添加攻击速度加成
        self.add_attribute_bonus("attack_speed_bonus", self.skill_attack_speed_bonus)
        
        # 设置技能结束时间
        self.skill_end_time = pygame.time.get_ticks() + int(self.skill_duration * 1000)
    
    def end_skill(self):
        """结束技能效果"""
        self.add_attribute_bonus("attack_speed_bonus", -self.skill_attack_speed_bonus)
        self.skill_end_time = None
    
    def render(self, screen: pygame.Surface):
        """渲染士兵和子弹"""
        super().render(screen)
        
        # 渲染子弹
        for bullet in self.bullets:
            bullet.render(screen)
    
    def level_up(self):
        """升级效果"""
        super().level_up()
        
        # 提升基础属性
        self.max_health += 10
        self.health = self.max_health
        self.damage += 2
        self.attack_speed += 0.1 