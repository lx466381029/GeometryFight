import pygame
from typing import Dict, Callable
from ui.ui_element import UIElement, Button, Label, Panel
from ui.dialog import Dialog
from scene_manager import Scene
from resource_manager import ResourceManager
from save_manager import SaveManager

class MainMenu(Scene):
    """主菜单场景"""
    def __init__(self, screen_width: int, screen_height: int):
        # 创建UI根节点
        self.ui_root = Panel(0, 0, screen_width, screen_height)
        
        # 创建标题
        title = Label(
            screen_width // 2 - 200,  # 向左移动以居中
            screen_height // 4,       # 移到屏幕1/4处
            "几何战斗",
            96,                       # 增大字号
            bold=True
        )
        self.ui_root.add_child(title)
        
        # 按钮设置
        button_width = 200
        button_height = 50
        button_spacing = 30
        start_y = screen_height // 2  # 从屏幕中间开始放置按钮
        
        # 创建按钮
        self.buttons = {}
        button_configs = [
            ('new_game', '新游戏'),
            ('continue', '继续游戏'),
            ('shop', '商店'),
            ('quit', '退出')
        ]
        
        # 回调函数字典
        self.callbacks = {}
        
        def create_button_callback(name: str):
            return lambda: self.on_button_click(name)
        
        for i, (name, text) in enumerate(button_configs):
            button = Button(
                screen_width // 2 - button_width // 2,
                start_y + i * (button_height + button_spacing),
                button_width,
                button_height,
                text,
                create_button_callback(name)  # 为每个按钮创建独立的回调函数
            )
            self.buttons[name] = button
            self.ui_root.add_child(button)
        
        # 创建确认对话框
        self.confirm_dialog = Dialog(
            screen_width // 2 - 200,
            screen_height // 2 - 100,
            400,
            200,
            "确认",
            "当前存在游戏存档，是否开始新游戏？\n这将覆盖现有存档。",
            self._on_new_game_confirmed,
            self._on_new_game_cancelled
        )
        self.ui_root.add_child(self.confirm_dialog)
        
        # 存档管理器
        self.save_manager = SaveManager()
        self.has_save = False
        
        # 资源管理器
        self.resource_manager = ResourceManager()
        
        print("主菜单初始化完成")
    
    def initialize(self):
        """初始化场景"""
        self.has_save = self.save_manager.save_exists()
        self._update_button_states()
    
    def _update_button_states(self):
        """更新按钮状态"""
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
            self.confirm_dialog.show()
            return
        
        if button_name in self.callbacks:
            self.callbacks[button_name]()
    
    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        self.ui_root.handle_event(event)
    
    def update(self):
        """更新主菜单"""
        self.ui_root.update()
    
    def render(self, screen: pygame.Surface):
        """渲染主菜单"""
        # 绘制背景
        screen.fill((30, 30, 30))
        
        # 渲染UI元素
        self.ui_root.render(screen) 