import pygame
import os
import json
from map import Map

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
ROWS = 500
COLS = 500
TILE_SIZE = 32

#scroll setup
scroll_value = 1
scroll_speed = 0.05

# Screen setup
LOWER_MARGIN = window_size[1] / 1
SIDE_MARGIN = window_size[0] / 1.4

# Define grid boundaries
GRID_MIN_X = 0
GRID_MIN_Y = 0
GRID_MAX_X = COLS * TILE_SIZE
GRID_MAX_Y = ROWS * TILE_SIZE

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
sprites = []

current_ascii = 33 # Start with ASCII 33 ('!')
selected_tile = chr(current_ascii)  # Default selected tile

'''make it chouseble by the player'''
level = 0 # Default level number

level_file = "level_" + str(level) + ".csv"
SAVE_FILE = level_file

def load_level():
    pass

def save_level():
    pass


def draw_grid(scroll_value):
    scaled_tile_size = TILE_SIZE * scroll_value

    # Vertical lines
    for col in range(COLS + 1):
        x = col * scaled_tile_size
        if x <= window_size[0]:
            pygame.draw.line(screen, BLACK, (x, 0), (x, window_size[0]))

    for row in range(ROWS + 1):
        y = row * scaled_tile_size
        if y < window_size[1]:
            pygame.draw.line(screen, BLACK, (0, y), (window_size[0], y))

def handle_scroll(event, scroll_value, mouse_pos):

    if event.type == pygame.MOUSEBUTTONDOWN:


        # Adjust zoom level
        if event.button == 4:  # Scroll up (zoom in)
            scroll_value += scroll_speed
        elif event.button == 5:  # Scroll down (zoom out)
            scroll_value -= scroll_speed




def main():

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_grid(1)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()