import os

from Game.grid import Grid
from Game.score import Score
from ability import Ability
from Display.toolbar import Toolbar
from Util.bomb import Bomb
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

        #buttons

        self.button_font = pygame.font.SysFont("arial", 24)
        self.buttons = {
            "Reset": pygame.Rect(self.surface.get_width() - 140, 20, 120, 40)
        }

        self.tile_rects = [
            [pygame.Rect(START_X + c * STEP, START_Y + r * STEP, TILE_W, TILE_H)
            for c in range(self.grid.width)]
            for r in range(self.grid.height)
        ]

        self.score = Score()
        self.images = {}
        self._load_image("images")

        #toolbar stuff
        self.toolbar = Toolbar(self.surface, y = 0)
        toolbar_y = START_Y + (self.grid.height * STEP) + 15
        self.toolbar.set_y(toolbar_y)

        #Global clicks
        self.max_clicks = 15
        self.clicks_left = self.max_clicks

    def _load_image(self, folder: str):
        names = set(self.grid.kinds) | {"empty", "blownup"}
        for name in names:
            path = os.path.join(folder, f"{name.lower()}.jpg")
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (TILE_W, TILE_H))
            except Exception as e:
                img = pygame.Surface((TILE_W, TILE_H), pygame.SRCALPHA)
                img.fill((80, 80, 80, 255))
            self.images[name] = img

    #TILE CLICKS
    def handle_click(self, pos):
        #reset buttons
        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self._on_button(name)
                return

        #toolbar
        if self.toolbar.handle_click(pos) is not None:
            return

        #Tile clicks
        for r in range(self.grid.height):
            for c in range(self.grid.width):
                if self.tile_rects[r][c].collidepoint(pos):
                    tile = self.grid.grid[r][c]

                    if self.clicks_left <= 0:
                        return

                    if tile.fruit and tile.fruit.name == "Bomb":
                        if not tile.dug and self.clicks_left >0:
                            self.clicks_left -= 1
                            tile.dug = True
                            Bomb.explode(self.grid, tile.row, tile.col)
                            return

                    if not tile.dug and self.clicks_left > 0:
                        self.clicks_left -= 1
                        tile.dug = True
                        if tile.fruit:
                            self.score.add(Ability.getScore(tile.fruit.base_points, tile.fruit, tile, self.grid))
                    return

    def draw_board(self):
        self.surface.fill(self.bg)
        self._draw_hud()

        for r in range(self.grid.height):
            for c in range(self.grid.width):

                rect = self.tile_rects[r][c]
                tile = self.grid.grid[r][c]

                if tile.blownup:
                    self.surface.blit(self.images["blownup"], rect.topleft)
                elif tile.dug and tile.fruit:
                    name = tile.fruit.name
                    img = self.images.get(name, self.images["empty"])
                    self.surface.blit(img, rect.topleft)
                else:
                    pygame.draw.rect(self.surface, TILE_OFF, rect)
        
        for name, rect in self.buttons.items():
            pygame.draw.rect(self.surface, (60, 60, 72), rect, border_radius=6)
            label = self.button_font.render(name.title(), True, (255, 255, 255))
            self.surface.blit(label, label.get_rect(center=rect.center))

        self.toolbar.draw()

        pygame.display.flip()

    def _draw_hud(self):
        pygame.draw.rect(self.surface, (28, 28, 34), pygame.Rect(0, 0, self.surface.get_width(), 80))
        text = self.font.render(f"Score: {self.score.total}", True, self.text_color)
        self.surface.blit(text, (15, 20))

        click_text = self.font.render(f"Click: {self.clicks_left}", True, self.text_color)
        self.surface.blit(click_text, (300, 20))

    #RESET BUTTON clicked
    def _on_button(self, name):
        if name == "Reset":
            self.grid = Grid()
            self.grid.propigate_self()
            self.grid.print_grid()
            self.clicks_left = self.max_clicks
            # rebuild rects in case grid size changes
            self.tile_rects = [
                [pygame.Rect(START_X + c * STEP, START_Y + r * STEP, TILE_W, TILE_H)
                for c in range(self.grid.width)]
                for r in range(self.grid.height)
            ]
            self.score.total = 0
            Ability.resetGameAbilities()

        toolbar_y = START_Y + (self.grid.height * STEP) + 15
        self.toolbar.set_y(toolbar_y)
