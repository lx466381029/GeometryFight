# 游戏架构设计

## 核心系统（Core Systems）

### GameManager
- 游戏主循环控制
- 场景管理和切换
- 游戏状态管理
- 难度系统管理

### SceneManager
- 场景基类（Scene）
- 主菜单场景（MainMenuScene）
- 游戏场景（GameScene）
- 商店场景（ShopScene）
- 角色选择场景（CharacterSelectScene）

### ResourceManager
- 图形资源管理
- 音频资源管理
- 配置文件管理
- 字体管理（支持中英文，思源黑体）

## 游戏实体（Game Entities）

### Character System
#### Player
- 基础角色类
- 士兵（Soldier）
- 突击手（Assault）
- 炮兵（Artillery）
- 角色属性系统
- 技能系统

#### Enemy
- 基础敌人类
- 基础几何图形敌人
  - 三角形敌人
  - 圆形敌人
  - 方块敌人
- 精英敌人
- Boss敌人
- AI行为系统

### Combat System
- 碰撞检测系统
- 伤害计算系统
- 子弹系统
  - 基础子弹类
  - 特殊子弹效果
- 技能效果系统

## 进度系统（Progression Systems）

### Shop System
- 临时商店（关卡内）
- 永久商店（主菜单）
- 商品管理
- 购买逻辑

### Upgrade System
- 角色永久升级
- 符文系统
- 解锁系统

### Resource System
- 碎片系统
- 星星系统
- 资源获取和消耗逻辑

## 辅助系统（Support Systems）

### UI System
- HUD显示
- 菜单界面
- 商店界面
- 升级界面
- 提示系统

### Input System
- 键盘输入处理
- 鼠标输入处理
- 按键配置

### Audio System
- 背景音乐管理
- 音效管理
- 音量控制

### Save System
- 游戏进度保存
- 配置保存
- 成就系统

## 工具类（Utilities）

### Math
- Vector2D：二维向量
- 碰撞检测工具
- 随机数生成器

### Debug
- 日志系统
- 性能监控
- 调试工具

### Config
- 游戏配置管理
- 难度设置
- 本地化设置

## 游戏循环（Game Loop）
```python
while running:
    # 输入处理
    InputSystem.handle_events()
    
    # 更新游戏状态
    GameManager.update()
    
    # 渲染
    RenderSystem.clear()
    GameManager.render()
    RenderSystem.present()
    
    # 维持帧率
    Clock.tick(FPS)
```