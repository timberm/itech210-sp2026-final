import pygame
import random
from settings import * 
from grid import *

cloud = pygame.image.load("media/cloud.png").convert_alpha()
star = pygame.image.load("media/star.png").convert_alpha()
star2 = pygame.transform.scale(star, (32,32))

score = 0

def get_collisions(rect, radius=1):
    colliders = []
    collider_grid = grid
    
    #convert rect to cell
    top_left = get_world_pos_to_grid((rect.left, rect.top))
    bottom_right = get_world_pos_to_grid((rect.left+rect.width, rect.top+rect.height))
   
    #general - get colliders in a radius around rect
    general = []
    for x in range(top_left[0]-radius, bottom_right[0]+radius+1):
        for y in range(top_left[1]-radius, bottom_right[1]+radius+1):
            collider = collider_grid.get(f"{x},{y}")
            if collider is not None and collider not in general:
                general.append(collider)
   
    #specific - check each of the colliders from general
    for collider in general:
        if rect.colliderect(collider) and collider not in colliders:
            colliders.append(collider)
    
    return colliders

def add_collider_to_grid(pos, size, grid):
    #pos and size are tuples in cell coordinates

    rect = pygame.Rect(get_grid_to_world_pos(pos), (size[0]*CELL_SIZE, size[1]*CELL_SIZE))
    for x in range(pos[0], pos[0]+size[0]):
        for y in range(pos[1], pos[1]+size[1]):
            grid[f"{x},{y}"] = rect

def draw_colliders(surface, camera, grid):
    for key,val in grid.items():
        pos = key.split(',')
        x = int(pos[0])*CELL_SIZE - camera['pos'][0]
        y = int(pos[1])*CELL_SIZE - camera['pos'][1]
        if val is not None:
            #col_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            # pygame.draw.rect(col_surface, BLUE_A, col_surface.get_rect())
            cloud_width, cloud_height = cloud.get_size()
            offset_x = (CELL_SIZE - cloud_width) / 2
            x_centered = x + offset_x + cloud_width / 2
            cloud_rect = cloud.get_rect(midtop=(x_centered, y))
            surface.blit(cloud, cloud_rect)
            #surface.blit(col_surface, (x,y))

def create_star_positions():
    positions = []
    for _ in range(500):
        if random.randint(1,100) > 50:
            x = random.randint(1,73) * 2
            y = random.randint(1,250) * 2
            positions.append((x,y))
    return positions

# store the list of the star positions
star_positions = create_star_positions()

def draw_stars(surface, camera, grid):
    for pos in star_positions:
        x = pos[0]*CELL_SIZE - camera['pos'][0]
        y = pos[1]*CELL_SIZE - camera['pos'][1]
        star_rect = star2.get_rect(topleft=(x,y))
        surface.blit(star2, star_rect)

def check_star_collisions(player, star_positions, star_image, camera, score):
    for star in star_positions:
        star_x, star_y = star

        # Convert star position to screen coordinates
        screen_x = star_x * CELL_SIZE - camera['pos'][0]
        screen_y = star_y * CELL_SIZE - camera['pos'][1]
        star_rect = star_image.get_rect(topleft=(screen_x, screen_y))

        
        # Check collision
        if star_rect.colliderect(player['rect']):
            star_positions.remove(star)
            score += 100  