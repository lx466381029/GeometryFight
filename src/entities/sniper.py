from .player import Player
from .bullet import PlayerBullet
import pygame
import math
from typing import List, Optional

class Sniper(Player):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        
        # 狙击手特有属性
        self.max_health = 80   # 较低的生命值
        self.health = self.max_health
        self.speed = 4.0       # 较慢的速度
        self.damage = 35       # 最高的伤害
        self.attack_speed = 1.0  # 最慢的攻击速度
        
        # 子弹属性
        self.bullet_speed = 20.0  # 最快的子弹速度
        self.bullets: List[PlayerBullet] = []
        
        # 技能：瞄准
        self.skill_cooldown = 8.0
        self.skill_duration = 3.0
        self.skill_damage_bonus = 2.0  # 技能期间伤害翻倍
        self.skill_end_time: Optional[int] = None
        
        # 创建狙击手图像
        self._create_sniper_image()
    
    def _create_sniper_image(self):
        """创建狙击手的几何图形图像"""
        try:
            # 创建一个带有透明度的表面
            image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # 绘制一个红色菱形
            center = (self.width // 2, self.height // 2)
            radius = min(self.width, self.height) // 2 - 2
            points = []
            for i in range(4):
                angle = math.pi * 2 / 4 * i - math.pi / 4
                x = center[0] + radius * math.cos(angle)
                y = center[1] + radius * math.sin(angle)
                points.append((x, y))
            
            pygame.draw.polygon(image, (220, 20, 60), points)
            pygame.draw.polygon(image, (255, 0, 0), points, 2)
            
            # 绘制一个小圆表示瞄准镜
            scope_pos = (center[0], center[1] - radius + 6)
            pygame.draw.circle(image, (200, 0, 0), scope_pos, 4)
            pygame.draw.circle(image, (255, 0, 0), scope_pos, 4, 1)
            
            self.set_image(image)
            print(f"为狙击手 {self.__class__.__name__} 创建图像")
        
        except Exception as e:
            print(f"创建狙击手图像时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def update(self):
        """更新狙击手状态"""
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
        bullet = PlayerBullet(
            center_x, 
            center_y, 
            dx, 
            dy, 
            self.bullet_speed,
            self.get_damage(),
            "sniper"
        )
        self.bullets.append(bullet)
    
    def use_skill(self):
        """使用技能：瞄准"""
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
        """渲染狙击手和子弹"""
        # 渲染子弹
        for bullet in self.bullets:
            bullet.render(screen)
        
        # 渲染狙击手
        super().render(screen)
    
    def level_up(self):
        """升级效果"""
        super().level_up()
        
        # 提升基础属性
        self.max_health += 6
        self.health = self.max_health
        self.damage += 3.5
        self.attack_speed += 0.08 