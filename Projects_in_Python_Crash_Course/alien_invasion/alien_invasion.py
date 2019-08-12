import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import Gamestats

def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    stats = Gamestats(ai_settings)
    ship = Ship(screen,ai_settings) # 创建一个名为ship的Ship实例，调用screen
    aliens = Group() # 创建一个外星人编组
    bullets = Group() # 创建一个用于存储子弹的编组

    gf.create_fleet(ai_settings, screen, ship, aliens) # 创建外星人群

    # 开始游戏的主循环
    while True:
        # 检测按键（左移、右移、生成子弹）
        gf.check_events(ai_settings,screen,ship,bullets) #根据按键情况改变移动标志的状态

        # 确定游戏的哪些部分仅在游戏处于活动状态时才运行
        if stats.game_active: 
            # 根据移动标志判断是否移动飞船
            ship.update()

            # 移动子弹（只要子弹生成就一直向上移动）
            bullets.update()

            # 如果子弹到顶就remove
            gf.update_bullets(ai_settings,screen,ship,aliens,bullets)

            gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets)

        # 重绘屏幕，画出子弹，画飞船，使屏幕可见
        gf.update_screen(ai_settings,screen,ship,aliens,bullets)

run_game()