import json
import os
from typing import Dict, Any, Optional

class SaveManager:
    """存档管理器，负责处理游戏存档的保存和加载"""
    
    def __init__(self):
        # 存档目录
        self.save_dir = "save"
        self.save_file = os.path.join(self.save_dir, "game_save.json")
        
        # 确保存档目录存在
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        # 当前存档数据
        self.current_save: Optional[Dict[str, Any]] = None
    
    def save_exists(self) -> bool:
        """检查是否存在存档"""
        return os.path.exists(self.save_file)
    
    def save_game(self, data: Dict[str, Any]) -> bool:
        """保存游戏数据"""
        try:
            # 确保存档目录存在
            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)
            
            # 保存数据
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            self.current_save = data
            return True
        except Exception as e:
            print(f"保存游戏失败: {e}")
            return False
    
    def load_game(self) -> Optional[Dict[str, Any]]:
        """加载游戏数据"""
        try:
            if not os.path.exists(self.save_file):
                return None
            
            with open(self.save_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.current_save = data
            return data
        except Exception as e:
            print(f"加载游戏失败: {e}")
            return None
    
    def delete_save(self) -> bool:
        """删除存档"""
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
                self.current_save = None
                return True
            return False
        except Exception as e:
            print(f"删除存档失败: {e}")
            return False
    
    def get_current_save(self) -> Optional[Dict[str, Any]]:
        """获取当前存档数据"""
        return self.current_save 