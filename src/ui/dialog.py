import pygame
from typing import Callable, Optional
from src.ui.ui_element import UIElement, Button, Label, Panel

class Dialog(UIElement):
    """对话框组件"""
    def __init__(self, x: int, y: int, width: int, height: int,
                 title: str, message: str,
                 on_confirm: Optional[Callable[[], None]] = None,
                 on_cancel: Optional[Callable[[], None]] = None):
        super().__init__(x, y, width, height)
        
        # 创建背景遮罩
        self.overlay = pygame.Surface((pygame.display.get_surface().get_size()))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(128)
        
        # 创建对话框面板
        self.panel = Panel(x, y, width, height)
        self.add_child(self.panel)
        
        # 标题
        title_label = Label(x + 10, y + 10, title, 32, bold=True)
        self.panel.add_child(title_label)
        
        # 消息
        message_label = Label(x + 10, y + 60, message, 24)
        self.panel.add_child(message_label)
        
        # 按钮
        button_width = 100
        button_height = 40
        button_y = y + height - 60
        
        # 确认按钮
        self.confirm_button = Button(
            x + width // 2 - button_width - 10,
            button_y,
            button_width,
            button_height,
            "确认",
            self._on_confirm if on_confirm else lambda: None
        )
        self.panel.add_child(self.confirm_button)
        
        # 取消按钮
        self.cancel_button = Button(
            x + width // 2 + 10,
            button_y,
            button_width,
            button_height,
            "取消",
            self._on_cancel if on_cancel else lambda: None
        )
        self.panel.add_child(self.cancel_button)
        
        # 回调函数
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
    
    def _on_confirm(self):
        """确认回调"""
        if self.on_confirm:
            self.on_confirm()
        self.visible = False
    
    def _on_cancel(self):
        """取消回调"""
        if self.on_cancel:
            self.on_cancel()
        self.visible = False
    
    def show(self):
        """显示对话框"""
        self.visible = True
    
    def hide(self):
        """隐藏对话框"""
        self.visible = False
    
    def render(self, screen: pygame.Surface):
        """渲染对话框"""
        if not self.visible:
            return
        
        # 绘制背景遮罩
        screen.blit(self.overlay, (0, 0))
        
        # 渲染对话框
        super().render(screen) 