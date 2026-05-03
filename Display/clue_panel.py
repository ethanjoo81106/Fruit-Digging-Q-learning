import pygame

from ability import Ability

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

        neighbors = self._get_neighbors(tile.row, tile.col, grid)

        # Iron reports the number of adjacent bombs.
        if tool_name == "Iron":
            mine_count = sum(
                1 for neighbor in neighbors
                if neighbor.fruit and neighbor.fruit.name == "Bomb"
            )
            mine_label = "mine" if mine_count == 1 else "mines"
            self.text = f"{mine_count} adjacent {mine_label}."
            return

        # Diamond highlights the nearby fruit with the lowest current score value.
        if tool_name == "Diamond":
            fruit_neighbors = [
                neighbor for neighbor in neighbors
                if neighbor.fruit
                and neighbor.fruit.name not in ("Bomb", "Rum")
                and not neighbor.dug
                and not neighbor.blownup
            ]

            if not fruit_neighbors:
                self.text = "No nearby fruit found."
                return

            target = min(
                fruit_neighbors,
                key=lambda neighbor: (self._get_current_fruit_score(neighbor.fruit), neighbor.row, neighbor.col)
            )
            self.highlight_tiles.add((target.row, target.col))
            self.text = f"Lowest nearby fruit: {target.fruit.name} at {target.row + 1},{target.col + 1}."
            return

        # Gold and other fruit clue tools report the nearby fruit with the highest score value.
        fruit_neighbors = [
            neighbor for neighbor in neighbors
            if neighbor.fruit and neighbor.fruit.name not in ("Bomb", "Rum")
        ]

        if not fruit_neighbors:
            self.text = "No nearby fruit found."
            return

        target = max(
            fruit_neighbors,
            key=lambda neighbor: (self._get_current_fruit_score(neighbor.fruit), neighbor.row, neighbor.col)
        )
        self.text = f"Highest nearby fruit: {target.fruit.name}"

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
    # Gets all valid tiles surrounding a grid position.
    #
    # Args:
    #     row: Center tile row.
    #     col: Center tile column.
    #     grid: Current game grid.
    #
    # Returns:
    #     List of neighboring tiles around the center position.
    #
    def _get_neighbors(self, row: int, col: int, grid):
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue

                nr = row + dr
                nc = col + dc
                if 0 <= nr < grid.height and 0 <= nc < grid.width:
                    neighbors.append(grid.grid[nr][nc])

        return neighbors

    #
    # Calculates the current score value a fruit would give if dug now.
    #
    # Args:
    #     fruit: Fruit object to evaluate.
    #
    # Returns:
    #     Current score value after active fruit scaling and multipliers.
    #
    def _get_current_fruit_score(self, fruit):
        point_multiplier = 1
        if Ability.mode == 3:
            point_multiplier = 1.5
        elif Ability.mode == 6:
            point_multiplier = 0.5

        if fruit.ability == 1:
            points = (Ability.apples + 1) * 100
        elif fruit.ability == 5 and Ability.cherry + 1 == 2:
            points = fruit.base_points + 200
        else:
            points = fruit.base_points

        score = points * point_multiplier
        if isinstance(score, float) and score.is_integer():
            return int(score)
        return score

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
