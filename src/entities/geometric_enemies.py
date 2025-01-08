import pygame
import math
from typing import List, Optional, Tuple
from .enemy import Enemy
from .character import Character

class TriangleEnemy(Enemy):
    def __init__(self, x: float, y: float, target: Optional[Character] = None):
        super().__init__(x, y, target)
        
        # 三角形敌人属性
        self.max_health = 60
        self.health = self.max_health
        self.speed = 6.0      # 较快的速度
        self.damage = 10
        self.attack_speed = 1.0
        self.color = (255, 100, 100)  # 浅红色
        
        # 攻击相关
        self.attack_range = 300  # 较远的攻击范围
        self.bullet_speed = 8.0
        self.bullets: List['TriangleBullet'] = []
    
    def attack(self):
        """发射三角形子弹"""
        if not self.can_attack():
            return
        
        super().attack()
        
        # 创建子弹
        direction = self.get_direction_to_target()
        bullet = TriangleBullet(
            *self.get_center(),
            direction[0],
            direction[1],
            self.bullet_speed,
            self.get_damage()
        )
        self.bullets.append(bullet)
    
    def update(self):
        """更新三角形敌人状态"""
        super().update()
        
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active:
                self.bullets.remove(bullet)
    
    def render(self, screen: pygame.Surface):
        """渲染三角形敌人和子弹"""
        # 渲染三角形
        center_x, center_y = self.get_center()
        points = [
            (center_x, center_y - self.height/2),  # 顶点
            (center_x - self.width/2, center_y + self.height/2),  # 左下
            (center_x + self.width/2, center_y + self.height/2)   # 右下
        ]
        pygame.draw.polygon(screen, self.color, points)
        
        # 渲染子弹
        for bullet in self.bullets:
            bullet.render(screen)

class CircleEnemy(Enemy):
    def __init__(self, x: float, y: float, target: Optional[Character] = None):
        super().__init__(x, y, target)
        
        # 圆形敌人属性
        self.max_health = 80
        self.health = self.max_health
        self.speed = 4.0      # 中等速度
        self.damage = 15
        self.attack_speed = 0.8
        self.color = (100, 100, 255)  # 浅蓝色
        
        # 攻击相关
        self.attack_range = 150  # 较近的攻击范围
        self.bullet_spread = 30  # 子弹散射角度
        self.bullets_per_shot = 3  # 每次射击的子弹数
        self.bullet_speed = 6.0
        self.bullets: List['CircleBullet'] = []
    
    def attack(self):
        """发射散射子弹"""
        if not self.can_attack():
            return
        
        super().attack()
        
        # 计算基础方向
        base_direction = self.get_direction_to_target()
        base_angle = math.degrees(math.atan2(base_direction[1], base_direction[0]))
        
        # 创建多个子弹
        for i in range(self.bullets_per_shot):
            angle = base_angle + self.bullet_spread * (i - (self.bullets_per_shot-1)/2)
            rad = math.radians(angle)
            dx = math.cos(rad)
            dy = math.sin(rad)
            
            bullet = CircleBullet(
                *self.get_center(),
                dx,
                dy,
                self.bullet_speed,
                self.get_damage()
            )
            self.bullets.append(bullet)
    
    def update(self):
        """更新圆形敌人状态"""
        super().update()
        
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active:
                self.bullets.remove(bullet)
    
    def render(self, screen: pygame.Surface):
        """渲染圆形敌人和子弹"""
        # 渲染圆形
        pygame.draw.circle(screen, self.color, 
                         (int(self.x + self.width/2), int(self.y + self.height/2)), 
                         int(self.width/2))
        
        # 渲染子弹
        for bullet in self.bullets:
            bullet.render(screen)

class SquareEnemy(Enemy):
    def __init__(self, x: float, y: float, target: Optional[Character] = None):
        super().__init__(x, y, target)
        
        # 方块敌人属性
        self.max_health = 100
        self.health = self.max_health
        self.speed = 3.0      # 较慢的速度
        self.damage = 20
        self.attack_speed = 0.5
        self.color = (100, 255, 100)  # 浅绿色
        
        # 攻击相关
        self.attack_range = 200
        self.bullet_speed = 5.0
        self.bullets: List['SquareBullet'] = []
        
        # 追踪子弹
        self.bullet_turn_speed = 2.0  # 子弹转向速度
    
    def attack(self):
        """发射追踪子弹"""
        if not self.can_attack():
            return
        
        super().attack()
        
        # 创建追踪子弹
        direction = self.get_direction_to_target()
        bullet = SquareBullet(
            *self.get_center(),
            direction[0],
            direction[1],
            self.bullet_speed,
            self.get_damage(),
            self.bullet_turn_speed,
            self.target
        )
        self.bullets.append(bullet)
    
    def update(self):
        """更新方块敌人状态"""
        super().update()
        
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active:
                self.bullets.remove(bullet)
    
    def render(self, screen: pygame.Surface):
        """渲染方块敌人和子弹"""
        # 渲染方块
        pygame.draw.rect(screen, self.color, self.rect)
        
        # 渲染子弹
        for bullet in self.bullets:
            bullet.render(screen)

# 子弹类
class TriangleBullet:
    def __init__(self, x: float, y: float, dx: float, dy: float, speed: float, damage: float):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.size = 6
        self.is_active = True
    
    def update(self):
        """更新子弹位置"""
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
    
    def render(self, screen: pygame.Surface):
        """渲染三角形子弹"""
        points = [
            (self.x, self.y - self.size),
            (self.x - self.size, self.y + self.size),
            (self.x + self.size, self.y + self.size)
        ]
        pygame.draw.polygon(screen, (255, 200, 200), points)

class CircleBullet:
    def __init__(self, x: float, y: float, dx: float, dy: float, speed: float, damage: float):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.radius = 4
        self.is_active = True
    
    def update(self):
        """更新子弹位置"""
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
    
    def render(self, screen: pygame.Surface):
        """渲染圆形子弹"""
        pygame.draw.circle(screen, (200, 200, 255), 
                         (int(self.x), int(self.y)), 
                         self.radius)

class SquareBullet:
    def __init__(self, x: float, y: float, dx: float, dy: float, speed: float, 
                 damage: float, turn_speed: float, target: Optional[Character]):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.size = 5
        self.is_active = True
        self.turn_speed = turn_speed
        self.target = target
    
    def update(self):
        """更新追踪子弹"""
        if self.target and self.target.is_alive:
            # 计算目标方向
            target_x, target_y = self.target.get_center()
            dx = target_x - self.x
            dy = target_y - self.y
            length = math.sqrt(dx * dx + dy * dy)
            
            if length > 0:
                # 标准化目标方向
                target_dx = dx / length
                target_dy = dy / length
                
                # 逐渐转向目标
                self.dx += (target_dx - self.dx) * self.turn_speed * 0.1
                self.dy += (target_dy - self.dy) * self.turn_speed * 0.1
                
                # 重新标准化速度向量
                length = math.sqrt(self.dx * self.dx + self.dy * self.dy)
                if length > 0:
                    self.dx /= length
                    self.dy /= length
        
        # 更新位置
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
    
    def render(self, screen: pygame.Surface):
        """渲染方形子弹"""
        rect = pygame.Rect(self.x - self.size/2, self.y - self.size/2, 
                         self.size, self.size)
        pygame.draw.rect(screen, (200, 255, 200), rect) 