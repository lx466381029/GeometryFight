import pygame
from typing import Dict, List, Callable, Optional
from src.ui.ui_element import UIElement, Button, Label, Panel
from src.entities.player import Player
from src.scene_manager import Scene

class ShopItem:
    """商店物品"""
    def __init__(self, name: str, description: str, price: int, 
                 currency: str, effect: Callable[[Player], None]):
        self.name = name
        self.description = description
        self.price = price
        self.currency = currency  # 'fragments' 或 'stars'
        self.effect = effect

class ItemCard(Panel):
    """物品卡片"""
    def __init__(self, x: int, y: int, width: int, height: int, 
                 item: ShopItem, on_purchase: Callable[[], None]):
        super().__init__(x, y, width, height)
        
        # 物品名称
        name_label = Label(x + 10, y + 10, item.name, 24, bold=True)
        self.add_child(name_label)
        
        # 物品描述
        desc_label = Label(x + 10, y + 40, item.description, 18)
        self.add_child(desc_label)
        
        # 价格
        currency_symbol = "★" if item.currency == "stars" else "◆"
        price_label = Label(
            x + 10, 
            y + height - 40,
            f"价格: {item.price}{currency_symbol}",
            20
        )
        self.add_child(price_label)
        
        # 购买按钮
        self.purchase_button = Button(
            x + width - 90,
            y + height - 40,
            80,
            30,
            "购买",
            on_purchase
        )
        self.add_child(self.purchase_button)

class Shop(Scene, UIElement):
    def __init__(self, screen_width: int, screen_height: int):
        UIElement.__init__(self, 0, 0, screen_width, screen_height)
        
        # 创建标题
        title_label = Label(screen_width // 2 - 50, 50, "商店", 48, bold=True)
        self.add_child(title_label)
        
        # 创建标签页按钮
        tab_width = 150
        tab_height = 40
        tab_y = 120
        
        self.temp_shop_button = Button(
            screen_width // 2 - tab_width - 10,
            tab_y,
            tab_width,
            tab_height,
            "临时商店",
            lambda: self.switch_shop('temp')
        )
        self.add_child(self.temp_shop_button)
        
        self.perm_shop_button = Button(
            screen_width // 2 + 10,
            tab_y,
            tab_width,
            tab_height,
            "永久商店",
            lambda: self.switch_shop('perm')
        )
        self.add_child(self.perm_shop_button)
        
        # 创建商店面板
        panel_width = screen_width - 200
        panel_height = screen_height - 300
        self.shop_panel = Panel(
            100,
            180,
            panel_width,
            panel_height
        )
        self.add_child(self.shop_panel)
        
        # 返回按钮
        self.back_button = Button(
            screen_width // 2 - 75,
            screen_height - 80,
            150,
            40,
            "返回",
            lambda: None  # 将在外部设置
        )
        self.add_child(self.back_button)
        
        # 商店物品
        self.temp_items: List[ShopItem] = [
            ShopItem(
                "生命恢复",
                "恢复50%最大生命值",
                30,
                "fragments",
                lambda player: setattr(player, 'health', 
                                     min(player.health + player.max_health * 0.5,
                                         player.max_health))
            ),
            ShopItem(
                "攻击力提升",
                "临时提升30%攻击力，持续60秒",
                40,
                "fragments",
                lambda player: setattr(player, 'damage_bonus', 
                                     player.damage_bonus + 0.3)
            ),
            ShopItem(
                "速度提升",
                "临时提升20%移动速度，持续60秒",
                35,
                "fragments",
                lambda player: setattr(player, 'speed_bonus', 
                                     player.speed_bonus + 0.2)
            )
        ]
        
        self.perm_items: List[ShopItem] = [
            ShopItem(
                "最大生命值提升",
                "永久提升10%最大生命值",
                3,
                "stars",
                lambda player: setattr(player, 'max_health', 
                                     player.max_health * 1.1)
            ),
            ShopItem(
                "基础攻击力提升",
                "永久提升10%基础攻击力",
                4,
                "stars",
                lambda player: setattr(player, 'base_damage', 
                                     player.base_damage * 1.1)
            ),
            ShopItem(
                "基础速度提升",
                "永久提升10%基础速度",
                4,
                "stars",
                lambda player: setattr(player, 'base_speed', 
                                     player.base_speed * 1.1)
            )
        ]
        
        # 当前显示的商店类型
        self.current_shop = 'temp'
        self.current_items = self.temp_items
        
        # 创建物品卡片
        self.item_cards: Dict[str, List[ItemCard]] = {
            'temp': [],
            'perm': []
        }
        
        self._create_item_cards()
        
        # 玩家引用
        self.player: Optional[Player] = None
        
        # 回调函数
        self.on_back: Optional[Callable[[], None]] = None
    
    def initialize(self):
        """初始化场景"""
        pass
    
    def _create_item_cards(self):
        """创建物品卡片"""
        card_width = 300
        card_height = 120
        cards_per_row = 2
        spacing_x = 50
        spacing_y = 30
        
        start_x = self.shop_panel.x + (self.shop_panel.width - 
                                     (card_width * cards_per_row + 
                                      spacing_x * (cards_per_row - 1))) // 2
        start_y = self.shop_panel.y + 20
        
        # 创建临时商店卡片
        for i, item in enumerate(self.temp_items):
            row = i // cards_per_row
            col = i % cards_per_row
            card = ItemCard(
                start_x + col * (card_width + spacing_x),
                start_y + row * (card_height + spacing_y),
                card_width,
                card_height,
                item,
                lambda item=item: self.purchase_item(item)
            )
            self.item_cards['temp'].append(card)
        
        # 创建永久商店卡片
        for i, item in enumerate(self.perm_items):
            row = i // cards_per_row
            col = i % cards_per_row
            card = ItemCard(
                start_x + col * (card_width + spacing_x),
                start_y + row * (card_height + spacing_y),
                card_width,
                card_height,
                item,
                lambda item=item: self.purchase_item(item)
            )
            self.item_cards['perm'].append(card)
    
    def switch_shop(self, shop_type: str):
        """切换商店类型"""
        self.current_shop = shop_type
        self.current_items = (self.temp_items if shop_type == 'temp' 
                            else self.perm_items)
        
        # 更新按钮状态
        self.temp_shop_button.pressed = shop_type == 'temp'
        self.perm_shop_button.pressed = shop_type == 'perm'
        
        # 更新商店面板的子元素
        self.shop_panel.children.clear()
        for card in self.item_cards[shop_type]:
            self.shop_panel.add_child(card)
    
    def set_player(self, player: Player):
        """设置玩家引用"""
        self.player = player
    
    def purchase_item(self, item: ShopItem):
        """购买物品"""
        if not self.player:
            return
        
        # 检查是否有足够的货币
        if item.currency == 'fragments':
            if self.player.fragments >= item.price:
                self.player.fragments -= item.price
                item.effect(self.player)
        else:  # stars
            if self.player.stars >= item.price:
                self.player.stars -= item.price
                item.effect(self.player)
    
    def set_callbacks(self, on_back: Callable[[], None]):
        """设置回调函数"""
        self.on_back = on_back
        self.back_button.callback = on_back
    
    def update(self):
        """更新商店界面"""
        super().update()
        
        if not self.player:
            return
        
        # 更新物品可购买状态
        for card in self.item_cards[self.current_shop]:
            item = next(item for item in self.current_items 
                       if item.name == card.children[0].text)
            if item.currency == 'fragments':
                card.purchase_button.enabled = self.player.fragments >= item.price
            else:
                card.purchase_button.enabled = self.player.stars >= item.price
    
    def render(self, screen: pygame.Surface):
        """渲染商店界面"""
        # 绘制背景
        screen.fill((30, 30, 30))
        
        # 渲染UI元素
        super().render(screen)
        
        # 渲染货币信息
        if self.player:
            fragment_text = f"碎片: {self.player.fragments}"
            star_text = f"星星: {self.player.stars}"
            
            fragment_label = Label(20, 20, fragment_text)
            star_label = Label(20, 50, star_text)
            
            fragment_label.render(screen)
            star_label.render(screen) 