from .player import Player
from .bullet import PlayerBullet
import pygame
import math
from typing import List, Optional

class Tank(Player):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        
        # 坦克特有属性
        self.max_health = 150  # 最高的生命值
        self.health = self.max_health
        self.speed = 3.0      # 最慢的速度
        self.damage = 20      # 较高的伤害
        self.attack_speed = 1.5  # 较慢的攻击速度
        
        # 子弹属性
        self.bullet_speed = 8.0  # 最慢的子弹速度
        self.bullets: List[PlayerBullet] = []
        
        # 技能：护盾
        self.skill_cooldown = 12.0
        self.skill_duration = 4.0
        self.skill_defense_bonus = 0.5  # 技能期间减伤50%
        self.skill_end_time: Optional[int] = None
        
        # 创建坦克图像
        self._create_tank_image()
    
    def _create_tank_image(self):
        """创建坦克的几何图形图像"""
        try:
            # 创建一个带有透明度的表面
            image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # 绘制一个蓝色正方形
            center = (self.width // 2, self.height // 2)
            radius = min(self.width, self.height) // 2 - 2
            points = []
            for i in range(4):
                angle = math.pi * 2 / 4 * i
                x = center[0] + radius * math.cos(angle)
                y = center[1] + radius * math.sin(angle)
                points.append((x, y))
            
            pygame.draw.polygon(image, (30, 144, 255), points)
            pygame.draw.polygon(image, (0, 191, 255), points, 2)
            
            # 绘制一个小圆表示炮塔
            turret_pos = (center[0], center[1] - radius + 8)
            pygame.draw.circle(image, (135, 206, 250), turret_pos, 5)
            pygame.draw.circle(image, (0, 191, 255), turret_pos, 5, 1)
            
            self.set_image(image)
            print(f"为坦克 {self.__class__.__name__} 创建图像")
        
        except Exception as e:
            print(f"创建坦克图像时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def update(self):
        """更新坦克状态"""
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
            "tank"
        )
        self.bullets.append(bullet)
    
    def use_skill(self):
        """使用技能：护盾"""
        if not self.is_skill_ready:
            return
        
        super().use_skill()
        
        # 添加防御加成
        self.add_attribute_bonus("defense_bonus", self.skill_defense_bonus)
        
        # 设置技能结束时间
        self.skill_end_time = pygame.time.get_ticks() + int(self.skill_duration * 1000)
    
    def end_skill(self):
        """结束技能效果"""
        self.add_attribute_bonus("defense_bonus", -self.skill_defense_bonus)
        self.skill_end_time = None
    
    def render(self, screen: pygame.Surface):
        """渲染坦克和子弹"""
        # 渲染子弹
        for bullet in self.bullets:
            bullet.render(screen)
        
        # 渲染坦克
        super().render(screen)
    
    def level_up(self):
        """升级效果"""
        super().level_up()
        
        # 提升基础属性
        self.max_health += 12
        self.health = self.max_health
        self.damage += 2
        self.attack_speed += 0.1 