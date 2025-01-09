import pygame
from typing import Optional, Tuple
from .character import Character
import math

class Player(Character):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        
        # 玩家特有属性
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        self.score = 0
        
        # 资源
        self.fragments = 0  # 碎片
        self.stars = 0      # 星星
        
        # 技能相关
        self.skill_cooldown = 5.0  # 技能冷却时间（秒）
        self.last_skill_time = 0
        self.is_skill_ready = True
        
        # 子弹列表
        self.bullets = []
        
        # 移动控制
        self.move_keys = {
            pygame.K_w: (0, -1),
            pygame.K_s: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0)
        }
        
        # 创建玩家图像
        self._create_player_image()
        
        print(f"玩家初始化完成: {self.__class__.__name__}")
    
    def _create_player_image(self):
        """创建玩家图像"""
        try:
            # 创建一个带有透明度的表面
            image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # 根据玩家类型设置颜色
            if self.__class__.__name__ == "Soldier":
                self.color = (0, 255, 0)  # 士兵是绿色
            elif self.__class__.__name__ == "Assault":
                self.color = (255, 165, 0)  # 突击手是橙色
            elif self.__class__.__name__ == "Artillery":
                self.color = (0, 0, 255)  # 炮兵是蓝色
            else:
                self.color = (255, 255, 255)  # 默认是白色
            
            # 绘制一个六边形作为玩家图像
            center_x = self.width / 2
            center_y = self.height / 2
            radius = min(self.width, self.height) / 2 - 2
            points = []
            
            for i in range(6):
                angle = math.pi / 3 * i
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))
            
            # 绘制填充的六边形
            pygame.draw.polygon(image, self.color, points)
            # 绘制边框
            pygame.draw.polygon(image, (255, 255, 255), points, 2)
            
            # 绘制一个小圆表示朝向
            front_x = center_x + radius * 0.8
            front_y = center_y
            pygame.draw.circle(image, (255, 255, 255), (int(front_x), int(front_y)), 3)
            
            self.set_image(image)
            print(f"为玩家 {self.__class__.__name__} 创建图像")
        
        except Exception as e:
            print(f"创建玩家图像时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def update(self):
        """更新玩家状态"""
        super().update()
        
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active:
                self.bullets.remove(bullet)
        
        # 更新技能冷却
        current_time = pygame.time.get_ticks()
        if not self.is_skill_ready and current_time - self.last_skill_time >= self.skill_cooldown * 1000:
            self.is_skill_ready = True
            print(f"玩家 {self.__class__.__name__} 技能冷却完成")
    
    def handle_input(self, keys, mouse_pos: Tuple[int, int], mouse_buttons: Tuple[int, ...]):
        """处理输入"""
        # 处理移动
        dx = dy = 0
        for key, (move_x, move_y) in self.move_keys.items():
            if keys[key]:
                dx += move_x
                dy += move_y
        
        # 标准化移动向量
        if dx != 0 or dy != 0:
            length = math.sqrt(dx * dx + dy * dy)
            dx /= length
            dy /= length
            self.move(dx * self.get_speed(), dy * self.get_speed())
            print(f"玩家 {self.__class__.__name__} 移动: ({dx:.2f}, {dy:.2f})")
        
        # 处理旋转（朝向鼠标）
        center_x, center_y = self.get_center()
        mouse_x, mouse_y = mouse_pos
        angle = math.degrees(math.atan2(mouse_y - center_y, mouse_x - center_x))
        self.set_rotation(angle)
        
        # 处理攻击
        if mouse_buttons[0]:  # 左键射击
            self.attack()
        
        if mouse_buttons[2] and self.is_skill_ready:  # 右键技能
            self.use_skill()
            print(f"玩家 {self.__class__.__name__} 使用技能")
    
    def use_skill(self):
        """使用技能"""
        if not self.is_skill_ready:
            return
        
        self.is_skill_ready = False
        self.last_skill_time = pygame.time.get_ticks()
        print(f"玩家 {self.__class__.__name__} 技能开始冷却")
        # 具体技能效果由子类实现
    
    def add_experience(self, amount: int):
        """增加经验值"""
        self.experience += amount
        print(f"玩家 {self.__class__.__name__} 获得经验: {amount}")
        while self.experience >= self.experience_to_next_level:
            self.level_up()
    
    def level_up(self):
        """升级"""
        self.experience -= self.experience_to_next_level
        self.level += 1
        self.experience_to_next_level = int(self.experience_to_next_level * 1.2)
        print(f"玩家 {self.__class__.__name__} 升级到 {self.level} 级")
        # 具体升级效果由子类实现
    
    def add_score(self, amount: int):
        """增加得分"""
        self.score += amount
        print(f"玩家 {self.__class__.__name__} 获得得分: {amount}")
    
    def add_fragments(self, amount: int):
        """增加碎片"""
        self.fragments += amount
        print(f"玩家 {self.__class__.__name__} 获得碎片: {amount}")
    
    def add_stars(self, amount: int):
        """增加星星"""
        self.stars += amount
        print(f"玩家 {self.__class__.__name__} 获得星星: {amount}")
    
    def get_skill_cooldown_percentage(self) -> float:
        """获取技能冷却进度（0-1）"""
        if self.is_skill_ready:
            return 1.0
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_skill_time) / 1000
        return min(elapsed / self.skill_cooldown, 1.0)
    
    def render(self, screen: pygame.Surface):
        """渲染玩家和子弹"""
        # 渲染子弹
        for bullet in self.bullets:
            bullet.render(screen)
        
        # 渲染玩家
        super().render(screen)
        
        # 如果技能冷却中，绘制冷却指示器
        if not self.is_skill_ready:
            cooldown_percentage = self.get_skill_cooldown_percentage()
            radius = min(self.width, self.height) / 2
            center_x, center_y = self.get_center()
            
            # 绘制冷却环
            start_angle = -90  # 从正上方开始
            end_angle = start_angle + 360 * cooldown_percentage
            
            pygame.draw.arc(screen, (100, 100, 255), 
                          (center_x - radius, center_y - radius, 
                           radius * 2, radius * 2),
                          math.radians(start_angle), 
                          math.radians(end_angle), 
                          2) 