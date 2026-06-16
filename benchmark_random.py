import argparse
import random
from statistics import mean

from Game.environment import FruitDiggingEnv

def run_episode(env: FruitDiggingEnv) -> int | float:
    env.reset()
    done = False
    total_reward = 0

    while not done:
        valid_actions = env.valid_actions()
        if not valid_actions:
            break

        action = random.choice(valid_actions)
        result = env.step(action)
        total_reward += result.reward
        done = result.done

    return total_reward


def benchmark(episodes: int, seed: int | None = None) -> list[int | float]:
    if seed is not None:
        random.seed(seed)

    env = FruitDiggingEnv(include_hidden_state=False)
    scores = []

    for _ in range(episodes):
        scores.append(run_episode(env))

    return scores


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark a baseline agent that randomly chooses valid tiles."
    )
    parser.add_argument("--episodes", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    scores = benchmark(args.episodes, args.seed)

    print(f"episodes={len(scores)}")
    print(f"average_score={mean(scores):.2f}")
    print(f"min_score={min(scores)}")
    print(f"max_score={max(scores)}")


if __name__ == "__main__":
    main()
