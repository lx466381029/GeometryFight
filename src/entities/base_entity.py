import pygame
from typing import Tuple, Optional
import math

class BaseEntity:
    def __init__(self, x: float, y: float, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_x = 0
        self.velocity_y = 0
        self.rotation = 0  # 角度，0表示朝右
        self.image: Optional[pygame.Surface] = None
        self.rect = pygame.Rect(x, y, width, height)
    
    def move(self, dx: float, dy: float):
        """移动实体"""
        self.x += dx
        self.y += dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def set_position(self, x: float, y: float):
        """设置实体位置"""
        self.x = x
        self.y = y
        self.rect.x = int(x)
        self.rect.y = int(y)
    
    def set_rotation(self, angle: float):
        """设置实体旋转角度"""
        self.rotation = angle
        if self.image:
            self.image = pygame.transform.rotate(self.image, -angle)
    
    def get_position(self) -> Tuple[float, float]:
        """获取实体位置"""
        return self.x, self.y
    
    def get_center(self) -> Tuple[float, float]:
        """获取实体中心点位置"""
        return self.x + self.width / 2, self.y + self.height / 2
    
    def get_direction(self) -> Tuple[float, float]:
        """获取实体朝向的单位向量"""
        angle_rad = math.radians(self.rotation)
        return math.cos(angle_rad), math.sin(angle_rad)
    
    def update(self):
        """更新实体状态"""
        self.move(self.velocity_x, self.velocity_y)
    
    def render(self, screen: pygame.Surface):
        """渲染实体"""
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            # 如果没有图像，绘制一个矩形作为占位符
            pygame.draw.rect(screen, (255, 255, 255), self.rect)
    
    def collides_with(self, other: 'BaseEntity') -> bool:
        """检测与其他实体的碰撞"""
        return self.rect.colliderect(other.rect) 