class Settings():
    """存储《外星人入侵》的所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200 #屏幕宽度
        self.screen_height = 800 #屏幕高度
        self.bg_color = (0,0,255) #设置背景色

        # 飞船的设置
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # 子弹的设置
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 255,255,255
        self.bullet_speed_factor = 3
        self.bullet_allowed = 3

        # 外星人设置
        self.alien_speed_factor = 3
        self.fleet_drop_speed = 50
        self.fleet_direction = 1 #为1时向右移，为-1时表示向左移

