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
        self.wander_direction = (0, 0)
        
        # 子弹列表
        self.bullets = []
        
        # 创建敌人图像
        self.color = (255, 0, 0)  # 敌人是红色
        self._create_enemy_image()
        
        print(f"敌人初始化完成: {self.__class__.__name__}")
    
    def _create_enemy_image(self):
        """创建敌人图像"""
        try:
            # 创建一个带有透明度的表面
            image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # 绘制一个五边形作为敌人图像
            center_x = self.width / 2
            center_y = self.height / 2
            radius = min(self.width, self.height) / 2 - 2
            points = []
            
            for i in range(5):
                angle = math.pi * 2 / 5 * i - math.pi / 2
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))
            
            # 绘制填充的五边形
            pygame.draw.polygon(image, self.color, points)
            # 绘制边框
            pygame.draw.polygon(image, (255, 255, 255), points, 2)
            
            # 绘制一个小圆表示"眼睛"
            eye_pos = (center_x, center_y - radius // 2)
            pygame.draw.circle(image, (255, 255, 0), eye_pos, 3)
            
            self.set_image(image)
            print(f"为敌人 {self.__class__.__name__} 创建图像")
        
        except Exception as e:
            print(f"创建敌人图像时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def update(self):
        """更新敌人状态"""
        super().update()
        
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active:
                self.bullets.remove(bullet)
        
        # 更新AI行为
        current_time = pygame.time.get_ticks()
        if current_time - self.behavior_timer >= self.behavior_change_interval:
            self._change_behavior()
            self.behavior_timer = current_time
        
        # 执行当前行为
        if self.current_behavior == "chase" and self.target:
            self._chase_target()
        elif self.current_behavior == "wander":
            self._wander()
        elif self.current_behavior == "attack" and self.target:
            self._attack_target()
    
    def _change_behavior(self):
        """改变AI行为"""
        if not self.target:
            self.current_behavior = "wander"
            return
        
        # 计算与目标的距离
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # 根据距离选择行为
        if distance <= self.attack_range:
            self.current_behavior = "attack"
        elif distance <= self.detection_range:
            self.current_behavior = "chase"
        else:
            self.current_behavior = "wander"
            # 随机选择一个漫游方向
            angle = random.uniform(0, math.pi * 2)
            self.wander_direction = (math.cos(angle), math.sin(angle))
    
    def _chase_target(self):
        """追逐目标"""
        if not self.target:
            return
        
        # 计算方向
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        length = math.sqrt(dx * dx + dy * dy)
        
        if length > 0:
            dx /= length
            dy /= length
            
            # 移动
            self.move(dx * self.get_speed(), dy * self.get_speed())
            
            # 更新朝向
            angle = math.degrees(math.atan2(dy, dx))
            self.set_rotation(angle)
    
    def _wander(self):
        """漫游"""
        if self.wander_direction == (0, 0):
            angle = random.uniform(0, math.pi * 2)
            self.wander_direction = (math.cos(angle), math.sin(angle))
        
        # 移动
        self.move(
            self.wander_direction[0] * self.get_speed() * 0.5,
            self.wander_direction[1] * self.get_speed() * 0.5
        )
        
        # 更新朝向
        angle = math.degrees(math.atan2(self.wander_direction[1], 
                                      self.wander_direction[0]))
        self.set_rotation(angle)
    
    def _attack_target(self):
        """攻击目标"""
        if not self.target:
            return
        
        # 计算朝向目标的角度
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        angle = math.degrees(math.atan2(dy, dx))
        self.set_rotation(angle)
        
        # 尝试攻击
        if self.can_attack():
            self.attack()
    
    def render(self, screen: pygame.Surface):
        """渲染敌人和子弹"""
        # 渲染子弹
        for bullet in self.bullets:
            bullet.render(screen)
        
        # 渲染敌人
        super().render(screen)
        
        # 绘制血条
        health_width = self.width
        health_height = 4
        health_x = self.x
        health_y = self.y - 10
        
        # 血条背景
        pygame.draw.rect(screen, (64, 64, 64),
                        pygame.Rect(health_x, health_y, health_width, health_height))
        
        # 当前血量
        current_health_width = int(health_width * (self.health / self.max_health))
        pygame.draw.rect(screen, (255, 0, 0),
                        pygame.Rect(health_x, health_y, current_health_width, health_height))
    
    def die(self):
        """敌人死亡"""
        super().die()
        
        if not self.target:
            return
        
        # 增加玩家得分
        if hasattr(self.target, 'add_score'):
            self.target.add_score(self.score_value)
        
        # 随机掉落碎片
        if random.random() < self.fragment_drop_chance:
            if hasattr(self.target, 'add_fragments'):
                self.target.add_fragments(self.fragment_drop_amount)
        
        # 随机掉落星星
        if random.random() < self.star_drop_chance:
            if hasattr(self.target, 'add_stars'):
                self.target.add_stars(self.star_drop_amount) 