from .player import Player
import pygame
import math
from typing import List, Optional

class AssaultBullet:
    def __init__(self, x: float, y: float, dx: float, dy: float, speed: float, damage: float):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.radius = 2
        self.is_active = True
    
    def update(self):
        """更新子弹位置"""
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
    
    def render(self, screen: pygame.Surface):
        """渲染子弹"""
        pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), self.radius)

class Assault(Player):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        
        # 突击手特有属性
        self.max_health = 80   # 较低的生命值
        self.health = self.max_health
        self.speed = 6.0      # 较快的速度
        self.damage = 8       # 较低的单发伤害
        self.attack_speed = 4.0  # 较快的攻击速度
        
        # 子弹属性
        self.bullet_speed = 12.0
        self.bullets: List[AssaultBullet] = []
        self.bullets_per_shot = 1
        
        # 技能：爆发射击
        self.skill_cooldown = 10.0
        self.skill_duration = 2.0
        self.skill_attack_speed_bonus = 2.0  # 技能期间攻击速度翻三倍
        self.skill_bullets_per_shot = 2      # 技能期间每次射击2发子弹
        self.skill_end_time: Optional[int] = None
        
        # 颜色
        self.color = (255, 165, 0)  # 橙色
    
    def update(self):
        """更新突击手状态"""
        super().update()
        
        # 更新技能状态
        if self.skill_end_time is not None:
            current_time = pygame.time.get_ticks()
            if current_time >= self.skill_end_time:
                self.end_skill()
        
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active:
                self.bullets.remove(bullet)
    
    def attack(self):
        """射击"""
        if not self.can_attack():
            return
        
        super().attack()
        
        # 获取当前应该发射的子弹数量
        current_bullets = (self.skill_bullets_per_shot 
                         if self.skill_end_time is not None 
                         else self.bullets_per_shot)
        
        # 计算基础方向
        center_x, center_y = self.get_center()
        dx, dy = self.get_direction()
        
        # 创建子弹
        for i in range(current_bullets):
            # 添加一点随机偏移，模拟突击手的快速射击不太精确
            angle_offset = random.uniform(-5, 5)
            rad = math.radians(angle_offset)
            cos_offset = math.cos(rad)
            sin_offset = math.sin(rad)
            
            # 计算偏移后的方向
            new_dx = dx * cos_offset - dy * sin_offset
            new_dy = dx * sin_offset + dy * cos_offset
            
            bullet = AssaultBullet(
                center_x,
                center_y,
                new_dx,
                new_dy,
                self.bullet_speed,
                self.get_damage()
            )
            self.bullets.append(bullet)
    
    def use_skill(self):
        """使用技能：爆发射击"""
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
        """渲染突击手和子弹"""
        # 渲染突击手
        if self.image:
            super().render(screen)
        else:
            # 如果没有图像，绘制一个菱形
            center_x, center_y = self.get_center()
            points = [
                (center_x, center_y - self.height/2),  # 上
                (center_x + self.width/2, center_y),   # 右
                (center_x, center_y + self.height/2),  # 下
                (center_x - self.width/2, center_y)    # 左
            ]
            pygame.draw.polygon(screen, self.color, points)
        
        # 渲染子弹
        for bullet in self.bullets:
            bullet.render(screen)
    
    def level_up(self):
        """升级效果"""
        super().level_up()
        
        # 提升基础属性
        self.max_health += 5
        self.health = self.max_health
        self.damage += 1
        self.attack_speed += 0.2 