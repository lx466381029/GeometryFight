from .player import Player
import pygame
import math
import random
from typing import List, Optional, Tuple

class ArtilleryShell:
    def __init__(self, x: float, y: float, dx: float, dy: float, speed: float, 
                 damage: float, explosion_radius: float, explosion_damage: float):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.radius = 4
        self.is_active = True
        self.explosion_radius = explosion_radius
        self.explosion_damage = explosion_damage
        self.exploding = False
        self.explosion_time = 0
        self.explosion_duration = 200  # 爆炸持续200毫秒
    
    def update(self):
        """更新炮弹位置"""
        if self.exploding:
            current_time = pygame.time.get_ticks()
            if current_time - self.explosion_time >= self.explosion_duration:
                self.is_active = False
            return
        
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
    
    def explode(self):
        """触发爆炸"""
        if not self.exploding:
            self.exploding = True
            self.explosion_time = pygame.time.get_ticks()
    
    def render(self, screen: pygame.Surface):
        """渲染炮弹或爆炸效果"""
        if self.exploding:
            # 渲染爆炸效果
            progress = (pygame.time.get_ticks() - self.explosion_time) / self.explosion_duration
            radius = int(self.explosion_radius * (1 - progress))
            alpha = int(255 * (1 - progress))
            
            # 创建一个临时surface来绘制半透明的爆炸效果
            explosion_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(explosion_surface, (255, 100, 0, alpha), 
                             (radius, radius), radius)
            screen.blit(explosion_surface, 
                       (int(self.x - radius), int(self.y - radius)))
        else:
            # 渲染炮弹
            pygame.draw.circle(screen, (139, 69, 19), 
                             (int(self.x), int(self.y)), self.radius)

class Artillery(Player):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        
        # 炮兵特有属性
        self.max_health = 70   # 最低的生命值
        self.health = self.max_health
        self.speed = 3.5      # 最慢的速度
        self.damage = 25      # 最高的伤害
        self.attack_speed = 0.8  # 最慢的攻击速度
        
        # 炮弹属性
        self.shell_speed = 8.0
        self.shells: List[ArtilleryShell] = []
        self.explosion_radius = 60.0
        self.explosion_damage_multiplier = 0.5  # 爆炸伤害为基础伤害的50%
        
        # 技能：炮火覆盖
        self.skill_cooldown = 15.0
        self.skill_duration = 3.0
        self.skill_shells = 6  # 技能期间发射的炮弹数量
        self.skill_interval = 0.4  # 技能期间炮弹发射间隔（秒）
        self.skill_end_time: Optional[int] = None
        self.next_skill_shell_time: Optional[int] = None
        self.remaining_skill_shells = 0
        
        # 颜色
        self.color = (139, 69, 19)  # 棕色
    
    def update(self):
        """更新炮兵状态"""
        super().update()
        
        # 更新技能状态
        current_time = pygame.time.get_ticks()
        
        if self.skill_end_time is not None:
            if current_time >= self.skill_end_time:
                self.end_skill()
            elif (self.remaining_skill_shells > 0 and 
                  current_time >= self.next_skill_shell_time):
                self.fire_skill_shell()
        
        # 更新炮弹
        for shell in self.shells[:]:
            shell.update()
            if not shell.is_active:
                self.shells.remove(shell)
    
    def attack(self):
        """发射炮弹"""
        if not self.can_attack():
            return
        
        super().attack()
        
        # 创建炮弹
        center_x, center_y = self.get_center()
        dx, dy = self.get_direction()
        
        shell = ArtilleryShell(
            center_x,
            center_y,
            dx,
            dy,
            self.shell_speed,
            self.get_damage(),
            self.explosion_radius,
            self.get_damage() * self.explosion_damage_multiplier
        )
        self.shells.append(shell)
    
    def fire_skill_shell(self):
        """发射技能炮弹"""
        # 创建一个随机方向的炮弹
        center_x, center_y = self.get_center()
        angle = random.uniform(0, 2 * math.pi)
        dx = math.cos(angle)
        dy = math.sin(angle)
        
        shell = ArtilleryShell(
            center_x,
            center_y,
            dx,
            dy,
            self.shell_speed * 0.8,  # 技能炮弹速度稍慢
            self.get_damage() * 1.2,  # 技能炮弹伤害稍高
            self.explosion_radius * 1.2,  # 技能炮弹爆炸范围稍大
            self.get_damage() * self.explosion_damage_multiplier * 1.2
        )
        self.shells.append(shell)
        
        self.remaining_skill_shells -= 1
        self.next_skill_shell_time = pygame.time.get_ticks() + int(self.skill_interval * 1000)
    
    def use_skill(self):
        """使用技能：炮火覆盖"""
        if not self.is_skill_ready:
            return
        
        super().use_skill()
        
        # 初始化技能状态
        self.skill_end_time = pygame.time.get_ticks() + int(self.skill_duration * 1000)
        self.remaining_skill_shells = self.skill_shells
        self.next_skill_shell_time = pygame.time.get_ticks()
    
    def end_skill(self):
        """结束技能效果"""
        self.skill_end_time = None
        self.next_skill_shell_time = None
        self.remaining_skill_shells = 0
    
    def render(self, screen: pygame.Surface):
        """渲染炮兵和炮弹"""
        # 渲染炮兵
        if self.image:
            super().render(screen)
        else:
            # 如果没有图像，绘制一个六边形
            center_x, center_y = self.get_center()
            radius = self.width / 2
            points = []
            for i in range(6):
                angle = math.pi / 3 * i
                points.append((
                    center_x + radius * math.cos(angle),
                    center_y + radius * math.sin(angle)
                ))
            pygame.draw.polygon(screen, self.color, points)
        
        # 渲染炮弹
        for shell in self.shells:
            shell.render(screen)
    
    def level_up(self):
        """升级效果"""
        super().level_up()
        
        # 提升基础属性
        self.max_health += 4
        self.health = self.max_health
        self.damage += 3
        self.explosion_radius += 2 