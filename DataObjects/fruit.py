class Fruit:
    #
    # Creates a fruit with its name, base score value, and ability id.
    #
    # Args:
    #     name: Fruit name used by the grid, board renderer, and image loader.
    #     base_points: Score value before temporary multipliers or abilities.
    #     ability: Optional ability id, overridden by known fruit names.
    #
    def __init__(self, name, base_points, ability=0):
        self.name = name
        self.base_points = base_points
        self.pointsBase = base_points
        self.ability = ability

        #
        # Ability id map:
        # 0 = no special scoring ability
        # 1 = apple scaling score
        # 2 = watermelon chain explosion
        # 3 = pomegranate score multiplier
        # 4 = coconut ability
        # 5 = cherry pair bonus
        # 6 = durian score multiplier
        #
        if name == "Mango":
            self.ability = 0
        elif name == "Apple":
            self.ability = 1
        elif name == "Watermelon":
            self.ability = 2
        elif name == "Pomegranate":
            self.ability = 3
        elif name == "Coconut":
            self.ability = 4
        elif name == "Cherry":
            self.ability = 5
        elif name == "Durian":
            self.ability = 6
        elif name == "Dragonfruit":
            self.ability = 0
