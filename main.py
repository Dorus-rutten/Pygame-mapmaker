import pygame
from map import Map
import os
import json

map = Map()

# Initialize Pygame
pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Define game variables
ROWS = HEIGHT // 16
MAX_COLS = 150
TILE_SIZE = HEIGHT // ROWS

scroll_left = False
scroll_right = False
scroll_value = 1
scroll_speed = 0.1

size_swipe_ver = 0
size_swipe_hor = 0

# Screen settings
screen = pygame.display.set_mode((WIDTH / 1.5, HEIGHT / 1.5))
window_size = pygame.display.get_window_size()

LOWER_MARGIN = window_size[1] / 1
SIDE_MARGIN = window_size[0] / 1.4  # Sidebar margin

pygame.display.set_caption('Level Editor')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Mulit-tile selection
multi_tiled = [0, 4, 6]

map.load_sprites()
sprites = []

# Sidebar Scroll Variable
sidebar_scroll = 0
sidebar_scroll_speed = 10  # Pixels to scroll per scroll event

# Data structures
placed_tiles = {}  # Stores tiles as {(grid_x, grid_y): tile_type}
placing_tile = False  # Tracks if the mouse is being held down
removing_tile = False  # Tracks if the right mouse button is held down
moving_grid = False  # Tracks if the middle mouse button is held
previous_mouse_pos = None  # Tracks the previous mouse position for grid movement

# File for saving and loading tiles
SAVE_FILE = "tile_data.json"

# Load placeholder tiles
def load_tiles():
    """Simulate loading tiles."""
    tile_dict = {"!": pygame.Surface((TILE_SIZE, TILE_SIZE))}
    tile_dict["!"].fill((255, 0, 0))  # Red square as example tile
    return tile_dict

tiles = load_tiles()

# Load saved tiles
def load_saved_tiles():
    """Load placed tiles from a JSON file."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                raw_data = json.load(f)
                # Convert string keys to tuples
                return {eval(key): value for key, value in raw_data.items()}
        except (json.JSONDecodeError, SyntaxError):
            print(f"Warning: {SAVE_FILE} is corrupted. Resetting file.")
            return {}  # Reset if file is invalid
    return {}

def save_tiles():
    """Save placed tiles to a JSON file."""
    with open(SAVE_FILE, "w") as f:
        json.dump({str(key): value for key, value in placed_tiles.items()}, f, indent=4)





def handle_scroll(event, scroll_value, mouse_pos):
    """Handle mouse scroll events and update the scroll value."""
    if event.type == pygame.MOUSEBUTTONDOWN and mouse_pos[0] < SIDE_MARGIN:
        if event.button == 4:  # Scroll up
            scroll_value += scroll_speed
        elif event.button == 5:  # Scroll down
            scroll_value -= scroll_speed
    
    elif event.type == pygame.KEYDOWN and mouse_pos[0] > SIDE_MARGIN:
        pass
    return scroll_value


def draw_grid(scroll_value):
    """Draw grid based on scale factor (scroll_value)."""
    scaled_tile_size = TILE_SIZE * scroll_value

    # Vertical lines
    for col in range(MAX_COLS + 1):
        x = col * scaled_tile_size - size_swipe_hor
        if x < SIDE_MARGIN:  # Prevent grid rendering into the sidebar
            pygame.draw.line(screen, BLACK, (x, 0), (x, window_size[1]))

    # Horizontal lines
    for row in range(ROWS + 1):
        y = row * scaled_tile_size - size_swipe_ver
        pygame.draw.line(screen, BLACK, (0, y), (SIDE_MARGIN, y))


def draw_sidebar():
    # Draw the background for the sidebar
    pygame.draw.rect(screen, GRAY, (SIDE_MARGIN, 0, window_size[0] - SIDE_MARGIN, window_size[1]), 0)


def draw_lowerbar():
    """Draw the lower bar with options or tile previews."""
    lower_bar_height = 50  # Fixed height for the lower bar
    pygame.draw.rect(screen, GRAY, (0, window_size[1] - lower_bar_height, window_size[0], lower_bar_height), 0)
    font = pygame.font.SysFont('Arial', 20)
    text = font.render('Lower Bar - BIG DICKS IN YOU ASS', True, WHITE)
    screen.blit(text, (10, window_size[1] - lower_bar_height + 10))


def snap_to_grid(pos, scroll_value):
    """Snap a position to the nearest grid cell, considering zoom (scroll_value)."""
    scaled_tile_size = TILE_SIZE * scroll_value
    grid_x = int((pos[0] + size_swipe_hor) // scaled_tile_size) * scaled_tile_size - size_swipe_hor
    grid_y = int((pos[1] + size_swipe_ver) // scaled_tile_size) * scaled_tile_size - size_swipe_ver
    return grid_x, grid_y


# Replace the placeholder loading with actual textures from map.tiles
def load_tiles():
    """Load tiles from the map object."""
    return map.tiles  # Assuming map.tiles is already loaded with textures

tiles = load_tiles()  # Update to use actual textures

# Update handle_tile_placement to place tiles based on a selected texture
selected_tile = "!"  # Default selected tile from map.tiles

def handle_tile_placement(event):
    global placing_tile, removing_tile
    mouse_pos = pygame.mouse.get_pos()

    if mouse_pos[0] > SIDE_MARGIN:  # Only place tiles in the grid area
        grid_pos = snap_to_grid(mouse_pos, scroll_value)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left-click to place a tile
                placing_tile = True
                placed_tiles[grid_pos] = selected_tile
            elif event.button == 3:  # Right-click to remove a tile
                removing_tile = True
                placed_tiles.pop(grid_pos, None)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                placing_tile = False
            elif event.button == 3:
                removing_tile = False

# Update draw_tiles to render textures
def draw_tiles():
    for (grid_x, grid_y), tile_type in placed_tiles.items():
        scaled_tile_size = TILE_SIZE * scroll_value
        screen_x = grid_x * scaled_tile_size - size_swipe_hor
        screen_y = grid_y * scaled_tile_size - size_swipe_ver
        if tile_type in tiles:
            scaled_tile = pygame.transform.scale(tiles[tile_type], (scaled_tile_size, scaled_tile_size))
            screen.blit(scaled_tile, (screen_x, screen_y))



def handle_grid_movement(event):
    global moving_grid, previous_mouse_pos, size_swipe_hor, size_swipe_ver

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:  # Middle mouse button pressed
        moving_grid = True
        previous_mouse_pos = pygame.mouse.get_pos()

    elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:  # Middle mouse button released
        moving_grid = False

    elif event.type == pygame.MOUSEMOTION and moving_grid:  # Move the grid
        current_mouse_pos = pygame.mouse.get_pos()
        dx, dy = current_mouse_pos[0] - previous_mouse_pos[0], current_mouse_pos[1] - previous_mouse_pos[1]
        size_swipe_hor -= dx
        size_swipe_ver -= dy
        previous_mouse_pos = current_mouse_pos
def current_tile():
    global selected_tile
    if selected_tile == "!":
        return "Red Square"
    elif selected_tile == "#":
        return "Blue Square"
    else:
        return "Unknown Tile"




def main():
    global scroll_value, size_swipe_ver, size_swipe_hor, placing_tile
    running = True

    # Ensure that map.tiles is loaded before entering the main loop
    map.load_sprites()

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle mouse scroll events
            scroll_value = handle_scroll(event, scroll_value, pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()
                handle_tile_placement(event, scroll_value)
                if size_swipe_ver >= 0:
                    if event.key == pygame.K_UP:
                        size_swipe_ver -= TILE_SIZE
                if event.key == pygame.K_DOWN:
                    size_swipe_ver += TILE_SIZE

                if size_swipe_hor >= 0:
                    if event.key == pygame.K_LEFT:
                        size_swipe_hor -= TILE_SIZE
                if event.key == pygame.K_RIGHT:
                    size_swipe_hor += TILE_SIZE

        # Ensure the scroll value is within bounds
        scroll_value = max(1, scroll_value)

        # Get mouse position and align it to the grid
        mouse_pos = pygame.mouse.get_pos()
        grid_pos = snap_to_grid(mouse_pos, scroll_value)

        # Scale the tile based on scroll_value
        scaled_tile_size = TILE_SIZE * scroll_value
        tile_key = "!"  # Example of the tile key you want to use

        # Ensure the tile exists in map.tiles
        if tile_key in map.tiles:
            scaled_tile = pygame.transform.scale(map.tiles[tile_key], (scaled_tile_size, scaled_tile_size))

            # Draw the tile aligned to the grid
            if grid_pos[0] < SIDE_MARGIN:  # Prevent tiles rendering into the sidebar
                screen.blit(scaled_tile, grid_pos)
        key = "!"
        # Draw the scaled grid
        draw_grid(scroll_value)
        draw_sidebar()
        draw_lowerbar()
        draw_tiles()

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
