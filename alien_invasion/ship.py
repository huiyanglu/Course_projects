import pygame

class Ship():

    def __init__(self,screen,ai_settings): #添加形参ai_settings，获取速度设置
        """初始化飞船并设置其初始位置"""
        self.screen = screen # screen指定了飞船将要绘制到什么地方
        self.ai_settings = ai_settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship2.bmp') # 加载图像，将返回一个表示飞船的surface，这个surface存储在self.image中
        self.rect = self.image.get_rect() #用get_rect()处理surface的属性rect
        self.screen_rect = screen.get_rect() #表示屏幕的矩形

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx #屏幕的横向中间对准飞船矩形的横向中间
        self.rect.bottom = self.screen_rect.bottom # 屏幕的底部下边缘对准飞船矩形的下边缘

        self.center = float(self.rect.centerx) #在飞船的属性center中存储centerx的小数值

        #移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
        # self.rect.right返回飞船外接矩形self.rect属性的右边缘x坐标
        # self.screen_rect.right返回屏幕矩形self.screen_rect右边缘的坐标
            self.center += self.ai_settings.ship_speed_factor #self.center可存储小数
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect) #根据self.rect指定的位置将image绘制在屏幕screen上

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx