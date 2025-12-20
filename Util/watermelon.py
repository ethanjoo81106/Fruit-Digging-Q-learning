from collections import deque

class Watermelon:

    @staticmethod
    def explode_chain_for_half_points(grid, row: int, col: int) -> int:
        total_bonus = 0

        origins = deque([(row, col)])

        while origins:
            orow, ocol = origins.popleft()
            bonus, triggered = Watermelon._explode_one(grid, orow, ocol)
            total_bonus += bonus
            if triggered is not None:
                origins.append(triggered)

        return total_bonus

    @staticmethod
    def _explode_one(grid, row: int, col: int):
        dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        #         up     right   down    left

        visited = {(row, col)}
        queue = [(row, col)]

        while queue:
            cr, cc = queue.pop(0)

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

                exploded_name = tile.fruit.name
                points_value = getattr(tile.fruit, "pointsBase", tile.fruit.base_points)
                bonus = points_value // 2

                tile.dug = True

                if exploded_name == "Watermelon":
                    return bonus, (nr, nc)
                return bonus, None
        return 0, None