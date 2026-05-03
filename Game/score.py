class Score:
    #
    # Creates a score tracker starting at zero.
    #
    def __init__(self):
        self.total = 0

    #
    # Adds points from a dug fruit or triggered fruit ability.
    #
    # Args:
    #     points: Number of points to add to the running total.
    #
    def add(self, points: int):
        self.total += points

    #
    # Clears the score when starting a new board.
    #
    def reset(self):
        self.total = 0
