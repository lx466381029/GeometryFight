import pygame
from typing import Optional, Type
from src.scene_manager import Scene
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.ui.hud import HUD
from src.ui.ui_element import Label

class GameScene(Scene):
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 玩家
        self.player: Optional[Player] = None
        self.player_class: Optional[Type[Player]] = None
        
        # 敌人列表
        self.enemies: list[Enemy] = []
        
        # UI
        self.hud = HUD(screen_width, screen_height)
        
        # 游戏状态
        self.paused = False
        self.game_over = False
        
        # 创建暂停和游戏结束标签
        self.pause_label = Label(
            screen_width // 2 - 100,
            screen_height // 2 - 50,
            "游戏暂停",
            64,
            bold=True
        )
        self.pause_tip = Label(
            screen_width // 2 - 75,
            screen_height // 2 + 50,
            "按ESC继续",
            32
        )
        
        self.game_over_label = Label(
            screen_width // 2 - 100,
            screen_height // 2 - 50,
            "游戏结束",
            64,
            bold=True,
            color=(255, 0, 0)
        )
    
    def set_player_class(self, player_class: Type[Player]):
        """设置玩家类型"""
        self.player_class = player_class
    
    def initialize(self):
        """初始化场景"""
        if self.player_class:
            # 创建玩家
            self.player = self.player_class(
                self.screen_width // 2,
                self.screen_height // 2
            )
            # 设置HUD的玩家引用
            self.hud.set_player(self.player)
    
    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
        
        if not self.paused and not self.game_over:
            if self.player:
                self.player.handle_event(event)
    
    def update(self):
        """更新场景"""
        if self.paused or self.game_over:
            return
        
        # 更新玩家
        if self.player:
            self.player.update()
            
            # 检查玩家是否死亡
            if not self.player.is_alive:
                self.game_over = True
        
        # 更新敌人
        for enemy in self.enemies[:]:
            enemy.update()
            if not enemy.is_alive:
                self.enemies.remove(enemy)
        
        # 更新HUD
        self.hud.update()
        
        # 检查碰撞
        self._check_collisions()
    
    def render(self, screen: pygame.Surface):
        """渲染场景"""
        # 清空屏幕
        screen.fill((0, 0, 0))
        
        # 渲染敌人
        for enemy in self.enemies:
            enemy.render(screen)
        
        # 渲染玩家
        if self.player:
            self.player.render(screen)
        
        # 渲染HUD
        self.hud.render(screen)
        
        # 渲染暂停或游戏结束提示
        if self.paused:
            self._render_pause_screen(screen)
        elif self.game_over:
            self._render_game_over_screen(screen)
    
    def _check_collisions(self):
        """检查碰撞"""
        if not self.player:
            return
        
        # 检查玩家子弹与敌人的碰撞
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies:
                if enemy.contains_point(bullet.x, bullet.y):
                    enemy.take_damage(bullet.damage)
                    bullet.is_active = False
                    break
        
        # 检查敌人子弹与玩家的碰撞
        for enemy in self.enemies:
            for bullet in enemy.bullets[:]:
                if self.player.contains_point(bullet.x, bullet.y):
                    self.player.take_damage(bullet.damage)
                    bullet.is_active = False
        
        # 检查玩家与敌人的直接碰撞
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(enemy.get_damage())
                enemy.take_damage(self.player.get_damage())
    
    def _render_pause_screen(self, screen: pygame.Surface):
        """渲染暂停界面"""
        # 创建半透明遮罩
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # 渲染暂停文本和提示
        self.pause_label.render(screen)
        self.pause_tip.render(screen)
    
    def _render_game_over_screen(self, screen: pygame.Surface):
        """渲染游戏结束界面"""
        # 创建半透明遮罩
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # 渲染游戏结束文本
        self.game_over_label.render(screen)
        
        if self.player:
            # 渲染得分
            score_label = Label(
                self.screen_width // 2 - 75,
                self.screen_height // 2 + 50,
                f"得分: {self.player.score}",
                48,
                bold=True
            )
            score_label.render(screen)
            
            # 渲染资源获取情况
            fragment_label = Label(
                self.screen_width // 2 - 75,
                self.screen_height // 2 + 100,
                f"获得碎片: {self.player.fragments}",
                32
            )
            fragment_label.render(screen)
            
            star_label = Label(
                self.screen_width // 2 - 75,
                self.screen_height // 2 + 130,
                f"获得星星: {self.player.stars}",
                32
            )
            star_label.render(screen) 