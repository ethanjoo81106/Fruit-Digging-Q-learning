import os

from Game.grid import Grid
from Game.score import Score
from ability import Ability
from Display.clue_panel import CluePanel
from Display.toolbar import Toolbar
from Util.bomb import Bomb
import pygame

#Default board settings
BG = (18, 18, 22)
PANEL = (28, 28, 34)
GRID_BG = (24, 24, 30)
GRID_LINE = (72, 72, 80)
TILE_OFF = (36, 36, 44)
TILE_ON = (70, 180, 120)
HOVER = (60, 60, 72)

#Default gui settings
TILE_W = 90
TILE_H = 90
START_X = 15 
START_Y = 135
STEP   = 100
HUD_HEIGHT = 115

class Board:
    #
    # Creates the game board, loads display assets, and initializes game state.
    #
    # Args:
    #     surface: Pygame surface where the board and HUD are drawn.
    #
    def __init__(self, surface: pygame.Surface):

        # Font and color settings used by the score and click HUD.
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 36)
        self.text_color = (255, 255, 255)

        # Main drawing surface and background color.
        self.surface = surface
        self.bg = BG

        # Board data model. The grid fills itself with random fruit.
        self.grid = Grid()
        self.grid.propigate_self()
        self.grid.print_grid()

        # Reset button shown in the top-right HUD.
        self.button_font = pygame.font.SysFont("arial", 24)
        self.buttons = {
            "Reset": pygame.Rect(self.surface.get_width() - 140, 20, 120, 40)
        }

        # Screen rectangles for each grid tile.
        self.tile_rects = [
            [pygame.Rect(START_X + c * STEP, START_Y + r * STEP, TILE_W, TILE_H)
            for c in range(self.grid.width)]
            for r in range(self.grid.height)
        ]

        # Score tracker, fruit images, and clue display.
        self.score = Score()
        self.images = {}
        self._load_image("images")
        self.clue_panel = CluePanel()

        # Tool selector under the board.
        self.toolbar = Toolbar(self.surface, y = 0)
        toolbar_y = START_Y + (self.grid.height * STEP) + 15
        self.toolbar.set_y(toolbar_y)

        # Click limit for one round.
        self.max_clicks = 15
        self.clicks_left = self.max_clicks

    #
    # Loads fruit and board-state images from the given folder.
    #
    # Args:
    #     folder: Folder containing image files named after each fruit.
    #
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

    #
    # Handles reset button, toolbar, and tile clicks.
    #
    # Args:
    #     pos: Mouse click position in screen coordinates.
    #
    def handle_click(self, pos):
        # Check reset and other HUD buttons before board clicks.
        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self._on_button(name)
                return

        # Check whether the player selected a clue tool.
        selected_tool = self.toolbar.handle_click(pos)
        if selected_tool is not None:
            self.clue_panel.set_tool(selected_tool)
            return

        # Check the clicked tile, apply fruit scoring, and update clues.
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
                            self.clue_panel.update_from_tile(self.toolbar.selected_label or "Iron", tile, self.grid)
                            return

                    if not tile.dug and self.clicks_left > 0:
                        self.clicks_left -= 1
                        tile.dug = True
                        if tile.fruit:
                            self.score.add(Ability.getScore(tile.fruit.base_points, tile.fruit, tile, self.grid))
                        self.clue_panel.update_from_tile(self.toolbar.selected_label or "Iron", tile, self.grid)
                    return

    #
    # Draws the full board, revealed fruit, buttons, highlights, and toolbar.
    #
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
                self.clue_panel.draw_tile_highlight(self.surface, rect, r, c)
        
        for name, rect in self.buttons.items():
            pygame.draw.rect(self.surface, (60, 60, 72), rect, border_radius=6)
            label = self.button_font.render(name.title(), True, (255, 255, 255))
            self.surface.blit(label, label.get_rect(center=rect.center))

        self.toolbar.draw()

        pygame.display.flip()

    #
    # Draws the top HUD containing score, clicks left, and clue text.
    #
    def _draw_hud(self):
        pygame.draw.rect(self.surface, (28, 28, 34), pygame.Rect(0, 0, self.surface.get_width(), HUD_HEIGHT))
        text = self.font.render(f"Score: {self.score.total}", True, self.text_color)
        self.surface.blit(text, (15, 18))

        click_text = self.font.render(f"Click: {self.clicks_left}", True, self.text_color)
        self.surface.blit(click_text, (250, 18))

        clue_rect = pygame.Rect(15, 72, self.surface.get_width() - 30, 32)
        self.clue_panel.draw_hud(self.surface, clue_rect)

    #
    # Runs the action for a clicked board button.
    #
    # Args:
    #     name: Button label that was clicked.
    #
    def _on_button(self, name):
        if name == "Reset":
            self.grid = Grid()
            self.grid.propigate_self()
            self.grid.print_grid()
            self.clicks_left = self.max_clicks

            # Rebuild tile rectangles in case grid dimensions change later.
            self.tile_rects = [
                [pygame.Rect(START_X + c * STEP, START_Y + r * STEP, TILE_W, TILE_H)
                for c in range(self.grid.width)]
                for r in range(self.grid.height)
            ]
            self.score.total = 0
            Ability.resetGameAbilities()
            self.clue_panel.reset(self.toolbar.selected_label or "Iron")

        toolbar_y = START_Y + (self.grid.height * STEP) + 15
        self.toolbar.set_y(toolbar_y)
