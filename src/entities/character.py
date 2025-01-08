from typing import Dict, Optional
import pygame
from .base_entity import BaseEntity

class Character(BaseEntity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 40, 40)  # 默认大小40x40
        
        # 基础属性
        self.max_health = 100
        self.health = self.max_health
        self.speed = 5.0
        self.damage = 10
        self.attack_speed = 1.0  # 每秒攻击次数
        
        # 额外属性
        self.attributes: Dict[str, float] = {
            "health_bonus": 0,      # 生命值加成
            "speed_bonus": 0,       # 移动速度加成
            "damage_bonus": 0,      # 伤害加成
            "attack_speed_bonus": 0 # 攻击速度加成
        }
        
        # 计时器
        self.attack_timer = 0
        self.last_attack_time = 0
        
        # 状态
        self.is_moving = False
        self.is_attacking = False
        self.is_alive = True
    
    def update(self):
        """更新角色状态"""
        super().update()
        
        # 更新攻击计时器
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= 1000 / self.get_attack_speed():
            self.attack_timer = 0
    
    def move(self, dx: float, dy: float):
        """移动角色"""
        actual_speed = self.get_speed()
        super().move(dx * actual_speed, dy * actual_speed)
        self.is_moving = dx != 0 or dy != 0
    
    def take_damage(self, amount: float):
        """受到伤害"""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.die()
    
    def heal(self, amount: float):
        """恢复生命值"""
        self.health = min(self.health + amount, self.get_max_health())
    
    def die(self):
        """角色死亡"""
        self.is_alive = False
    
    def can_attack(self) -> bool:
        """检查是否可以攻击"""
        return self.attack_timer == 0 and self.is_alive
    
    def attack(self):
        """执行攻击"""
        if not self.can_attack():
            return
        
        self.is_attacking = True
        self.last_attack_time = pygame.time.get_ticks()
        self.attack_timer = 1
    
    # 获取实际属性值（包含加成）
    def get_max_health(self) -> float:
        return self.max_health * (1 + self.attributes["health_bonus"])
    
    def get_speed(self) -> float:
        return self.speed * (1 + self.attributes["speed_bonus"])
    
    def get_damage(self) -> float:
        return self.damage * (1 + self.attributes["damage_bonus"])
    
    def get_attack_speed(self) -> float:
        return self.attack_speed * (1 + self.attributes["attack_speed_bonus"])
    
    # 属性加成
    def add_attribute_bonus(self, attribute: str, value: float):
        """添加属性加成"""
        if attribute in self.attributes:
            self.attributes[attribute] += value 