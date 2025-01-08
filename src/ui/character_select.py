import pygame
from typing import Dict, Callable, Optional, Type
from src.ui.ui_element import UIElement, Button, Label, Panel
from src.entities.player import Player
from src.entities.soldier import Soldier
from src.entities.assault import Assault
from src.entities.artillery import Artillery
from src.scene_manager import Scene

class CharacterCard(Panel):
    """角色信息卡片"""
    def __init__(self, x: int, y: int, width: int, height: int, 
                 character_class: Type[Player]):
        super().__init__(x, y, width, height)
        
        # 创建示例角色
        self.character = character_class(0, 0)
        
        # 角色名称（中文）
        character_names = {
            'Soldier': '士兵',
            'Assault': '突击手',
            'Artillery': '炮兵'
        }
        name = character_names.get(character_class.__name__, character_class.__name__)
        name_label = Label(x + 10, y + 10, name, 32, bold=True)
        self.add_child(name_label)
        
        # 角色属性
        stats_x = x + 10
        stats_y = y + 50
        line_height = 25
        
        # 基础属性
        stats = [
            f"生命值: {self.character.max_health}",
            f"速度: {self.character.speed}",
            f"伤害: {self.character.damage}",
            f"攻击速度: {self.character.attack_speed}"
        ]
        
        for i, stat in enumerate(stats):
            stat_label = Label(stats_x, stats_y + i * line_height, stat)
            self.add_child(stat_label)
        
        # 选择按钮
        self.select_button = Button(
            x + width // 4,
            y + height - 40,
            width // 2,
            30,
            "选择",
            lambda: None  # 将在外部设置回调
        )
        self.add_child(self.select_button)
    
    def set_selected(self, selected: bool):
        """设置是否被选中"""
        self.color = (100, 100, 100, 200) if selected else (50, 50, 50, 200)

class CharacterSelect(Scene, UIElement):
    def __init__(self, screen_width: int, screen_height: int):
        UIElement.__init__(self, 0, 0, screen_width, screen_height)
        
        # 创建标题
        title_label = Label(screen_width // 2 - 100, 50, "选择角色", 48, bold=True)
        self.add_child(title_label)
        
        # 角色卡片
        card_width = 250
        card_height = 300
        spacing = 50
        total_width = (card_width + spacing) * 3 - spacing
        start_x = screen_width // 2 - total_width // 2
        
        self.character_cards: Dict[str, CharacterCard] = {}
        self.selected_character: Optional[Type[Player]] = None
        
        # 创建角色卡片
        character_classes = [Soldier, Assault, Artillery]
        for i, char_class in enumerate(character_classes):
            card = CharacterCard(
                start_x + i * (card_width + spacing),
                150,
                card_width,
                card_height,
                char_class
            )
            self.character_cards[char_class.__name__] = card
            card.select_button.callback = lambda c=char_class: self.select_character(c)
            self.add_child(card)
        
        # 创建确认和返回按钮
        button_width = 150
        button_height = 40
        button_y = screen_height - 100
        
        # 确认按钮
        self.confirm_button = Button(
            screen_width // 2 - button_width - 20,
            button_y,
            button_width,
            button_height,
            "确认",
            self.confirm_selection
        )
        self.add_child(self.confirm_button)
        
        # 返回按钮
        self.back_button = Button(
            screen_width // 2 + 20,
            button_y,
            button_width,
            button_height,
            "返回",
            lambda: None  # 将在外部设置回调
        )
        self.add_child(self.back_button)
        
        # 回调函数
        self.on_confirm: Optional[Callable[[Type[Player]], None]] = None
        self.on_back: Optional[Callable[[], None]] = None
    
    def initialize(self):
        """初始化场景"""
        pass
    
    def select_character(self, character_class: Type[Player]):
        """选择角色"""
        self.selected_character = character_class
        
        # 更新卡片显示
        for name, card in self.character_cards.items():
            card.set_selected(name == character_class.__name__)
    
    def confirm_selection(self):
        """确认选择"""
        if self.selected_character and self.on_confirm:
            self.on_confirm(self.selected_character)
    
    def set_callbacks(self, on_confirm: Callable[[Type[Player]], None], 
                     on_back: Callable[[], None]):
        """设置回调函数"""
        self.on_confirm = on_confirm
        self.on_back = on_back
        self.back_button.callback = on_back
    
    def update(self):
        """更新角色选择界面"""
        super().update()
        
        # 禁用确认按钮，直到选择了角色
        self.confirm_button.enabled = self.selected_character is not None
    
    def render(self, screen: pygame.Surface):
        """渲染角色选择界面"""
        # 绘制背景
        screen.fill((30, 30, 30))
        
        # 渲染UI元素
        super().render(screen) 