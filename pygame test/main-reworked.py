import pygame
import os
import json
from map import Map

#TODO:
# - Add a way to save the level
# - Add a way to load the level
# - Add a way to change the level
# - fix the zoom function
# - fix the tile selection
# - make a way to select multiple tiles
# - add background
# - add a scroll bar
# - add a way to chouse to bigness of the level
# - find a girlfriend


map = Map()

# Initialize Pygame
pygame.init()

# Set up display caption
pygame.display.set_caption('Level Editor')

# get resolution of the screen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Set up display
screen = pygame.display.set_mode((WIDTH // 1.5, HEIGHT // 1.5), pygame.RESIZABLE)
window_size = pygame.display.get_window_size()

# Define game variables
'''fix: make them chosen by user'''
ROWS = 100
COLS = 200
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

sheet = []  # 2D list to store the level data

level_file = "level_" + str(level) + ".txt"
SAVE_FILE = level_file

def load_level():
    global sheet, selected_tile
    if not os.path.exists(SAVE_FILE): 
        print("Level file not found. Creating a new one...")
        with open(SAVE_FILE, "w") as file:
            for i in range(ROWS):
                for j in range(COLS):
                    file.write("-")
                file.write("\n")
    
    with open(SAVE_FILE, "r") as file:
        lines = file.readlines()
        sheet = [list(line.strip()) for line in lines]

def save_level():
    global sheet
    with open(SAVE_FILE, "w") as file:
        for row in sheet:
            file.write("".join(row) + "\n")


def check_fucking_boundrys():
    global scaled_tile_size, scroll_value, grid_mov_hor, grid_mov_ver, grid_max_x_scaled, grid_max_y_scaled
    window_size = pygame.display.get_window_size()
    grid_max_x_scaled = (COLS * scaled_tile_size) - window_size[0]
    grid_max_y_scaled = (ROWS * scaled_tile_size) - window_size[1]

    print(grid_mov_hor, grid_max_x_scaled)


    if (scaled_tile_size * COLS) - grid_mov_hor < window_size[0]:
        scroll_value += scroll_speed
        scaled_tile_size = TILE_SIZE * scroll_value

    if (scaled_tile_size * ROWS) - grid_mov_ver < window_size[1]:
        scroll_value += scroll_speed
        scaled_tile_size = TILE_SIZE * scroll_value
        



def handle_scroll(event, scroll_value):
    global scaled_tile_size, grid_mov_hor, grid_mov_ver, mouse_pos
    mouse_pos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
        
        if event.button == 4:  # Scroll up (zoom in)
                scroll_value += scroll_speed

        elif event.button == 5:# Scroll down (zoom out)
                scroll_value -= scroll_speed


    return scroll_value, scaled_tile_size

def handle_grid_movement(event):
    global grid_mov_hor, grid_mov_ver, move_speed, scaled_tile_size, grid_max_x_scaled, grid_max_y_scaled
    # Handle middle mouse button dragging
    
    if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[1]:
        dx, dy = event.rel  # Relative movement

        grid_mov_hor = max(0, min(grid_mov_hor - dx, grid_max_x_scaled))
        grid_mov_ver = max(0, min(grid_mov_ver - dy, grid_max_y_scaled))
        

def draw_grid(scaled_tile_size):
    window_size = pygame.display.get_window_size()
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

# Handle tile placement and removal
def handle_tile_placement(event):
    global placing_tile, removing_tile, placed_tiles, selected_tile, multi_tiled    
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left mouse button
            placing_tile = True
        elif event.button == 3:  # Right mouse button
            removing_tile = True

    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:  # Left mouse button
            placing_tile = False
        elif event.button == 3:  # Right mouse button
            removing_tile = False



def draw_tiles(tile_size=None):
    global sheet
    mouse_pos = pygame.mouse.get_pos()
    grid_x = int((mouse_pos[0] + grid_mov_hor) // scaled_tile_size)
    grid_y = int((mouse_pos[1] + grid_mov_ver) // scaled_tile_size)
    x = grid_x * scaled_tile_size - grid_mov_hor
    y = grid_y * scaled_tile_size - grid_mov_ver

    scaled_tile = pygame.transform.scale(tiles[selected_tile], (scaled_tile_size, scaled_tile_size))
    screen.blit(scaled_tile, (x, y))
    if placing_tile:
        sheet[grid_y][grid_x]  = selected_tile
    elif removing_tile:
        sheet[grid_y][grid_x] = "-"
    
    for nx, i in enumerate(sheet):
        for ny, j in enumerate(i):
            if j != "-":
                scaled_tile = pygame.transform.scale(tiles[j], (scaled_tile_size, scaled_tile_size))
                screen.blit(scaled_tile, (ny*tile_size - grid_mov_hor, nx*tile_size - grid_mov_ver))
    




    #grid_x and grid_y are the vector we can use
    
        
        


load_level()

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
            handle_tile_placement(event)
            check_fucking_boundrys()

        # print(scaled_tile_size)
        screen.fill(WHITE)
        check_fucking_boundrys() 
        draw_tiles(scaled_tile_size)
        draw_grid(scaled_tile_size)
        
        pygame.display.flip()
        clock.tick(FPS)
    save_level()
    pygame.quit()

if __name__ == "__main__":
    main()