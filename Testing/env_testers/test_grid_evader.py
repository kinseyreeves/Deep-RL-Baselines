import os

import gym
from gym_scalable.envs.grid.maps import map_loader
from pympler.tracker import SummaryTracker

tracker = SummaryTracker()

print(os.getcwd())
env = gym.make('n-grid_evaders-v0',
               config={"mapfile": map_loader.get_5x5_map(), "randomize_start": True, "randomize_goal": True,
                       "curriculum": True, "RL_evader": False, "curriculum_eps": 10, "state_encoding": "st"})

state = env.reset()
i = 0
goal = env.grid.goal

while i < 100000:

    i += 1
    env.render()
    print(env.total_eps)

    action_size = env.action_space.n

    action_ = env.action_space.sample()
    # print(action_)
    state, reward, done, _ = env.step(action_)
    # print(f"{state}  {reward}")

    # print(env.normalize_state)
    env.reset()
    print(env.curriculum_value)
    input()
    continue
    if (done):
        env.reset()

    time.sleep(0.2)

tracker.print_diff()
