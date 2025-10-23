class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.dug = False
        self.fruit = None
        self.imageName = self.fruit.name + ".jpg" if self.fruit else "empty.jpg"