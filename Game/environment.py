from dataclasses import dataclass
import random

from ability import Ability
from Game.clues import TOOLS, get_clue
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
    # Actions can be tile coordinates or agent choices:
    # tile_action = row * width + col
    # agent_action = (tool_name, tile_action)
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
        self.selected_tool = TOOLS[0]
        self.last_clue = ("None",)
        self.highlight_tiles = ()
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
        self.selected_tool = TOOLS[0]
        self.last_clue = ("None",)
        self.highlight_tiles = ()
        Ability.resetGameAbilities()
        return self.get_q_state(include_hidden=self.include_hidden_state)

    #
    # Applies one dig action and returns reward, next state, done flag, and info.
    #
    def step(self, action: int | tuple[int, int] | tuple[str, int] | tuple[str, tuple[int, int]]) -> StepResult:
        tool_name, tile_action = self.decode_agent_action(action)
        row, col = self.decode_action(tile_action)
        tile = self.grid.grid[row][col]
        score_before = self.score.total

        if self.clicks_left <= 0:
            return self._result(0, True, {"valid": False, "reason": "no_clicks_left", "tile": tile})

        if tile.dug or tile.blownup:
            return self._result(0, self.is_done(), {"valid": False, "reason": "already_revealed", "tile": tile})

        self.clicks_left -= 1
        tile.dug = True
        self.selected_tool = tool_name

        if tile.fruit and tile.fruit.name == "Bomb":
            Bomb.explode(self.grid, tile.row, tile.col)
        elif tile.fruit:
            self.score.add(Ability.getScore(tile.fruit.base_points, tile.fruit, tile, self.grid))

        clue = get_clue(tool_name, tile, self.grid)
        self.last_clue = clue.code
        self.highlight_tiles = clue.highlight_tiles

        reward = self.score.total - score_before
        return self._result(reward, self.is_done(), {"valid": True, "tile": tile, "clue": clue})

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
            "selected_tool": self.selected_tool,
            "last_clue": self.last_clue,
            "highlight_tiles": self.highlight_tiles,
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
            self.selected_tool,
            self.last_clue,
            tuple(self.highlight_tiles),
            tuple(tile_state),
        )

    #
    # Returns all tool/tile actions that can still be selected.
    #
    def valid_actions(self) -> list[tuple[str, int]]:
        return self.valid_agent_actions()

    def valid_tile_actions(self) -> list[int]:
        if self.clicks_left <= 0:
            return []

        actions = []
        for row in range(self.grid.height):
            for col in range(self.grid.width):
                tile = self.grid.grid[row][col]
                if not tile.dug and not tile.blownup:
                    actions.append(self.encode_action(row, col))
        return actions

    def valid_agent_actions(self) -> list[tuple[str, int]]:
        return [
            (tool_name, tile_action)
            for tool_name in TOOLS
            for tile_action in self.valid_tile_actions()
        ]

    def is_done(self) -> bool:
        return self.clicks_left <= 0 or len(self.valid_actions()) == 0

    def action_space_size(self) -> int:
        return len(TOOLS) * self.grid.width * self.grid.height

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

    def decode_agent_action(
            self,
            action: int | tuple[int, int] | tuple[str, int] | tuple[str, tuple[int, int]],
        ) -> tuple[str, int | tuple[int, int]]:
        if (
                isinstance(action, tuple)
                and len(action) == 2
                and isinstance(action[0], str)
            ):
            tool_name, tile_action = action
            if tool_name not in TOOLS:
                raise ValueError(f"Unknown tool: {tool_name}")
            return tool_name, tile_action

        return self.selected_tool, action

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
