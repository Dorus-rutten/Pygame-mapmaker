import pygame
import os
"""
! - Cliff
" - Grass
# - Path
$ - Water
% - Sand
& - Tree
' - Rock
( - Bush
) - Flower
* - Chest
+ - Sign
, - House
- - Fence
. - Gate
"""
# Dimensions of the individual sprites
sprite_width = 16
sprite_height = 16

# Number of sprites per row and column
columns = 3
rows = 6

multi_tiled = ["Cliff_Tile.png", "Path_Tile.png", "Water_Tile.png"]

class Map():
    def __init__(self):
        self.tiles = {}
        self.file_tile = [
            "Cliff_Tile.png", 
            "Grass_Middle.png", 
            "Path_Middle.png", 
            "Path_Tile.png", 
            "Water_Middle.png", 
            "Water_Tile.png"
        ]
        self.ascii_key_start = 33  # Start with ASCII code for '!' (33)

    # Initialize Pygame
    pygame.init()

    def load_sprites(self):
        try:
            current_ascii = self.ascii_key_start
            for tile_name in self.file_tile:
                tile_path = os.path.join("sprites", "Tiles", tile_name)
                if tile_name in multi_tiled:
                    sprite_sheet = pygame.image.load(tile_path)
                    sprites = self.sep_tiles(sprite_sheet)
                    for sprite in sprites:
                        self.tiles[chr(current_ascii)] = sprite
                        current_ascii += 1
                else:
                    self.tiles[chr(current_ascii)] = pygame.image.load(tile_path)
                    current_ascii += 1
        except pygame.error as e:
            print(f"Cannot load image: {e}")

    def sep_tiles(self, sprite_sheet):
        sprites = []
        # Extract each sprite
        for row in range(rows):
            for col in range(columns):
                # Calculate the rectangle area of the sprite
                x = col * sprite_width
                y = row * sprite_height
                rect = pygame.Rect(x, y, sprite_width, sprite_height)

                # Extract the sprite using subsurface
                sprite = sprite_sheet.subsurface(rect)
                sprites.append(sprite)
        return sprites

    pygame.quit()

    def hitbox(self):
        pass

# Example usage (ensure the proper file structure and paths exist):
# map_instance = Map()
# map_instance.load_sprites()
# print(map_instance.tiles)
