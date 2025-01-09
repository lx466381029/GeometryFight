import pygame
from typing import Optional
from ui.ui_element import UIElement, Label, ProgressBar, Panel
from entities.player import Player
from scene_manager import Scene

class HUD(Scene, UIElement):
    def __init__(self, screen_width: int, screen_height: int):
        UIElement.__init__(self, 0, 0, screen_width, screen_height)
        
        # 创建状态面板
        self.status_panel = Panel(10, 10, 200, 100)
        self.add_child(self.status_panel)
        
        # 创建状态标签和进度条
        self.health_label = Label(20, 20, "生命值: 100/100", bold=True)
        self.health_bar = ProgressBar(20, 45, 180, 15, 
                                    fill_color=(255, 0, 0))
        
        self.exp_label = Label(20, 70, "经验值: 0/100", bold=True)
        self.exp_bar = ProgressBar(20, 95, 180, 15, 
                                 fill_color=(0, 255, 255))
        
        # 添加到状态面板
        self.status_panel.add_child(self.health_label)
        self.status_panel.add_child(self.health_bar)
        self.status_panel.add_child(self.exp_label)
        self.status_panel.add_child(self.exp_bar)
        
        # 创建得分和资源面板
        self.resource_panel = Panel(screen_width - 210, 10, 200, 100)
        self.add_child(self.resource_panel)
        
        # 创建资源标签
        self.score_label = Label(screen_width - 200, 20, "得分: 0", bold=True)
        self.fragment_label = Label(screen_width - 200, 50, "碎片: 0", bold=True)
        self.star_label = Label(screen_width - 200, 80, "星星: 0", bold=True)
        
        # 添加到资源面板
        self.resource_panel.add_child(self.score_label)
        self.resource_panel.add_child(self.fragment_label)
        self.resource_panel.add_child(self.star_label)
        
        # 玩家引用
        self.player: Optional[Player] = None
        
        print("HUD初始化完成")
    
    def initialize(self):
        """初始化场景"""
        pass
    
    def set_player(self, player: Player):
        """设置要监控的玩家"""
        self.player = player
        print(f"HUD设置玩家: {player.__class__.__name__}")
    
    def update(self):
        """更新HUD显示的信息"""
        super().update()
        
        if self.player:
            # 更新生命值
            health_text = f"生命值: {int(self.player.health)}/{int(self.player.max_health)}"
            self.health_label.set_text(health_text)
            self.health_bar.set_progress(self.player.health / self.player.max_health)
            
            # 更新经验值
            exp_needed = self.player.experience_to_next_level
            exp_text = f"经验值: {self.player.experience}/{exp_needed}"
            self.exp_label.set_text(exp_text)
            self.exp_bar.set_progress(self.player.experience / exp_needed)
            
            # 更新资源
            self.score_label.set_text(f"得分: {self.player.score}")
            self.fragment_label.set_text(f"碎片: {self.player.fragments}")
            self.star_label.set_text(f"星星: {self.player.stars}")
            
            print(f"HUD更新 - 生命值: {int(self.player.health)}/{int(self.player.max_health)} " +
                  f"经验值: {self.player.experience}/{exp_needed} " +
                  f"得分: {self.player.score} " +
                  f"碎片: {self.player.fragments} " +
                  f"星星: {self.player.stars}")
    
    def render(self, screen: pygame.Surface):
        """渲染HUD"""
        super().render(screen) 