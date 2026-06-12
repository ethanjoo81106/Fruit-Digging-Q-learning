import random
from collections import defaultdict

from Game.environment import FruitDiggingEnv

EPISODES = 1000
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPSILON_START = 1.0
EPSILON_END = 0.05
EPSILON_DECAY = 0.995

def best_action(q_table, state, valid_actions):
    return max(valid_actions, key=lambda action: q_table[(state, action)])

def choose_action(q_table, state, valid_actions, epsilon):
    if random.random() < epsilon:
        return random.choice(valid_actions)
    return best_action(q_table, state, valid_actions)

def train():
    env = FruitDiggingEnv(include_hidden_state=False)
    q_table = defaultdict(float)
    epsilon = EPSILON_START

    for episode in range(EPISODES):
        state = env.reset()
        done = False
        total_reward = 0

        while not done:
            valid_actions = env.valid_actions()
            action = choose_action(q_table, state, valid_actions, epsilon)
            result = env.step(action)

            next_valid_actions = env.valid_actions()
            future_value = 0
            if next_valid_actions and not result.done:
                future_value = max(q_table[(result.state, next_action)] for next_action in next_valid_actions)

            old_value = q_table[(state, action)]
            q_table[(state, action)] = old_value + LEARNING_RATE * (
                result.reward + DISCOUNT * future_value - old_value
            )

            state = result.state
            done = result.done
            total_reward += result.reward

        epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)

        if (episode + 1) % 100 == 0:
            print(f"episode={episode + 1} score={total_reward} epsilon={epsilon:.3f}")

    return q_table


if __name__ == "__main__":
    train()
