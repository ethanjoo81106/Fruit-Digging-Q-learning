import pygame

from Game.clues import get_clue

class CluePanel:
    #
    # Creates the clue panel used to display tool feedback and tile highlights.
    #
    def __init__(self):
        # Font settings for the clue title and message.
        pygame.font.init()
        self.title_font = pygame.font.SysFont("arial", 22)
        self.body_font = pygame.font.SysFont("arial", 20)

        # Current clue state shown in the HUD.
        self.title = "Iron"
        self.text = "Mine a tile to reveal adjacent bombs."
        self.highlight_tiles = set()

        # Colors used for clue text, panel background, border, and highlights.
        self.text_color = (255, 255, 255)
        self.muted_text_color = (205, 205, 215)
        self.panel_color = (40, 40, 48)
        self.border_color = (72, 72, 84)
        self.highlight_color = (90, 210, 255)

    #
    # Sets the active clue tool and resets the panel text for that tool.
    #
    # Args:
    #     tool_name: Name of the selected clue tool.
    #
    def set_tool(self, tool_name: str):
        self.title = tool_name
        self.text = self._get_idle_tool_prompt(tool_name)
        self.highlight_tiles.clear()

    #
    # Resets the clue panel back to the selected tool's idle state.
    #
    # Args:
    #     tool_name: Name of the active clue tool after reset.
    #
    def reset(self, tool_name: str):
        self.set_tool(tool_name)

    #
    # Updates clue text and highlighted tiles after the player digs a tile.
    #
    # Args:
    #     tool_name: Active clue tool used for this update.
    #     tile: Tile that was just dug.
    #     grid: Current game grid.
    #
    def update_from_tile(self, tool_name: str, tile, grid):
        self.title = tool_name
        self.highlight_tiles.clear()

        clue = get_clue(tool_name, tile, grid)
        self.text = clue.text
        self.highlight_tiles.update(clue.highlight_tiles)

    #
    # Draws the clue panel inside the HUD.
    #
    # Args:
    #     surface: Pygame surface where the HUD is drawn.
    #     rect: Rectangle defining the clue panel area.
    #
    def draw_hud(self, surface: pygame.Surface, rect: pygame.Rect):
        pygame.draw.rect(surface, self.panel_color, rect, border_radius=8)
        pygame.draw.rect(surface, self.border_color, rect, width=1, border_radius=8)

        title = self.title_font.render(f"{self.title} Clue", True, self.text_color)
        title_y = rect.y + (rect.height - title.get_height()) // 2
        surface.blit(title, (rect.x + 10, title_y))

        body_x = rect.x + 10 + title.get_width() + 14
        clue_body = self._fit_text(self.text, self.body_font, rect.right - body_x - 10)
        body = self.body_font.render(clue_body, True, self.muted_text_color)
        body_y = rect.y + (rect.height - body.get_height()) // 2
        surface.blit(body, (body_x, body_y))

    #
    # Draws a highlight border around a tile if it is part of the active clue.
    #
    # Args:
    #     surface: Pygame surface where the tile is drawn.
    #     rect: Tile rectangle on the screen.
    #     row: Tile row in the grid.
    #     col: Tile column in the grid.
    #
    def draw_tile_highlight(self, surface: pygame.Surface, rect: pygame.Rect, row: int, col: int):
        if (row, col) in self.highlight_tiles:
            pygame.draw.rect(surface, self.highlight_color, rect, width=5, border_radius=8)

    #
    # Trims clue text so it fits within the available HUD width.
    #
    # Args:
    #     text: Text to display.
    #     font: Font used to measure the text width.
    #     max_width: Maximum allowed width in pixels.
    #
    # Returns:
    #     Text shortened with ellipses if needed.
    #
    def _fit_text(self, text: str, font: pygame.font.Font, max_width: int) -> str:
        if font.size(text)[0] <= max_width:
            return text

        trimmed = text
        while trimmed and font.size(trimmed + "...")[0] > max_width:
            trimmed = trimmed[:-1]

        return trimmed + "..." if trimmed else ""

    #
    # Gets the default clue message for the selected tool.
    #
    # Args:
    #     tool_name: Name of the selected clue tool.
    #
    # Returns:
    #     Idle prompt shown before the player digs a tile.
    #
    def _get_idle_tool_prompt(self, tool_name: str) -> str:
        if tool_name == "Iron":
            return "Mine a tile to reveal adjacent bombs."
        if tool_name == "Gold":
            return "Mine a tile to reveal the best nearby fruit."
        if tool_name == "Diamond":
            return "Mine a tile to mark the lowest nearby fruit."
        return "Mine a tile to reveal a clue."
