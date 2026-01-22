import numpy as np

class MediaEnvironment:
    def __init__(self, platforms):
        self.platforms = platforms

    def get_reward(self, action, roi):
        # Reward = ROI signal
        return roi[action] + np.random.normal(0, 0.05)
