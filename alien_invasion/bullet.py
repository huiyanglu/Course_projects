import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""

    def __init__(self,ai_settings,screen,ship):
        """在飞船所在位置创建一个子弹对象"""
        super().__init__() # Bullet类继承了Sprite类
        self.screen = screen

        # 创建子弹的属性rect
        # pygame.Rect()类在空白处创建一个矩形，提供矩形左上角的x,y轴坐标和矩形的宽度和高度
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)

        # 子弹属性rect的x坐标等于飞船的x坐标
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 将子弹的y坐标
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)
        # 函数draw.rect使用self.color颜色填充表示子弹的self.rect占据的屏幕部分


