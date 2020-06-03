import time

import gym
from gym_scalable.envs.grid.maps import map_loader
from pympler.tracker import SummaryTracker

tracker = SummaryTracker()

config = {"mapfile": map_loader.get_size_map(3),
          "randomize_start": True,
          "randomize_goal":True,
          "curriculum": False,
          "curriculum_eps" :5,
          "num_goals": 6,
          "capture_reward": False,
          "state_encoding": "st"
          }

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

    action_size = env.action_space.n
    env.render()
    a = input()


    #env.reset()
    #continue
    state, reward, done, _ = env.step(action)
    print(reward)
    #print(state.shape)
    #print(state)
    #print(env.grid.get_encoding_stacked_shape(num_goals=4))
    #print(f"{state}, {reward}, {done}")
    if (done):
        print(f"finished {i}")

    end = time.time()
    # print("step time : " + str(end - start))
    if (done):
        a = input()
        state = env.reset()

    a = input()

tracker.print_diff()
