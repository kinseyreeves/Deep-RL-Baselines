import time

import gym
from gym_scalable.envs.grid.maps import map_loader
from pympler.tracker import SummaryTracker

tracker = SummaryTracker()

config = {"mapfile": map_loader.get_8x8_map(), "randomize_start": True,"randomize_goal":True, "curriculum": False, "num_goals": 4,
          "capture_reward": True, "state_encoding": "st"}
env = gym.make('n-maze-v0', config=config)

state = env.reset()
i = 0

print(env.observation_space)
print(env.action_space)

while i < 100000:
    i += 1
    # env.render()
    start = time.time()
    action = env.action_space.sample()
    # print(env.entity.get_pos())

    action_size = env.action_space.n
    env.render()
    a = input()

    state, reward, done, _ = env.step(action)
    print(state.shape)
    print(env.grid.get_encoding_stacked_shape(num_goals=4))
    print(f"{state}, {reward}, {done}")
    if (done):
        print(f"finished {i}")

    end = time.time()
    # print("step time : " + str(end - start))
    if (done):
        a = input()
        state = env.reset()
    # time.sleep(0.1)
    a = input()

tracker.print_diff()
