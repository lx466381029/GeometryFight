import pygame
import math
import random
from typing import List, Optional, Type
from .enemy import Enemy
from .geometric_enemies import TriangleEnemy, CircleEnemy, SquareEnemy
from .character import Character

class SummonerElite(Enemy):
    """召唤师精英敌人，可以召唤基础几何敌人"""
    def __init__(self, x: float, y: float, target: Optional[Character] = None):
        super().__init__(x, y, target)
        
        # 精英属性
        self.max_health = 150
        self.health = self.max_health
        self.speed = 2.5
        self.damage = 15
        self.attack_speed = 0.5
        self.color = (255, 215, 0)  # 金色
        
        # 召唤相关
        self.summon_interval = 5000  # 每5秒召唤一次
        self.last_summon_time = 0
        self.summon_types = [TriangleEnemy, CircleEnemy, SquareEnemy]
        self.max_minions = 3
        self.minions: List[Enemy] = []
        
        # 掉落增加
        self.fragment_drop_chance = 0.8
        self.fragment_drop_amount = 3
        self.star_drop_chance = 0.3
        self.star_drop_amount = 2
        self.score_value = 50
    
    def update(self):
        """更新召唤师状态"""
        super().update()
        
        # 更新召唤物
        for minion in self.minions[:]:
            minion.update()
            if not minion.is_alive:
                self.minions.remove(minion)
        
        # 尝试召唤
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_summon_time >= self.summon_interval and 
            len(self.minions) < self.max_minions):
            self.summon()
            self.last_summon_time = current_time
    
    def summon(self):
        """召唤随机类型的敌人"""
        if len(self.minions) >= self.max_minions:
            return
        
        # 随机选择一个敌人类型
        enemy_type = random.choice(self.summon_types)
        
        # 在召唤师周围随机位置生成敌人
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(50, 100)
        x = self.x + math.cos(angle) * distance
        y = self.y + math.sin(angle) * distance
        
        # 创建敌人
        minion = enemy_type(x, y, self.target)
        # 减弱召唤物的属性
        minion.max_health *= 0.7
        minion.health = minion.max_health
        minion.damage *= 0.7
        self.minions.append(minion)
    
    def render(self, screen: pygame.Surface):
        """渲染召唤师和召唤物"""
        # 渲染召唤物
        for minion in self.minions:
            minion.render(screen)
        
        # 渲染召唤师（八角星形状）
        center_x, center_y = self.get_center()
        points = []
        for i in range(8):
            angle = math.pi / 4 * i
            radius = self.width / 2
            if i % 2 == 0:
                radius *= 0.6
            points.append((
                center_x + radius * math.cos(angle),
                center_y + radius * math.sin(angle)
            ))
        pygame.draw.polygon(screen, self.color, points)

class PoweredElite(Enemy):
    """强化精英敌人，具有多种强化属性和特殊攻击模式"""
    def __init__(self, x: float, y: float, target: Optional[Character] = None):
        super().__init__(x, y, target)
        
        # 精英属性
        self.max_health = 200
        self.health = self.max_health
        self.speed = 3.5
        self.damage = 20
        self.attack_speed = 1.0
        self.color = (148, 0, 211)  # 紫色
        
        # 强化属性
        self.shield = 50  # 护盾值
        self.max_shield = 50
        self.shield_regen = 5  # 每秒护盾恢复
        self.last_shield_regen = 0
        
        # 攻击相关
        self.bullets: List['PoweredBullet'] = []
        self.bullet_speed = 7.0
        self.bullet_patterns = ['single', 'spread', 'circle']
        self.current_pattern = 'single'
        self.pattern_change_interval = 3000  # 每3秒改变一次攻击模式
        self.last_pattern_change = 0
        
        # 掉落增加
        self.fragment_drop_chance = 0.9
        self.fragment_drop_amount = 4
        self.star_drop_chance = 0.4
        self.star_drop_amount = 2
        self.score_value = 60
    
    def update(self):
        """更新强化精英状态"""
        super().update()
        
        current_time = pygame.time.get_ticks()
        
        # 更新护盾恢复
        if current_time - self.last_shield_regen >= 1000:  # 每秒恢复
            self.shield = min(self.max_shield, self.shield + self.shield_regen)
            self.last_shield_regen = current_time
        
        # 更新攻击模式
        if current_time - self.last_pattern_change >= self.pattern_change_interval:
            self.current_pattern = random.choice(self.bullet_patterns)
            self.last_pattern_change = current_time
        
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active:
                self.bullets.remove(bullet)
    
    def take_damage(self, amount: float):
        """受到伤害时优先扣除护盾"""
        if self.shield > 0:
            if self.shield >= amount:
                self.shield -= amount
                return
            else:
                amount -= self.shield
                self.shield = 0
        super().take_damage(amount)
    
    def attack(self):
        """根据当前模式执行攻击"""
        if not self.can_attack():
            return
        
        super().attack()
        
        if self.current_pattern == 'single':
            self._single_shot()
        elif self.current_pattern == 'spread':
            self._spread_shot()
        else:  # circle
            self._circle_shot()
    
    def _single_shot(self):
        """发射单发强力子弹"""
        direction = self.get_direction_to_target()
        bullet = PoweredBullet(
            *self.get_center(),
            direction[0],
            direction[1],
            self.bullet_speed,
            self.get_damage() * 1.5
        )
        self.bullets.append(bullet)
    
    def _spread_shot(self):
        """发射扇形散射"""
        base_direction = self.get_direction_to_target()
        base_angle = math.degrees(math.atan2(base_direction[1], base_direction[0]))
        
        for i in range(5):
            angle = base_angle + 30 * (i - 2)  # -60到60度的扇形
            rad = math.radians(angle)
            dx = math.cos(rad)
            dy = math.sin(rad)
            
            bullet = PoweredBullet(
                *self.get_center(),
                dx,
                dy,
                self.bullet_speed,
                self.get_damage()
            )
            self.bullets.append(bullet)
    
    def _circle_shot(self):
        """发射环形子弹"""
        for i in range(8):
            angle = math.pi / 4 * i
            dx = math.cos(angle)
            dy = math.sin(angle)
            
            bullet = PoweredBullet(
                *self.get_center(),
                dx,
                dy,
                self.bullet_speed,
                self.get_damage()
            )
            self.bullets.append(bullet)
    
    def render(self, screen: pygame.Surface):
        """渲染强化精英和子弹"""
        # 渲染子弹
        for bullet in self.bullets:
            bullet.render(screen)
        
        # 渲染本体（五角星形状）
        center_x, center_y = self.get_center()
        points = []
        for i in range(5):
            angle = math.pi * 2 / 5 * i - math.pi / 2
            radius = self.width / 2
            points.append((
                center_x + radius * math.cos(angle),
                center_y + radius * math.sin(angle)
            ))
        pygame.draw.polygon(screen, self.color, points)
        
        # 渲染护盾条
        if self.shield > 0:
            shield_width = int(self.width * (self.shield / self.max_shield))
            shield_rect = pygame.Rect(
                self.x,
                self.y - 10,
                shield_width,
                5
            )
            pygame.draw.rect(screen, (0, 191, 255), shield_rect)

class PoweredBullet:
    def __init__(self, x: float, y: float, dx: float, dy: float, speed: float, damage: float):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.size = 5
        self.is_active = True
    
    def update(self):
        """更新子弹位置"""
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
    
    def render(self, screen: pygame.Surface):
        """渲染子弹（菱形）"""
        points = [
            (self.x, self.y - self.size),  # 上
            (self.x + self.size, self.y),  # 右
            (self.x, self.y + self.size),  # 下
            (self.x - self.size, self.y)   # 左
        ]
        pygame.draw.polygon(screen, (148, 0, 211), points) 