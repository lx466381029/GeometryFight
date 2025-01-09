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
            try:
                UIElement._fonts[font_type][size] = pygame.font.Font(font_path, size)
            except Exception as e:
                # 创建一个默认字体作为后备
                UIElement._fonts[font_type][size] = pygame.font.SysFont(None, size)
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
        
        # 渲染子元素
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
        
        # 创建按钮surface
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
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
        
        # 清空surface
        self.surface.fill((0, 0, 0, 0))
        
        # 绘制按钮背景
        pygame.draw.rect(self.surface, color, 
                        pygame.Rect(0, 0, self.width, self.height))
        
        # 绘制边框
        border_color = (200, 200, 200) if self.enabled else (100, 100, 100)
        pygame.draw.rect(self.surface, border_color, 
                        pygame.Rect(0, 0, self.width, self.height), 2)
        
        # 更新文本位置
        text_rect = self.text_surface.get_rect(center=(self.width // 2, self.height // 2))
        
        # 绘制文本
        self.surface.blit(self.text_surface, text_rect)
        
        # 将按钮surface绘制到屏幕上
        screen.blit(self.surface, self.rect)
        
        # 渲染子元素
        for child in self.children:
            child.render(screen)

class Label(UIElement):
    def __init__(self, x: int, y: int, text: str, font_size: int = 24, 
                 color: Tuple[int, int, int] = (255, 255, 255),
                 bold: bool = False):
        self.font = self.get_font(font_size, bold)
        self.text = text
        self.color = color
        self.font_size = font_size
        self.bold = bold
        self._update_text_surface()
        super().__init__(x, y, self.text_surface.get_width(), 
                        self.text_surface.get_height())
    
    def _update_text_surface(self):
        """更新文本表面"""
        self.text_surface = self.font.render(self.text, True, self.color)
    
    def set_text(self, text: str):
        """更新文本内容"""
        self.text = text
        self._update_text_surface()
        self.width = self.text_surface.get_width()
        self.height = self.text_surface.get_height()
        self.rect.width = self.width
        self.rect.height = self.height
    
    def render(self, screen: pygame.Surface):
        """渲染文本"""
        if not self.visible:
            return
        
        screen.blit(self.text_surface, self.rect)
        
        # 渲染子元素
        for child in self.children:
            child.render(screen)

class Panel(UIElement):
    def __init__(self, x: int, y: int, width: int, height: int, 
                 color: Tuple[int, int, int, int] = (50, 50, 50, 200)):
        super().__init__(x, y, width, height)
        self.color = color
        # 创建带Alpha通道的surface
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # 预先填充颜色
        pygame.draw.rect(self.surface, self.color, 
                        pygame.Rect(0, 0, width, height))
    
    def render(self, screen: pygame.Surface):
        """渲染面板"""
        if not self.visible:
            return
        
        # 将surface绘制到屏幕上
        screen.blit(self.surface, self.rect)
        
        # 渲染子元素
        for child in self.children:
            child.render(screen)

class ProgressBar(UIElement):
    def __init__(self, x: int, y: int, width: int, height: int, 
                 fill_color: Tuple[int, int, int] = (0, 255, 0),
                 background_color: Tuple[int, int, int] = (50, 50, 50),
                 border_color: Tuple[int, int, int] = (200, 200, 200)):
        super().__init__(x, y, width, height)
        self.fill_color = fill_color
        self.background_color = background_color
        self.border_color = border_color
        self.progress = 1.0  # 0.0 到 1.0 之间的值
        
        # 创建surface
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        print(f"创建进度条 - 位置: ({x}, {y}) 大小: {width}x{height}")
    
    def set_progress(self, value: float):
        """设置进度值（0.0 到 1.0 之间）"""
        self.progress = max(0.0, min(1.0, value))
        print(f"进度条更新: {self.progress:.2%}")
    
    def render(self, screen: pygame.Surface):
        """渲染进度条"""
        if not self.visible:
            return
        
        # 清空surface
        self.surface.fill((0, 0, 0, 0))
        
        # 绘制背景
        pygame.draw.rect(self.surface, self.background_color, 
                        pygame.Rect(0, 0, self.width, self.height))
        
        # 绘制进度
        if self.progress > 0:
            fill_width = int(self.width * self.progress)
            pygame.draw.rect(self.surface, self.fill_color,
                           pygame.Rect(0, 0, fill_width, self.height))
        
        # 绘制边框
        pygame.draw.rect(self.surface, self.border_color,
                        pygame.Rect(0, 0, self.width, self.height), 2)
        
        # 将surface绘制到屏幕上
        screen.blit(self.surface, self.rect)
        
        # 渲染子元素
        for child in self.children:
            child.render(screen) 