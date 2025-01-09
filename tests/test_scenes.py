import unittest
import pygame
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scenes.game_scene import GameScene
from src.ui.main_menu import MainMenu
from src.entities.soldier import Soldier
from src.entities.assault import Assault
from src.entities.artillery import Artillery

class TestScenes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """初始化Pygame和测试环境"""
        pygame.init()
        cls.screen = pygame.Surface((1280, 720))
    
    def setUp(self):
        """每个测试用例开始前的设置"""
        self.screen.fill((0, 0, 0))
    
    def test_main_menu_render(self):
        """测试主菜单渲染"""
        menu = MainMenu(1280, 720)
        menu.render(self.screen)
        
        # 检查屏幕是否被填充（不是纯黑色）
        pixels = pygame.surfarray.pixels3d(self.screen)
        self.assertTrue(pixels.any(), "屏幕应该有内容而不是纯黑")
    
    def test_game_scene_render(self):
        """测试游戏场景渲染"""
        scene = GameScene(1280, 720)
        
        # 测试不同角色类型
        for player_class in [Soldier, Assault, Artillery]:
            scene.set_player_class(player_class)
            scene.initialize()
            scene.render(self.screen)
            
            # 检查屏幕是否被填充（不是纯黑色）
            pixels = pygame.surfarray.pixels3d(self.screen)
            self.assertTrue(pixels.any(), f"{player_class.__name__} 场景应该有内容而不是纯黑")
            
            # 检查玩家是否正确创建和渲染
            self.assertIsNotNone(scene.player, f"{player_class.__name__} 玩家应该被创建")
            self.assertTrue(scene.player.is_alive, f"{player_class.__name__} 玩家应该存活")
            
            # 重置屏幕
            self.screen.fill((0, 0, 0))
    
    def test_scene_transitions(self):
        """测试场景切换"""
        menu = MainMenu(1280, 720)
        game = GameScene(1280, 720)
        
        # 测试从主菜单到游戏场景的切换
        menu.render(self.screen)
        pixels_menu = pygame.surfarray.pixels3d(self.screen).copy()
        
        self.screen.fill((0, 0, 0))
        game.set_player_class(Soldier)
        game.initialize()
        game.render(self.screen)
        pixels_game = pygame.surfarray.pixels3d(self.screen).copy()
        
        # 确保两个场景的渲染结果不同
        self.assertFalse((pixels_menu == pixels_game).all(), "场景切换后显示应该不同")
    
    @classmethod
    def tearDownClass(cls):
        """清理测试环境"""
        pygame.quit()

if __name__ == '__main__':
    unittest.main() 