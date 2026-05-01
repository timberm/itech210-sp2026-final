import pygame 
from settings import *
from collision import *
from grid import *

waabooz = pygame.image.load("media/bunny-sprite.png").convert_alpha()
waabooz_jump = pygame.image.load("media/bunny-jump.png").convert_alpha()
star_sprite = pygame.image.load("media/star1.png").convert_alpha()
player_sprite = pygame.transform.scale(waabooz, (32,32))
player_jump_sprite = pygame.transform.scale(waabooz_jump, (32,32))


def get_player_input():
    player_input = {
        'LEFT':False,
        'RIGHT':False,
        'JUMP':False,
    }
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
        player_input['LEFT'] = True
    if pressed[pygame.K_d]:
        player_input['RIGHT'] = True
    if pressed[pygame.K_SPACE]:
        player_input['JUMP'] = True

    return player_input
 
def draw_player(surface, camera):
    pos =  (player['pos'][0]-camera['pos'][0], player['pos'][1]-camera['pos'][1])
    # pygame.draw.rect(surface, GREEN, (pos, player['size']))
    screen.blit(player_sprite, (pos, player['size']))

def draw_player_jump(surface, camera):
    pos = (player['pos'][0]-camera['pos'][0], player['pos'][1]-camera['pos'][1])
    screen.blit(player_jump_sprite, (pos, player['size']))

def update_player(dt): 
    input = get_player_input()
    
    #check for on ground
    ghost_rect = player['rect'].move(0,1) #1 pixel below player
    on_ground = len(get_collisions(ghost_rect)) > 0
    if on_ground:
        player['force'][1] = 0
    else:
        player['force'][1] += GRAVITY * dt
           
    #get inputs
    if input.get('LEFT'):
        player['force'][0] -= player['speed'] * dt
    if input.get('RIGHT'):
        player['force'][0] += player['speed'] * dt
    if input.get('JUMP') and on_ground:
        player['force'][1] -= player['speed'] * 120 #* (dt/2) #height of jump action
        # player['draw'] = draw_player_jump

    player['force'][1] = min(player['force'][1], GRAVITY*7) #gravity 

    move_player(player)
    
    player['force'][0] = 0


def move_player(player):
    test_rect = player['rect'].move(player['force'])
    hits = get_collisions(test_rect)
    
    if len(hits) == 0:
        player['pos'] = test_rect.topleft
        player['rect'].topleft = player['pos']
    else:
        #handle x position
        test_x = player['rect'].move((player['force'][0], 0))
        hits_x = get_collisions(test_x)
        for h in hits_x:
            if player['force'][0]>0: #moving right
                test_x.x = h.left - player['size'][0]
            if player['force'][0]<0: #moving left
                test_x.x = h.right
            
            player['force'][0] = 0

        player['pos'] = test_x.topleft
        player['rect'].topleft = player['pos']

        #handle y position
        test_y = player['rect'].move((0,player['force'][1]))
        hits_y = get_collisions(test_y)

        for h in hits_y:
            if player['force'][1]>0: #moving down
                test_y.y = h.top - player['size'][1]
            if player['force'][1]<0: #moving up
                test_y.y = h.bottom
            
            player['force'][1] = 0

        player['pos'] = test_y.topleft
        player['rect'].topleft = player['pos']

player = {
    'pos': [2*CELL_SIZE,248*CELL_SIZE],
    'size': [32,32],
    'rect': pygame.Rect([2*CELL_SIZE,248*CELL_SIZE],[32,32]),
    'speed': 0.8,
    'force':  [0,0], 
    'update': update_player,
    'draw': draw_player,
    'color': GREEN
}