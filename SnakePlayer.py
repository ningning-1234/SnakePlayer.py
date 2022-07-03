import pygame
from random import randint
from Animation import *

SNAKE_COLOR1 = (81,128,243)
SNAKE_COLOR2 = (81,64,243)

tongue_file = 'images/tongue extend0.png'
tongue_img_default = pygame.image.load(tongue_file)

tongue_extend_imgs = []
tongue_extend_imgs.append(pygame.image.load('images/tongue extend1.png'))
tongue_extend_imgs.append(pygame.image.load('images/tongue extend2.png'))
tongue_extend_imgs.append(pygame.image.load('images/tongue extend3.png'))
tongue_extend_imgs.append(pygame.image.load('images/tongue extend4.png'))
tongue_extend_imgs.append(pygame.image.load('images/tongue extend5.png'))
tongue_extend_imgs.append(pygame.image.load('images/tongue extend4.png'))
tongue_extend_imgs.append(pygame.image.load('images/tongue extend5.png'))
tongue_extend_imgs.append(pygame.image.load('images/tongue extend3.png'))
tongue_extend_imgs.append(pygame.image.load('images/tongue extend2.png'))
tongue_extend_imgs.append(pygame.image.load('images/tongue extend1.png'))

eye_file = 'images/eye.png'
eye_img_default = pygame.image.load(eye_file)

eye_blink_imgs = []
eye_blink_imgs.append(pygame.image.load('images/eye blink1.png'))
eye_blink_imgs.append(pygame.image.load('images/eye blink2.png'))
eye_blink_imgs.append(pygame.image.load('images/eye blink3.png'))
eye_blink_imgs.append(pygame.image.load('images/eye blink2.png'))
eye_blink_imgs.append(pygame.image.load('images/eye blink1.png'))

color_toggle = True

pygame.init()
pygame.font.init()


class Snake(list):
    def __init__(self,rect, speed, tile_size):
        self.tile_size = tile_size
        self.speed=speed
        self.append(SnakeHead(rect, speed, tile_size))
        self.add_part_behind()
        self.add_part_behind()
        self.next_parts=0
        self.score=0

    def add_part(self):
        if(self.next_parts>0 and self[-1].tile_aligned() and self[-1].move_dir>=0):
            # snake_rect=pygame.Rect(self[-1][0], self[-1][1], self.tile_size, self.tile_size)
            # snake_part = SnakePart(snake_rect, self.tile_size, self[-1], self[0], self[-1].move_dir-4,self.speed)
            # snake_part.color=SNAKE_COLOR2
            # self.append(snake_part)
            self.add_part_behind()
            self.next_parts=self.next_parts-1

    def add_part_behind(self):
        snake_rect=pygame.Rect(self[-1][0], self[-1][1], self.tile_size, self.tile_size)
        if(self[-1].move_dir==0):
            snake_rect[0]=snake_rect[0]-self.tile_size
        if(self[-1].move_dir==1):
            snake_rect[1]=snake_rect[1]-self.tile_size
        if(self[-1].move_dir==2):
            snake_rect[0]=snake_rect[0]+self.tile_size
        if(self[-1].move_dir==3):
            snake_rect[1]=snake_rect[1]+self.tile_size

        snake_part = SnakePart(snake_rect, self.tile_size, self[-1], self[0], self[-1].move_dir,self.speed)
        snake_part.next_dir=snake_part.prev_part.move_dir
        self.append(snake_part)

    def check_player_collide(self):
        if(self.tile_aligned()):
            head=self[0]
            next_x = head.grid_x
            next_y = head.grid_y
            #print("head pos before : ", head[0], head[1])
            #print("head pos before : ", next_x, next_y)
            if(self.tile_aligned()==True):
                if(head.next_dir==0):
                    next_x= next_x+1
                if (head.next_dir == 1):
                    next_y = next_y + 1
                if (head.next_dir == 2):
                    next_x = next_x - 1
                if (head.next_dir == 3):
                    next_y = next_y - 1

            for s in self[1:]:
                if(s.grid_x==next_x and s.grid_y==next_y):
                    #print("head pos after: ", next_x, next_y)
                    #print("body pos: ", s.grid_x, s.grid_y)
                    return True
            return False

    def fruit_collide(self, lst):
        index = self[0].collidelist(lst)
        if (index != -1):
            lst.remove(lst[index])
            self.next_parts = self.next_parts + 1
            self.score = self.score + 1

    def tile_aligned(self):
        for s in self:
            if(not s.tile_aligned()):
                return False
        return True

    def draw(self, window):
        for part in self:
            part.draw(window)

    def update(self, *args, **kwargs):
        # print(self.tile_aligned())
        fruit_lst = kwargs['fruits']
        if(self.tile_aligned()==True):
            self.fruit_collide(fruit_lst)
        for part in self:
            part.update(*args, **kwargs)
        self.add_part()


class SnakePart(pygame.Rect):
    def __init__(self, rect, tile_size, prev_part, head, move_dir, speed):
        super().__init__(rect)
        self.tile_size = tile_size
        self.grid_x = self[0]//self.tile_size
        self.grid_y = self[1]//self.tile_size
        self.prev_part = prev_part
        self.head = head
        self.move_dir = move_dir
        self.next_dir = move_dir
        self.changed_dir = False
        self.color = SNAKE_COLOR1
        global color_toggle
        if (color_toggle == True):
            self.color = SNAKE_COLOR1
            color_toggle = False
        else:
            self.color = SNAKE_COLOR2
            color_toggle = True
        self.speed=speed
        self.eye_animation = RotateAnimation([-5, -10, -5, 0, 5, 10, 5, 0], 20)

    def tile_aligned(self):
        if (self[0] % self.tile_size == 0 and self[1] % self.tile_size == 0):
            return True
        return False

    def move(self):
        if(self.move_dir<0):
            if(self.prev_part.tile_aligned()):
                self.move_dir=self.move_dir+4
                self.next_dir=self.move_dir

        # right
        if (self.move_dir == 0):
            self.move_ip(self.speed, 0)
        # down
        elif (self.move_dir == 1):
            self.move_ip(0, self.speed)
        # left
        elif (self.move_dir == 2):
            self.move_ip(-self.speed, 0)
        # up
        elif (self.move_dir == 3):
            self.move_ip(0, -self.speed)

        if (self.tile_aligned() == True):
            self.move_dir = self.next_dir
            self.changed_dir = True
        else:
            self.changed_dir = False

    def update(self, *args, **kwargs):
        self.move()
        self.grid_x = self[0] // self.tile_size
        self.grid_y = self[1] // self.tile_size
        if(self.prev_part.changed_dir):
            self.next_dir=self.prev_part.move_dir

    def draw(self, window):
        pygame.draw.rect(window, self.color,self)

class SnakeHead(SnakePart):
    def __init__(self, rect, speed, tile_size):
        super().__init__(rect, tile_size, None, self, 0, speed)
        self.length=0
        '''
        0=right
        1=downs
        2=left
        3=up
        '''
        #4 = none
        self.extending = False
        self.blinking = False

    def update(self, *args, **kwargs):
        # print(self.tile_aligned())
        # print(self.move_dir)
        self.parse_inputs(kwargs['inputs'], kwargs['controller_inputs'])
        self.move()
        self.grid_x = self[0] // self.tile_size
        self.grid_y = self[1] // self.tile_size


    def parse_inputs(self, keys, controller=None):
        commands = []
        #right
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            commands.append('right')
        #down
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            commands.append('down')
        #left
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            commands.append('left')
        #up
        if (keys[pygame.K_w] or keys[pygame.K_UP]):
            commands.append('up')

        controller_mapping = {
            'right': 14,
            'down':12,
            'left':13,
            'up':11
        }

        if(controller is not None):
            # right
            if (controller.get_button(controller_mapping['right']) or controller.get_axis(0) * 128 > 96):
                commands.append('right')
            # down
            if (controller.get_button(controller_mapping['down']) or controller.get_axis(1) * 128 > 96):
                commands.append('down')
            # left
            if (controller.get_button(controller_mapping['left']) or controller.get_axis(0) * 128 < -96):
                commands.append('left')
            # up
            if (controller.get_button(controller_mapping['up']) or controller.get_axis(1) * 128 < -96):
                commands.append('up')
            # # right
            # if (controller.get_button(14) or controller.get_axis(0) * 128 > 92):
            #     commands.append('right')
            # # down
            # if (controller.get_button(12) or controller.get_axis(1) * 128 > 92):
            #     commands.append('down')
            # # left
            # if (controller.get_button(13) or controller.get_axis(0) * 128 < -92):
            #     commands.append('left')
            # # up
            # if (controller.get_button(11) or controller.get_axis(1) * 128 < -92):
            #     commands.append('up')

        commands = list(set(commands))
        self.parse_commands(commands)

    def parse_commands(self, commands):
        #right
        if ('right' in commands):
            if (self.move_dir == 1 or self.move_dir == 3):
                self.next_dir = 0
        #down
        if ('down' in commands):
            if (self.move_dir == 0 or self.move_dir == 2):
                self.next_dir = 1
        #left
        if ('left' in commands):
            if(self.move_dir == 1 or self.move_dir == 3):
                self.next_dir = 2
        #up
        if ('up' in commands):
            if (self.move_dir == 0 or self.move_dir == 2):
                self.next_dir = 3

    def draw(self, window):
        t_mult = 1

        tongue_surf = pygame.Surface((self[2]*(1+t_mult), self[3]*(1+t_mult)), pygame.SRCALPHA)
        eye_surf = pygame.Surface((self[2], self[3]), pygame.SRCALPHA)

        tongue_rect = pygame.Rect((self[2] * 0, tongue_surf.get_height() * 0.5 - self[3] * 0.3, self[2], self[3] * 0.2))
        #pygame.draw.rect(tongue_surf, (200, 49, 3), tongue_rect)

        if (not self.extending and randint(0, 500) == 1):
            self.extending = True
            self.extending_frames = 0

        tongue_img = tongue_img_default
        extend_frames = 15
        if (self.extending):
            tongue_img = tongue_extend_imgs[self.extending_frames // extend_frames]
            self.extending_frames = self.extending_frames + 1

            if (self.extending_frames // extend_frames >= len(tongue_extend_imgs)):
                self.extending_frames = 0
                self.extending = False

        tongue_surf.blit(tongue_img, tongue_rect)

        eye_rect1 = pygame.Rect((10, 10, 10, 10))
        eye_rect2 = pygame.Rect((10, 30, 10, 10))

        if(not self.blinking and randint(0,500)==1):
            self.blinking = True
            self.blinking_frame = 0

        eye_img = eye_img_default
        blink_frames = 15
        if(self.blinking):
            eye_img = eye_blink_imgs[self.blinking_frame//blink_frames]
            self.blinking_frame = self.blinking_frame+1

            if(self.blinking_frame//blink_frames >= len(eye_blink_imgs)):
                self.blinking_frame=0
                self.blinking = False

        eye_surf.blit(pygame.transform.scale(eye_img,(10,10)), eye_rect1)
        eye_surf.blit(pygame.transform.scale(eye_img,(10,10)), eye_rect2)
        # self.eye_animation.animate(eye_surf, pygame.transform.scale(eye_img,(10,10)), eye_rect1)
        # self.eye_animation.animate(eye_surf, pygame.transform.scale(eye_img,(10,10)), eye_rect2)

        head_rotate=0
        if(self.move_dir==0):
            head_rotate = 180

        if(self.move_dir==1):
            head_rotate = 90

        if(self.move_dir==2):
            head_rotate = 0

        if(self.move_dir==3):
            head_rotate = 270

        window.blit(pygame.transform.rotate(tongue_surf, head_rotate),(self[0] - self[2] * t_mult / 2, self[1] - self[3] * t_mult / 2))

        super().draw(window)

        window.blit(pygame.transform.rotate(eye_surf, head_rotate), (self[0], self[1]))

        '''
        rotate the surface based on the direction the snake is facing
        draw eyes
        '''