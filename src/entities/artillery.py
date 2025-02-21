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
        self.radius = 5  # 炮弹较大
        self.is_active = True
    
    def update(self):
        """更新子弹位置"""
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
    
    def render(self, screen: pygame.Surface):
        """渲染子弹"""
        pygame.draw.circle(screen, (255, 50, 50), (int(self.x), int(self.y)), self.radius)

class Artillery(Player):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        
        # 炮兵特有属性
        self.max_health = 80   # 较低的生命值
        self.health = self.max_health
        self.speed = 3.0      # 较慢的速度
        self.damage = 30      # 高伤害
        self.attack_speed = 1.0  # 较慢的攻击速度
        
        # 子弹属性
        self.bullet_speed = 8.0
        self.bullets: List[Bullet] = []
        
        # 技能：炮击
        self.skill_cooldown = 12.0
        self.skill_duration = 0.5
        self.skill_damage_bonus = 2.0  # 技能期间伤害翻倍
        self.skill_end_time: Optional[int] = None
        
        # 创建炮兵图像
        self._create_artillery_image()
    
    def _create_artillery_image(self):
        """创建炮兵的几何图形图像"""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # 绘制一个红色正方形
        center = (self.width // 2, self.height // 2)
        size = min(self.width, self.height) - 4
        rect = pygame.Rect(
            center[0] - size // 2,
            center[1] - size // 2,
            size,
            size
        )
        
        pygame.draw.rect(image, (200, 50, 50), rect)
        pygame.draw.rect(image, (255, 100, 100), rect, 2)
        
        # 绘制一个小圆表示炮口
        muzzle_pos = (center[0] + size // 2 - 2, center[1])
        pygame.draw.circle(image, (255, 150, 150), muzzle_pos, 4)
        
        self.set_image(image)
    
    def update(self):
        """更新炮兵状态"""
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
        """使用技能：炮击"""
        if not self.is_skill_ready:
            return
        
        super().use_skill()
        
        # 添加伤害加成
        self.add_attribute_bonus("damage_bonus", self.skill_damage_bonus)
        
        # 设置技能结束时间
        self.skill_end_time = pygame.time.get_ticks() + int(self.skill_duration * 1000)
    
    def end_skill(self):
        """结束技能效果"""
        self.add_attribute_bonus("damage_bonus", -self.skill_damage_bonus)
        self.skill_end_time = None
    
    def render(self, screen: pygame.Surface):
        """渲染炮兵和子弹"""
        super().render(screen)
        
        # 渲染子弹
        for bullet in self.bullets:
            bullet.render(screen)
    
    def level_up(self):
        """升级效果"""
        super().level_up()
        
        # 提升基础属性
        self.max_health += 6
        self.health = self.max_health
        self.damage += 4
        self.attack_speed += 0.05 