import pygame
from Animation import *
from random import randint

FRUIT_COLOR = (200,0,0)

fruit_imgs = []
fruit_imgs.append(pygame.image.load('images/fruit1.png'))
fruit_imgs.append(pygame.image.load('images/fruit2.png'))
fruit_imgs.append(pygame.image.load('images/fruit3.png'))

idle_movement1_2 = ([-3, 0, 3, 0])
idle_movement3 = [(-3, -3), (0, -3), (3, -3), (3, 0), (3, 3), (0, 3), (-3, 3), (-3, 0)]
idle_movement4 = [0, -5, -10, -5, 0, 5, 10, 5]
idle_movement5 = range(0,360,10)

class Fruit(pygame.Rect):
    def __init__(self, rect):
        super().__init__(rect)
        self.hit_player = False
        self.color = FRUIT_COLOR
        self.grid_x = self[0] // self[2]
        self.grid_y = self[1] // self[3]
        self.random_fruit = randint(0,len(fruit_imgs)-1)

        self.fruit_img = fruit_imgs[self.random_fruit]
        self.expand = ScaleAnimation(range(0, 50), 1, center=self.center, loop=1)
        self.idle_timer1 = randint(120, 240)
        self.idle_timer2 = randint(120, 240)

        # self.idle_animation_type = 3
        # if(self.idle_animation_type == 0):
        #     self.animation = MoveAnimation(idle_movement1_2, 20, 'y', loop=False)
        # if (self.idle_animation_type == 1):
        #     self.animation = MoveAnimation(idle_movement1_2, 20, 'x', loop=False)
        # if (self.idle_animation_type == 2):
        #     self.animation = MoveAnimation(idle_movement3, 10, loop=False)
        # if (self.idle_animation_type == 3):
        #     self.animation = RotateAnimation(idle_movement4, 10, center=self.center, loop=False)
        # if (self.idle_animation_type == 4):
        #     self.animation = RotateAnimation(idle_movement5, 10, center=self.center, loop=False)
        #self.animation = MoveAnimation(self.idle_movement3, 20)
        #self.idle_movement3_y = [-3, -3, -3, 0, 3, 3, 3, 0]

    def player_collide(self, player, game):
        if (self.hit_player == False):
            self.hit_player = True

    def update(self, *args, **kwargs):
        if (self.colliderect(kwargs['player']) == True):
            self.player_collide(kwargs['player'], kwargs['game'])

    def draw(self, window):
        self.expand.animate(window, self.fruit_img, self)
        if(self.expand.complete == True):
            fruit_img = pygame.transform.scale(self.fruit_img, (50, 50))
            if(self.idle_timer1 <= 0):
                self.animation.animate(window, fruit_img, self)
                if(self.animation.complete == True):
                    self.idle_timer1 = randint(120, 240)
            else:
                idle_animation_type = randint(0, 4)
                if (idle_animation_type == 0):
                    self.animation = MoveAnimation(idle_movement1_2, 20, 'y', loop=3)
                if (idle_animation_type == 1):
                    self.animation = MoveAnimation(idle_movement1_2, 20, 'x', loop=3)
                if (idle_animation_type == 2):
                    self.animation = MoveAnimation(idle_movement3, 10, loop=3)
                if (idle_animation_type == 3):
                    self.animation = RotateAnimation(idle_movement4, 10, center=self.center, loop=3)
                if (idle_animation_type == 4):
                    self.animation = RotateAnimation(idle_movement5, 10, center=self.center, loop=1)
                self.animation.complete = False
                self.idle_timer1 = self.idle_timer1 - 1
                window.blit(fruit_img, self)

    #todo
    # have the idle animation play at random intervals
    # have the animations be random