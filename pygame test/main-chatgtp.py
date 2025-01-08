import pygame
import os
import json
from map import Map

map = Map()
# Initialize Pygame
pygame.init()

# Screen and window settings
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Define game variables
ROWS = 32
MAX_COLS = 140
TILE_SIZE = 16

scroll_left = False
scroll_right = False
scroll_value = 1
scroll_speed = 0.05

size_swipe_ver = 0
size_swipe_hor = 0

# Screen setup
screen = pygame.display.set_mode((WIDTH // 1.5, HEIGHT // 1.5))
window_size = pygame.display.get_window_size()

LOWER_MARGIN = window_size[1] / 1
SIDE_MARGIN = window_size[0] / 1.4  # Sidebar margin

pygame.display.set_caption('Level Editor')

# Handle grid movement
# Define grid boundaries
GRID_MIN_X = 0
GRID_MIN_Y = 0
GRID_MAX_X = MAX_COLS * TILE_SIZE
GRID_MAX_Y = ROWS * TILE_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Data structures
placed_tiles = {}  # Stores tiles as {(grid_x, grid_y): tile_type}
placing_tile = False  # Tracks if the mouse is being held down
removing_tile = False  # Tracks if the right mouse button is held down
moving_grid = False  # Tracks if the middle mouse button is held
previous_mouse_pos = None  # Tracks the previous mouse position for grid movement
current_ascii = 33
# Mulit-tile selection
multi_tiled = [0, 4, 6]

map.load_sprites()

current_ascii = 33  # Start with ASCII 33 ('!')
selected_tile = chr(current_ascii)  # Default selected tile'

level = 0  # Default level number
level_file = "level_" + str(level) + ".csv"

# File for saving and loading tiles
SAVE_FILE = level_file

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

# Save placed tiles
def save_tiles():
    """Save placed tiles to a JSON file."""
    with open(SAVE_FILE, "w") as f:
        json.dump({str(key): value for key, value in placed_tiles.items()}, f, indent=4)

# Handle scrolling
# Handle scrolling
def handle_scroll(event, scroll_value, mouse_pos):
    global size_swipe_hor, size_swipe_ver
    
    if event.type == pygame.MOUSEBUTTONDOWN and mouse_pos[0] < SIDE_MARGIN:
        # Get the position of the mouse in the grid
        prev_tile_size = TILE_SIZE * scroll_value
        grid_x = (mouse_pos[0] + size_swipe_hor) / prev_tile_size
        grid_y = (mouse_pos[1] + size_swipe_ver) / prev_tile_size
        print(size_swipe_hor)

        # Adjust zoom level
        if event.button == 4:  # Scroll up (zoom in)
            scroll_value += scroll_speed
        elif event.button == 5:  # Scroll down (zoom out)
            scroll_value = max(0.1, scroll_value - scroll_speed)  # Minimum zoom level

        # New tile size after zoom
        new_tile_size = TILE_SIZE * scroll_value

        # Update swipe offsets to keep the mouse position centered
        size_swipe_hor = int(grid_x * new_tile_size - mouse_pos[0])
        size_swipe_ver = int(grid_y * new_tile_size - mouse_pos[1])

        if size_swipe_hor < 0 or size_swipe_ver < 0:
            size_swipe_hor = 0
            size_swipe_ver = 0
    return scroll_value


# Draw grid
def draw_grid(scroll_value):
    scaled_tile_size = TILE_SIZE * scroll_value

    # Skip grid rendering if tile size is too small
    if scaled_tile_size < 2:
        return

    # Vertical lines
    for col in range(MAX_COLS + 1):
        x = col * scaled_tile_size - size_swipe_hor
        if 0 <= x < SIDE_MARGIN:
            pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))

    # Horizontal lines
    for row in range(ROWS + 1):
        y = row * scaled_tile_size - size_swipe_ver
        if 0 <= y < window_size[1]:
            pygame.draw.line(screen, BLACK, (0, y), (SIDE_MARGIN, y))



# Draw sidebar
def draw_sidebar():
    pygame.draw.rect(screen, GRAY, (SIDE_MARGIN, 0, window_size[0] - SIDE_MARGIN, window_size[1]), 0)
    scaled_tile = pygame.transform.scale(tiles[selected_tile], (TILE_SIZE*5, TILE_SIZE*5))
    screen.blit(scaled_tile, (SIDE_MARGIN + 10, 10))


# Draw lower bar
def draw_lowerbar():
    lower_bar_height = 50
    pygame.draw.rect(screen, GRAY, (0, window_size[1] - lower_bar_height, window_size[0], lower_bar_height), 0)
    font = pygame.font.SysFont('Arial', 20)
    text = font.render('Lower Bar - Tile Placement', True, WHITE)
    screen.blit(text, (10, window_size[1] - lower_bar_height + 10))

# Snap to grid
def snap_to_grid(scroll_value):
    mouse_pos = pygame.mouse.get_pos()
    scaled_tile_size = TILE_SIZE * scroll_value
    grid_x = int((mouse_pos[0] + size_swipe_hor) // scaled_tile_size)
    grid_y = int((mouse_pos[1] + size_swipe_ver) // scaled_tile_size)
    return grid_x, grid_y

def load_tiles():
    """Load tiles from the map object."""
    return map.tiles  # Assuming map.tiles is already loaded with textures



tiles = load_tiles()  # Update to use actual textures
# Update handle_tile_placement to place tiles based on a selected texture
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
def handle_tile_placement(event, scroll_value):
    global placing_tile, removing_tile
    mouse_pos = pygame.mouse.get_pos()


    if mouse_pos[0] < SIDE_MARGIN:  # Only handle tiles within the editable area
        grid_pos = snap_to_grid(scroll_value)

        # Left-click: Place tile
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            placing_tile = True
            placed_tiles[grid_pos] = selected_tile

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            placing_tile = False

        # Right-click: Remove tile
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            removing_tile = True
            if grid_pos in placed_tiles:
                del placed_tiles[grid_pos]

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            removing_tile = False

        # Continuous placement or removal
        if placing_tile:
            placed_tiles[grid_pos] = selected_tile
        elif removing_tile:
            if grid_pos in placed_tiles:
                del placed_tiles[grid_pos]



def handle_grid_movement(event):
    """Handle movement of the grid view."""
    global size_swipe_hor, size_swipe_ver

    move_speed = 10  # Speed of grid movement

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            size_swipe_ver = max(size_swipe_ver - move_speed, GRID_MIN_Y)
        elif event.key == pygame.K_DOWN:
            size_swipe_ver = min(size_swipe_ver + move_speed, GRID_MAX_Y)
        elif event.key == pygame.K_LEFT:
            size_swipe_hor = max(size_swipe_hor - move_speed, GRID_MIN_X)
        elif event.key == pygame.K_RIGHT:
            size_swipe_hor = min(size_swipe_hor + move_speed, GRID_MAX_X)

    # Handle middle mouse button dragging
    elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[1]:
        dx, dy = event.rel  # Relative movement
        size_swipe_hor = max(GRID_MIN_X, min(size_swipe_hor - dx, GRID_MAX_X)) 
        size_swipe_ver = max(GRID_MIN_Y, min(size_swipe_ver - dy, GRID_MAX_Y))



# Draw placed tiles
def draw_tiles():
    for (grid_x, grid_y), tile_type in placed_tiles.items():
        if tile_type not in tiles:  # Controleer of de tile bestaat
            print(f"Warning: Tile type '{tile_type}' not found in tiles dictionary!")
            continue  # Sla deze tile over als het ongeldig is

        scaled_tile_size = TILE_SIZE * scroll_value
        screen_x = grid_x * scaled_tile_size - size_swipe_hor
        screen_y = grid_y * scaled_tile_size - size_swipe_ver
        scaled_tile = pygame.transform.scale(tiles[tile_type], (scaled_tile_size, scaled_tile_size))
        screen.blit(scaled_tile, (screen_x, screen_y))
        
sidebar_scroll = 0
sidebar_scroll_speed = 20
tiles_per_row = 4  # Set maximum number of tiles per row

def handle_sidebar_scroll(event):
    """Handle scrolling within the sidebar."""
    global sidebar_scroll
    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos()[0] >= SIDE_MARGIN:
        if event.button == 4:  # Scroll up
            sidebar_scroll = max(0, sidebar_scroll - sidebar_scroll_speed)
        elif event.button == 5:  # Scroll down
            sidebar_scroll += sidebar_scroll_speed

def draw_sidebar():
    """Draw the tile selection sidebar."""
    global selected_tile
    pygame.draw.rect(screen, GRAY, (SIDE_MARGIN, 0, window_size[0] - SIDE_MARGIN, window_size[1]), 0)

    # Calculate tile preview size and spacing
    preview_size = TILE_SIZE * 2
    spacing = 10
    start_x = SIDE_MARGIN + 10
    start_y = 10 - sidebar_scroll  # Apply scroll offset

    # Display all tiles in a grid within the sidebar
    for i, tile_type in enumerate(tiles.keys()):
        row = i // tiles_per_row
        col = i % tiles_per_row

        x = start_x + col * (preview_size + spacing)
        y = start_y + row * (preview_size + spacing)

        # Skip tiles outside the visible area
        if y + preview_size < 0 or y > window_size[1]:
            continue

        # Draw tile preview
        tile_surface = pygame.transform.scale(tiles[tile_type], (preview_size, preview_size))
        screen.blit(tile_surface, (x, y))

        # Highlight selected tile
        if tile_type == selected_tile:
            pygame.draw.rect(screen, WHITE, (x - 2, y - 2, preview_size + 4, preview_size + 4), 2)

        # Handle tile selection on click
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if x <= mouse_x <= x + preview_size and y <= mouse_y <= y + preview_size:
                selected_tile = tile_type
                print(f"Selected Tile: {selected_tile}")  # For debugging

# Update main loop
def main():
    global scroll_value, size_swipe_ver, size_swipe_hor, placing_tile, placed_tiles, sidebar_scroll

    # Load tiles at start
    placed_tiles = load_saved_tiles()

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_sidebar_scroll(event)  # Sidebar scrolling
            scroll_value = handle_scroll(event, scroll_value, pygame.mouse.get_pos())
            handle_grid_movement(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()
            handle_tile_placement(event, scroll_value)
            tile_selection(event)

        scroll_value = max(0.3, scroll_value)  # Prevent zoom-out too much

        draw_grid(scroll_value)
        draw_tiles()
        draw_sidebar()  # Updated to include clickable previews
        draw_lowerbar()

        pygame.display.flip()
        clock.tick(FPS)

    # Save tiles on exit
    save_tiles()
    pygame.quit()

if __name__ == "__main__":
    main()

