import pygame
import sys
import traceback
import time
from game_manager import GameManager, GameState
from resource_manager import ResourceManager
from scene_manager import SceneManager
from save_manager import SaveManager
from ui.main_menu import MainMenu
from ui.character_select import CharacterSelect
from ui.shop import Shop
from scenes.game_scene import GameScene

def initialize_game():
    """初始化游戏"""
    try:
        # 初始化Pygame
        pygame.init()
        if not pygame.display.get_init():
            print("错误：无法初始化显示模块")
            return None, None, None, None, None
        
        if not pygame.font.get_init():
            pygame.font.init()
            if not pygame.font.get_init():
                print("错误：无法初始化字体模块")
                return None, None, None, None, None
        
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            if not pygame.mixer.get_init():
                print("错误：无法初始化音频模块")
                return None, None, None, None, None
        
        print("Pygame初始化成功")
        
        # 创建游戏管理器
        game_manager = GameManager()
        print(f"游戏管理器创建成功，屏幕大小：{game_manager.screen_width}x{game_manager.screen_height}")
        
        try:
            # 创建窗口化屏幕
            screen = pygame.display.set_mode(
                (game_manager.screen_width, game_manager.screen_height),
                pygame.HWSURFACE | pygame.DOUBLEBUF  # 移除全屏标志
            )
            pygame.display.set_caption("几何战斗")
            print("显示窗口创建成功")
            
            # 设置图标
            try:
                icon = pygame.Surface((32, 32))
                icon.fill((255, 0, 0))  # 创建一个红色方块作为临时图标
                pygame.display.set_icon(icon)
            except pygame.error as e:
                print(f"设置窗口图标失败: {e}")
        except pygame.error as e:
            print(f"错误：无法创建显示窗口: {e}")
            return None, None, None, None, None
        
        # 创建资源管理器
        resource_manager = ResourceManager()
        print("资源管理器创建成功")
        
        # 创建场景管理器
        scene_manager = SceneManager()
        print("场景管理器创建成功")
        
        # 创建存档管理器
        save_manager = SaveManager()
        print("存档管理器创建成功")
        
        return game_manager, screen, resource_manager, scene_manager, save_manager
    except Exception as e:
        print(f"初始化游戏时发生错误: {e}")
        traceback.print_exc()
        return None, None, None, None, None

def create_scenes(game_manager, scene_manager, resource_manager):
    """创建并注册场景"""
    try:
        # 创建场景
        main_menu = MainMenu(game_manager.screen_width, game_manager.screen_height)
        shop = Shop(game_manager.screen_width, game_manager.screen_height)
        game_scene = GameScene(game_manager.screen_width, game_manager.screen_height)
        print("所有场景创建成功")
        
        # 注册场景
        scene_manager.register_scene("main_menu", main_menu)
        scene_manager.register_scene("shop", shop)
        scene_manager.register_scene("game", game_scene)
        print("场景注册完成")
        
        # 设置主菜单回调
        def start_game():
            # 直接使用士兵作为默认角色
            from entities.soldier import Soldier
            game_scene.set_player_class(Soldier)
            game_scene.initialize()
            game_manager.change_state(GameState.PLAYING)
            scene_manager.switch_scene("game")
            resource_manager.play_music("battle_bgm", loop=True)
            print("开始游戏，使用士兵角色")
        
        def open_shop():
            game_manager.change_state(GameState.SHOPPING)
            scene_manager.switch_scene("shop")
            print("切换到商店界面")
        
        def quit_game():
            game_manager.change_state(GameState.QUITTING)
            game_manager.quit()
        
        main_menu.set_callback("new_game", start_game)
        main_menu.set_callback("continue", lambda: scene_manager.switch_scene("game"))
        main_menu.set_callback("shop", open_shop)
        main_menu.set_callback("quit", quit_game)
        print("主菜单回调设置完成")
        
        # 设置商店回调
        def back_to_menu():
            game_manager.change_state(GameState.MAIN_MENU)
            scene_manager.switch_scene("main_menu")
            # 切换回主菜单音乐
            resource_manager.play_music("menu_bgm", loop=True)
            print("返回主菜单")
        
        shop.back_button.callback = back_to_menu
        print("商店回调设置完成")
        
        return True
    except Exception as e:
        print(f"创建场景时发生错误: {e}")
        traceback.print_exc()
        return False

def main():
    """游戏主函数"""
    # 初始化游戏
    game_manager, screen, resource_manager, scene_manager, save_manager = initialize_game()
    if not all([game_manager, screen, resource_manager, scene_manager, save_manager]):
        print("游戏初始化失败")
        return
    
    # 创建场景
    if not create_scenes(game_manager, scene_manager, resource_manager):
        print("场景创建失败")
        return
    
    # 切换到主菜单并播放菜单音乐
    game_manager.change_state(GameState.MAIN_MENU)
    scene_manager.switch_scene("main_menu")
    resource_manager.play_music("menu_bgm", loop=True)
    
    print("游戏初始化完成，开始主循环")
    
    # 游戏主循环
    clock = pygame.time.Clock()
    last_performance_check = time.time()
    performance_check_interval = 5.0  # 每5秒检查一次性能
    
    try:
        while game_manager.running:
            try:
                loop_start_time = time.time()
                
                # 处理事件
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_manager.change_state(GameState.QUITTING)
                        game_manager.quit()
                    elif event.type == pygame.KEYDOWN:
                        # 调试快捷键
                        if event.key == pygame.K_F3:
                            game_manager.toggle_debug_info()
                        elif event.key == pygame.K_F4:
                            game_manager.toggle_fps_display()
                        elif event.key == pygame.K_F5:
                            game_manager.toggle_performance_display()
                        elif event.key == pygame.K_F6:
                            game_manager.toggle_collision_display()
                        elif event.key == pygame.K_F7:
                            game_manager.toggle_entity_bounds_display()
                        else:
                            scene_manager.handle_event(event)
                    else:
                        scene_manager.handle_event(event)
                
                # 更新游戏状态
                game_manager.update()
                scene_manager.update()
                
                # 渲染画面
                try:
                    render_start_time = time.time()
                    
                    screen.fill((30, 30, 30))  # 背景色
                    scene_manager.render(screen)
                    
                    # 渲染调试信息
                    game_manager.render_debug_info(screen)
                    
                    pygame.display.flip()
                    
                    # 更新渲染时间
                    game_manager.debug_info['render_time'] = (time.time() - render_start_time) * 1000
                
                except pygame.error as e:
                    print(f"渲染错误: {e}")
                    traceback.print_exc()
                    continue
                
                # 控制帧率
                clock.tick(game_manager.fps)
                
                # 更新性能统计
                frame_time = time.time() - loop_start_time
                game_manager.debug_info['frame_time'] = frame_time * 1000  # 转换为毫秒
                
                # 定期检查性能
                current_time = time.time()
                if current_time - last_performance_check >= performance_check_interval:
                    stats = game_manager.get_performance_stats()
                    print("\n性能统计:")
                    print(f"当前FPS: {stats['fps']:.1f}")
                    print(f"平均FPS: {stats['average_fps']:.1f}")
                    print(f"帧时间: {stats['frame_time']:.1f}ms")
                    print(f"更新时间: {stats['update_time']:.1f}ms")
                    print(f"渲染时间: {stats['render_time']:.1f}ms\n")
                    last_performance_check = current_time
            
            except Exception as e:
                print(f"主循环中发生错误: {e}")
                traceback.print_exc()
                # 尝试恢复到主菜单
                try:
                    game_manager.change_state(GameState.MAIN_MENU)
                    scene_manager.switch_scene("main_menu")
                except:
                    print("无法恢复到主菜单，退出游戏")
                    break
        
        # 正常退出
        print("正在保存游戏数据...")
        try:
            # 保存游戏数据
            save_manager.save_game({
                'score': game_manager.total_score,
                'fragments': game_manager.total_fragments,
                'stars': game_manager.total_stars,
                'play_time': game_manager.total_play_time
            })
            print("游戏数据保存成功")
        except Exception as e:
            print(f"保存游戏数据时发生错误: {e}")
            traceback.print_exc()
        
        pygame.quit()
        print("游戏正常退出")
    
    except Exception as e:
        print(f"游戏发生致命错误: {e}")
        traceback.print_exc()
        try:
            pygame.quit()
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main() 