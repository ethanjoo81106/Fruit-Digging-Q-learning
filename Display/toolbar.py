import pygame

class Toolbar:
    #
    # Creates the clue tool toolbar and lays out its buttons.
    #
    # Args:
    #     surface: Pygame surface where the toolbar is drawn.
    #     y: Top y-coordinate for the toolbar.
    #     height: Toolbar height in pixels.
    #     padding: Space around and between buttons.
    #     labels: Tool labels shown as buttons.
    #
    def __init__(
            self,
            surface: pygame.Surface,
            y: int,
            height: int = 90,
            padding: int = 12,
            labels=("Iron", "Gold", "Diamond"),
        ):

        # Font and drawing surface setup.
        pygame.font.init()

        self.surface = surface
        self.rect = pygame.Rect(0, y, surface.get_width(), height)

        # Toolbar and button colors.
        self.bg_color = (28, 28, 34)
        self.button_color = (60, 60, 72)
        self.hover_color = (80, 80, 96)
        self.selected_color = (70, 180, 120)
        self.text_color = (255, 255, 255)

        self.font = pygame.font.SysFont("arial", 24)

        # Tool labels and selected tool state.
        self.labels = list(labels)
        self.selected_label = self.labels[0] if self.labels else None


        # Button rectangles keyed by label.
        self.buttons: dict[str, pygame.Rect] = {}
        self._layout_buttons(padding=padding)

    #
    # Recalculates button rectangles for the current toolbar size.
    #
    # Args:
    #     padding: Space around and between buttons.
    #
    def _layout_buttons(self, *, padding: int):
        num = len(self.labels)

        if num == 0:
            return

        total_pad = padding * (num + 1)
        button_width = max(1, (self.rect.width - total_pad) // num)
        button_height = max(1, (self.rect.height - padding * 2))

        x = padding
        y = self.rect.y + padding
        self.buttons.clear()

        for label in self.labels:
            self.buttons[label] = pygame.Rect(x, y, button_width, button_height)
            x += button_width + padding

    #
    # Selects a toolbar button if the click position is inside one.
    #
    # Args:
    #     pos: Mouse click position in screen coordinates.
    #
    # Returns:
    #     Selected tool label, or None if no button was clicked.
    #
    def handle_click(self, pos) -> str | None:
        for label, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.selected_label = label;
                return label
        return None

    #
    # Draws the toolbar background and each tool button.
    #
    def draw(self):
        pygame.draw.rect(self.surface, self.bg_color, self.rect)

        mouse_pos = pygame.mouse.get_pos()
        for label, rect in self.buttons.items():
            if label == self.selected_label:
                color = self.selected_color
            elif rect.collidepoint(mouse_pos):
                color = self.hover_color
            else:
                color = self.button_color

            pygame.draw.rect(self.surface, color, rect, border_radius=8)
            text = self.font.render(label, True, self.text_color)
            self.surface.blit(text, text.get_rect(center=rect.center))

    #
    # Moves the toolbar vertically and rebuilds the button layout.
    #
    # Args:
    #     y: New top y-coordinate for the toolbar.
    #     padding: Space around and between buttons.
    #
    def set_y(self, y: int, *, padding: int = 12):
        self.rect.y = y
        self._layout_buttons(padding=padding)
