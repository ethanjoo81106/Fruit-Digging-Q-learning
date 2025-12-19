class Fruit:
    def __init__(self, name, base_points, ability=0):
        self.name = name
        self.base_points = base_points
        self.ability = ability

        if name == "Mango":
            self.ability = 0
            self.pointsBase = 300
        elif name == "Apple":
            self.ability = 1
            self.pointsBase = 100
        elif name == "Watermelon":
            self.ability = 2
            self.pointsBase = 100
        elif name == "Pomegranate":
            self.ability = 3
            self.pointsBase = 200
        elif name == "Coconut":
            self.ability = 4
            self.pointsBase = 200
        elif name == "Cherry":
            self.ability = 5
            self.pointsBase = 200
        elif name == "Durian":
            self.ability = 6
            self.pointsBase = 800
        elif name == "Dragionfruit":
            self.ability = 0
            self.pointsBase = 1200