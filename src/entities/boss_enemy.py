import pygame
import math
import random
from typing import List, Optional, Dict
from .enemy import Enemy
from .character import Character
from .geometric_enemies import TriangleEnemy, CircleEnemy, SquareEnemy

class BossPhase:
    """Boss战斗阶段基类"""
    def __init__(self, boss: 'BossEnemy'):
        self.boss = boss
        self.duration = 20000  # 默认阶段持续20秒
        self.start_time = 0
        self.is_active = False
    
    def start(self):
        """开始阶段"""
        self.start_time = pygame.time.get_ticks()
        self.is_active = True
    
    def update(self):
        """更新阶段状态"""
        if not self.is_active:
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.end()
    
    def end(self):
        """结束阶段"""
        self.is_active = False

class AttackPhase(BossPhase):
    """攻击阶段：发射多种类型的子弹"""
    def __init__(self, boss: 'BossEnemy'):
        super().__init__(boss)
        self.attack_patterns = ['spiral', 'rain', 'targeted']
        self.current_pattern = 'spiral'
        self.pattern_timer = 0
        self.pattern_interval = 5000  # 每5秒切换一次攻击模式
        self.spiral_angle = 0
    
    def update(self):
        """更新攻击阶段"""
        super().update()
        if not self.is_active:
            return
        
        current_time = pygame.time.get_ticks()
        
        # 切换攻击模式
        if current_time - self.pattern_timer >= self.pattern_interval:
            self.current_pattern = random.choice(self.attack_patterns)
            self.pattern_timer = current_time
        
        # 执行攻击
        if self.current_pattern == 'spiral':
            self._spiral_attack()
        elif self.current_pattern == 'rain':
            self._rain_attack()
        else:
            self._targeted_attack()
    
    def _spiral_attack(self):
        """螺旋形攻击"""
        for i in range(3):
            angle = self.spiral_angle + i * (2 * math.pi / 3)
            dx = math.cos(angle)
            dy = math.sin(angle)
            self.boss.shoot(dx, dy)
        self.spiral_angle += 0.2
    
    def _rain_attack(self):
        """从天而降的攻击"""
        if random.random() < 0.1:  # 10%概率发射
            x = random.uniform(0, 800)  # 假设屏幕宽度为800
            self.boss.shoot(0, 1, start_x=x, start_y=0)
    
    def _targeted_attack(self):
        """追踪玩家的攻击"""
        if self.boss.target and random.random() < 0.2:  # 20%概率发射
            direction = self.boss.get_direction_to_target()
            self.boss.shoot(direction[0], direction[1])

class SummonPhase(BossPhase):
    """召唤阶段：召唤小怪并增强它们"""
    def __init__(self, boss: 'BossEnemy'):
        super().__init__(boss)
        self.summon_types = [TriangleEnemy, CircleEnemy, SquareEnemy]
        self.summon_timer = 0
        self.summon_interval = 3000  # 每3秒召唤一次
        self.max_minions = 5
    
    def update(self):
        """更新召唤阶段"""
        super().update()
        if not self.is_active:
            return
        
        current_time = pygame.time.get_ticks()
        if (current_time - self.summon_timer >= self.summon_interval and 
            len(self.boss.minions) < self.max_minions):
            self._summon_minion()
            self.summon_timer = current_time
    
    def _summon_minion(self):
        """召唤增强的小怪"""
        enemy_type = random.choice(self.summon_types)
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(100, 150)
        x = self.boss.x + math.cos(angle) * distance
        y = self.boss.y + math.sin(angle) * distance
        
        minion = enemy_type(x, y, self.boss.target)
        # 增强小怪属性
        minion.max_health *= 1.5
        minion.health = minion.max_health
        minion.damage *= 1.2
        self.boss.minions.append(minion)

class ShieldPhase(BossPhase):
    """护盾阶段：生成护盾并反弹玩家的攻击"""
    def __init__(self, boss: 'BossEnemy'):
        super().__init__(boss)
        self.shield_health = 100
        self.max_shield_health = 100
        self.reflection_chance = 0.3  # 30%概率反弹攻击
    
    def start(self):
        """开始护盾阶段"""
        super().start()
        self.shield_health = self.max_shield_health
        self.boss.is_vulnerable = False
    
    def take_damage(self, amount: float) -> float:
        """处理护盾受到的伤害，返回反弹的伤害量"""
        if self.shield_health <= 0:
            return 0
        
        self.shield_health -= amount
        if self.shield_health <= 0:
            self.end()
        
        # 有概率反弹伤害
        if random.random() < self.reflection_chance:
            return amount * 0.5
        return 0
    
    def end(self):
        """结束护盾阶段"""
        super().end()
        self.boss.is_vulnerable = True

class BossEnemy(Enemy):
    """Boss敌人，具有多个战斗阶段和复杂的攻击模式"""
    def __init__(self, x: float, y: float, target: Optional[Character] = None):
        super().__init__(x, y, target)
        
        # Boss属性
        self.max_health = 1000
        self.health = self.max_health
        self.speed = 2.0
        self.damage = 25
        self.attack_speed = 1.0
        self.color = (255, 0, 0)  # 红色
        self.width = 60
        self.height = 60
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # 战斗相关
        self.is_vulnerable = True
        self.bullets: List['BossBullet'] = []
        self.minions: List[Enemy] = []
        self.bullet_speed = 6.0
        
        # 阶段系统
        self.phases = {
            'attack': AttackPhase(self),
            'summon': SummonPhase(self),
            'shield': ShieldPhase(self)
        }
        self.current_phase = None
        self.phase_timer = 0
        
        # 掉落增加
        self.fragment_drop_chance = 1.0
        self.fragment_drop_amount = 10
        self.star_drop_chance = 1.0
        self.star_drop_amount = 5
        self.score_value = 200
    
    def update(self):
        """更新Boss状态"""
        super().update()
        
        # 更新当前阶段
        if self.current_phase:
            self.phases[self.current_phase].update()
            if not self.phases[self.current_phase].is_active:
                self._switch_phase()
        else:
            self._switch_phase()
        
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active:
                self.bullets.remove(bullet)
        
        # 更新小怪
        for minion in self.minions[:]:
            minion.update()
            if not minion.is_alive:
                self.minions.remove(minion)
    
    def _switch_phase(self):
        """切换到新的战斗阶段"""
        available_phases = [p for p in self.phases.keys() 
                          if not self.phases[p].is_active]
        if not available_phases:
            return
        
        self.current_phase = random.choice(available_phases)
        self.phases[self.current_phase].start()
    
    def take_damage(self, amount: float):
        """处理受到的伤害"""
        if not self.is_vulnerable:
            # 如果在护盾阶段，伤害由护盾处理
            reflected = self.phases['shield'].take_damage(amount)
            if reflected > 0 and self.target:
                self.target.take_damage(reflected)
            return
        
        super().take_damage(amount)
    
    def shoot(self, dx: float, dy: float, start_x: Optional[float] = None, 
             start_y: Optional[float] = None):
        """发射子弹"""
        if start_x is None or start_y is None:
            start_x, start_y = self.get_center()
        
        bullet = BossBullet(
            start_x,
            start_y,
            dx,
            dy,
            self.bullet_speed,
            self.get_damage()
        )
        self.bullets.append(bullet)
    
    def render(self, screen: pygame.Surface):
        """渲染Boss、子弹和小怪"""
        # 渲染小怪
        for minion in self.minions:
            minion.render(screen)
        
        # 渲染子弹
        for bullet in self.bullets:
            bullet.render(screen)
        
        # 渲染Boss本体（十字星形状）
        center_x, center_y = self.get_center()
        
        # 绘制主体
        points = []
        num_points = 12
        inner_radius = self.width * 0.3
        outer_radius = self.width * 0.5
        
        for i in range(num_points * 2):
            angle = math.pi * i / num_points
            radius = outer_radius if i % 2 == 0 else inner_radius
            points.append((
                center_x + radius * math.cos(angle),
                center_y + radius * math.sin(angle)
            ))
        
        pygame.draw.polygon(screen, self.color, points)
        
        # 如果在护盾阶段，绘制护盾效果
        if self.current_phase == 'shield' and not self.is_vulnerable:
            shield = self.phases['shield']
            shield_radius = self.width * 0.7
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), 
                                         pygame.SRCALPHA)
            alpha = int(255 * (shield.shield_health / shield.max_shield_health))
            pygame.draw.circle(shield_surface, (100, 200, 255, alpha),
                             (shield_radius, shield_radius), shield_radius)
            screen.blit(shield_surface, 
                       (center_x - shield_radius, center_y - shield_radius))
        
        # 绘制血条
        health_width = int(self.width * 1.5)
        health_height = 8
        health_x = center_x - health_width / 2
        health_y = self.y - 20
        
        # 血条背景
        pygame.draw.rect(screen, (64, 64, 64),
                        pygame.Rect(health_x, health_y, health_width, health_height))
        
        # 当前血量
        current_health_width = int(health_width * (self.health / self.max_health))
        pygame.draw.rect(screen, (255, 0, 0),
                        pygame.Rect(health_x, health_y, current_health_width, health_height))

class BossBullet:
    def __init__(self, x: float, y: float, dx: float, dy: float, speed: float, damage: float):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.size = 6
        self.is_active = True
        self.rotation = 0
        self.rotation_speed = 10
    
    def update(self):
        """更新子弹位置和旋转"""
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.rotation += self.rotation_speed
    
    def render(self, screen: pygame.Surface):
        """渲染子弹（旋转的十字）"""
        center = (int(self.x), int(self.y))
        
        # 计算旋转后的四个端点
        points = []
        for i in range(4):
            angle = math.radians(self.rotation + i * 90)
            points.append((
                self.x + self.size * math.cos(angle),
                self.y + self.size * math.sin(angle)
            ))
        
        # 绘制两条交叉的线
        pygame.draw.line(screen, (255, 0, 0), points[0], points[2], 3)
        pygame.draw.line(screen, (255, 0, 0), points[1], points[3], 3) 