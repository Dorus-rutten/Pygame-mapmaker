import pygame
import os
import json
from map import Map

#a list of all the variables and explain what they do.
#
#
#
#
#
#
#
#
map = Map()

# Initialize Pygame
pygame.init()

# Set up display caption
pygame.display.set_caption('Level Editor')

# get resolution of the screen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Set up display
screen = pygame.display.set_mode((WIDTH // 1.5, HEIGHT // 1.5))
window_size = pygame.display.get_window_size()

# Define game variables
'''fix: make them chosen by user'''
ROWS = 100
COLS = 100
TILE_SIZE = 16

scaled_tile_size = TILE_SIZE

#mouse setup
scroll_value = 1
scroll_speed = 0.05
mouse_pos = pygame.mouse.get_pos()

# Screen setup
LOWER_MARGIN = window_size[1] / 1
SIDE_MARGIN = window_size[0] / 1.4

# Define grid boundaries
GRID_MIN_X = 0
GRID_MIN_Y = 0
GRID_MAX_X = COLS * TILE_SIZE
GRID_MAX_Y = ROWS * TILE_SIZE

#grid 
grid_mov_hor = 0
grid_mov_ver = 0

grid_max_x_scaled = grid_mov_hor
grid_max_y_scaled = grid_mov_ver

move_speed = 10  # Speed of grid movement

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Mulit-tile selection
multi_tiled = [0, 4, 6]

# Data structures
placed_tiles = {}  # Stores tiles as {(grid_x, grid_y): tile_type}
placing_tile = False  # Tracks if the mouse is being held down
removing_tile = False  # Tracks if the right mouse button is held down


map.load_sprites()

current_ascii = 33 # Start with ASCII 33 ('!')
selected_tile = chr(current_ascii)  # Default selected tile

'''make it chouseble by the player'''
level = 0 # Default level number

level_file = "level_" + str(level) + ".txt"
SAVE_FILE = level_file

def load_level():
    pass

def save_level():
    pass

def check_fucking_boundrys(scaled_tile_size):
        
        mouse_pos = pygame.mouse.get_pos()
        global grid_mov_hor, grid_mov_ver, grid_max_x_scaled, grid_max_y_scaled

        grid_x = (mouse_pos[0] + grid_mov_hor) / scaled_tile_size
        grid_y = (mouse_pos[1] + grid_mov_ver) / scaled_tile_size
        
        grid_mov_hor = grid_x * scaled_tile_size - mouse_pos[0]
        grid_mov_ver = grid_y * scaled_tile_size - mouse_pos[1]

        grid_max_x_scaled = (COLS * scaled_tile_size) - window_size[0]
        grid_max_y_scaled = (ROWS * scaled_tile_size) - window_size[1]


        print(scaled_tile_size * COLS- grid_mov_hor, window_size[0])
        
        if (scaled_tile_size * COLS) - grid_mov_hor< window_size[0]:

            print("gog")
        # print(scaled_tile_size)

def handle_scroll(event, scroll_value):
    global scaled_tile_size
    if event.type == pygame.MOUSEBUTTONUP:
        
        if event.button == 4:  # Scroll up (zoom in)
                scroll_value += scroll_speed
                print(".")

        elif event.button == 5:# Scroll down (zoom out)
                scroll_value -= scroll_speed
                print("..")
                check_fucking_boundrys(scaled_tile_size)
    return scroll_value, scaled_tile_size

def handle_grid_movement(event):
    global grid_mov_hor, grid_mov_ver, move_speed, scaled_tile_size, grid_max_x_scaled, grid_max_y_scaled
    # Handle middle mouse button dragging
    
    if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[1]:
        dx, dy = event.rel  # Relative movement

        check_fucking_boundrys(scaled_tile_size)

        grid_mov_hor = max(0, min(grid_mov_hor - dx, grid_max_x_scaled))
        grid_mov_ver = max(0, min(grid_mov_ver - dy, grid_max_y_scaled))
        
        

def draw_grid(scaled_tile_size):
    # Horizontal lines
    for col in range(COLS + 1):
        x = col * scaled_tile_size - grid_mov_hor
        if x <= window_size[0]:
            pygame.draw.line(screen, BLACK, (x, 0), (x, window_size[0]))

    # Vertical lines
    for row in range(ROWS + 1):
        y = row * scaled_tile_size - grid_mov_ver
        if y < window_size[1]:
            pygame.draw.line(screen, BLACK, (0, y), (window_size[0], y))

""""is this needed?"""
def snap_to_grid(mouse_pos,scaled_tile_size):
    grid_x = int((mouse_pos[0] + grid_mov_hor) // scaled_tile_size)
    grid_y = int((mouse_pos[1] + grid_mov_ver) // scaled_tile_size)
    return grid_x, grid_y


def load_tiles():
    return map.tiles  # Assuming map.tiles is already loaded with textures

tiles = load_tiles()  # Update to use actual textures

def tile_selection(event):
    global current_ascii, selected_tile
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            current_ascii = min(current_ascii + 1, 126)  # Limit to printable ASCII
        elif event.key == pygame.K_DOWN:
            current_ascii = max(current_ascii - 1, 33)   # Avoid non-printable ASCII
        selected_tile = chr(current_ascii)
        print(f"Selected Tile: {selected_tile}")  # For debugging

def main():
    global scroll_value, mouse_pos, scaled_tile_size

    running = True
    while running:
        scaled_tile_size = TILE_SIZE * scroll_value
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scroll_value, scaled_tile_size = handle_scroll(event, scroll_value)
            tile_selection(event)
            handle_grid_movement(event)
        screen.fill(WHITE)
        draw_grid(scaled_tile_size)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()