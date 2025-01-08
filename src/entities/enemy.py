from typing import Optional, Tuple
import pygame
import math
import random
from .character import Character

class Enemy(Character):
    def __init__(self, x: float, y: float, target: Optional[Character] = None):
        super().__init__(x, y)
        
        # 基础属性
        self.target = target
        self.detection_range = 400  # 检测范围
        self.attack_range = 200     # 攻击范围
        self.score_value = 10       # 击杀得分
        
        # 掉落概率
        self.fragment_drop_chance = 0.3  # 30%概率掉落碎片
        self.fragment_drop_amount = 1    # 掉落碎片数量
        self.star_drop_chance = 0.1      # 10%概率掉落星星
        self.star_drop_amount = 1        # 掉落星星数量
        
        # AI行为相关
        self.behavior_timer = 0
        self.behavior_change_interval = 2000  # 2秒改变一次行为
        self.current_behavior = "idle"
        self.wander_direction: Tuple[float, float] = (0, 0)
        
        # 颜色（用于渲染）
        self.color = (255, 0, 0)  # 默认红色
    
    def update(self):
        """更新敌人状态"""
        super().update()
        
        # 更新AI行为
        current_time = pygame.time.get_ticks()
        if current_time - self.behavior_timer >= self.behavior_change_interval:
            self.behavior_timer = current_time
            self.choose_behavior()
        
        # 执行当前行为
        self.execute_behavior()
    
    def choose_behavior(self):
        """选择行为"""
        if not self.target:
            self.current_behavior = "wander"
            return
        
        distance = self.get_distance_to_target()
        
        if distance <= self.attack_range:
            self.current_behavior = "attack"
        elif distance <= self.detection_range:
            self.current_behavior = "chase"
        else:
            self.current_behavior = "wander"
        
        if self.current_behavior == "wander":
            # 随机选择一个漫游方向
            angle = random.uniform(0, 2 * math.pi)
            self.wander_direction = (math.cos(angle), math.sin(angle))
    
    def execute_behavior(self):
        """执行当前行为"""
        if self.current_behavior == "wander":
            self.move(self.wander_direction[0], self.wander_direction[1])
        elif self.current_behavior == "chase" and self.target:
            direction = self.get_direction_to_target()
            self.move(direction[0], direction[1])
        elif self.current_behavior == "attack" and self.target:
            self.attack()
            direction = self.get_direction_to_target()
            self.set_rotation(math.degrees(math.atan2(direction[1], direction[0])))
    
    def get_distance_to_target(self) -> float:
        """获取到目标的距离"""
        if not self.target:
            return float('inf')
        
        target_x, target_y = self.target.get_center()
        center_x, center_y = self.get_center()
        dx = target_x - center_x
        dy = target_y - center_y
        return math.sqrt(dx * dx + dy * dy)
    
    def get_direction_to_target(self) -> Tuple[float, float]:
        """获取指向目标的单位向量"""
        if not self.target:
            return (0, 0)
        
        target_x, target_y = self.target.get_center()
        center_x, center_y = self.get_center()
        dx = target_x - center_x
        dy = target_y - center_y
        length = math.sqrt(dx * dx + dy * dy)
        
        if length == 0:
            return (0, 0)
        
        return (dx / length, dy / length)
    
    def render(self, screen: pygame.Surface):
        """渲染敌人"""
        if self.image:
            super().render(screen)
        else:
            # 如果没有图像，绘制一个有颜色的矩形
            pygame.draw.rect(screen, self.color, self.rect)
    
    def on_death(self):
        """处理死亡事件"""
        # 处理掉落物
        drops = {
            "fragments": 0,
            "stars": 0
        }
        
        if random.random() < self.fragment_drop_chance:
            drops["fragments"] = self.fragment_drop_amount
        
        if random.random() < self.star_drop_chance:
            drops["stars"] = self.star_drop_amount
        
        return {
            "score": self.score_value,
            "drops": drops
        } 