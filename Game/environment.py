from dataclasses import dataclass
import random

from ability import Ability
from Game.grid import Grid
from Game.score import Score
from Util.bomb import Bomb

@dataclass(frozen=True)
class StepResult:
    state: tuple
    reward: int | float
    done: bool
    info: dict

class FruitDiggingEnv:
    #
    # Headless game environment for reinforcement learning.
    #
    # Actions are tile coordinates encoded as an integer:
    # action = row * width + col
    #
    def __init__(
            self,
            max_clicks: int = 15,
            seed: int | None = None,
            include_hidden_state: bool = False,
        ):
        self.max_clicks = max_clicks
        self.random_seed = seed
        self.include_hidden_state = include_hidden_state
        self.grid = None
        self.score = Score()
        self.clicks_left = max_clicks
        self.reset(seed=seed)

    #
    # Starts a new board and returns the initial Q-learning state.
    #
    def reset(self, seed: int | None = None) -> tuple:
        if seed is not None:
            self.random_seed = seed
            random.seed(seed)
        elif self.random_seed is not None:
            random.seed(self.random_seed)

        self.grid = Grid()
        self.grid.propigate_self()
        self.score.reset()
        self.clicks_left = self.max_clicks
        Ability.resetGameAbilities()
        return self.get_q_state(include_hidden=self.include_hidden_state)

    #
    # Applies one dig action and returns reward, next state, done flag, and info.
    #
    def step(self, action: int | tuple[int, int]) -> StepResult:
        row, col = self.decode_action(action)
        tile = self.grid.grid[row][col]
        score_before = self.score.total

        if self.clicks_left <= 0:
            return self._result(0, True, {"valid": False, "reason": "no_clicks_left", "tile": tile})

        if tile.dug or tile.blownup:
            return self._result(0, self.is_done(), {"valid": False, "reason": "already_revealed", "tile": tile})

        self.clicks_left -= 1
        tile.dug = True

        if tile.fruit and tile.fruit.name == "Bomb":
            Bomb.explode(self.grid, tile.row, tile.col)
        elif tile.fruit:
            self.score.add(Ability.getScore(tile.fruit.base_points, tile.fruit, tile, self.grid))

        reward = self.score.total - score_before
        return self._result(reward, self.is_done(), {"valid": True, "tile": tile})

    #
    # Returns the current state as a plain dictionary for inspection/debugging.
    #
    def get_state(self, include_hidden: bool = False) -> dict:
        return {
            "width": self.grid.width,
            "height": self.grid.height,
            "clicks_left": self.clicks_left,
            "score": self.score.total,
            "ability_mode": Ability.mode,
            "apples": Ability.apples,
            "cherries": Ability.cherry,
            "tiles": [
                [
                    self._tile_state(self.grid.grid[row][col], include_hidden=include_hidden)
                    for col in range(self.grid.width)
                ]
                for row in range(self.grid.height)
            ],
        }

    #
    # Returns a compact, hashable state suitable for tabular Q-learning.
    #
    def get_q_state(self, include_hidden: bool = False) -> tuple:
        tile_state = []
        for row in range(self.grid.height):
            for col in range(self.grid.width):
                tile = self.grid.grid[row][col]
                tile_state.append(self._tile_code(tile, include_hidden=include_hidden))

        return (
            self.clicks_left,
            Ability.mode,
            Ability.apples,
            Ability.cherry,
            tuple(tile_state),
        )

    #
    # Returns all actions that can still be selected.
    #
    def valid_actions(self) -> list[int]:
        if self.clicks_left <= 0:
            return []

        actions = []
        for row in range(self.grid.height):
            for col in range(self.grid.width):
                tile = self.grid.grid[row][col]
                if not tile.dug and not tile.blownup:
                    actions.append(self.encode_action(row, col))
        return actions

    def is_done(self) -> bool:
        return self.clicks_left <= 0 or len(self.valid_actions()) == 0

    def action_space_size(self) -> int:
        return self.grid.width * self.grid.height

    def encode_action(self, row: int, col: int) -> int:
        if row < 0 or col < 0 or row >= self.grid.height or col >= self.grid.width:
            raise ValueError(f"Action coordinates out of bounds: {(row, col)}")
        return row * self.grid.width + col

    def decode_action(self, action: int | tuple[int, int]) -> tuple[int, int]:
        if isinstance(action, tuple):
            row, col = action
        else:
            row = action // self.grid.width
            col = action % self.grid.width

        if row < 0 or col < 0 or row >= self.grid.height or col >= self.grid.width:
            raise ValueError(f"Action out of bounds: {action}")
        return row, col

    def _result(self, reward, done: bool, info: dict) -> StepResult:
        return StepResult(
            state=self.get_q_state(include_hidden=self.include_hidden_state),
            reward=reward,
            done=done,
            info=info,
        )

    def _tile_state(self, tile, include_hidden: bool) -> dict:
        fruit_name = tile.fruit.name if tile.fruit else None
        visible_name = fruit_name if include_hidden or tile.dug or tile.blownup else None
        return {
            "row": tile.row,
            "col": tile.col,
            "dug": tile.dug,
            "blownup": tile.blownup,
            "fruit": visible_name,
        }

    def _tile_code(self, tile, include_hidden: bool) -> tuple:
        if tile.blownup:
            visibility = "blownup"
        elif tile.dug:
            visibility = "dug"
        else:
            visibility = "hidden"

        fruit_name = tile.fruit.name if tile.fruit else "None"
        if not include_hidden and visibility == "hidden":
            fruit_name = "Unknown"

        return (visibility, fruit_name)
