import pygame
import math
from typing import Optional, Tuple

class Bullet:
    """子弹基类"""
    def __init__(self, x: float, y: float, dx: float, dy: float, speed: float, damage: float):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.size = 4
        self.is_active = True
        self.color = (255, 255, 255)  # 默认白色
    
    def update(self):
        """更新子弹位置"""
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
    
    def render(self, screen: pygame.Surface):
        """渲染子弹"""
        try:
            # 默认渲染一个圆形
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        except Exception as e:
            print(f"渲染子弹时发生错误: {e}")
            import traceback
            traceback.print_exc()

class PlayerBullet(Bullet):
    """玩家子弹"""
    def __init__(self, x: float, y: float, dx: float, dy: float, speed: float, damage: float, 
                 bullet_type: str = "normal"):
        super().__init__(x, y, dx, dy, speed, damage)
        self.bullet_type = bullet_type
        
        # 根据子弹类型设置属性
        if bullet_type == "soldier":
            self.color = (255, 255, 0)  # 黄色
            self.size = 3
        elif bullet_type == "assault":
            self.color = (255, 165, 0)  # 橙色
            self.size = 2
        elif bullet_type == "artillery":
            self.color = (255, 50, 50)  # 红色
            self.size = 5
    
    def render(self, screen: pygame.Surface):
        """渲染玩家子弹"""
        try:
            if self.bullet_type == "artillery":
                # 炮兵子弹是一个大圆
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
                pygame.draw.circle(screen, (255, 200, 200), (int(self.x), int(self.y)), self.size - 1)
            elif self.bullet_type == "assault":
                # 突击手子弹是一个小菱形
                points = [
                    (self.x, self.y - self.size),  # 上
                    (self.x + self.size, self.y),  # 右
                    (self.x, self.y + self.size),  # 下
                    (self.x - self.size, self.y)   # 左
                ]
                pygame.draw.polygon(screen, self.color, points)
            else:
                # 士兵子弹是一个小圆
                super().render(screen)
        except Exception as e:
            print(f"渲染玩家子弹时发生错误: {e}")
            import traceback
            traceback.print_exc()

class EnemyBullet(Bullet):
    """敌人子弹"""
    def __init__(self, x: float, y: float, dx: float, dy: float, speed: float, damage: float,
                 bullet_type: str = "normal", target: Optional['Character'] = None):
        super().__init__(x, y, dx, dy, speed, damage)
        self.bullet_type = bullet_type
        self.target = target
        self.turn_speed = 0.1  # 追踪子弹的转向速度
        self.rotation = 0      # 旋转角度
        
        # 根据子弹类型设置属性
        if bullet_type == "tracking":
            self.color = (200, 255, 200)  # 追踪子弹是绿色
            self.size = 4
        elif bullet_type == "spread":
            self.color = (200, 200, 255)  # 散射子弹是蓝色
            self.size = 3
        elif bullet_type == "boss":
            self.color = (255, 0, 0)  # Boss子弹是红色
            self.size = 6
            self.rotation_speed = 10
    
    def update(self):
        """更新敌人子弹"""
        if self.bullet_type == "tracking" and self.target and self.target.is_alive:
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
                self.dx += (target_dx - self.dx) * self.turn_speed
                self.dy += (target_dy - self.dy) * self.turn_speed
                
                # 重新标准化速度向量
                length = math.sqrt(self.dx * self.dx + self.dy * self.dy)
                if length > 0:
                    self.dx /= length
                    self.dy /= length
        
        elif self.bullet_type == "boss":
            # Boss子弹旋转
            self.rotation += self.rotation_speed
        
        # 更新位置
        super().update()
    
    def render(self, screen: pygame.Surface):
        """渲染敌人子弹"""
        try:
            if self.bullet_type == "tracking":
                # 追踪子弹是一个方块
                rect = pygame.Rect(self.x - self.size/2, self.y - self.size/2, 
                                self.size, self.size)
                pygame.draw.rect(screen, self.color, rect)
            
            elif self.bullet_type == "spread":
                # 散射子弹是一个圆形
                super().render(screen)
            
            elif self.bullet_type == "boss":
                # Boss子弹是一个旋转的十字
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
                pygame.draw.line(screen, self.color, points[0], points[2], 2)
                pygame.draw.line(screen, self.color, points[1], points[3], 2)
            
            else:
                # 默认子弹是一个小圆
                super().render(screen)
        
        except Exception as e:
            print(f"渲染敌人子弹时发生错误: {e}")
            import traceback
            traceback.print_exc() 