import pygame
import json
import os
from typing import Dict, Callable
from src.ui.ui_element import UIElement, Button, Label, Panel
from src.ui.dialog import Dialog
from src.scene_manager import Scene
from src.resource_manager import ResourceManager
from src.save_manager import SaveManager

class MainMenu(Scene, UIElement):
    def __init__(self, screen_width: int, screen_height: int):
        UIElement.__init__(self, 0, 0, screen_width, screen_height)
        
        # 创建标题
        title_label = Label(
            screen_width // 2 - 200,  # 调整X坐标
            100,
            "几何战斗",
            72,  # 增大字体大小
            bold=True,
            color=(255, 255, 255)  # 设置为白色
        )
        self.add_child(title_label)
        
        # 创建主菜单面板
        panel_width = 300
        panel_height = 400
        menu_panel = Panel(
            screen_width // 2 - panel_width // 2,
            200,
            panel_width,
            panel_height,
            color=(50, 50, 50, 200)  # 半透明深灰色
        )
        self.add_child(menu_panel)
        
        # 创建按钮
        button_width = 200
        button_height = 50
        button_spacing = 30  # 按钮之间的间距
        button_x = screen_width // 2 - button_width // 2
        start_y = 250
        
        self.buttons: Dict[str, Button] = {}
        
        # 新游戏按钮
        self.buttons['new_game'] = Button(
            button_x,
            start_y,
            button_width,
            button_height,
            "开始新游戏",
            lambda: self.on_button_click('new_game')
        )
        
        # 继续游戏按钮
        self.buttons['continue'] = Button(
            button_x,
            start_y + button_height + button_spacing,
            button_width,
            button_height,
            "继续游戏",
            lambda: self.on_button_click('continue')
        )
        
        # 退出按钮
        self.buttons['quit'] = Button(
            button_x,
            start_y + (button_height + button_spacing) * 2,
            button_width,
            button_height,
            "退出游戏",
            lambda: self.on_button_click('quit')
        )
        
        # 添加按钮到面板
        for button in self.buttons.values():
            menu_panel.add_child(button)
        
        # 回调函数字典
        self.callbacks: Dict[str, Callable[[], None]] = {}
        
        # 资源管理器
        self.resource_manager = ResourceManager()
        
        # 存档管理器
        self.save_manager = SaveManager()
        
        # 检查存档状态
        self.has_save = self.save_manager.save_exists()
        
        # 更新按钮状态
        self._update_button_states()
        
        # 创建确认对话框
        dialog_width = 400
        dialog_height = 200
        dialog_x = screen_width // 2 - dialog_width // 2
        dialog_y = screen_height // 2 - dialog_height // 2
        
        self.confirm_dialog = Dialog(
            dialog_x,
            dialog_y,
            dialog_width,
            dialog_height,
            "确认新游戏",
            "已存在存档，开始新游戏将覆盖现有存档。\n是否继续？",
            self._on_new_game_confirmed,
            self._on_new_game_cancelled
        )
        self.confirm_dialog.visible = False
        self.add_child(self.confirm_dialog)
    
    def initialize(self):
        """初始化场景"""
        # 检查存档状态并更新按钮
        self.has_save = self.save_manager.save_exists()
        self._update_button_states()
    
    def _update_button_states(self):
        """更新按钮状态"""
        # 继续游戏按钮只在有存档时可用
        self.buttons['continue'].enabled = self.has_save
    
    def set_callback(self, button_name: str, callback: Callable[[], None]):
        """设置按钮回调函数"""
        self.callbacks[button_name] = callback
    
    def _on_new_game_confirmed(self):
        """确认开始新游戏"""
        if 'new_game' in self.callbacks:
            self.callbacks['new_game']()
    
    def _on_new_game_cancelled(self):
        """取消开始新游戏"""
        pass
    
    def on_button_click(self, button_name: str):
        """处理按钮点击"""
        if button_name == 'new_game' and self.has_save:
            # 如果已有存档，显示确认对话框
            self.confirm_dialog.show()
            return
        
        if button_name in self.callbacks:
            self.callbacks[button_name]()
    
    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        if self.confirm_dialog.visible:
            self.confirm_dialog.handle_event(event)
        else:
            super().handle_event(event)
    
    def update(self):
        """更新主菜单"""
        super().update()
    
    def render(self, screen: pygame.Surface):
        """渲染主菜单"""
        # 绘制背景
        screen.fill((30, 30, 30))  # 深灰色背景
        
        # 渲染UI元素
        super().render(screen) 