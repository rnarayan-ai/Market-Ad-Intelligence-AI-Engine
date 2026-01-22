from rl.rl_environment import MediaEnvironment
from rl.rl_agent import BanditAgent

platforms = ["TV", "YouTube", "Meta"]
env = MediaEnvironment(platforms)
agent = BanditAgent(len(platforms))

roi_signals = {"TV": 1.1, "YouTube": 1.4, "Meta": 1.25}

for _ in range(100):
    action = agent.select_action()
    reward = env.get_reward(action, list(roi_signals.values()))
    agent.update(action, reward)

print("Optimal Budget Distribution:", agent.q_values)
