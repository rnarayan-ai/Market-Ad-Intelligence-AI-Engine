import numpy as np

class BanditAgent:
    def __init__(self, n_actions):
        self.n_actions = n_actions
        self.q_values = np.zeros(n_actions)
        self.action_counts = np.zeros(n_actions)

    def select_action(self):
        return np.argmax(self.q_values)

    def update(self, action, reward):
        self.action_counts[action] += 1
        alpha = 1 / self.action_counts[action]
        self.q_values[action] += alpha * (reward - self.q_values[action])
