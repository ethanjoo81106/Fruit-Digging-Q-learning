from DataObjects.tile import Tile
from DataObjects.fruit import Fruit
import random


class Grid:
    def __init__(self):
        self.width = 7
        self.height = 7
        self.grid = []

        for r in range(self.height):
            row = []
            for c in range(self.width):
                row.append(Tile(r, c))
            self.grid.append(row)

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

        self.counts = {k: 0 for k in self.kinds}

    def get_limit(self, num: int) -> int:
        kind = self.kinds[num - 1]
        return self.limits[kind]

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