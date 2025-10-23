import os
from grid import Grid
from score import Score
import pygame

BG = (18, 18, 22)
PANEL = (28, 28, 34)
GRID_BG = (24, 24, 30)
GRID_LINE = (72, 72, 80)
TILE_OFF = (36, 36, 44)
TILE_ON = (70, 180, 120)
HOVER = (60, 60, 72)

TILE_W = 90
TILE_H = 90
START_X = 15 
START_Y = 100
STEP   = 100

class Board:
    def __init__(self, surface: pygame.Surface):

        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 36)
        self.text_color = (255, 255, 255)

        self.surface = surface
        self.bg = BG

        self.grid = Grid()
        self.grid.propigate_self()
        self.grid.print_grid()

        self.tile_rects = [
            [pygame.Rect(START_X + c * STEP, START_Y + r * STEP, TILE_W, TILE_H)
            for c in range(self.grid.width)]
            for r in range(self.grid.height)
        ]

        self.score = Score()
        self.images = {}
        self._load_image("images")

    def _load_image(self, folder: str):
        names = set(self.grid.kinds) | {"empty"}
        for name in names:
            path = os.path.join(folder, f"{name.lower()}.jpg")
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (TILE_W, TILE_H))
            except Exception as e:
                img = pygame.Surface((TILE_W, TILE_H), pygame.SRCALPHA)
                img.fill((80, 80, 80, 255))
            self.images[name] = img

    def handle_click(self, pos):
        for r in range(self.grid.height):
            for c in range(self.grid.width):
                if self.tile_rects[r][c].collidepoint(pos):
                    tile = self.grid.grid[r][c]
                    tile.dug = True
                    return

    def drawBoard(self):
        self.surface.fill(self.bg)

        for r in range(self.grid.height):
            for c in range(self.grid.width):
                rect = self.tile_rects[r][c]
                tile = self.grid.grid[r][c]

                if tile.dug and tile.fruit:
                    name = tile.fruit.name
                    img = self.images.get(name, self.images["empty"])
                    self.surface.blit(img, rect.topleft)
                else:
                    pygame.draw.rect(self.surface, TILE_OFF, rect)
        
        pygame.display.flip()