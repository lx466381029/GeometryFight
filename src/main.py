import pygame
import sys
from src.game_manager import GameManager
from src.resource_manager import ResourceManager
from src.scene_manager import SceneManager
from src.save_manager import SaveManager
from src.ui.main_menu import MainMenu
from src.ui.character_select import CharacterSelect
from src.ui.shop import Shop
from src.scenes.game_scene import GameScene

def main():
    try:
        # 初始化Pygame
        pygame.init()
        if not pygame.display.get_init():
            print("无法初始化显示模块")
            return
        
        if not pygame.font.get_init():
            pygame.font.init()
            if not pygame.font.get_init():
                print("无法初始化字体模块")
                return
        
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            if not pygame.mixer.get_init():
                print("无法初始化音频模块")
                return
        
        # 创建游戏管理器
        game_manager = GameManager()
        
        # 创建屏幕
        screen = pygame.display.set_mode((game_manager.screen_width, game_manager.screen_height))
        pygame.display.set_caption("几何战斗")
        
        # 创建资源管理器
        resource_manager = ResourceManager()
        
        # 创建场景管理器
        scene_manager = SceneManager()
        
        # 创建存档管理器
        save_manager = SaveManager()
        
        # 创建场景
        main_menu = MainMenu(game_manager.screen_width, game_manager.screen_height)
        character_select = CharacterSelect(game_manager.screen_width, game_manager.screen_height)
        shop = Shop(game_manager.screen_width, game_manager.screen_height)
        game_scene = GameScene(game_manager.screen_width, game_manager.screen_height)
        
        # 注册场景
        scene_manager.register_scene("main_menu", main_menu)
        scene_manager.register_scene("character_select", character_select)
        scene_manager.register_scene("shop", shop)
        scene_manager.register_scene("game", game_scene)
        
        # 设置主菜单回调
        def start_game():
            scene_manager.switch_scene("character_select")
        
        def open_shop():
            scene_manager.switch_scene("shop")
        
        def quit_game():
            game_manager.quit()
        
        main_menu.set_callback("new_game", start_game)
        main_menu.set_callback("continue", lambda: scene_manager.switch_scene("game"))
        main_menu.set_callback("quit", quit_game)
        
        # 设置角色选择回调
        def on_character_select(player_class):
            game_scene.set_player_class(player_class)
            # 切换到游戏场景并播放战斗音乐
            scene_manager.switch_scene("game")
            resource_manager.play_music("battle_bgm", loop=True)
        
        def back_to_menu():
            scene_manager.switch_scene("main_menu")
            # 切换回主菜单音乐
            resource_manager.play_music("menu_bgm", loop=True)
        
        character_select.set_callbacks(on_character_select, back_to_menu)
        
        # 设置商店回调
        shop.back_button.callback = back_to_menu
        
        # 切换到主菜单并播放菜单音乐
        scene_manager.switch_scene("main_menu")
        resource_manager.play_music("menu_bgm", loop=True)
        
        print("游戏初始化完成，开始主循环")
        
        # 游戏主循环
        clock = pygame.time.Clock()
        while game_manager.running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_manager.quit()
                else:
                    scene_manager.handle_event(event)
            
            # 更新游戏状态
            game_manager.update()
            scene_manager.update()
            
            # 渲染画面
            screen.fill((30, 30, 30))  # 背景色
            scene_manager.render(screen)
            pygame.display.flip()
            
            # 控制帧率
            clock.tick(game_manager.fps)
        
        # 退出游戏
        pygame.quit()
    
    except Exception as e:
        print(f"游戏发生错误: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main() 