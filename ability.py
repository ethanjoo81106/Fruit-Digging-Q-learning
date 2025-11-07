class Ability:

    mode = 0
    apples = 0
    cherry = 0

    @staticmethod
    def appleAdd():
        Ability.apples += 1

    @staticmethod
    def cherryAdd():
        Ability.cherry += 1

    @staticmethod
    def getScore(base_points, fruit, tile):
        points = base_points
        pointMulti = 1

        if Ability.mode == 3:
            pointMulti = 1.5
        elif Ability.mode == 6:
            pointMulti = 0.5

        if fruit.ability == 0:
            Ability.mode = 0
        elif fruit.ability == 1:
            Ability.appleAdd()
            points = Ability.apples * 100
            Ability.mode = 1
        elif fruit.ability == 2:
            Ability.watermelonPop(tile.col, tile.row)
            Ability.mode = 2
        elif fruit.ability == 3:
            Ability.mode = 3
        elif fruit.ability == 4:
            Ability.mode = 4
        elif fruit.ability == 5:
            Ability.cherryAdd()
            if Ability.cherry == 2:
                points += 200
            Ability.mode = 5
        elif fruit.ability == 6:
            Ability.mode = 6

        print("APPLE!", Ability.apples, points)


        return points * pointMulti
    
    

    @staticmethod
    def watermelonPop(x, y):
        print("Watermelon ability activated!")