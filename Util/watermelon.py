from collections import deque

class Watermelon:

    #
    # Triggers watermelon explosion scoring and follows chained watermelons.
    #
    # Args:
    #     grid: Current game grid.
    #     row: Row of the original watermelon tile.
    #     col: Column of the original watermelon tile.
    #     point_multiplier: Active score multiplier applied to explosion bonuses.
    #
    # Returns:
    #     Total bonus score earned by the watermelon chain.
    #
    @staticmethod
    def explode_chain_for_half_points(grid, row: int, col: int, point_multiplier=1):
        total_bonus = 0

        origins = deque([(row, col)])

        while origins:
            orow, ocol = origins.popleft()
            bonus, triggered = Watermelon._explode_one(grid, orow, ocol, point_multiplier)
            total_bonus += bonus
            if triggered is not None:
                origins.append(triggered)

        return total_bonus

    #
    # Finds and digs the lowest-value reachable fruit for one watermelon blast.
    #
    # Args:
    #     grid: Current game grid.
    #     row: Row where the blast starts.
    #     col: Column where the blast starts.
    #     point_multiplier: Active score multiplier applied before halving.
    #
    # Returns:
    #     Tuple containing the bonus score and chained watermelon position, if any.
    #
    @staticmethod
    def _explode_one(grid, row: int, col: int, point_multiplier=1):
        dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        #         up     right   down    left

        visited = {(row, col)}
        queue = deque([(row, col)])

        while queue:
            candidates = []

            for _ in range(len(queue)):
                cr, cc = queue.popleft()

                for dr, dc in dirs:
                    nr, nc = cr + dr, cc + dc

                    if nr < 0 or nc < 0 or nr >= grid.height or nc >= grid.width:
                        continue

                    if (nr, nc) in visited:
                        continue

                    visited.add((nr, nc))
                    queue.append((nr, nc))

                    tile = grid.grid[nr][nc]
                    if not tile.fruit or tile.dug:
                        continue
                    if tile.fruit.name in ("Bomb", "Rum"):
                        continue

                    points_value = tile.fruit.base_points
                    bonus = (points_value * point_multiplier) / 2
                    candidates.append((bonus, nr, nc, tile))

            if not candidates:
                continue

            bonus, nr, nc, tile = min(candidates, key=lambda candidate: (candidate[0], candidate[1], candidate[2]))
            tile.dug = True

            if tile.fruit.name == "Watermelon":
                return bonus, (nr, nc)
            return bonus, None

        return 0, None
