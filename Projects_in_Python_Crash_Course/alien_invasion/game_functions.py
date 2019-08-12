import sys
import pygame
from bullet import Bullet
from alien import Alien
from random import randint
from time import sleep


def check_keydown_events(event,ship,ai_settings,bullets,screen):
    """响应按键"""
    if event.key == pygame.K_RIGHT:  # 检查按下的是否为右箭头
        ship.moving_right = True  # 如果是右箭头，就让飞船向右移动
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings,screen,ship,bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event,ship):
    """响应松开按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,ship,bullets): #按键控制飞船移动，所以加入形参ship
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # 检测到KEYDOWN事件时做出响应
            check_keydown_events(event,ship,ai_settings,bullets,screen)
        elif event.type == pygame.KEYUP: #按键抬起时的响应
            check_keyup_events(event,ship)

def update_screen(ai_settings,screen,ship,aliens,bullets):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)  # 重绘屏幕screen
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()  # 调用ship类里的方法blitme函数，放在screen.fill后面保证飞船出现在背景前面
    aliens.draw(screen) # 对编组调用draw()，pygame自动绘制编组的每个元素，在屏幕上
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings,screen,ship,aliens,bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets):
    """响应子弹和外星人的碰撞"""
    # 检查是否有子弹击中了外星人
    # 如果是，就删除相应的子弹和外星人（存储在字典中的键值对）
    # 两个布尔实参True、True告诉Pygame删除发生碰撞的子弹和外星人
    # 若第一个为False，则只删除被击中的外星人，子弹能够到达顶端再消失
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    random_number = randint(-10,10)
    alien.width = alien.rect.width # 外星人之间的宽度
    alien.x = alien.width + 2 * alien.width * alien_number +random_number
    alien.rect.x = alien.x #alien.x参数不能缩减
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number +random_number
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人的间距为外星人的宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,alien.rect.height)
    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,row_number)

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘时采取措施"""
    for alien in aliens.sprites(): # 遍历外星人群中的每个外星人，对其调用check_edges()
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 剩余飞船数-1
        stats.ships_left -= 1

        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放在屏幕低端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False # 飞船用完后，玩家结束游戏

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
    """检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings,aliens) #若到边，改变y轴和移动方向
    aliens.update() #根据改变后的坐标和移动方向，更新外星人的位置

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens): #字典中被加入了碰撞的飞船和外星人不为空字典了
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)

    # 检查是否有外星人到达屏幕低端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
    """检查是否有外星人到达屏幕低端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 处理方式和飞船被撞到一样
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break

