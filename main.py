import pygame
import random
from settings import *
from camera import *
from player import *
from grid import *
from collision import *


bg = pygame.image.load("media/bg1.png").convert_alpha()
clouds = pygame.image.load("media/map (1).png").convert_alpha()

pygame.init()

def init():
    #initialize all of the game here
    pygame.display.set_caption("Jiibayaabooz")
    config = {}

    #collider grid
    collider_grid = grid
    for x in range(LEVEL[0]//CELL_SIZE):
        for y in range(LEVEL[1]//CELL_SIZE):
            collider_grid[f"{x},{y}"] = None
    config['collider_grid'] = collider_grid
    
    # add colliders to the grid

    # ground base
    add_collider_to_grid((0,249), (73,3), collider_grid)

    # left side 
    add_collider_to_grid((-1,0),(1,250), collider_grid)
    
    # right side
    add_collider_to_grid((73,0), (1,250), collider_grid)

    # count = 0

    # # create random colliders
    for i in range(250):
        power_up = random.randint(1,100)
        x_coord = random.randint(1,73)
        y_coord = random.randint(1,250)
        size = random.randint(2,7)
        add_collider_to_grid((x_coord,y_coord),(size,1),collider_grid)

        

    #camera
    config['camera'] = camera

    #objects
    objects = []
    config['objects'] = objects

    #player
    config['player'] = player
    objects.append(player)
    
    game_loop(screen, clock, config)

def update(dt, objects):
    #all update calls are made here
    for obj in objects:
        obj['update'](dt)

def draw(surface, camera, objects):
    #all draw calls are made from here
    for obj in objects:
        obj['draw'](surface, camera)

def game_loop(screen, clock, config):
    #where the main game loop happens
    camera = config['camera']
    grid = config['collider_grid']
    objects = config['objects']
    player = config['player']

    running = True

    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update(dt, objects)
        update_camera(player)
        
        screen.blit(bg, (0,0))
        # create_colliders()

        draw(screen, camera, objects)

        # print(f"Cloud image size: {cloud.get_size()}")

        # draw score
        score_text = score_font.render(f"Score: {score}", True, (255,255,255))
        score_rect = score_text.get_rect(center=(WIDTH//2, 25))
        screen.blit(score_text, score_rect)

        #debug mode
        if debug:
            draw_colliders(screen, camera, grid)
            draw_stars(screen, camera, grid)
            check_star_collisions(player, star_positions, star2, camera, score)
            # draw_stars()
            # draw_grid(screen, camera, grid)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    init()