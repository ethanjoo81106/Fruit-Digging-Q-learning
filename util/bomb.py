class Bomb:
    @staticmethod
    def explode(grid, row: int, col: int):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue

                r = row + dr
                c = col + dc

                if r < 0 or c < 0 or r >= grid.height or c>= grid.width:
                    continue

                tile = grid.grid[r][c]
                if not tile.fruit:
                    continue

                if tile.fruit.name in ("Bomb", "Rum"):
                    continue

                if tile.dug:
                    continue

                tile.dug = True
                tile.blownup = True