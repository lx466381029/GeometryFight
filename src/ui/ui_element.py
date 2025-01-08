import pygame
from typing import Tuple, Optional, Callable, Dict

class UIElement:
    # 字体缓存
    _fonts: Dict[str, Dict[int, pygame.font.Font]] = {
        'regular': {},
        'bold': {}
    }
    
    @staticmethod
    def get_font(size: int, bold: bool = False) -> pygame.font.Font:
        """获取指定大小的字体"""
        font_type = 'bold' if bold else 'regular'
        if size not in UIElement._fonts[font_type]:
            font_path = "assets/fonts/SourceHanSans-Bold.ttc" if bold else "assets/fonts/SourceHanSans-Regular.ttc"
            UIElement._fonts[font_type][size] = pygame.font.Font(font_path, size)
        return UIElement._fonts[font_type][size]
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True
        self.parent: Optional['UIElement'] = None
        self.children: list['UIElement'] = []
    
    def set_position(self, x: int, y: int):
        """设置元素位置"""
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self._update_children_position()
    
    def _update_children_position(self):
        """更新子元素位置"""
        for child in self.children:
            child.set_position(
                self.x + child.x - child.parent.x,
                self.y + child.y - child.parent.y
            )
    
    def add_child(self, child: 'UIElement'):
        """添加子元素"""
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child: 'UIElement'):
        """移除子元素"""
        if child in self.children:
            child.parent = None
            self.children.remove(child)
    
    def update(self):
        """更新UI元素"""
        if not self.visible or not self.enabled:
            return
        
        for child in self.children:
            child.update()
    
    def render(self, screen: pygame.Surface):
        """渲染UI元素"""
        if not self.visible:
            return
        
        for child in self.children:
            child.render(screen)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """处理事件"""
        if not self.visible or not self.enabled:
            return False
        
        # 从后往前处理子元素事件，这样最上层的元素优先处理
        for child in reversed(self.children):
            if child.handle_event(event):
                return True
        
        return False
    
    def contains_point(self, x: int, y: int) -> bool:
        """检查点是否在元素内"""
        return self.rect.collidepoint(x, y)

class Button(UIElement):
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, callback: Callable[[], None]):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        self.pressed = False
        
        # 颜色
        self.normal_color = (80, 80, 80)  # 深灰色
        self.hover_color = (100, 100, 100)  # 中灰色
        self.pressed_color = (60, 60, 60)  # 更深的灰色
        self.disabled_color = (50, 50, 50)  # 禁用状态的颜色
        self.text_color = (255, 255, 255)  # 白色文本
        self.disabled_text_color = (150, 150, 150)  # 禁用状态的文本颜色
        
        # 创建文本
        self.font = self.get_font(24, bold=True)  # 使用粗体
        self._update_text_surface()
    
    def _update_text_surface(self):
        """更新文本表面"""
        color = self.disabled_text_color if not self.enabled else self.text_color
        self.text_surface = self.font.render(self.text, True, color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def set_enabled(self, enabled: bool):
        """设置按钮是否可用"""
        if self.enabled != enabled:
            self.enabled = enabled
            self._update_text_surface()
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """处理按钮事件"""
        if not self.visible or not self.enabled:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.contains_point(*event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed:
                self.pressed = False
                if self.hovered and self.callback:
                    self.callback()
        
        return self.hovered
    
    def render(self, screen: pygame.Surface):
        """渲染按钮"""
        if not self.visible:
            return
        
        # 选择颜色
        if not self.enabled:
            color = self.disabled_color
        elif self.pressed:
            color = self.pressed_color
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.normal_color
        
        # 绘制按钮背景
        pygame.draw.rect(screen, color, self.rect)
        
        # 绘制边框
        border_color = (200, 200, 200) if self.enabled else (100, 100, 100)
        pygame.draw.rect(screen, border_color, self.rect, 2)
        
        # 绘制文本
        screen.blit(self.text_surface, self.text_rect)
        
        # 渲染子元素
        super().render(screen)

class Label(UIElement):
    def __init__(self, x: int, y: int, text: str, font_size: int = 24, 
                 color: Tuple[int, int, int] = (255, 255, 255),
                 bold: bool = False):
        self.font = self.get_font(font_size, bold)
        self.text = text
        self.color = color
        self.font_size = font_size
        self.bold = bold
        self.text_surface = self.font.render(text, True, color)
        super().__init__(x, y, self.text_surface.get_width(), 
                        self.text_surface.get_height())
    
    def set_text(self, text: str):
        """更新文本内容"""
        self.text = text
        self.text_surface = self.font.render(text, True, self.color)
        self.width = self.text_surface.get_width()
        self.height = self.text_surface.get_height()
        self.rect.width = self.width
        self.rect.height = self.height
    
    def render(self, screen: pygame.Surface):
        """渲染文本"""
        if not self.visible:
            return
        
        screen.blit(self.text_surface, self.rect)
        super().render(screen)

class Panel(UIElement):
    def __init__(self, x: int, y: int, width: int, height: int, 
                 color: Tuple[int, int, int] = (50, 50, 50, 200)):
        super().__init__(x, y, width, height)
        self.color = color
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    def render(self, screen: pygame.Surface):
        """渲染面板"""
        if not self.visible:
            return
        
        # 绘制半透明背景
        pygame.draw.rect(self.surface, self.color, 
                        pygame.Rect(0, 0, self.width, self.height))
        screen.blit(self.surface, self.rect)
        
        # 渲染子元素
        super().render(screen)

class ProgressBar(UIElement):
    def __init__(self, x: int, y: int, width: int, height: int, 
                 bg_color: Tuple[int, int, int] = (50, 50, 50),
                 fill_color: Tuple[int, int, int] = (0, 255, 0)):
        super().__init__(x, y, width, height)
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.progress = 1.0  # 0.0 到 1.0
    
    def set_progress(self, value: float):
        """设置进度值（0.0到1.0）"""
        self.progress = max(0.0, min(1.0, value))
    
    def render(self, screen: pygame.Surface):
        """渲染进度条"""
        if not self.visible:
            return
        
        # 绘制背景
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # 绘制进度
        if self.progress > 0:
            fill_rect = pygame.Rect(
                self.x,
                self.y,
                int(self.width * self.progress),
                self.height
            )
            pygame.draw.rect(screen, self.fill_color, fill_rect)
        
        # 绘制边框
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        
        super().render(screen) 