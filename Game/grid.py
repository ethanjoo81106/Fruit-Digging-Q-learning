from DataObjects.tile import Tile
from DataObjects.fruit import Fruit
import random

class Grid:
    #
    # Creates an empty grid and defines fruit counts and score values.
    #
    def __init__(self):
        # Grid dimensions.
        self.width = 7
        self.height = 7
        self.grid = []

        # Tile objects stored by row and column.
        for r in range(self.height):
            row = []
            for c in range(self.width):
                row.append(Tile(r, c))
            self.grid.append(row)

        # Fruit and hazard names available for random placement.
        self.kinds = [
            "Bomb", 
            "Rum", 
            "Mango", 
            "Apple", 
            "Watermelon",
            "Pomegranate", 
            "Coconut", 
            "Cherry", 
            "Durian", 
            "Dragonfruit"
        ]

        # Maximum number of each kind allowed on the board.
        self.limits = {
            "Bomb": 10,
            "Rum": 5,
            "Mango": 10, 
            "Apple": 8, 
            "Watermelon": 4,
            "Pomegranate": 4, 
            "Coconut": 3, 
            "Cherry": 2, 
            "Durian": 2,
            "Dragonfruit": 1
        }

        # Base score value for each fruit or hazard.
        self.base_points = {
            "Mango": 300, 
            "Apple": 0, 
            "Watermelon": 100, 
            "Pomegranate": 200,
            "Coconut": 200, 
            "Cherry": 200, 
            "Durian": 800, 
            "Dragonfruit": 1200,
            "Bomb": 0, 
            "Rum": 0
        }

        # Tracks how many of each kind have been placed.
        self.counts = {k: 0 for k in self.kinds}

    #
    # Gets the placement limit for a kind by its 1-based index.
    #
    # Args:
    #     num: 1-based position in the kinds list.
    #
    # Returns:
    #     Maximum count allowed for that kind.
    #
    def get_limit(self, num: int) -> int:
        kind = self.kinds[num - 1]
        return self.limits[kind]

    #
    # Randomly fills every tile while respecting each kind's placement limit.
    #
    def propigate_self(self):
        self.counts = {k: 0 for k in self.kinds}

        total_cells = self.width * self.height
        placed = 0

        while placed < total_cells:
            num = random.randint(1, 10)
            kind = self.kinds[num - 1]

            if self.counts[kind] < self.limits[kind]:
                r = placed // self.width
                c = placed % self.width
                tile = self.grid[r][c]

                tile.fruit = Fruit(kind, self.base_points[kind])

                self.counts[kind] += 1
                placed += 1
            else:
                continue

    #
    # Prints the current grid fruit names to the console for debugging.
    #
    def print_grid(self):

        print("\nCurrent Grid:")

        for r in range(self.height):
            row_display = []
            for c in range(self.width):
                tile = self.grid[r][c]
                if hasattr(tile, "fruit") and tile.fruit:
                    name = tile.fruit.name
                    row_display.append(name)
                else:
                    row_display.append(".")
            print(" ".join(row_display))
        print()
