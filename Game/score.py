class Score:
    def __init__(self):
        self.total = 0

    def add(self, points: int):
        self.total += points

    def reset(self):
        self.total = 0