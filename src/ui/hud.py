import pygame
from typing import Optional
from ui.ui_element import UIElement, Label, ProgressBar, Panel
from entities.player import Player
from scene_manager import Scene

class HUD(Scene, UIElement):
    def __init__(self, screen_width: int, screen_height: int):
        UIElement.__init__(self, 0, 0, screen_width, screen_height)
        
        # 创建状态面板
        panel_width = 300
        panel_height = 150
        self.status_panel = Panel(
            20, 20,
            panel_width, panel_height,
            color=(50, 50, 50, 200)
        )
        self.add_child(self.status_panel)
        
        # 创建角色信息标签
        self.character_label = Label(
            30, 30,
            "角色：士兵",
            32,
            bold=True
        )
        self.status_panel.add_child(self.character_label)
        
        # 创建生命值标签和进度条
        self.health_label = Label(30, 70, "生命值: 100/100", 24)
        self.health_bar = ProgressBar(30, 100, 260, 20, (255, 0, 0))
        self.status_panel.add_child(self.health_label)
        self.status_panel.add_child(self.health_bar)
        
        # 创建经验值标签和进度条
        self.exp_label = Label(30, 130, "经验值: 0/100", 24)
        self.exp_bar = ProgressBar(30, 160, 260, 20, (0, 255, 0))
        self.status_panel.add_child(self.exp_label)
        self.status_panel.add_child(self.exp_bar)
        
        # 创建资源面板
        self.resource_panel = Panel(
            screen_width - 220, 20,
            200, 120,
            color=(50, 50, 50, 200)
        )
        self.add_child(self.resource_panel)
        
        # 创建资源标签
        self.score_label = Label(screen_width - 210, 30, "得分: 0", 24)
        self.fragment_label = Label(screen_width - 210, 60, "碎片: 0", 24)
        self.star_label = Label(screen_width - 210, 90, "星星: 0", 24)
        
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
        # 更新角色标签
        character_names = {
            'Soldier': '士兵',
            'Assault': '突击手',
            'Artillery': '炮兵',
            'Tank': '坦克',
            'Sniper': '狙击手'
        }
        character_name = character_names.get(player.__class__.__name__, player.__class__.__name__)
        self.character_label.set_text(f"角色：{character_name}")
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