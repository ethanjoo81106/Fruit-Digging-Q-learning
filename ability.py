from Util.watermelon import Watermelon

class Ability:

    # Current fruit ability mode that can affect the next score calculation.
    mode = 0

    # Number of apples dug so far. Apples are worth more as this increases.
    apples = 0

    # Number of cherries dug so far. The second cherry gives a bonus.
    cherry = 0

    #
    # Resets all ability counters and active modes for a new game.
    #
    @staticmethod
    def resetGameAbilities():
        Ability.mode = 0
        Ability.apples = 0
        Ability.cherry = 0

    #
    # Adds one apple to the running apple counter.
    #
    @staticmethod
    def appleAdd():
        Ability.apples += 1

    #
    # Adds one cherry to the running cherry counter.
    #
    @staticmethod
    def cherryAdd():
        Ability.cherry += 1

    #
    # Calculates score for a dug fruit and updates active ability state.
    #
    # Args:
    #     base_points: Base score value of the dug fruit.
    #     fruit: Fruit object from the dug tile.
    #     tile: Tile that was dug.
    #     grid: Current game grid used by area abilities.
    #
    # Returns:
    #     Total score earned from the dug fruit and any triggered bonuses.
    #
    @staticmethod
    def getScore(base_points, fruit, tile, grid):
        points = base_points
        pointMulti = 1
        bonus_points = 0

        # Apply the previous fruit's multiplier before the current fruit changes mode.
        if Ability.mode == 3:
            pointMulti = 1.5
        elif Ability.mode == 6:
            pointMulti = 0.5

        # Apply the current fruit's ability and set the mode for the next dig.
        if fruit.ability == 0:
            Ability.mode = 0
        elif fruit.ability == 1:
            Ability.appleAdd()
            points = Ability.apples * 100
            Ability.mode = 1
        elif fruit.ability == 2:
            bonus_points = Watermelon.explode_chain_for_half_points(grid, tile.row, tile.col, pointMulti)
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

        total = (points * pointMulti) + bonus_points
        if isinstance(total, float) and total.is_integer():
            total = int(total)

        print("BASE     MULTI     TOTAL \n", points, ' ', pointMulti, ' ', total)

        return total
