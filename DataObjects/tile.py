class Tile:
    #
    # Creates one grid tile at the given row and column.
    #
    # Args:
    #     row: Tile row in the grid.
    #     col: Tile column in the grid.
    #
    def __init__(self, row, col):
        # Tile position in the grid.
        self.row = row
        self.col = col

        # Tracks whether the player has revealed this tile.
        self.dug = False

        # Fruit object stored in this tile. Set later by the grid.
        self.fruit = None

        # Image filename used before a fruit has been assigned.
        self.imageName = self.fruit.name + ".jpg" if self.fruit else "empty.jpg"

        # Tracks whether this tile was destroyed by a bomb.
        self.blownup = False
