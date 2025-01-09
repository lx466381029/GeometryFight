import pygame
from typing import Dict, Optional, List
import traceback

class Scene:
    """场景基类"""
    def initialize(self):
        """初始化场景"""
        pass
    
    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        pass
    
    def update(self):
        """更新场景"""
        pass
    
    def render(self, screen: pygame.Surface):
        """渲染场景"""
        pass
    
    def cleanup(self):
        """清理场景资源"""
        pass

class SceneManager:
    """场景管理器，负责管理和切换场景"""
    def __init__(self):
        self.scenes: Dict[str, Scene] = {}
        self.current_scene: Optional[Scene] = None
        self.current_scene_name: Optional[str] = None
        self.scene_stack: List[str] = []  # 场景栈，用于场景回退
        self.transition_time = 500  # 场景切换动画时间（毫秒）
        self.is_transitioning = False
        self.transition_start_time = 0
        self.transition_from = None
        self.transition_to = None
        print("场景管理器初始化完成")
    
    def register_scene(self, name: str, scene: Scene):
        """注册场景"""
        try:
            if name in self.scenes:
                print(f"警告：场景 {name} 已存在，将被覆盖")
            self.scenes[name] = scene
            print(f"注册场景: {name} ({scene.__class__.__name__})")
        except Exception as e:
            print(f"注册场景 {name} 失败: {e}")
            traceback.print_exc()
    
    def switch_scene(self, name: str, push_to_stack: bool = True):
        """切换场景"""
        try:
            print(f"切换场景到: {name}")
            if name not in self.scenes:
                print(f"错误：场景 {name} 不存在")
                print(f"当前已注册的场景: {', '.join(self.scenes.keys())}")
                return
            
            # 清理当前场景
            if self.current_scene:
                try:
                    self.current_scene.cleanup()
                except Exception as e:
                    print(f"清理场景 {self.current_scene_name} 时发生错误: {e}")
                    traceback.print_exc()
            
            # 保存当前场景到栈中
            if push_to_stack and self.current_scene_name:
                self.scene_stack.append(self.current_scene_name)
            
            # 切换场景
            old_scene = self.current_scene_name
            self.current_scene = self.scenes[name]
            self.current_scene_name = name
            
            # 开始场景切换动画
            self.is_transitioning = True
            self.transition_start_time = pygame.time.get_ticks()
            self.transition_from = old_scene
            self.transition_to = name
            
            print(f"从 {old_scene if old_scene else '无'} 切换到 {name}")
            
            # 初始化新场景
            try:
                print(f"初始化新场景: {name}")
                self.current_scene.initialize()
                print(f"场景 {name} 初始化完成")
            except Exception as e:
                print(f"初始化场景 {name} 时发生错误: {e}")
                traceback.print_exc()
        
        except Exception as e:
            print(f"切换场景时发生错误: {e}")
            traceback.print_exc()
    
    def pop_scene(self):
        """返回上一个场景"""
        if self.scene_stack:
            previous_scene = self.scene_stack.pop()
            self.switch_scene(previous_scene, push_to_stack=False)
        else:
            print("警告：场景栈为空，无法返回上一个场景")
    
    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        if not self.current_scene:
            return
        
        try:
            # 记录事件信息
            if event.type == pygame.KEYDOWN:
                print(f"场景 {self.current_scene_name} 处理按键事件: {pygame.key.name(event.key)}")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"场景 {self.current_scene_name} 处理鼠标按下事件: {event.pos}")
            
            # 处理事件
            self.current_scene.handle_event(event)
        
        except Exception as e:
            print(f"处理事件时发生错误: {e}")
            traceback.print_exc()
    
    def update(self):
        """更新当前场景"""
        if not self.current_scene:
            return
        
        try:
            # 更新场景
            self.current_scene.update()
            
            # 更新场景切换动画
            if self.is_transitioning:
                current_time = pygame.time.get_ticks()
                if current_time - self.transition_start_time >= self.transition_time:
                    self.is_transitioning = False
        
        except Exception as e:
            print(f"更新场景时发生错误: {e}")
            traceback.print_exc()
    
    def render(self, screen: pygame.Surface):
        """渲染当前场景"""
        if not self.current_scene:
            return
        
        try:
            # 渲染场景
            self.current_scene.render(screen)
            
            # 渲染场景切换动画
            if self.is_transitioning:
                progress = (pygame.time.get_ticks() - self.transition_start_time) / self.transition_time
                alpha = int(255 * (1 - progress))
                overlay = pygame.Surface((screen.get_width(), screen.get_height()))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(alpha)
                screen.blit(overlay, (0, 0))
        
        except Exception as e:
            print(f"渲染场景时发生错误: {e}")
            traceback.print_exc()
            
            # 在错误情况下显示错误信息
            try:
                screen.fill((30, 30, 30))
                font = pygame.font.SysFont(None, 48)
                error_text = font.render("渲染错误", True, (255, 0, 0))
                screen.blit(error_text, (screen.get_width() // 2 - error_text.get_width() // 2,
                                       screen.get_height() // 2 - error_text.get_height() // 2))
            except:
                pass  # 如果连错误信息都无法渲染，就放弃 