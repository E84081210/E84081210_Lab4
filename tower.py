import pygame
import os
import math
from settings import WHITE,FPS,WIN_HEIGHT,WIN_WIDTH

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """
        x1,y1=enemy.get_pos()   #(Get enemy position)
        x2,y2=self.center       #(Get Tower position)
        distance=math.sqrt((x1-x2)**2+(y1-y2)**2)  #(計算兩點的距離)
        #(距離在塔攻擊範圍內判定，是則執行攻擊程序)
        if distance<=self.radius:
            return True
        else:
            return False

    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        transparent_surface=pygame.Surface((WIN_WIDTH,WIN_HEIGHT),pygame.SRCALPHA)
        transparency=50 #(transparnecy:0~255, 0 means fully transparent)
        pygame.draw.circle(transparent_surface,(255,255,255,transparency),self.center,self.radius)
        win.blit(transparent_surface,(0,0))


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = True  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """
        if self.cd_count < self.cd_max_count:
            self.cd_count+=1   #(讓CD不斷增加，直到Max_count)
            return False
        else:
            self.cd_count=0
            return True        #(CD結束，開始進行下一波攻擊)




    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """
        #(攻擊條件：符合tower冷卻時間且Enemy在攻擊範圍  執行：Enemy受攻擊扣血)
        for enemy in enemy_group.get():
            if self.is_cool_down() and self.range_circle.collide(enemy):
                enemy.get_hurt(self.damage)
                return


    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        #(Hint: rect物件中：right、left 代表 右、左 top、bottom 代表 上、下)
        #(取用左上角為min右下角為max：基於座標點從左上角開始計算)
        x_min,y_min=self.rect.topleft
        x_max,y_max=self.rect.bottomright
        #(限制click的範圍)
        if x_min<=x<=x_max and y_min<=y<=y_max:
            return True
        else:
            return False




    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """

        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

