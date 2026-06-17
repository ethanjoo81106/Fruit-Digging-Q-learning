from dataclasses import dataclass

from ability import Ability

TOOLS = ("Iron", "Gold", "Diamond")


@dataclass(frozen=True)
class Clue:
    tool: str
    code: tuple
    text: str
    highlight_tiles: tuple[tuple[int, int], ...] = ()


def get_clue(tool_name: str, tile, grid) -> Clue:
    neighbors = get_neighbors(tile.row, tile.col, grid)

    if tool_name == "Iron":
        mine_count = sum(
            1 for neighbor in neighbors
            if neighbor.fruit and neighbor.fruit.name == "Bomb"
        )
        mine_label = "mine" if mine_count == 1 else "mines"
        return Clue(
            tool=tool_name,
            code=("Iron", tile.row, tile.col, mine_count),
            text=f"{mine_count} adjacent {mine_label}.",
        )

    if tool_name == "Diamond":
        fruit_neighbors = [
            neighbor for neighbor in neighbors
            if neighbor.fruit
            and neighbor.fruit.name not in ("Bomb", "Rum")
            and not neighbor.dug
            and not neighbor.blownup
        ]

        if not fruit_neighbors:
            return Clue(
                tool=tool_name,
                code=("Diamond", tile.row, tile.col, "none"),
                text="No nearby fruit found.",
            )

        target = min(
            fruit_neighbors,
            key=lambda neighbor: (get_current_fruit_score(neighbor.fruit), neighbor.row, neighbor.col),
        )
        return Clue(
            tool=tool_name,
            code=("Diamond", tile.row, tile.col, target.row, target.col, target.fruit.name),
            text=f"Lowest nearby fruit: {target.fruit.name} at {target.row + 1},{target.col + 1}.",
            highlight_tiles=((target.row, target.col),),
        )

    fruit_neighbors = [
        neighbor for neighbor in neighbors
        if neighbor.fruit and neighbor.fruit.name not in ("Bomb", "Rum")
    ]

    if not fruit_neighbors:
        return Clue(
            tool=tool_name,
            code=(tool_name, tile.row, tile.col, "none"),
            text="No nearby fruit found.",
        )

    target = max(
        fruit_neighbors,
        key=lambda neighbor: (get_current_fruit_score(neighbor.fruit), neighbor.row, neighbor.col),
    )
    return Clue(
        tool=tool_name,
        code=(tool_name, tile.row, tile.col, target.fruit.name),
        text=f"Highest nearby fruit: {target.fruit.name}",
    )


def get_neighbors(row: int, col: int, grid):
    neighbors = []
    for row_delta in (-1, 0, 1):
        for col_delta in (-1, 0, 1):
            if row_delta == 0 and col_delta == 0:
                continue

            neighbor_row = row + row_delta
            neighbor_col = col + col_delta
            if 0 <= neighbor_row < grid.height and 0 <= neighbor_col < grid.width:
                neighbors.append(grid.grid[neighbor_row][neighbor_col])

    return neighbors


def get_current_fruit_score(fruit):
    point_multiplier = 1
    if Ability.mode == 3:
        point_multiplier = 1.5
    elif Ability.mode == 6:
        point_multiplier = 0.5

    if fruit.ability == 1:
        points = (Ability.apples + 1) * 100
    elif fruit.ability == 5 and Ability.cherry + 1 == 2:
        points = fruit.base_points + 200
    else:
        points = fruit.base_points

    score = points * point_multiplier
    if isinstance(score, float) and score.is_integer():
        return int(score)
    return score
