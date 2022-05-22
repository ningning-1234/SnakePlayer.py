import pygame
from random import randint
from SnakePlayer import *
from Fruit import *
run=True

pygame.init()
pygame.font.init()

WIN_WIDTH = 750
WIN_HEIGHT = 750
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = pygame.time.Clock()
FPS = 150

fruit_lst = []
fruit_limit = 3

BG_COLOR = pygame.color.Color('0x000000')
GRID_COLOR_LIGHT=(0, 209, 0)
GRID_COLOR_DARK=(0, 161 ,0)
TILE_SIZE = 50

test_rect = pygame.Rect((250,250,TILE_SIZE,TILE_SIZE))
'''
Detects if the rectangle is lined up with a tile
'''


# print(tile_aligned(test_rect))
# player=Snake()
snake_rect =  pygame.Rect((200,350,TILE_SIZE,TILE_SIZE))
player = Snake(snake_rect,2,TILE_SIZE)

def spawn():
    spawn_pos_x = randint(1, 15)*TILE_SIZE-TILE_SIZE
    spawn_pos_y = randint(1, 15)*TILE_SIZE-TILE_SIZE
    spawn_grid_x = spawn_pos_x // TILE_SIZE
    spawn_grid_y = spawn_pos_y // TILE_SIZE
    overlap = False
    for f in fruit_lst:
        if(spawn_grid_x==f.grid_x and spawn_grid_y==f.grid_y):
            overlap = True
    for s in player:
        if(spawn_grid_x==s.grid_x and spawn_grid_y==s.grid_y):
            overlap = True
    if(overlap==False):
        fruit_rect = pygame.Rect(spawn_pos_x, spawn_pos_y, TILE_SIZE, TILE_SIZE)
        fruit = Fruit(fruit_rect)
        fruit_lst.append(fruit)

for g in range(fruit_limit):
    spawn()

def game_over():
    global run
    run=False

while (run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type ==0:
            print(event)

    if(player[0][0] > WIN_WIDTH-TILE_SIZE):
        game_over()

    if (player[0][0] < 0):
        game_over()

    if (player[0][1] > WIN_HEIGHT - TILE_SIZE):
        game_over()

    if (player[0][1] < 0):
        game_over()

    keys = pygame.key.get_pressed()
    player.update(inputs=keys, fruits=fruit_lst)
    # print(player[0].grid_x,player[0].grid_y)
    if(player.check_player_collide()):
        game_over()
    if(len(fruit_lst)<fruit_limit and player.tile_aligned()):
        spawn()


        #fruit_lst[collide_index].player_collide(player)

    # Move into the SnakePlayer file

    #_____Draw_____
    window.fill(BG_COLOR)
    game_font = pygame.font.Font('freesansbold.ttf', 20)

    #draw grid
    for i in range(1, 9):
        for g in range(1, 9):
            pygame.draw.rect(window, GRID_COLOR_DARK, pygame.Rect((2*TILE_SIZE)*(g-1), (2*TILE_SIZE)*(i-1), TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(window, GRID_COLOR_LIGHT, pygame.Rect((2*TILE_SIZE)*(g-1), TILE_SIZE*(2*i-1), TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(window, GRID_COLOR_LIGHT, pygame.Rect(TILE_SIZE*(2*g-1), (2*TILE_SIZE)*(i-1), TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(window, GRID_COLOR_DARK, pygame.Rect(TILE_SIZE*(2*g-1),TILE_SIZE*(2*i-1), TILE_SIZE, TILE_SIZE))

    score = game_font.render(str(player.score), False, (0, 200, 255))
    window.blit(score, (19, 15))

    for f in fruit_lst:
        f.draw(window)
    player.draw(window)
    # print(len(fruit_lst))

    # pygame.draw.rect(window, (100,100,200),test_rect)

    pygame.display.flip()
    clock.tick(FPS)
