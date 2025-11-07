class Fruit:
    def __init__(self, name, base_points, ability=0):
        self.name = name
        self.base_points = base_points
        self.ability = ability

        if name == "mango":
            self.ability = 0
            self.pointsBase = 300
        elif name == "apple":
            self.ability = 1
            self.pointsBase = 100
        elif name == "watermelon":
            self.ability = 2
            self.pointsBase = 100
        elif name == "pomegranate":
            self.ability = 3
            self.pointsBase = 200
        elif name == "coconut":
            self.ability = 4
            self.pointsBase = 200
        elif name == "cherry":
            self.ability = 5
            self.pointsBase = 200
        elif name == "durian":
            self.ability = 6
            self.pointsBase = 800
        elif name == "dragionfruit":
            self.ability = 0
            self.pointsBase = 1200