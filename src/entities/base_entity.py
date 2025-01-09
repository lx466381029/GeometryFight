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
        self.original_image: Optional[pygame.Surface] = None
        self.image: Optional[pygame.Surface] = None
        self.rect = pygame.Rect(
            x - width // 2,
            y - height // 2,
            width,
            height
        )
        self.color = (255, 255, 255)  # 默认颜色为白色
        
        # 创建默认图像
        self._create_default_image()
    
    def _create_default_image(self):
        """创建默认图像"""
        try:
            # 创建一个带有透明度的表面
            image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # 绘制一个三角形作为默认图像
            points = [
                (self.width * 0.2, self.height * 0.8),  # 左下
                (self.width * 0.8, self.height * 0.8),  # 右下
                (self.width * 0.5, self.height * 0.2)   # 顶部
            ]
            pygame.draw.polygon(image, self.color, points)
            pygame.draw.polygon(image, (200, 200, 200), points, 2)  # 边框
            
            self.set_image(image)
            print(f"为实体 {self.__class__.__name__} 创建默认图像")
        
        except Exception as e:
            print(f"创建默认图像时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def move(self, dx: float, dy: float):
        """移动实体"""
        self.x += dx
        self.y += dy
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
    
    def set_position(self, x: float, y: float):
        """设置实体位置"""
        self.x = x
        self.y = y
        self.rect.centerx = int(x)
        self.rect.centery = int(y)
    
    def set_image(self, image: pygame.Surface):
        """设置实体图像"""
        try:
            self.original_image = image
            self.image = image
            # 更新图像大小以匹配实体大小
            if self.original_image:
                self.original_image = pygame.transform.scale(
                    self.original_image, 
                    (self.width, self.height)
                )
                self.image = self.original_image
                print(f"实体 {self.__class__.__name__} 图像已设置和缩放")
        except Exception as e:
            print(f"设置图像时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def set_rotation(self, angle: float):
        """设置实体旋转角度"""
        try:
            self.rotation = angle
            if self.original_image:
                # 保存当前中心点
                center = self.rect.center
                # 旋转图像
                self.image = pygame.transform.rotate(self.original_image, -angle)
                # 获取新的矩形
                self.rect = self.image.get_rect()
                # 保持中心点不变
                self.rect.center = center
        except Exception as e:
            print(f"设置旋转角度时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
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
        try:
            if self.image:
                screen.blit(self.image, self.rect)
            else:
                # 如果没有图像，绘制一个矩形作为占位符
                pygame.draw.rect(screen, self.color, self.rect)
                # 绘制一个箭头表示朝向
                center_x, center_y = self.get_center()
                direction_x, direction_y = self.get_direction()
                end_x = center_x + direction_x * (self.width / 2)
                end_y = center_y + direction_y * (self.height / 2)
                pygame.draw.line(
                    screen,
                    (255, 0, 0),
                    (center_x, center_y),
                    (end_x, end_y),
                    2
                )
        except Exception as e:
            print(f"渲染实体时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def collides_with(self, other: 'BaseEntity') -> bool:
        """检测与其他实体的碰撞"""
        return self.rect.colliderect(other.rect) 