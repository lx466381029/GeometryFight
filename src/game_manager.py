import pygame
import time
from typing import Optional, Dict, Any
from enum import Enum, auto

class GameState(Enum):
    """游戏状态枚举"""
    INITIALIZING = auto()
    MAIN_MENU = auto()
    CHARACTER_SELECT = auto()
    PLAYING = auto()
    PAUSED = auto()
    SHOPPING = auto()
    GAME_OVER = auto()
    QUITTING = auto()

class GameManager:
    """游戏管理器，负责管理游戏的全局状态"""
    def __init__(self):
        # 游戏状态
        self.running = True
        self.state = GameState.INITIALIZING
        self.previous_state = None
        
        # 游戏设置
        self.screen_width = 1280
        self.screen_height = 720
        self.fps = 60
        self.vsync = False  # 禁用垂直同步
        self.fullscreen = False  # 禁用全屏
        
        # 游戏统计
        self.total_score = 0
        self.total_fragments = 0
        self.total_stars = 0
        self.total_play_time = 0
        self.frame_count = 0
        
        # 性能监控
        self.fps_stats = []
        self.last_fps_update = time.time()
        self.current_fps = 0.0
        
        # 游戏时钟
        self.clock = pygame.time.Clock()
        self.last_update_time = pygame.time.get_ticks()
        
        # 调试信息
        self.debug_info: Dict[str, Any] = {
            'frame_time': 0.0,
            'update_time': 0.0,
            'render_time': 0.0,
            'entity_count': 0,
            'memory_usage': 0,
            'show_fps': True,
            'show_debug': False,
            'show_collisions': False,
            'show_entity_bounds': False,
            'show_performance': False
        }
        
        print(f"游戏管理器初始化完成 - 分辨率: {self.screen_width}x{self.screen_height}, 目标FPS: {self.fps}")
    
    def update(self):
        """更新游戏状态"""
        try:
            start_time = time.time()
            
            # 更新游戏时间
            current_time = pygame.time.get_ticks()
            delta_time = current_time - self.last_update_time
            self.last_update_time = current_time
            
            if self.state != GameState.PAUSED:
                self.total_play_time += delta_time
            
            # 更新FPS统计
            self.frame_count += 1
            if time.time() - self.last_fps_update >= 1.0:
                self.current_fps = self.frame_count
                self.fps_stats.append(self.current_fps)
                if len(self.fps_stats) > 60:  # 保留最近60秒的FPS记录
                    self.fps_stats.pop(0)
                self.frame_count = 0
                self.last_fps_update = time.time()
            
            # 更新调试信息
            self.debug_info['update_time'] = time.time() - start_time
            self.debug_info['frame_time'] = self.clock.get_time()
            
            if self.debug_info['frame_time'] > 1000.0 / self.fps:
                print(f"警告：帧时间过长 ({self.debug_info['frame_time']:.1f}ms)")
        
        except Exception as e:
            print(f"游戏状态更新错误: {e}")
            import traceback
            traceback.print_exc()
    
    def render_debug_info(self, screen: pygame.Surface):
        """渲染调试信息"""
        if not self.debug_info['show_debug']:
            return
        
        try:
            font = pygame.font.SysFont(None, 24)
            y = 10
            line_height = 20
            
            # 显示FPS
            if self.debug_info['show_fps']:
                fps_text = f"FPS: {self.current_fps:.1f}"
                text_surface = font.render(fps_text, True, (255, 255, 255))
                screen.blit(text_surface, (10, y))
                y += line_height
            
            # 显示性能信息
            if self.debug_info['show_performance']:
                perf_texts = [
                    f"帧时间: {self.debug_info['frame_time']:.1f}ms",
                    f"更新时间: {self.debug_info['update_time']:.1f}ms",
                    f"渲染时间: {self.debug_info['render_time']:.1f}ms",
                    f"实体数量: {self.debug_info['entity_count']}",
                    f"内存使用: {self.debug_info['memory_usage'] / 1024 / 1024:.1f}MB"
                ]
                
                for text in perf_texts:
                    text_surface = font.render(text, True, (255, 255, 255))
                    screen.blit(text_surface, (10, y))
                    y += line_height
            
            # 显示游戏状态
            state_text = f"游戏状态: {self.state.name}"
            text_surface = font.render(state_text, True, (255, 255, 255))
            screen.blit(text_surface, (10, y))
            y += line_height
            
            # 显示游戏统计
            stats_texts = [
                f"得分: {self.total_score}",
                f"碎片: {self.total_fragments}",
                f"星星: {self.total_stars}",
                f"游戏时间: {self.get_play_time_str()}"
            ]
            
            for text in stats_texts:
                text_surface = font.render(text, True, (255, 255, 255))
                screen.blit(text_surface, (10, y))
                y += line_height
        
        except Exception as e:
            print(f"渲染调试信息时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def toggle_debug_info(self):
        """切换调试信息显示"""
        self.debug_info['show_debug'] = not self.debug_info['show_debug']
        print(f"调试信息显示: {'开启' if self.debug_info['show_debug'] else '关闭'}")
    
    def toggle_fps_display(self):
        """切换FPS显示"""
        self.debug_info['show_fps'] = not self.debug_info['show_fps']
        print(f"FPS显示: {'开启' if self.debug_info['show_fps'] else '关闭'}")
    
    def toggle_performance_display(self):
        """切换性能信息显示"""
        self.debug_info['show_performance'] = not self.debug_info['show_performance']
        print(f"性能信息显示: {'开启' if self.debug_info['show_performance'] else '关闭'}")
    
    def toggle_collision_display(self):
        """切换碰撞显示"""
        self.debug_info['show_collisions'] = not self.debug_info['show_collisions']
        print(f"碰撞显示: {'开启' if self.debug_info['show_collisions'] else '关闭'}")
    
    def toggle_entity_bounds_display(self):
        """切换实体边界显示"""
        self.debug_info['show_entity_bounds'] = not self.debug_info['show_entity_bounds']
        print(f"实体边界显示: {'开启' if self.debug_info['show_entity_bounds'] else '关闭'}")
    
    def change_state(self, new_state: GameState):
        """切换游戏状态"""
        if new_state != self.state:
            print(f"游戏状态从 {self.state.name} 切换到 {new_state.name}")
            self.previous_state = self.state
            self.state = new_state
    
    def pause(self):
        """暂停游戏"""
        if self.state == GameState.PLAYING:
            self.change_state(GameState.PAUSED)
    
    def resume(self):
        """恢复游戏"""
        if self.state == GameState.PAUSED:
            self.change_state(GameState.PLAYING)
            self.last_update_time = pygame.time.get_ticks()
    
    def quit(self):
        """退出游戏"""
        print("正在退出游戏...")
        print(f"游戏统计:")
        print(f"- 总得分: {self.total_score}")
        print(f"- 收集碎片: {self.total_fragments}")
        print(f"- 收集星星: {self.total_stars}")
        print(f"- 游戏时间: {self.get_play_time_str()}")
        print(f"- 平均FPS: {sum(self.fps_stats) / len(self.fps_stats):.1f}" if self.fps_stats else "- 平均FPS: N/A")
        self.running = False
    
    def add_score(self, score: int):
        """增加得分"""
        try:
            if score < 0:
                print(f"警告：尝试添加负分数 ({score})")
                return
            self.total_score += score
            print(f"得分增加 {score}，当前总分：{self.total_score}")
        except Exception as e:
            print(f"添加得分时发生错误: {e}")
    
    def add_fragments(self, amount: int):
        """增加碎片"""
        try:
            if amount < 0:
                print(f"警告：尝试添加负数碎片 ({amount})")
                return
            self.total_fragments += amount
            print(f"碎片增加 {amount}，当前总数：{self.total_fragments}")
        except Exception as e:
            print(f"添加碎片时发生错误: {e}")
    
    def add_stars(self, amount: int):
        """增加星星"""
        try:
            if amount < 0:
                print(f"警告：尝试添加负数星星 ({amount})")
                return
            self.total_stars += amount
            print(f"星星增加 {amount}，当前总数：{self.total_stars}")
        except Exception as e:
            print(f"添加星星时发生错误: {e}")
    
    def get_play_time_str(self) -> str:
        """获取游戏时间字符串"""
        try:
            total_seconds = self.total_play_time // 1000
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except Exception as e:
            print(f"获取游戏时间字符串时发生错误: {e}")
            return "00:00:00"
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计信息"""
        return {
            'fps': self.current_fps,
            'frame_time': self.debug_info['frame_time'],
            'update_time': self.debug_info['update_time'],
            'render_time': self.debug_info['render_time'],
            'average_fps': sum(self.fps_stats) / len(self.fps_stats) if self.fps_stats else 0
        } 