import pygame
from typing import Optional, Type, List, Tuple
from scene_manager import Scene
from entities.player import Player
from entities.enemy import Enemy
from entities.geometric_enemies import TriangleEnemy, CircleEnemy, SquareEnemy
from ui.hud import HUD
from ui.ui_element import Label
import random
import math

class GameScene(Scene):
    """游戏主场景"""
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 游戏状态
        self.paused = False
        self.game_over = False
        
        # 玩家相关
        self.player_class = None
        self.player = None
        
        # 敌人列表
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 2000  # 每2秒生成一个敌人
        self.max_enemies = 10
        
        # 创建HUD
        self.hud = HUD(screen_width, screen_height)
        
        # 创建暂停和游戏结束提示
        self.pause_label = Label(
            screen_width // 2 - 100,
            screen_height // 2 - 50,
            "游戏暂停",
            64,
            bold=True
        )
        
        self.pause_tip = Label(
            screen_width // 2 - 150,
            screen_height // 2 + 20,
            "按ESC继续游戏",
            32
        )
        
        self.game_over_label = Label(
            screen_width // 2 - 150,
            screen_height // 2 - 50,
            "游戏结束",
            64,
            bold=True
        )
        
        print("游戏场景初始化完成，屏幕大小:", screen_width, "x", screen_height)
    
    def set_player_class(self, player_class: Type[Player]):
        """设置玩家类型"""
        self.player_class = player_class
        print(f"设置玩家类型: {player_class.__name__}")
    
    def initialize(self):
        """初始化场景"""
        try:
            if self.player_class:
                # 创建玩家
                self.player = self.player_class(
                    self.screen_width // 2,
                    self.screen_height // 2
                )
                # 设置HUD的玩家引用
                self.hud.set_player(self.player)
                print(f"玩家 {self.player.__class__.__name__} 已创建")
                
                # 重置游戏状态
                self.paused = False
                self.game_over = False
                self.enemies.clear()
                self.enemy_spawn_timer = pygame.time.get_ticks()
                
                print("游戏场景初始化完成")
            else:
                print("错误：未设置玩家类型")
        except Exception as e:
            print(f"初始化游戏场景时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                print(f"游戏{'暂停' if self.paused else '继续'}")
        
        if not self.paused and not self.game_over:
            if self.player:
                # 获取键盘状态
                keys = pygame.key.get_pressed()
                # 获取鼠标位置和按钮状态
                mouse_pos = pygame.mouse.get_pos()
                mouse_buttons = pygame.mouse.get_pressed()
                # 处理玩家输入
                self.player.handle_input(keys, mouse_pos, mouse_buttons)
    
    def _spawn_enemy(self):
        """生成敌人"""
        try:
            # 随机选择敌人类型
            enemy_types = [TriangleEnemy, CircleEnemy, SquareEnemy]
            enemy_class = random.choice(enemy_types)
            
            # 随机生成位置（在屏幕边缘）
            side = random.randint(0, 3)  # 0: 上, 1: 右, 2: 下, 3: 左
            if side == 0:  # 上边
                x = random.randint(0, self.screen_width)
                y = -50
            elif side == 1:  # 右边
                x = self.screen_width + 50
                y = random.randint(0, self.screen_height)
            elif side == 2:  # 下边
                x = random.randint(0, self.screen_width)
                y = self.screen_height + 50
            else:  # 左边
                x = -50
                y = random.randint(0, self.screen_height)
            
            # 创建敌人并设置目标
            enemy = enemy_class(x, y, self.player)
            self.enemies.append(enemy)
            print(f"生成敌人 {enemy_class.__name__} 在位置 ({x}, {y})")
        
        except Exception as e:
            print(f"生成敌人时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def _check_collisions(self):
        """检查碰撞"""
        try:
            if not self.player or not self.player.is_alive:
                return
            
            # 检查玩家子弹与敌人的碰撞
            for bullet in self.player.bullets[:]:
                bullet_rect = pygame.Rect(
                    bullet.x - bullet.radius,
                    bullet.y - bullet.radius,
                    bullet.radius * 2,
                    bullet.radius * 2
                )
                
                for enemy in self.enemies[:]:
                    if not enemy.is_alive:
                        continue
                    
                    enemy_rect = pygame.Rect(
                        enemy.x - enemy.width // 2,
                        enemy.y - enemy.height // 2,
                        enemy.width,
                        enemy.height
                    )
                    
                    if bullet_rect.colliderect(enemy_rect):
                        # 子弹击中敌人
                        enemy.take_damage(bullet.damage)
                        bullet.is_active = False
                        print(f"玩家子弹击中敌人，造成 {bullet.damage} 点伤害")
                        
                        # 如果敌人死亡，给予玩家奖励
                        if not enemy.is_alive:
                            self.player.score += 100
                            self.player.fragments += random.randint(1, 3)
                            self.player.experience += random.randint(10, 20)
                            print(f"击杀敌人，获得分数和资源")
                            
                            # 检查是否升级
                            if self.player.experience >= self.player.experience_to_next_level:
                                self.player.level_up()
                                print(f"玩家升级！当前等级: {self.player.level}")
            
            # 检查敌人子弹与玩家的碰撞
            player_rect = pygame.Rect(
                self.player.x - self.player.width // 2,
                self.player.y - self.player.height // 2,
                self.player.width,
                self.player.height
            )
            
            for enemy in self.enemies:
                for bullet in enemy.bullets[:]:
                    bullet_rect = pygame.Rect(
                        bullet.x - bullet.size,
                        bullet.y - bullet.size,
                        bullet.size * 2,
                        bullet.size * 2
                    )
                    
                    if bullet_rect.colliderect(player_rect):
                        # 敌人子弹击中玩家
                        self.player.take_damage(bullet.damage)
                        bullet.is_active = False
                        print(f"敌人子弹击中玩家，造成 {bullet.damage} 点伤害")
            
            # 检查玩家与敌人的直接碰撞
            for enemy in self.enemies:
                if not enemy.is_alive:
                    continue
                
                enemy_rect = pygame.Rect(
                    enemy.x - enemy.width // 2,
                    enemy.y - enemy.height // 2,
                    enemy.width,
                    enemy.height
                )
                
                if player_rect.colliderect(enemy_rect):
                    # 玩家与敌人碰撞
                    self.player.take_damage(enemy.get_damage())
                    enemy.take_damage(self.player.get_damage())
                    print(f"玩家与敌人碰撞，双方受到伤害")
        
        except Exception as e:
            print(f"检查碰撞时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def _check_screen_bounds(self):
        """检查并处理屏幕边界"""
        try:
            if not self.player:
                return
            
            # 获取玩家的边界矩形
            half_width = self.player.width // 2
            half_height = self.player.height // 2
            
            # 限制玩家在屏幕内
            self.player.x = max(half_width, min(self.screen_width - half_width, self.player.x))
            self.player.y = max(half_height, min(self.screen_height - half_height, self.player.y))
            
            # 检查子弹是否超出屏幕
            for bullet in self.player.bullets[:]:
                if (bullet.x < -50 or bullet.x > self.screen_width + 50 or
                    bullet.y < -50 or bullet.y > self.screen_height + 50):
                    bullet.is_active = False
            
            # 检查敌人是否超出屏幕太远（清理超出屏幕太远的敌人）
            margin = 100  # 额外边距
            for enemy in self.enemies[:]:
                if (enemy.x < -margin or enemy.x > self.screen_width + margin or
                    enemy.y < -margin or enemy.y > self.screen_height + margin):
                    self.enemies.remove(enemy)
                    print(f"清理超出屏幕的敌人")
        
        except Exception as e:
            print(f"检查屏幕边界时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def update(self):
        """更新场景"""
        if self.paused or self.game_over:
            return
        
        try:
            # 更新玩家
            if self.player:
                self.player.update()
                
                # 检查玩家是否死亡
                if not self.player.is_alive:
                    self.game_over = True
                    print("游戏结束！")
            
            # 生成敌人
            current_time = pygame.time.get_ticks()
            if (len(self.enemies) < self.max_enemies and 
                current_time - self.enemy_spawn_timer >= self.enemy_spawn_interval):
                self._spawn_enemy()
                self.enemy_spawn_timer = current_time
            
            # 更新敌人
            for enemy in self.enemies[:]:
                enemy.update()
                if not enemy.is_alive:
                    self.enemies.remove(enemy)
                    print(f"敌人被消灭，剩余敌人数量: {len(self.enemies)}")
            
            # 更新HUD
            self.hud.update()
            
            # 检查碰撞
            self._check_collisions()
            
            # 检查屏幕边界
            self._check_screen_bounds()
        
        except Exception as e:
            print(f"更新游戏场景时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def render(self, screen: pygame.Surface):
        """渲染场景"""
        try:
            # 清空屏幕
            screen.fill((30, 30, 30))  # 使用深灰色背景
            
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
                self.pause_label.render(screen)
                self.pause_tip.render(screen)
            elif self.game_over:
                self.game_over_label.render(screen)
        
        except Exception as e:
            print(f"渲染游戏场景时发生错误: {e}")
            import traceback
            traceback.print_exc()
            
            # 在错误情况下显示错误信息
            try:
                screen.fill((30, 30, 30))
                font = pygame.font.SysFont(None, 48)
                error_text = font.render("渲染错误", True, (255, 0, 0))
                screen.blit(error_text, (screen.get_width() // 2 - error_text.get_width() // 2,
                                       screen.get_height() // 2 - error_text.get_height() // 2))
            except:
                pass
    
    def _render_pause_screen(self, screen: pygame.Surface):
        """渲染暂停界面"""
        try:
            # 创建半透明遮罩
            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            screen.blit(overlay, (0, 0))
            
            # 渲染暂停文本和提示
            self.pause_label.render(screen)
            self.pause_tip.render(screen)
        
        except Exception as e:
            print(f"渲染暂停界面时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def _render_game_over_screen(self, screen: pygame.Surface):
        """渲染游戏结束界面"""
        try:
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
        
        except Exception as e:
            print(f"渲染游戏结束界面时发生错误: {e}")
            import traceback
            traceback.print_exc() 